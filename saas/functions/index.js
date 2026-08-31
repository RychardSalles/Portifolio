const { onRequest } = require("firebase-functions/v2/https");
const { setGlobalOptions } = require("firebase-functions/v2");
const { defineSecret } = require("firebase-functions/params");
const logger = require("firebase-functions/logger");
const admin = require("firebase-admin");
const crypto = require("crypto");

admin.initializeApp();
const db = admin.firestore();

setGlobalOptions({ region: "southamerica-east1", maxInstances: 10 });

// Segredos de verdade (Secret Manager), configurados com:
//   firebase functions:secrets:set META_VERIFY_TOKEN
// Nada disso vaza pro código-fonte — só o NOME do segredo fica aqui.
const metaVerifyToken = defineSecret("META_VERIFY_TOKEN");
const metaAppSecret = defineSecret("META_APP_SECRET");
const n8nWebhookUrl = defineSecret("N8N_WEBHOOK_URL");
const n8nWebhookSecret = defineSecret("N8N_WEBHOOK_SECRET");

/**
 * Confere a assinatura HMAC que a Meta manda em todo POST
 * (cabeçalho x-hub-signature-256), usando o App Secret do app.
 * Sem isso, qualquer um que descobrisse a URL do webhook
 * poderia mandar mensagens falsas pro sistema.
 */
function verifyMetaSignature(req, appSecret) {
  const signature = req.get("x-hub-signature-256");
  if (!signature || !appSecret || !req.rawBody) return false;

  const expected =
    "sha256=" +
    crypto.createHmac("sha256", appSecret).update(req.rawBody).digest("hex");

  const a = Buffer.from(signature);
  const b = Buffer.from(expected);
  return a.length === b.length && crypto.timingSafeEqual(a, b);
}

/**
 * Cada empresa cadastra o phone_number_id do WhatsApp que já usa
 * (ver saas/firestore/schema.md). É assim que uma única função
 * consegue atender várias empresas ao mesmo tempo (multi-tenant).
 */
async function findEmpresaByPhoneNumberId(phoneNumberId) {
  const snap = await db
    .collection("empresas")
    .where("whatsappPhoneNumberId", "==", phoneNumberId)
    .limit(1)
    .get();

  if (snap.empty) return null;
  const doc = snap.docs[0];
  return { id: doc.id, ...doc.data() };
}

async function forwardToN8n(payload, webhookUrl, sharedSecret) {
  if (!webhookUrl) {
    logger.error("N8N_WEBHOOK_URL não configurada — mensagem não encaminhada.", { payload });
    return;
  }

  try {
    const resp = await fetch(webhookUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "x-rd-webhook-secret": sharedSecret || "",
      },
      body: JSON.stringify(payload),
    });

    if (!resp.ok) {
      logger.error("n8n respondeu com erro ao receber a mensagem.", { status: resp.status });
    }
  } catch (err) {
    logger.error("Falha ao encaminhar mensagem para o n8n.", err);
  }
}

/**
 * "WEBHOOK RD" da arquitetura: é a única peça que conversa
 * diretamente com a WhatsApp Business Platform (Cloud API).
 * Job dela é só: verificar a assinatura, descobrir de qual
 * empresa é a mensagem e repassar pro n8n — toda a lógica de
 * negócio (IA, regras, Firestore) fica no fluxo do n8n.
 */
exports.webhookWhatsApp = onRequest(
  { secrets: [metaVerifyToken, metaAppSecret, n8nWebhookUrl, n8nWebhookSecret] },
  async (req, res) => {
  // Handshake de verificação que a Meta faz uma vez, ao configurar o webhook no painel do app.
  if (req.method === "GET") {
    const mode = req.query["hub.mode"];
    const token = req.query["hub.verify_token"];
    const challenge = req.query["hub.challenge"];

    if (mode === "subscribe" && token === metaVerifyToken.value()) {
      res.status(200).send(challenge);
    } else {
      logger.warn("Falha na verificação do webhook.", { mode });
      res.sendStatus(403);
    }
    return;
  }

  if (req.method !== "POST") {
    res.sendStatus(405);
    return;
  }

  if (!verifyMetaSignature(req, metaAppSecret.value())) {
    logger.warn("Assinatura inválida no webhook do WhatsApp.");
    res.sendStatus(401);
    return;
  }

  try {
    const entries = req.body?.entry ?? [];
    const forwards = [];

    for (const entry of entries) {
      for (const change of entry.changes ?? []) {
        const value = change.value ?? {};
        const phoneNumberId = value.metadata?.phone_number_id;
        const messages = value.messages ?? [];

        // Sem phone_number_id ou sem mensagens = evento de status (entregue/lido) ou outro tipo de notificação. Ignorado por ora.
        if (!phoneNumberId || messages.length === 0) continue;

        const empresa = await findEmpresaByPhoneNumberId(phoneNumberId);
        if (!empresa) {
          logger.warn("Nenhuma empresa encontrada para este número.", { phoneNumberId });
          await db.collection("webhooks_nao_identificados").add({
            phoneNumberId,
            recebidoEm: admin.firestore.FieldValue.serverTimestamp(),
            payload: value,
          });
          continue;
        }

        const contact = (value.contacts ?? [])[0];

        for (const message of messages) {
          forwards.push(
            forwardToN8n(
              {
                empresaId: empresa.id,
                phoneNumberId,
                from: message.from,
                nomeContato: contact?.profile?.name ?? null,
                messageId: message.id,
                timestamp: message.timestamp,
                type: message.type,
                texto: message.text?.body ?? null,
                interativo: message.interactive ?? null,
              },
              n8nWebhookUrl.value(),
              n8nWebhookSecret.value()
            )
          );
        }
      }
    }

    await Promise.all(forwards);
  } catch (err) {
    logger.error("Erro processando webhook do WhatsApp.", err);
  }

  // Responde 200 mesmo se algo acima falhar, pra Meta não ficar reenviando o mesmo
  // evento em loop — qualquer erro real fica registrado no log pra investigar depois.
  res.sendStatus(200);
});

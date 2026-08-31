# RD Webdesign SaaS — Webhook + Atendimento WhatsApp (v1)

Primeira peça implementada do SaaS multi-tenant descrito para a RD
Webdesign: o caminho que uma mensagem percorre desde o WhatsApp do salão
até uma resposta de IA (ou transferência para um atendente humano).

```
Cliente → WhatsApp → WhatsApp Business Platform (Cloud API)
        → n8n Cloud, workflow "RD Webdesign — Atendimento WhatsApp"
          (https://rychardsss.app.n8n.cloud/workflow/Rtvv9cKFCLgAVO2K)
             → Firestore (dados da empresa/serviços/clientes)
             → IA (Anthropic, AI Agent com memória de conversa)
             → WhatsApp (resposta) ou transferência para humano
```

O workflow em si **não é mais um arquivo neste repositório** — foi criado
direto no seu n8n usando nós nativos (WhatsApp Trigger, Firestore, AI
Agent) via a API do n8n. Detalhes e link de acesso em `n8n/README.md`.

Este módulo (`saas/`) vive dentro do repositório do site institucional da
RD Webdesign, mas é **independente** dele — nenhum arquivo do site
(`index.html`, `servicos.html` etc.) foi tocado.

## Estrutura

```
saas/
├── n8n/
│   ├── README.md         Link do workflow, credenciais que faltam, como testar
│   └── whatsapp-atendimento.json   Versão anterior, obsoleta — só referência
├── firestore/
│   ├── schema.md         Modelo de dados multi-tenant
│   └── firestore.rules
├── functions/            Opcional — não usado no fluxo atual, ver abaixo
└── firebase.json
```

O workflow de verdade (30 nós, nativo) vive no seu n8n, não neste
repositório: **https://rychardsss.app.n8n.cloud/workflow/Rtvv9cKFCLgAVO2K**.

## Como chegamos nesse desenho (histórico rápido)

Duas mudanças em relação ao plano original:

1. **Sem Cloud Function no meio.** A primeira versão tinha uma Cloud
   Function do Firebase ("Webhook RD") entre a Meta e o n8n, só pra
   verificar a assinatura da mensagem e descobrir a empresa antes de
   repassar. Isso exigia o **plano Blaze** do Firebase, e esbarramos num
   problema de ativação de conta de faturamento do Google sem solução
   rápida. Como o n8n consegue fazer isso sozinho e o Firestore **não**
   exige Blaze, a function saiu do caminho principal. O código dela
   (`saas/functions/`) continua no repositório como peça **opcional**
   (ex: se um dia quiser verificação HMAC extra antes do n8n).

2. **Sem JSON pra importar manualmente.** A segunda versão era um arquivo
   `saas/n8n/whatsapp-atendimento.json` pra importar na interface do n8n,
   com todas as chamadas ao WhatsApp e ao Firestore feitas via HTTP
   Request cru. Ao ganhar acesso direto ao n8n (via MCP), reconstruímos
   usando os nós **nativos** do n8n para WhatsApp, Firestore e IA — mais
   robusto, com verificação automática do webhook da Meta e memória de
   conversa na IA. Esse workflow foi criado direto no seu n8n; o arquivo
   antigo ficou só de referência histórica.

Resultado: **o módulo inteiro roda de graça** (Firestore no plano Spark +
n8n + as APIs externas), sem depender de faturamento do Google em nenhum
ponto.

## Passo a passo para colocar no ar

### 1. Firebase (só Firestore — sem Blaze)

1. Crie (ou reaproveite) um projeto no [console.firebase.google.com](https://console.firebase.google.com).
2. Ative o **Firestore** (modo produção). Isso funciona no plano gratuito
   Spark, sem precisar de cartão nem upgrade de plano.
3. Publique as regras: `firebase deploy --only firestore:rules --project SEU_PROJETO` (usa `saas/firestore/firestore.rules`, referenciado em `saas/firebase.json`).
4. Crie uma **conta de serviço** pro n8n acessar o Firestore: no
   [Google Cloud Console](https://console.cloud.google.com/iam-admin/serviceaccounts) do mesmo projeto, crie uma conta de serviço, dê o papel
   **Cloud Datastore User** (`roles/datastore.user`) e gere uma chave JSON.
   Guarde esse arquivo — é o que o n8n pede na credencial "Google Service
   Account" (detalhes em `n8n/README.md`).

### 2. n8n

O workflow já está criado: **https://rychardsss.app.n8n.cloud/workflow/Rtvv9cKFCLgAVO2K**.
Siga `saas/n8n/README.md` pra configurar as 4 credenciais que faltam
(WhatsApp Trigger, Google Service Account do passo anterior, Anthropic,
WhatsApp Business Cloud) e ativar o workflow.

### 3. Meta (WhatsApp Cloud API)

1. Crie um app do tipo **Business** em [developers.facebook.com](https://developers.facebook.com/apps), adicione o produto **WhatsApp**.
2. O **WhatsApp Trigger** do n8n verifica o webhook automaticamente
   (não precisa mais inventar um "verify token" nem cadastrar URL de
   callback manualmente — ver detalhes em `n8n/README.md`). Pegue o
   Client ID/Client Secret do app pra credencial `WhatsApp Trigger`.
3. Para usar o número que o salão **já tem** no WhatsApp Business App, siga
   o fluxo de **coexistência** dentro do próprio WhatsApp Manager (Meta) —
   é o dono do número quem autoriza, mantendo a empresa como titular da
   conta (ver seção 18 do documento de arquitetura: a RD atua como
   integradora, não como dona do número).
4. Anote o **`phone_number_id`** gerado e o **token de acesso** — são os
   valores que vão nos campos `whatsappPhoneNumberId` e
   `whatsappAccessToken` do documento da empresa no Firestore.

### 4. Cadastrar a primeira empresa (manual, até existir painel admin)

Crie um documento em `empresas/{empresaId}` no console do Firestore
seguindo `saas/firestore/schema.md`. O mínimo pra funcionar:

```json
{
  "nome": "Salão Bella",
  "iaAtiva": true,
  "iaPersonalidade": "simpática, objetiva e usa emojis com moderação",
  "whatsappPhoneNumberId": "SEU_PHONE_NUMBER_ID",
  "whatsappAccessToken": "SEU_TOKEN"
}
```

Adicione alguns documentos em `empresas/{empresaId}/servicos` e mande uma
mensagem de teste pro número real do salão.

## O que ainda não existe (fora do escopo desta rodada)

- Painel administrativo para o dono do salão cadastrar empresa/serviços/IA
  sem mexer direto no Firestore (seção 11 da arquitetura).
- Onboarding automatizado (seção 14) — hoje o cadastro da empresa é manual.
- Suporte a outros tipos de mensagem além de texto (áudio, imagem, botões).
- Ver também "Limitações conhecidas" em `n8n/README.md`.

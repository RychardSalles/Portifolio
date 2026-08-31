# Fluxo n8n — Atendimento WhatsApp

**O workflow já está publicado no seu n8n**, criado direto pela API/MCP do
n8n (não por importação manual de JSON):

👉 **https://rychardsss.app.n8n.cloud/workflow/Rtvv9cKFCLgAVO2K**

> O arquivo `whatsapp-atendimento.json` nesta pasta é uma versão **anterior
> e obsoleta** (baseada em HTTP Request cru + um segredo na URL). Ficou
> aqui só de referência histórica — o workflow de verdade é o do link
> acima, que usa nós nativos do n8n para WhatsApp, Firestore e IA.

## Por que essa versão é mais simples

Diferente da primeira tentativa (que reimplementava tudo com chamadas
HTTP manuais), esta versão usa três nós **nativos** do n8n:

- **WhatsApp Trigger** (`n8n-nodes-base.whatsAppTrigger`) — recebe os
  eventos da Meta. A verificação do webhook (o handshake `hub.challenge`)
  é **automática**: o n8n registra a inscrição do webhook e confirma o
  desafio da Meta usando o próprio ID do node. **Não existe mais "verify
  token" pra você inventar** — se em algum passo do painel da Meta pedir
  um "Verify token" manualmente, é o ID deste node que vai lá, não um
  valor arbitrário.
- **Google Cloud Firestore** (`n8n-nodes-base.googleFirebaseCloudFirestore`) —
  substitui todas as chamadas HTTP cruas à API REST do Firestore da
  versão anterior.
- **AI Agent + Anthropic Chat Model + Simple Memory** — em vez de uma
  chamada HTTP direta à Anthropic, agora é um Agente de IA de verdade,
  com **memória de conversa** (10 últimas interações, por número de
  telefone do cliente) — resolve uma das limitações da v1 anterior.
- **WhatsApp Business Cloud** (`n8n-nodes-base.whatsApp`) — envia as
  respostas, em vez de montar a chamada à Graph API na mão.

## O que o fluxo faz

```
WhatsApp Trigger (Meta)
  → Normalizar mensagem (1 item por mensagem recebida)
  → Buscar empresa (Firestore, por whatsappPhoneNumberId)
  → Empresa encontrada?
       ├─ não → Registrar webhook não identificado (fim)
       └─ sim → Registrar mensagem recebida
                   → Pediu humano por palavra-chave?
                        ├─ sim → Preparar transferência direta ─┐
                        └─ não → Buscar serviços → Parse         │
                                 → Montar prompt IA               │
                                 → Agente de atendimento (IA)     │
                                 → Interpretar resposta da IA     │
                                                                    ▼
                                                       Transferir para humano?
                                                          ├─ sim → atualiza cliente
                                                          │        → avisa cliente → registra
                                                          │        → tem telefone de equipe? → avisa equipe
                                                          └─ não → envia resposta ao cliente
                                                                   → registra → atualiza cliente
```

Mesma lógica de negócio da v1 anterior (transferência por palavra-chave
OU decisão da própria IA via marcador `[[TRANSFERIR_HUMANO]]`), só que
implementada com nós nativos e validados.

## Credenciais que faltam configurar

Abra o workflow no link acima. Quatro nós/grupos de nós precisam de
credencial (o n8n mostra um aviso nos nós que ainda não têm):

| Credencial | Nó(s) que usam | Tipo | Onde conseguir |
|---|---|---|---|
| `WhatsApp Trigger (RD Webdesign)` | WhatsApp Trigger | Client ID + Client Secret | App da Meta (developers.facebook.com) — Configurações do app > Básico |
| `Google Service Account (Firestore)` | Todos os nós Firestore (7 nós) | Service Account JSON | Google Cloud Console do projeto `rdwebdesign-b5734` — IAM > Contas de serviço, papel "Cloud Datastore User" |
| `Anthropic API` | Modelo Anthropic | API Key | console.anthropic.com |
| `WhatsApp Business Cloud (RD Webdesign)` | Avisar cliente / Avisar equipe / Enviar resposta (3 nós) | Token de acesso da Cloud API | App da Meta > WhatsApp > Configuração da API |

Clique em cada nó com aviso, abra o campo de credencial e crie/selecione
a correspondente — o n8n reconhece pelo nome quando você já criou uma
antes, então só precisa criar cada uma **uma vez**.

## Depois de configurar as credenciais

1. Ative o workflow (toggle no canto superior direito do editor).
2. Cadastre pelo menos uma empresa de teste no Firestore
   (`saas/firestore/schema.md`) com o `whatsappPhoneNumberId` do número
   de teste da Meta.
3. Mande uma mensagem real pro número de teste e acompanhe a execução na
   aba "Executions" do n8n.

## Limitações conhecidas desta v1

- Só trata mensagens de texto.
- Se várias mensagens chegarem no **mesmo** evento de webhook (raro, mas
  possível), a busca de serviços e o prompt da IA podem misturar dados
  entre elas — cada execução assume 1 mensagem por evento na prática.
- `whatsappAccessToken` fica em texto plano no documento da empresa no
  Firestore — considerar Secret Manager antes de produção com clientes
  reais.
- Sem retomada automática da IA depois que um humano assume a conversa.

---

# Fluxo n8n — Lembretes (manutenção + aniversário)

Segundo workflow, separado do atendimento: roda uma vez por dia (9h) e
manda mensagem automática pra clientes com **aniversário hoje** ou com a
**manutenção de um serviço vencendo hoje** (ex: retoque de cílios 20 dias
depois da aplicação).

👉 **https://rychardsss.app.n8n.cloud/workflow/RzdiJmD62sZiPtll**

## Como funciona

```
Gatilho diário 9h
  → Buscar empresas (todas)
  → Loop empresas (uma de cada vez)
       → Buscar serviços da empresa   (pra saber o intervalo de manutenção de cada um)
       → Buscar clientes da empresa
       → Montar lembretes do dia (compara dataNascimento e ultimoServicoData + intervaloManutencaoDias com hoje)
       → É aniversário?
            ├─ sim → Avisar cliente (template "aniversario_cliente") → registra
            └─ não → Avisar cliente (template "lembrete_manutencao") → registra
       → próxima empresa
```

Reaproveita as credenciais `Google Service Account (Firestore)` e
`WhatsApp Business Cloud (RD Webdesign)` já configuradas no workflow de
atendimento — não precisa criar de novo, o n8n casa pelo nome.

## Pré-requisito obrigatório: modelos de mensagem (Meta)

Diferente do fluxo de atendimento (que responde dentro da janela de 24h
aberta pelo cliente), estas são mensagens que a **empresa** inicia sem o
cliente ter mandado nada antes. A regra da Meta pra isso é clara: só pode
usar um **modelo de mensagem (template) aprovado** — texto livre não
funciona. Antes de ativar este workflow, crie no **WhatsApp Manager**
(Meta) → **Modelos de mensagens**, idioma `pt_BR`:

| Nome exato | Variáveis do corpo | Exemplo |
|---|---|---|
| `aniversario_cliente` | `{{1}}` nome do cliente, `{{2}}` nome da empresa | "Feliz aniversário, {{1}}! 🎉 Toda a equipe do {{2}} deseja um dia incrível pra você." |
| `lembrete_manutencao` | `{{1}}` nome do cliente, `{{2}}` nome do serviço, `{{3}}` data por extenso | "Oi {{1}}! Sua {{2}} foi em {{3}} — já está quase na hora da manutenção 💅 Quer agendar?" |

Os nomes precisam bater **exatamente** com o que está no workflow. A
aprovação da Meta costuma ser rápida (minutos a poucas horas).

## Campos novos no Firestore

Pra esse workflow funcionar, cada cliente/serviço precisa ter (ver
`firestore/schema.md`):

- `clientes/{telefone}`: `dataNascimento`, `ultimoServicoNome`, `ultimoServicoData`.
- `servicos/{servicoId}`: `intervaloManutencaoDias`.

Até existir painel administrativo, isso é preenchido manualmente no
console do Firestore depois de cada atendimento.

## Limitações conhecidas

- Se o n8n ficar fora do ar no dia exato do aniversário/manutenção, o
  lembrete daquele ciclo é perdido (não há reenvio automático depois —
  a comparação é sempre "é hoje?", não "está atrasado?").
- `ultimoServicoNome` precisa bater com o nome do serviço letra por letra;
  não há normalização/fuzzy match.
- Um cliente com aniversário e manutenção no mesmo dia recebe as duas
  mensagens separadamente.

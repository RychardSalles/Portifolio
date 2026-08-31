# Esquema do Firestore — RD Webdesign SaaS

Modelo multi-tenant: cada empresa (salão) é um documento em `empresas`, com
tudo que é dela (serviços, clientes, conversas) guardado em subcoleções por
baixo desse documento. Nada de uma empresa nunca deve aparecer em consultas
de outra — toda leitura/escrita feita pela function e pelo n8n é sempre
filtrada por `empresaId`.

Os campos são **propositalmente planos** (sem mapas aninhados tipo
`whatsapp.phoneNumberId`) pra simplificar o parsing das respostas da
API REST do Firestore no workflow do n8n.

## `empresas/{empresaId}`

| Campo | Tipo | Descrição |
|---|---|---|
| `nome` | string | Nome do salão, usado na identidade da IA e nas mensagens. |
| `endereco` | string | Endereço mostrado pela IA quando perguntado. |
| `horario` | string | Ex: `"Seg a Sáb, 9h às 19h"`. Texto livre — a IA só repassa. |
| `descricao` | string | Descrição curta do negócio (opcional). |
| `instagram` | string | `@usuario` (opcional). |
| `iaAtiva` | boolean | Liga/desliga a IA pra essa empresa inteira. |
| `iaPersonalidade` | string | Ex: `"simpática, objetiva e usa emojis com moderação"`. |
| `iaSaudacao` | string | Saudação preferida (opcional — a IA decide sozinha se vazio). |
| `iaRegrasAdicionais` | string | Regras extras específicas do negócio, coladas no prompt. |
| `iaPalavrasChaveTransferencia` | array\<string\> | Palavras que, se aparecerem na mensagem do cliente, pulam a IA e vão direto pro atendimento humano. Padrão sugerido: `["atendente", "humano", "pessoa de verdade", "falar com alguém"]`. |
| `whatsappPhoneNumberId` | string | `phone_number_id` da Cloud API — é a chave usada pela Cloud Function pra descobrir de qual empresa é cada mensagem recebida. |
| `whatsappAccessToken` | string | Token de acesso da Cloud API usado pra **enviar** mensagens por essa empresa. Ver aviso de segurança abaixo. |
| `whatsappTelefoneNotificacao` | string | Número (formato `55DDDNÚMERO`) de um funcionário/dona pra avisar quando um cliente pede atendimento humano. Opcional. |

> ⚠️ **Sobre o `whatsappAccessToken`**: por ora ele fica direto no documento
> porque é o que o workflow do n8n consegue ler de forma simples via REST.
> Isso é aceitável para uma primeira versão (o documento não é público — só
> a Cloud Function via Admin SDK e o n8n via conta de serviço com IAM têm
> acesso), mas para produção o recomendado é mover esse valor para o
> **Secret Manager** do Google Cloud e o n8n buscar o segredo por lá em vez
> de ler do Firestore. Deixado como próxima melhoria, não bloqueia o v1.

## `empresas/{empresaId}/servicos/{servicoId}`

| Campo | Tipo | Descrição |
|---|---|---|
| `nome` | string | Ex: `"Alongamento de unha"`. |
| `descricao` | string | Descrição curta (opcional). |
| `preco` | number | Em reais. Se não informado, a IA diz "sob consulta". |
| `duracaoMinutos` | number | Duração estimada (opcional). |
| `disponivel` | boolean | Só serviços com `true` entram no prompt da IA. |
| `intervaloManutencaoDias` | number | Opcional. Se preenchido, o workflow de lembretes (`n8n/README.md`) avisa o cliente quando esse tanto de dias tiver passado desde o último atendimento com esse serviço. |

## `empresas/{empresaId}/clientes/{telefone}`

`{telefone}` é o `wa_id` do cliente (o número de WhatsApp dele, sem `+` nem
espaços — é o mesmo formato que a Cloud API já manda no campo `from`).

| Campo | Tipo | Descrição |
|---|---|---|
| `nome` | string | Nome do contato (vem do perfil do WhatsApp, quando disponível). |
| `status` | string | `"ia"` (IA está respondendo) ou `"aguardando_humano"`. |
| `iaAtiva` | boolean | Espelha o status — `false` enquanto aguarda humano. |
| `ultimaInteracaoEm` | timestamp | Atualizado a cada mensagem trocada. |
| `dataNascimento` | string | Opcional, formato `"AAAA-MM-DD"`. Usado pelo workflow de lembretes pra mandar mensagem de aniversário (o ano é ignorado, só mês/dia importam). |
| `ultimoServicoNome` | string | Opcional. Nome do último serviço feito (precisa bater exatamente com o `nome` de um documento em `servicos`). Preenchido manualmente até existir painel admin. |
| `ultimoServicoData` | string | Opcional, formato `"AAAA-MM-DD"`. Data do último atendimento — base pro cálculo da manutenção. |

### `empresas/{empresaId}/clientes/{telefone}/mensagens/{mensagemId}`

Histórico da conversa, uma mensagem por documento (ID automático).

| Campo | Tipo | Descrição |
|---|---|---|
| `direcao` | string | `"entrada"` (do cliente) ou `"saida"` (da IA/empresa). |
| `texto` | string | Conteúdo da mensagem. |
| `tipo` | string | `"text"`, `"interactive"`, etc. |
| `motivoTransferencia` | string | Só em mensagens de saída que avisam a transferência: `"palavra-chave"` ou `"ia"`. |
| `registradoEm` | timestamp | Quando foi gravado. |

## `webhooks_nao_identificados/{id}`

Rede de segurança: toda mensagem que chega num `phone_number_id` sem
nenhuma empresa cadastrada cai aqui em vez de ser descartada, pra dar pra
investigar (número cadastrado errado, empresa ainda não configurada etc.).
Só a Cloud Function (via Admin SDK, que ignora as regras do Firestore)
escreve aqui.

## Índices

Nenhum índice composto é necessário — a única consulta feita pela Cloud
Function (`where whatsappPhoneNumberId ==`) é um filtro de campo único,
que o Firestore já indexa automaticamente.

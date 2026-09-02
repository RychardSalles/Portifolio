# -*- coding: utf-8 -*-
"""
content.py — Fonte única de conteúdo do site RD Webdesign.

Edite os dados aqui e rode `python build.py` para regerar o site em dist/.
Nada de HTML: só texto, preços e listas. Os templates cuidam da marcação.
"""

# ─────────────────────────────────────────────────────────────
#  Dados globais da marca
# ─────────────────────────────────────────────────────────────
SITE = {
    "brand": "RD Webdesign",
    "domain": "rdwebdesign.com.br",
    "base_url": "https://rdwebdesign.com.br",
    "tagline": "Ajudamos empresas a crescer com tecnologia, automação e presença digital",
    "description": (
        "Ajudamos empresas a conseguirem mais clientes e aumentarem suas vendas "
        "através de soluções digitais: sites, landing pages, lojas virtuais e "
        "presença digital completa."
    ),
    "philosophy": (
        "Nós não vendemos sites. Criamos soluções digitais que ajudam empresas a "
        "vender mais, economizar tempo e crescer de forma sustentável."
    ),
    "niche": "Especialista em presença digital para negócios de beleza e estética",
    "whatsapp": "5511919948528",
    "whatsapp_display": "(11) 91994-8528",
    "email": "rychardsilva205@gmail.com",
    "hours": "Seg–Sex, 9h às 18h",
    "year": 2026,
    "response_time": "Respondo em até 2 horas no WhatsApp",
}

WHATSAPP_DEFAULT_MSG = "Olá! Vim pelo site da RD Webdesign e gostaria de um orçamento."


# ─────────────────────────────────────────────────────────────
#  Navegação principal
# ─────────────────────────────────────────────────────────────
NAV = [
    {"label": "Serviços", "href": "/servicos.html"},
    {"label": "Planos", "href": "/precos.html#planos"},
    {"label": "Preços", "href": "/precos.html"},
    {"label": "Portfólio", "href": "/portifolio.html"},
    {"label": "Processo", "href": "/index.html#processo"},
    {"label": "Por que eu?", "href": "/index.html#prova"},
    {"label": "Dúvidas", "href": "/index.html#faq"},
]


# ─────────────────────────────────────────────────────────────
#  Estatísticas honestas (home)
# ─────────────────────────────────────────────────────────────
STATS = [
    {"value": 7, "suffix": "d", "label": "Prazo médio de entrega"},
    {"value": 30, "suffix": "d", "label": "Suporte incluso pós-entrega"},
    {"value": 100, "suffix": "%", "label": "Dedicação ao seu projeto"},
]


# ─────────────────────────────────────────────────────────────
#  Serviços — usados na home, em /servicos e para gerar as
#  páginas de detalhe rd-*.html
# ─────────────────────────────────────────────────────────────
SERVICES = [
    {
        "slug": "site-institucional",
        "page": "rd-site-institucional.html",
        "icon": "🌐",
        "name": "Site Institucional",
        "short": "Presença profissional que transmite credibilidade e atrai clientes 24h por dia.",
        "price": "R$ 3.900",
        "price_full": "R$ 3.900,00",
        "highlights": [
            "Até 15 páginas",
            "Design exclusivo e responsivo",
            "SEO otimizado",
            "Domínio e hospedagem inclusos (1 ano)",
        ],
        "cta": "Saiba mais",
        "detail": {
            "badge": "🌐 Site Institucional",
            "hero_title_html": "Sua empresa <span>online</span> com presença que gera resultados",
            "hero_sub": (
                "Um site profissional que funciona como seu melhor vendedor: atrai "
                "clientes, transmite credibilidade e aparece no Google — tudo 24h "
                "por dia, 7 dias por semana."
            ),
            "meta_title": "Site Institucional Profissional – RD Webdesign",
            "meta_desc": (
                "Site institucional profissional que atrai clientes 24h por dia. "
                "Design exclusivo, SEO, domínio e hospedagem inclusos. A partir de R$ 3.900."
            ),
            "guarantees": ["Entrega em até 7 dias", "Design exclusivo", "Suporte 30 dias grátis"],
            "for_who": [
                {"icon": "🏪", "title": "Empresário local", "desc": "Quer ser encontrado no Google quando alguém procurar pelo seu serviço na cidade."},
                {"icon": "💼", "title": "Profissional liberal", "desc": "Médico, advogado, consultor, arquiteto — quer um canal digital que transmita autoridade."},
                {"icon": "🏗️", "title": "Prestador de serviços", "desc": "Construtora, clínica, academia, escola — precisa de um site que mostre seu trabalho."},
                {"icon": "🚀", "title": "Empresa em crescimento", "desc": "Quer profissionalizar a imagem digital e atrair clientes maiores e melhores."},
            ],
            "includes": [
                ("Até 15 páginas personalizadas", "Home, Sobre, Serviços, Blog, Contato, Portfólio e muito mais."),
                ("Design 100% exclusivo e responsivo", "Perfeito em celular, tablet e computador. Feito sob medida para sua marca."),
                ("SEO básico otimizado", "Configuração para aparecer no Google com as palavras-chave do seu negócio."),
                ("Domínio + Hospedagem inclusos (1 ano)", "Seu endereço .com.br e servidor rápido já incluídos no preço."),
                ("Formulário e WhatsApp integrados", "Receba mensagens direto no seu e-mail e WhatsApp."),
                ("Suporte técnico por 30 dias", "Após a entrega, acompanhamos e corrigimos qualquer ajuste necessário."),
                ("Velocidade otimizada (menos de 2s)", "Sites lentos perdem clientes. O seu vai carregar na velocidade da luz."),
            ],
            "price_note": "Preço fixo. Sem mensalidade obrigatória após 1 ano.",
            "process": [
                ("💬", "Briefing", "Conversa pelo WhatsApp para entender sua empresa, público e objetivos."),
                ("🎨", "Layout", "Criamos o design e enviamos para sua aprovação antes de desenvolver."),
                ("⚙️", "Desenvolvimento", "Desenvolvemos o site com todas as funcionalidades e conteúdo."),
                ("🚀", "Publicação", "Publicamos o site e acompanhamos por 30 dias de suporte gratuito."),
            ],
            "faq": [
                ("Preciso ter um domínio antes de contratar?", "Não! O domínio já está incluso no pacote. Escolhemos o endereço ideal para o seu negócio e configuramos tudo."),
                ("Consigo mexer no site depois de pronto?", "Sim. Entregamos com painel de fácil administração onde você edita textos, imagens e adiciona conteúdo sem precisar de técnico."),
                ("Qual é a forma de pagamento?", "50% de entrada para iniciar o projeto e 50% na entrega. Aceito Pix, transferência bancária e cartão de crédito."),
                ("O site vai aparecer no Google?", "Faço a otimização SEO básica (títulos, meta tags, velocidade, mapa do site) para facilitar a indexação. Resultados orgânicos levam de 30 a 90 dias."),
                ("E depois do 1º ano de hospedagem?", "Você pode renovar comigo (planos a partir de R$ 297/mês) ou migrar para qualquer servidor que preferir. O site é todo seu."),
            ],
            "portfolio_tag": "institucional",
        },
    },
    {
        "slug": "landing-page",
        "page": "rd-landing-page.html",
        "icon": "🎯",
        "name": "Landing Page",
        "short": "Página de alta conversão focada em transformar visitantes em clientes e leads qualificados.",
        "price": "R$ 1.400",
        "price_full": "R$ 1.400,00",
        "highlights": [
            "Copywriting incluso",
            "Formulário de captura",
            "Integração com WhatsApp",
            "Entrega em 3 dias",
        ],
        "cta": "Saiba mais",
        "featured": True,
        "detail": {
            "badge": "🎯 Landing Page",
            "hero_title_html": "Transforme cliques em <span>clientes de verdade</span>",
            "hero_sub": (
                "Uma página criada com um único objetivo: converter. Copywriting "
                "estratégico, design focado e entrega em 3 dias para você já começar "
                "a colher resultados."
            ),
            "meta_title": "Landing Page de Alta Conversão – RD Webdesign",
            "meta_desc": (
                "Landing pages que transformam visitantes em clientes. Copywriting "
                "incluso, entrega em 3 dias. A partir de R$ 1.400."
            ),
            "guarantees": ["Entrega em 3 dias", "Copywriting incluso", "Alta conversão"],
            "for_who": [
                {"icon": "🎯", "title": "Foco total em conversão", "desc": "Sem distrações, menus ou links externos. Toda a atenção do visitante vai para a única ação que importa."},
                {"icon": "✍️", "title": "Copywriting estratégico incluso", "desc": "Escrevo todos os textos com técnicas de persuasão que fazem o visitante querer agir agora."},
                {"icon": "📱", "title": "Integração com WhatsApp", "desc": "O cliente clica e cai direto no seu WhatsApp com uma mensagem pré-formatada. Zero atrito."},
                {"icon": "⚡", "title": "Carrega em menos de 2 segundos", "desc": "Sites lentos perdem até 53% dos visitantes. Sua landing page é otimizada para converter."},
            ],
            "includes": [
                ("Copywriting profissional incluso", "Escrevo todos os textos da página com foco em conversão."),
                ("Design responsivo e focado", "Layout exclusivo para desktop e mobile, sem distrações."),
                ("Formulário de captura de leads", "Receba dados dos interessados diretamente no seu e-mail."),
                ("Botão WhatsApp integrado", "CTA direto para o WhatsApp com mensagem pré-configurada."),
                ("Hospedagem por 1 ano inclusa", "Publico a página no seu domínio ou em um subdomínio dedicado."),
                ("Pixel do Facebook + Google Tag Manager", "Configuro o rastreamento para suas campanhas de tráfego pago."),
                ("Entrega em 3 dias úteis", "Processo ágil e sem burocracia do briefing à publicação."),
            ],
            "price_note": "Preço único. Sem mensalidades ocultas.",
            "badge_extra": "⭐ Mais contratado",
            "process": [
                ("💬", "Briefing", "Você me conta sobre seu produto/serviço, público e objetivo."),
                ("✍️", "Copy + Design", "Crio os textos e o layout. Você aprova antes de publicar."),
                ("⚙️", "Desenvolvimento", "Desenvolvo a página com todos os rastreamentos configurados."),
                ("🚀", "No ar!", "Publico e você já pode divulgar e colher leads."),
            ],
            "faq": [
                ("Landing page é diferente de um site?", "Sim. Um site tem várias páginas e objetivos. Uma landing page tem uma página só, com um único objetivo, o que a torna muito mais eficiente para campanhas."),
                ("Funciona com Google Ads e Facebook Ads?", "Perfeitamente. Configuro os pixels e tags necessários para que seu tráfego pago converta melhor e você acompanhe o custo por lead."),
                ("Preciso ter texto pronto para passar?", "Não! O copywriting está incluso. Basta fazer o briefing respondendo sobre seu produto, diferenciais e público-alvo."),
                ("Posso alterar o conteúdo depois?", "Sim. Dentro dos 30 dias de suporte, faço alterações de texto e imagens sem custo extra."),
                ("Qual é o prazo de entrega real?", "3 dias úteis após aprovação do briefing e pagamento da entrada. Em alguns casos entrego em menos tempo."),
            ],
            "portfolio_tag": "landing",
        },
    },
    {
        "slug": "loja-virtual",
        "page": "rd-loja-virtual.html",
        "icon": "🛒",
        "name": "Loja Virtual",
        "short": "E-commerce completo para você vender todos os dias. Integrado com Pix, cartão e boleto.",
        "price": "R$ 6.900",
        "price_full": "R$ 6.900,00",
        "highlights": [
            "Até 50 produtos",
            "Pagamentos integrados",
            "Painel administrativo",
            "Gestão de estoque",
        ],
        "cta": "Saiba mais",
        "detail": {
            "badge": "🛒 Loja Virtual",
            "hero_title_html": "Venda todos os dias <span>pela internet</span>",
            "hero_sub": (
                "E-commerce completo com pagamentos integrados, controle de estoque "
                "e painel de gestão fácil. Você foca em vender — a loja cuida do resto."
            ),
            "meta_title": "Loja Virtual Profissional – RD Webdesign",
            "meta_desc": (
                "E-commerce completo com Pix, cartão, boleto e painel de gestão. "
                "Até 50 produtos. A partir de R$ 6.900."
            ),
            "guarantees": ["Até 50 produtos", "Pix + Cartão + Boleto", "Painel de gestão"],
            "for_who": [
                {"icon": "👗", "title": "Loja de roupas e acessórios", "desc": "Mostre seu catálogo completo, aceite pagamentos e venda mesmo com a loja física fechada."},
                {"icon": "🍕", "title": "Restaurante e delivery", "desc": "Cardápio digital com pedidos online, integrado ao WhatsApp para confirmação."},
                {"icon": "💄", "title": "Cosméticos e beleza", "desc": "Venda produtos para todo o Brasil com frete automatizado e checkout seguro."},
                {"icon": "🛍️", "title": "Qualquer produto físico", "desc": "Se você tem algo para vender, a loja virtual permite escalar sem ponto físico."},
            ],
            "includes": [
                ("Até 50 produtos cadastrados", "Fotos, descrições, preços e variações (tamanho, cor etc.)."),
                ("Pix, cartão de crédito e boleto integrados", "Checkout seguro sem o cliente precisar sair da loja."),
                ("Painel administrativo completo", "Você mesmo adiciona produtos, vê pedidos e gerencia tudo."),
                ("Controle de estoque automático", "O estoque baixa automaticamente a cada venda."),
                ("Cálculo de frete automático (Correios)", "O cliente calcula o frete antes de finalizar o pedido."),
                ("Design exclusivo e responsivo", "Layout profissional personalizado para a identidade da sua marca."),
                ("Domínio + Hospedagem (1 ano)", "Tudo pronto para você já compartilhar o link da loja."),
            ],
            "price_note": "Preço único. Sem mensalidade de plataforma.",
            "process": [
                ("💬", "Briefing", "Conversa sobre produtos, marca, meios de pagamento e logística."),
                ("🎨", "Layout", "Crio o design da loja e aprovo com você antes de desenvolver."),
                ("⚙️", "Desenvolvimento", "Desenvolvo, cadastro produtos e configuro os pagamentos."),
                ("🚀", "Publicação", "Loja no ar, testada e pronta para receber seus primeiros pedidos."),
            ],
            "faq": [
                ("Preciso pagar mensalidade de plataforma?", "Não! A loja é desenvolvida de forma própria. Você só paga a renovação anual da hospedagem — sem mensalidades de Shopify ou Nuvemshop."),
                ("Como funcionam os pagamentos?", "Integro com gateways como Mercado Pago ou PagSeguro. O dinheiro cai direto na sua conta em 1 a 14 dias dependendo da forma de pagamento."),
                ("Posso adicionar mais produtos depois?", "Sim! Você mesmo adiciona produtos pelo painel administrativo depois da entrega. O treinamento está incluso."),
                ("A loja funciona no celular?", "Com certeza. O design é 100% responsivo. A maioria das compras hoje é feita pelo celular."),
                ("Qual é o prazo de entrega?", "Entre 7 e 10 dias úteis após briefing e pagamento da entrada, dependendo da quantidade de produtos e integrações."),
            ],
            "portfolio_tag": "loja",
        },
    },
    {
        "slug": "logotipo",
        "page": "rd-logotipo.html",
        "icon": "✏️",
        "name": "Logotipo & Identidade Visual",
        "short": "Identidade visual profissional que diferencia sua marca e gera reconhecimento no mercado.",
        "price": "R$ 950",
        "price_full": "R$ 950,00",
        "highlights": [
            "3 conceitos iniciais",
            "Revisões incluídas",
            "Arquivos vetoriais",
            "Manual de marca",
        ],
        "cta": "Saiba mais",
        "detail": {
            "badge": "✏️ Logotipo & Identidade Visual",
            "hero_title_html": "Sua marca com uma <span>identidade que impõe</span> respeito",
            "hero_sub": (
                "Um logotipo profissional é o primeiro passo para ser levado a sério. "
                "Crio marcas que ficam na memória, geram confiança e se destacam da "
                "concorrência."
            ),
            "meta_title": "Logotipo & Identidade Visual – RD Webdesign",
            "meta_desc": (
                "Logotipo profissional com identidade visual completa. 3 conceitos, "
                "arquivos vetoriais e manual de marca. R$ 950."
            ),
            "guarantees": ["3 conceitos iniciais", "Arquivos vetoriais", "Manual de marca incluso"],
            "for_who": [
                {"icon": "🧠", "title": "Fica na memória", "desc": "Um logo bem feito é reconhecido em frações de segundo. Clientes lembram de você sem ler o nome."},
                {"icon": "🤝", "title": "Gera confiança", "desc": "Uma identidade visual profissional transmite seriedade e faz os clientes se sentirem seguros para comprar."},
                {"icon": "🏆", "title": "Diferencia da concorrência", "desc": "Com um visual único e coerente, você se destaca no mercado e justifica cobrar mais."},
                {"icon": "🔄", "title": "Funciona em todo lugar", "desc": "Site, cartão, uniforme, embalagem, redes sociais — entrego versões para cada aplicação."},
            ],
            "includes": [
                ("3 conceitos iniciais diferentes", "Três direções criativas para você escolher a que mais representa sua marca."),
                ("Revisões inclusas até aprovação", "Ajusto cores, tipografia e formas até você ficar satisfeito."),
                ("Arquivos vetoriais (AI, SVG, PDF)", "Formatos profissionais para impressão em qualquer tamanho sem perder qualidade."),
                ("Versões PNG com fundo transparente", "Para usar no site, WhatsApp, apresentações e redes sociais."),
                ("Variações (cor, P&B, fundo escuro e claro)", "Logo adaptado para cada contexto de uso."),
                ("Manual de marca (brand guidelines)", "Documento com as cores, fontes e regras de uso correto da identidade visual."),
            ],
            "price_note": "Preço único. Todos os arquivos são seus.",
            "process": [
                ("📝", "Briefing", "Você responde sobre sua empresa, público, valores e referências visuais."),
                ("💡", "3 Conceitos", "Envio 3 propostas criativas diferentes para sua avaliação."),
                ("✏️", "Refinamento", "Você escolhe um conceito e ajustamos os detalhes até ficar perfeito."),
                ("📦", "Entrega final", "Todos os arquivos + manual de marca entregues pelo Google Drive."),
            ],
            "faq": [
                ("Quantas revisões estão incluídas?", "Não limito o número de revisões. Trabalho até você estar satisfeito. Revisões que saem completamente do briefing original podem gerar custo adicional."),
                ("Posso usar o logo para imprimir em qualquer tamanho?", "Sim! Entrego em formato vetorial (AI e SVG), o que permite impressão de cartão de visitas a outdoor sem perder qualidade."),
                ("Preciso ter alguma ideia do logo antes?", "Não é obrigatório. Quanto mais referências você tiver, melhor. Mas o briefing que aplico ajuda a descobrir a direção certa."),
                ("O logotipo fica sendo meu?", "Sim! Após a aprovação e pagamento integral, todos os direitos são transferidos para você. O arquivo é seu para sempre."),
                ("Posso usar o logo nas redes sociais?", "Sim, e ainda entrego versões em PNG com fundo transparente, no tamanho ideal para Instagram, WhatsApp e outras plataformas."),
            ],
            "portfolio_tag": "institucional",
        },
    },
]

# Serviços extras (aparecem na home e em /servicos, sem página de detalhe)
EXTRA_SERVICES = [
    {
        "icon": "📍",
        "name": "Apareça no Google Maps",
        "short": "Cadastro completo no Google Meu Negócio para você aparecer nas buscas locais e no mapa.",
        "highlights": ["Perfil otimizado", "Fotos e categorias corretas", "Verificação do negócio", "Aparece no Google Maps"],
        "cta": "Fale comigo",
    },
    {
        "icon": "⚡",
        "name": "Outros Serviços",
        "short": "Cartão de visitas digital, atualização de sites, assinatura de e-mail e mais.",
        "highlights": ["Cartão de visitas digital", "Atualização de sites", "Assinatura de e-mail"],
        "cta": "Fale comigo",
    },
]


# ─────────────────────────────────────────────────────────────
#  Planos de manutenção mensal
# ─────────────────────────────────────────────────────────────
PLAN_FEATURES = [
    "Hospedagem inclusa",
    "Suporte via WhatsApp",
    "Alterações mensais",
    "Relatório de visitas",
    "Atualização de conteúdo",
    "Automação de WhatsApp",
    "Captação de leads",
]

PLANS = [
    {
        "name": "Plano Base",
        "price": "R$ 297",
        "period": "/mês",
        "cta": "Quero o Básico",
        "featured": False,
        "cells": ["sim", "sim", "2x por mês", "não", "não", "não", "não"],
    },
    {
        "name": "Plano Crescimento",
        "price": "R$ 597",
        "period": "/mês",
        "cta": "Quero Crescer",
        "featured": True,
        "badge": "Mais popular",
        "cells": ["sim", "sim", "Ilimitadas", "sim", "sim", "não", "não"],
    },
    {
        "name": "Plano Premium",
        "price": "R$ 1.197",
        "period": "/mês",
        "cta": "Quero o Máximo",
        "featured": False,
        "cells": ["sim", "sim", "Ilimitadas", "sim", "sim", "sim", "sim"],
    },
]

MAINTENANCE_NOTE = (
    "Um site sem manutenção é como uma loja com vitrine parada. Links quebram, "
    "textos ficam desatualizados e o Google penaliza sites lentos. Com um plano "
    "mensal, seu site continua funcionando, atualizado e aparecendo nas buscas — "
    "enquanto você foca no seu negócio."
)


# ─────────────────────────────────────────────────────────────
#  Tabela de preços completa (/precos)
# ─────────────────────────────────────────────────────────────
PRICE_TABLE = [
    {"icon": "🌐", "name": "Site Institucional (até 15 páginas)", "price": "R$ 3.900,00", "href": "/rd-site-institucional.html"},
    {"icon": "🛒", "name": "Loja Virtual (até 50 produtos)", "price": "R$ 6.900,00", "href": "/rd-loja-virtual.html"},
    {"icon": "🎯", "name": "Landing Page", "price": "R$ 1.400,00", "href": "/rd-landing-page.html", "highlight": True},
    {"icon": "✏️", "name": "Logotipo + Identidade Visual", "price": "R$ 950,00", "href": "/rd-logotipo.html"},
    {"icon": "📧", "name": "Assinatura de E-mail Profissional", "price": "R$ 280,00", "href": "/index.html#contato"},
    {"icon": "📍", "name": "Cadastro no Google Meu Negócio", "price": "R$ 750,00", "href": "/index.html#contato"},
    {"icon": "💳", "name": "Cartão de Visitas Digital", "price": "R$ 240,00", "href": "/index.html#contato"},
    {"icon": "🔧", "name": "Atualização de Site Existente", "price": "R$ 420,00", "href": "/index.html#contato"},
    {"icon": "🖨️", "name": "Cartão de Visitas Impresso (1.000 un.)", "price": "R$ 570,00", "href": "/index.html#contato"},
    {"icon": "📖", "name": "Manuais (até 28 páginas)", "price": "R$ 4.500,00", "href": "/index.html#contato"},
]

PRICE_NOTE = (
    "Todos os valores são fixos e negociados antes do início do projeto. Não cobro "
    "por revisões básicas, ajustes de conteúdo ou funcionalidades que já deveriam "
    "estar inclusas. Se o escopo mudar durante o desenvolvimento, combinamos o "
    "valor extra com antecedência — sempre com sua aprovação."
)


# ─────────────────────────────────────────────────────────────
#  Portfólio — projetos reais publicados
#  category: landing | loja | institucional
# ─────────────────────────────────────────────────────────────
PROJECTS = [
    {"name": "Belle Cílios", "url": "https://belle-cilios.netlify.app/", "category": "landing", "tag": "Landing Page • Beleza", "featured": True},
    {"name": "Restaurante FOOD", "url": "https://landing-page-restaurante.netlify.app", "category": "landing", "tag": "Landing Page • Restaurante"},
    {"name": "Beauty Bella Studios", "url": "https://beauty-bella-studios.netlify.app", "category": "landing", "tag": "Landing Page • Beleza"},
    {"name": "Marketing Criativo", "url": "https://landing-pagen.netlify.app", "category": "landing", "tag": "Landing Page • Newsletter"},
    {"name": "Nova Era Store", "url": "https://nova-era-store.netlify.app", "category": "loja", "tag": "Loja Virtual • Streetwear"},
    {"name": "Black Gold Barbearia", "url": "https://black-gold-barbearia.netlify.app", "category": "institucional", "tag": "Site Institucional • Barbearia"},
    {"name": "Brasa & Sal", "url": "https://brasa-e-sal.netlify.app", "category": "institucional", "tag": "Site Institucional • Restaurante"},
    {"name": "Pinnacle Imóveis", "url": "https://pinnacle-imoveis.netlify.app", "category": "institucional", "tag": "Site Institucional • Imóveis"},
    {"name": "Chácara Monte Verde", "url": "https://chacara-monteverde.netlify.app", "category": "institucional", "tag": "Site Institucional • Eventos"},
    {"name": "Abby Consultora de Imóveis", "url": "https://consultora-imoveis.netlify.app", "category": "landing", "tag": "Landing Page • Imóveis"},
    {"name": "Saber Ensino Individual", "url": "https://saber-ensino-site.netlify.app", "category": "institucional", "tag": "Site Institucional • Educação"},
]

PROJECT_FILTERS = [
    {"key": "all", "label": "Todos"},
    {"key": "landing", "label": "Landing Page"},
    {"key": "loja", "label": "Loja Virtual"},
    {"key": "institucional", "label": "Site Institucional"},
]


# ─────────────────────────────────────────────────────────────
#  Processo (home)
# ─────────────────────────────────────────────────────────────
PROCESS = [
    {"num": "01", "emoji": "💬", "title": "Briefing", "desc": "Conversa inicial pelo WhatsApp para entender seu negócio e objetivos."},
    {"num": "02", "emoji": "🎨", "title": "Design", "desc": "Crio o layout exclusivo e envio para sua aprovação."},
    {"num": "03", "emoji": "⚙️", "title": "Desenvolvimento", "desc": "Desenvolvo rápido, seguro e responsivo para todos os dispositivos."},
    {"num": "04", "emoji": "🚀", "title": "Entrega", "desc": "Publico, acompanho os primeiros 30 dias e ofereço planos de manutenção mensal para quem quer continuar crescendo."},
]


# ─────────────────────────────────────────────────────────────
#  Por que a RD Webdesign? (home)
# ─────────────────────────────────────────────────────────────
PROOF_INTRO = (
    "Trabalho com foco total — sem terceirização, sem equipes genéricas. Cada "
    "projeto recebe atenção que agência grande não consegue dar."
)

TESTIMONIALS = [
    {
        "text": "Olá, bom dia! Está sendo ótimo, bastante elogios do site.",
        "author": "Leandra, Belle Cílios (via WhatsApp)",
    },
]

COMMITMENTS = [
    {"icon": "🎯", "title": "Atenção exclusiva no seu projeto", "text": "Não trabalho com dezenas de clientes ao mesmo tempo. Quando o projeto é seu, é 100% meu — sem terceirizações, sem equipes genéricas."},
    {"icon": "💰", "title": "Preço fechado, sem surpresas", "text": "O valor combinado no início é o valor que você paga no final. Sem cobrar por ajustes básicos, revisões obrigatórias ou funcionalidades que já deveriam estar inclusas."},
    {"icon": "📱", "title": "Comunicação direta e humana", "text": "Você fala comigo diretamente pelo WhatsApp — não com assistente, secretária ou formulário. Atualização constante e clareza em cada etapa."},
]


# ─────────────────────────────────────────────────────────────
#  FAQ (home)
# ─────────────────────────────────────────────────────────────
FAQ = [
    ("Achei caro, dá pra fazer mais barato?", "O valor cobre um projeto sob medida — design exclusivo, otimizado pra conversão e com suporte real, não um template genérico. Se o seu orçamento agora é mais enxuto, a Landing Page (R$ 1.400) já entrega presença digital profissional com um investimento menor. Me chama e vemos juntos a melhor opção."),
    ("Posso pensar e te chamo depois?", "Claro, sem pressão nenhuma. Só um ponto: como eu assumo um projeto por vez pra dar atenção total a cada cliente, a data de início é reservada por ordem de chegada. Se quiser garantir a vaga mais próxima, é só avisar quando decidir."),
    ("Domínio e hospedagem, como funciona?", "No Site Institucional, domínio e hospedagem do primeiro ano já estão inclusos no valor — você não paga nada a mais pra colocar o site no ar. A partir do segundo ano, a renovação do domínio (geralmente entre R$ 40 e R$ 60/ano) é cobrada direto pelo registro do domínio, não por mim."),
]


# ─────────────────────────────────────────────────────────────
#  Formulário de contato — opções do select
# ─────────────────────────────────────────────────────────────
CONTACT_OPTIONS = [
    "Site Institucional – R$ 3.900",
    "Landing Page – R$ 1.400",
    "Loja Virtual – R$ 6.900",
    "Logotipo – R$ 950",
    "Plano de Manutenção Mensal – a partir de R$ 297/mês",
    "Outro",
]

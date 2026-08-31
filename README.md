# RD Webdesign — site

Site da RD Webdesign. O HTML **não é escrito à mão**: um script Python
(`build.py`) monta as páginas a partir do conteúdo em `content.py` e dos
templates em `templates/`. O resultado vai para `dist/`, que é o que o
Netlify publica.

## Estrutura

```
content.py              → TODO o texto/preços/projetos do site (edite aqui)
templates/              → moldes HTML (Jinja2)
  _base.html            → nav, rodapé, cursor, transições, scripts
  _macros.html          → componentes reutilizáveis (cards, FAQ…)
  index.html            → home
  servicos.html         → lista de serviços
  precos.html           → tabela de preços + planos
  portifolio.html       → grade de projetos com filtro
  servico.html          → gera as 4 páginas rd-*.html
static/                 → arquivos copiados como estão
  assets/css/style.css  → todo o CSS
  assets/js/app.js       → todas as animações/interações (vanilla JS)
  img/favicon.png
build.py                → o gerador
dist/                   → SAÍDA (gerada, não versionada)
```

## Editar o site

1. Abra `content.py` e mude o que precisar (um preço, um projeto novo,
   um texto de FAQ…). Nenhum HTML envolvido.
2. Rode o build:
   ```
   python build.py
   ```
3. Confira localmente:
   ```
   python build.py --serve
   ```
   Abre em <http://localhost:8000>. **Não abra os arquivos de `dist/`
   com dois cliques** — os caminhos são absolutos (`/assets/...`) e só
   funcionam servidos por um servidor (o `--serve` ou o Netlify).
4. `git add -A && git commit && git push` — o Netlify roda o `build.py`
   sozinho e publica o `dist/`.

## Como o Netlify sabe o que fazer

Está tudo no `netlify.toml`:

- **Build command:** `pip install -r requirements.txt && python build.py`
- **Publish directory:** `dist`
- **Python:** 3.12

## Dependências

Só o Jinja2 (`requirements.txt`). Instale local com:

```
pip install -r requirements.txt
```

## Adicionar um projeto ao portfólio

Em `content.py`, na lista `PROJECTS`, adicione:

```python
{"name": "Nome do Cliente", "url": "https://site.netlify.app",
 "category": "landing", "tag": "Landing Page • Nicho"},
```

`category` = `landing`, `loja` ou `institucional` (controla o filtro).

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build.py — Gerador estático do site RD Webdesign.

Uso:
    python build.py            # gera o site em dist/
    python build.py --serve    # gera e sobe um preview em http://localhost:8000

Fluxo:
    content.py  ->  templates/*.html (Jinja2)  ->  dist/*.html
    static/**   ->  dist/**  (copiado como está: CSS, JS, imagens)

Deploy (Netlify): o netlify.toml roda `python build.py` e publica dist/.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import http.server
import shutil
import socketserver
import sys
from pathlib import Path

try:
    from jinja2 import Environment, FileSystemLoader, select_autoescape
except ModuleNotFoundError:
    sys.exit(
        "Jinja2 não encontrado. Instale com:\n"
        "    pip install -r requirements.txt"
    )

import content

ROOT = Path(__file__).parent.resolve()
TEMPLATES_DIR = ROOT / "templates"
STATIC_DIR = ROOT / "static"
DIST_DIR = ROOT / "dist"


# ─────────────────────────────────────────────────────────────
#  Helpers expostos aos templates
# ─────────────────────────────────────────────────────────────
def wa_link(message: str | None = None) -> str:
    """Monta um link wa.me com mensagem pré-preenchida."""
    from urllib.parse import quote

    msg = message or content.WHATSAPP_DEFAULT_MSG
    return f"https://wa.me/{content.SITE['whatsapp']}?text={quote(msg)}"


def build_env() -> Environment:
    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        autoescape=select_autoescape(["html", "xml"]),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    env.globals.update(
        SITE=content.SITE,
        NAV=content.NAV,
        wa_link=wa_link,
        now=_dt.datetime.now(),
        current_year=content.SITE["year"],
    )
    return env


# ─────────────────────────────────────────────────────────────
#  Geração
# ─────────────────────────────────────────────────────────────
def clean_dist() -> None:
    if DIST_DIR.exists():
        shutil.rmtree(DIST_DIR)
    DIST_DIR.mkdir(parents=True)


def copy_static() -> None:
    if STATIC_DIR.exists():
        shutil.copytree(STATIC_DIR, DIST_DIR, dirs_exist_ok=True)


def render(env: Environment, template_name: str, out_name: str, **ctx) -> None:
    html = env.get_template(template_name).render(**ctx)
    out_path = DIST_DIR / out_name
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html, encoding="utf-8")
    print(f"  · {out_name}")


def build_sitemap(pages: list[str]) -> None:
    base = content.SITE["base_url"].rstrip("/")
    today = _dt.date.today().isoformat()
    urls = "\n".join(
        f"  <url><loc>{base}/{p}</loc><lastmod>{today}</lastmod></url>"
        for p in pages
    )
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{urls}\n"
        "</urlset>\n"
    )
    (DIST_DIR / "sitemap.xml").write_text(xml, encoding="utf-8")
    robots = (
        "User-agent: *\n"
        "Allow: /\n"
        f"Sitemap: {base}/sitemap.xml\n"
    )
    (DIST_DIR / "robots.txt").write_text(robots, encoding="utf-8")
    print("  · sitemap.xml + robots.txt")


def build() -> None:
    print("Gerando site RD Webdesign…")
    clean_dist()
    copy_static()
    env = build_env()

    pages: list[str] = []

    render(
        env, "index.html", "index.html",
        page_title=f"{content.SITE['brand']} – {content.SITE['tagline']}",
        meta_desc=content.SITE["description"],
        nav_active="home",
        stats=content.STATS,
        services=content.SERVICES,
        extra_services=content.EXTRA_SERVICES,
        plans=content.PLANS,
        plan_features=content.PLAN_FEATURES,
        maintenance_note=content.MAINTENANCE_NOTE,
        projects=[p for p in content.PROJECTS if p.get("featured") or p["category"] == "landing"][:4],
        process=content.PROCESS,
        proof_intro=content.PROOF_INTRO,
        testimonials=content.TESTIMONIALS,
        commitments=content.COMMITMENTS,
        faq=content.FAQ,
        contact_options=content.CONTACT_OPTIONS,
    )
    pages.append("index.html")

    render(
        env, "servicos.html", "servicos.html",
        page_title=f"Serviços – {content.SITE['brand']}",
        meta_desc="Selecione o serviço ideal para o seu negócio: sites, landing pages, lojas virtuais, logotipo e mais.",
        nav_active="servicos",
        services=content.SERVICES,
        extra_services=content.EXTRA_SERVICES,
    )
    pages.append("servicos.html")

    render(
        env, "precos.html", "precos.html",
        page_title=f"Preços e Planos – {content.SITE['brand']}",
        meta_desc="Preços transparentes e sem surpresas. Tabela completa de serviços e planos de manutenção mensal.",
        nav_active="precos",
        services=content.SERVICES,
        price_table=content.PRICE_TABLE,
        price_note=content.PRICE_NOTE,
        plans=content.PLANS,
        plan_features=content.PLAN_FEATURES,
        maintenance_note=content.MAINTENANCE_NOTE,
    )
    pages.append("precos.html")

    render(
        env, "portifolio.html", "portifolio.html",
        page_title=f"Portfólio – {content.SITE['brand']}",
        meta_desc="Projetos desenvolvidos pela RD Webdesign: landing pages, sites institucionais e lojas virtuais.",
        nav_active="portifolio",
        projects=content.PROJECTS,
        filters=content.PROJECT_FILTERS,
    )
    pages.append("portifolio.html")

    for svc in content.SERVICES:
        d = svc["detail"]
        related = [
            p for p in content.PROJECTS
            if p["category"] == d["portfolio_tag"]
        ][:3]
        render(
            env, "servico.html", svc["page"],
            page_title=d["meta_title"],
            meta_desc=d["meta_desc"],
            nav_active="servicos",
            svc=svc,
            d=d,
            related=related,
        )
        pages.append(svc["page"])

    build_sitemap(pages)
    print(f"\nPronto. {len(pages)} páginas em {DIST_DIR.relative_to(ROOT)}/")


# ─────────────────────────────────────────────────────────────
#  Preview local
# ─────────────────────────────────────────────────────────────
def serve(port: int = 8000) -> None:
    handler = lambda *a, **kw: http.server.SimpleHTTPRequestHandler(
        *a, directory=str(DIST_DIR), **kw
    )
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"Preview em http://localhost:{port}  (Ctrl+C para sair)")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nEncerrado.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Gerador do site RD Webdesign")
    parser.add_argument("--serve", action="store_true", help="sobe um preview local após gerar")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()

    build()
    if args.serve:
        serve(args.port)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Corrige <id="page-top"> -> <body id="page-top">, asegura </body>,
y mueve algunos estilos inline repetidos a clases CSS.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def fix_body_tags():
    for html in ROOT.glob("*.html"):
        text = html.read_text(encoding="utf-8")
        orig = text

        # Reemplazar <id="page-top"> según corresponda
        if '<id="page-top">' in text:
            if "<body" not in text:
                text = text.replace('<id="page-top">', '<body id="page-top">', 1)
            else:
                text = text.replace('<id="page-top">', "", 1)

        # Asegurar cierre </body> antes de </html>
        if "</html>" in text and "</body>" not in text:
            text = text.replace("</html>", "</body>\n</html>")

        if text != orig:
            html.write_text(text, encoding="utf-8")
            print(f"✅ body corregido en {html.name}")


def update_css():
    css_path = ROOT / "css" / "main.css"
    css = css_path.read_text(encoding="utf-8")
    additions = ""

    if ".section-pad-hero" not in css:
        additions += "\n.section-pad-hero { padding-top: 40px; }\n"
    if ".section-pad-10-20-grey" not in css:
        additions += ".section-pad-10-20-grey { padding-top: 10px; padding-bottom: 20px; background-color: #e8e8e8; }\n"
    if ".section-pad-2" not in css:
        additions += ".section-pad-2 { padding: 2%; }\n"
    if ".wrap-texto-pad-20" not in css:
        additions += ".wrap-texto-pad-20 { padding-top: 20%; }\n"

    if additions:
        css_path.write_text(css + "\n" + additions, encoding="utf-8")
        print("✅ Nuevas clases CSS agregadas a main.css")


def replace_inline_styles():
    for html in ROOT.glob("*.html"):
        text = html.read_text(encoding="utf-8")
        orig = text

        # index: headings con padding-top: 40px
        text = text.replace(
            'class="headings headed leblanc" style="padding-top: 40px"',
            'class="headings headed leblanc section-pad-hero"',
        )

        # index: sección ¿Qué hacemos?
        text = text.replace(
            'class="headings" style="padding-top: 10px; padding-bottom: 20px;background-color: #e8e8e8"',
            'class="headings section-pad-10-20-grey"',
        )

        # constructora y otras: section padding 2%
        text = text.replace('<section style="padding: 2%">', '<section class="section-pad-2">')

        # wrap-texto2 padding-top 20%
        text = text.replace(
            'class="wrap-texto2" style="padding-top: 20%"',
            'class="wrap-texto2 wrap-texto-pad-20"',
        )

        if text != orig:
            html.write_text(text, encoding="utf-8")
            print(f"✅ Estilos inline refactorizados en {html.name}")


def clean_comments():
    # Quitar comentarios viejos evidentes en footers
    for footer in [ROOT / "partials" / "footer.html", ROOT / "partials" / "footer-casaflex.html"]:
        text = footer.read_text(encoding="utf-8")
        orig = text
        text = text.replace('          <!--<p class="letraa" >Contacto</p>-->\n', "")
        if text != orig:
            footer.write_text(text, encoding="utf-8")
            print(f"✅ Comentarios viejos limpiados en {footer.name}")


def main():
    fix_body_tags()
    update_css()
    replace_inline_styles()
    clean_comments()


if __name__ == "__main__":
    main()



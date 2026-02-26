#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Inyecta el head común en todas las páginas HTML y elimina líneas duplicadas
de estilos/ fuentes que ahora viven en partials/head-common.html.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SNIPPET = '  <meta data-head-include="partials/head-common.html">\n  <script src="js/head-loader.js"></script>\n'

# Patrones que representan recursos ahora movidos al parcial
REMOVE_PATTERNS = [
    r'[ \t]*<link[^>]*href=["\']\.?/img/favicon1\.ico["\'][^>]*>\s*',
    r'[ \t]*<link[^>]*href=["\']css/bootstrap\.min\.css["\'][^>]*>\s*',
    r'[ \t]*<link[^>]*href=["\']https://facudelboca\.github\.io/denovo-web/vendor/webfontkit-20201016-132343/auro-regular-webfont\.woff["\'][^>]*>\s*',
    r'[ \t]*<link[^>]*href=["\']https://fonts\.googleapis\.com[^>]*>\s*',
    r'[ \t]*<link[^>]*href=["\']css/main\.css["\'][^>]*>\s*',
]


def inject_and_clean(filepath: Path) -> bool:
    content = filepath.read_text(encoding="utf-8")
    original = content

    # Insertar snippet si no está presente
    if 'data-head-include="partials/head-common.html"' not in content:
        content = content.replace("<head>", "<head>\n" + SNIPPET, 1)

    # Remover líneas duplicadas de recursos comunes
    for pattern in REMOVE_PATTERNS:
        content = re.sub(pattern, "", content, flags=re.IGNORECASE)

    # Normalizar saltos excesivos
    content = re.sub(r"\n{3,}", "\n\n", content)

    if content != original:
        filepath.write_text(content, encoding="utf-8")
        return True
    return False


def main():
    updated = 0
    for html_file in ROOT.glob("*.html"):
        # Evitar partials y archivos no HTML de páginas
        if html_file.parts[-2] == "partials":
            continue
        if inject_and_clean(html_file):
            print(f"✅ Actualizado: {html_file.name}")
            updated += 1
    print(f"\n✨ Proceso completado. {updated} archivos actualizados.")


if __name__ == "__main__":
    main()


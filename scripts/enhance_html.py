"""Automatiza mejoras SEO/Accessibility/Performance en HTML
- Añade meta description si está vacío
- Cambia main.css por main.min.css
- Agrega defer a scripts no críticos
- Añade alt y dimensiones a <img>
- Añade loading=lazy a imágenes no del header
- Normaliza <video> tags para evitar CLS
- Envuelve contenido principal con <main>
"""
import re
from pathlib import Path
from bs4 import BeautifulSoup
from PIL import Image

WORKSPACE = Path(r"c:/Users/facun/Desktop/denovo-web")
html_files = list(WORKSPACE.glob("**/*.html"))

for file_path in html_files:
    # skip partials
    if 'partials' in str(file_path):
        continue
    with open(file_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
    modified = False

    # meta description
    desc = soup.find('meta', attrs={'name': 'description'})
    if desc:
        if not desc.get('content') or desc['content'].strip()=='':
            desc['content'] = 'Empresa constructora y desarrolladora con enfoque sostenible.'
            modified = True
    else:
        new_meta = soup.new_tag('meta', charset=None)
        new_meta.attrs['name'] = 'description'
        new_meta.attrs['content'] = 'Empresa constructora y desarrolladora con enfoque sostenible.'
        soup.head.append(new_meta)
        modified = True

    # replace CSS link
    for link in soup.find_all('link', href=True):
        if 'main.css' in link['href'] and not 'min.css' in link['href']:
            link['href'] = link['href'].replace('main.css', 'main.min.css')
            modified = True

    # add defer to scripts except gtag and head-loader
    for script in soup.find_all('script', src=True):
        src = script['src']
        if 'gtag' in src or 'google-analytics' in src:
            continue
        if not script.has_attr('defer'):
            script['defer'] = True
            modified = True

    # ensure <main> surrounds primary sections (simple heuristic)
    body = soup.body
    if body and not soup.find('main'):
        # create main tag and move most children except nav/footer includes
        new_main = soup.new_tag('main')
        to_move = []
        for child in list(body.children):
            # skip whitespace and comments
            if child.name is None:
                continue
            # skip nav/footer includes
            if child.get('data-include') and ('nav.html' in child['data-include'] or 'footer.html' in child['data-include']):
                continue
            to_move.append(child)
        for item in to_move:
            new_main.append(item.extract())
        # insert before footer include if exists, else at end
        footer_div = body.find(lambda tag: tag.get('data-include') and 'footer.html' in tag['data-include'])
        if footer_div:
            footer_div.insert_before(new_main)
        else:
            body.append(new_main)
        modified = True

    # process img tags
    for img in soup.find_all('img'):
        if not img.has_attr('alt'):
            # derive alt from filename or leave empty
            fname = Path(img.get('src','')).name
            fname = re.sub(r"\.[^.]+$", "", fname)
            img['alt'] = fname.replace('-', ' ').replace('_', ' ')
            modified = True
        # add loading lazy for non-decorative images
        if not img.has_attr('loading'):
            img['loading'] = 'lazy'
            modified = True
        # add width/height if possible
        src = img.get('src','')
        if src and not img.has_attr('width') and not img.has_attr('height'):
            # resolve path
            path = WORKSPACE / src.lstrip('./').lstrip('/')
            if path.exists():
                try:
                    with Image.open(path) as im:
                        w,h = im.size
                        img['width'] = str(w)
                        img['height'] = str(h)
                        modified = True
                except Exception:
                    pass

    # process video tags
    for video in soup.find_all('video'):
        # remove width/height attributes with percents
        if video.has_attr('width'):
            del video['width']; modified=True
        if video.has_attr('height'):
            del video['height']; modified=True
        # add style for responsive aspect
        style = video.get('style','')
        if 'aspect-ratio' not in style:
            style += 'width:100%;height:auto;aspect-ratio:16/9;'
            video['style'] = style
            modified = True
        # add playsinline to avoid mobile issues
        if not video.has_attr('playsinline'):
            video['playsinline'] = ''
            modified = True

    # write back if changed
    if modified:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        print("Modified", file_path)

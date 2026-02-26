#!/usr/bin/env python3
"""Utility to adjust HTML files:
1. Remove .html extensions from hrefs
2. Add width/height attributes to <img> tags based on actual image dimensions
3. Prettify output via BeautifulSoup to clean up code

Runs in-place on all .html files under workspace.
"""
import os
import sys
from bs4 import BeautifulSoup
from PIL import Image

root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def process_file(path):
    changed = False
    with open(path, 'r', encoding='utf-8') as f:
        data = f.read()
    soup = BeautifulSoup(data, 'html.parser')

    # 1. update hrefs
    for a in soup.find_all('a', href=True):
        href = a['href']
        # ignore anchors and external links
        if href.startswith('#') or href.startswith('http') or href.startswith('mailto:'):
            continue
        if href.endswith('.html'):
            new = href[:-5]
            a['href'] = new
            changed = True
    # 2. add width/height to images
    for img in soup.find_all('img', src=True):
        src = img['src']
        if src.startswith('http') or src.startswith('data:'):
            continue
        # strip leading slash
        relpath = src.lstrip('/\\')
        full = os.path.join(root, relpath)
        if os.path.isfile(full):
            try:
                w,h = Image.open(full).size
                if not img.has_attr('width') or img['width'] != str(w):
                    img['width'] = str(w)
                    changed = True
                if not img.has_attr('height') or img['height'] != str(h):
                    img['height'] = str(h)
                    changed = True
            except Exception:
                pass

    # 3. prettify to clean
    newhtml = soup.prettify()
    if newhtml != data:
        changed = True
    if changed:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(newhtml)
        print("Modified", path)


def walk():
    for dirpath, dirs, files in os.walk(root):
        for fn in files:
            if fn.lower().endswith('.html'):
                process_file(os.path.join(dirpath, fn))

if __name__ == '__main__':
    walk()

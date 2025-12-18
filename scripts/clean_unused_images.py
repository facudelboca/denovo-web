#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Detecta y elimina imágenes no referenciadas en HTML/CSS/JS.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IMG_DIR = ROOT / "img"
SEARCH_EXT = {".html", ".css", ".js"}


def collect_references() -> set[str]:
    refs: set[str] = set()
    pattern = re.compile(r"[\"'\\(](?:\\.\\/|\\/)?img\\/([^\"'\\)\\s]+)[\"'\\)]|img\\/([\\w\\-\\.\\/%]+)")
    for path in ROOT.rglob("*"):
        if path.suffix.lower() not in SEARCH_EXT:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for m in pattern.finditer(text):
            candidate = m.group(1) or m.group(2)
            if candidate:
                refs.add(candidate)
    return refs


def list_images() -> set[str]:
    imgs: set[str] = set()
    for path in IMG_DIR.rglob("*"):
        if path.is_file():
            rel = path.relative_to(IMG_DIR).as_posix()
            imgs.add(rel)
    return imgs


def delete_unused(unused: set[str]):
    for rel in unused:
        target = IMG_DIR / rel
        try:
            target.unlink()
            print(f"🗑️  Borrado: {rel}")
        except Exception as e:
            print(f"⚠️  No se pudo borrar {rel}: {e}")


def main():
    refs = collect_references()
    imgs = list_images()

    unused = sorted(imgs - refs)
    if not unused:
        print("No hay imágenes sin uso.")
        return

    print("Imágenes a borrar:")
    for name in unused:
        print(f" - {name}")

    delete_unused(unused)
    print(f"\nEliminadas {len(unused)} imágenes sin uso.")


if __name__ == "__main__":
    main()


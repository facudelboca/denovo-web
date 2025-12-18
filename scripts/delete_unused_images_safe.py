#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para borrar SOLO las imágenes que realmente no se usan.
Usa el reporte generado por find_unused_images_safe.py
"""
import re
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IMG_DIR = ROOT / "img"

def normalize_filename(filename):
    """Normaliza el nombre del archivo para comparación."""
    try:
        filename = urllib.parse.unquote(filename)
    except:
        pass
    filename = filename.lower().strip()
    filename = re.sub(r'\s+', ' ', filename)
    return filename

def collect_image_references():
    """Recopila todas las referencias a imágenes."""
    references = set()
    
    patterns = [
        r'(?:src|href|data-src|data-bg|background-image)\s*=\s*["\']?(?:\.\/)?img\/([^"\')\s?#]+)',
        r'url\(["\']?(?:\.\/)?img\/([^"\')\s?#]+)',
        r'background[^:]*:\s*url\(["\']?(?:\.\/)?img\/([^"\')\s?#]+)',
        r'(?:\.\/)?img\/([^\s<>"\')\[\]{}]+\.(?:jpg|jpeg|png|gif|webp|svg|ico|mp4))',
    ]
    
    for file_path in ROOT.rglob("*"):
        if file_path.is_file() and file_path.suffix.lower() in {".html", ".css", ".js"}:
            try:
                content = file_path.read_text(encoding='utf-8', errors='ignore')
                for pattern in patterns:
                    for match in re.finditer(pattern, content, re.IGNORECASE):
                        img_ref = match.group(1)
                        if img_ref:
                            img_ref = img_ref.split('?')[0].split('#')[0].strip()
                            normalized = normalize_filename(img_ref)
                            if normalized:
                                references.add(normalized)
            except Exception:
                pass
    
    return references

def main():
    print("🔍 Verificando imágenes no usadas...")
    
    references = collect_image_references()
    unused_images = []
    
    if not IMG_DIR.exists():
        print("❌ La carpeta img no existe.")
        return
    
    for img_path in IMG_DIR.rglob("*"):
        if img_path.is_file() and img_path.suffix.lower() in {".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg", ".ico", ".mp4"}:
            rel_path = img_path.relative_to(IMG_DIR).as_posix()
            normalized = normalize_filename(rel_path)
            
            if normalized not in references:
                unused_images.append(img_path)
    
    if not unused_images:
        print("✅ Todas las imágenes están en uso. No hay nada que borrar.")
        return
    
    print(f"\n⚠️  Se encontraron {len(unused_images)} imágenes que NO se usan.")
    print("\nImágenes a borrar:")
    for img_path in sorted(unused_images):
        print(f"  - {img_path.name}")
    
    # Confirmar antes de borrar
    print(f"\n⚠️  ¿Borrar estas {len(unused_images)} imágenes? (s/n): ", end="")
    respuesta = input().strip().lower()
    
    if respuesta != 's':
        print("❌ Operación cancelada.")
        return
    
    # Borrar imágenes
    deleted = 0
    errors = 0
    
    for img_path in unused_images:
        try:
            img_path.unlink()
            print(f"🗑️  Borrado: {img_path.name}")
            deleted += 1
        except Exception as e:
            print(f"⚠️  Error borrando {img_path.name}: {e}")
            errors += 1
    
    print(f"\n✅ Proceso completado:")
    print(f"   - Borradas: {deleted}")
    print(f"   - Errores: {errors}")

if __name__ == "__main__":
    main()


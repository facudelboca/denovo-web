#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script mejorado para encontrar imágenes no usadas.
Solo lista, NO borra automáticamente.
"""
import re
import urllib.parse
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parent.parent
IMG_DIR = ROOT / "img"
SEARCH_EXTENSIONS = {".html", ".css", ".js"}
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg", ".ico", ".mp4"}

def normalize_filename(filename):
    """Normaliza el nombre del archivo para comparación."""
    # Decodifica URLs (%20 -> espacio, etc.)
    try:
        filename = urllib.parse.unquote(filename)
    except:
        pass
    # Convierte a minúsculas y normaliza espacios
    filename = filename.lower().strip()
    # Reemplaza espacios múltiples por uno solo
    filename = re.sub(r'\s+', ' ', filename)
    return filename

def collect_image_references():
    """Recopila todas las referencias a imágenes en todos los archivos."""
    references = defaultdict(list)  # {nombre_normalizado: [rutas_de_archivos]}
    
    # Patrones para encontrar referencias a imágenes
    patterns = [
        # src="img/..." o src='img/...' o src=img/...
        r'(?:src|href|data-src|data-bg|background-image)\s*=\s*["\']?(?:\.\/)?img\/([^"\')\s?#]+)',
        # url(img/...)
        r'url\(["\']?(?:\.\/)?img\/([^"\')\s?#]+)',
        # En CSS: background: url(...)
        r'background[^:]*:\s*url\(["\']?(?:\.\/)?img\/([^"\')\s?#]+)',
        # Referencias directas sin comillas
        r'(?:\.\/)?img\/([^\s<>"\')\[\]{}]+\.(?:jpg|jpeg|png|gif|webp|svg|ico|mp4))',
    ]
    
    # Buscar en todos los archivos
    for file_path in ROOT.rglob("*"):
        if file_path.is_file() and file_path.suffix.lower() in SEARCH_EXTENSIONS:
            try:
                content = file_path.read_text(encoding='utf-8', errors='ignore')
                
                for pattern in patterns:
                    for match in re.finditer(pattern, content, re.IGNORECASE):
                        img_ref = match.group(1)
                        if img_ref:
                            # Limpiar la referencia (quitar parámetros de query, etc.)
                            img_ref = img_ref.split('?')[0].split('#')[0].strip()
                            normalized = normalize_filename(img_ref)
                            if normalized:
                                references[normalized].append(str(file_path.relative_to(ROOT)))
            except Exception as e:
                print(f"⚠️  Error leyendo {file_path}: {e}")
    
    return references

def get_all_images():
    """Obtiene todas las imágenes en la carpeta img."""
    images = {}
    if not IMG_DIR.exists():
        return images
    
    for img_path in IMG_DIR.rglob("*"):
        if img_path.is_file() and img_path.suffix.lower() in IMAGE_EXTENSIONS:
            rel_path = img_path.relative_to(IMG_DIR).as_posix()
            normalized = normalize_filename(rel_path)
            images[normalized] = rel_path  # Guardamos el nombre original
    
    return images

def main():
    print("🔍 Buscando referencias a imágenes...")
    references = collect_image_references()
    
    print(f"📁 Analizando imágenes en {IMG_DIR}...")
    all_images = get_all_images()
    
    # Encontrar imágenes no referenciadas
    unused = []
    used = []
    
    for normalized_name, original_name in all_images.items():
        if normalized_name in references:
            used.append((original_name, references[normalized_name]))
        else:
            unused.append(original_name)
    
    # Mostrar resultados
    print(f"\n✅ Imágenes USADAS ({len(used)}):")
    for img_name, files in sorted(used):
        print(f"  ✓ {img_name}")
        for file_ref in files[:3]:  # Mostrar máximo 3 referencias
            print(f"    → {file_ref}")
        if len(files) > 3:
            print(f"    ... y {len(files) - 3} más")
    
    print(f"\n❌ Imágenes NO USADAS ({len(unused)}):")
    if unused:
        for img_name in sorted(unused):
            print(f"  ✗ {img_name}")
        
        print(f"\n⚠️  IMPORTANTE: Estas {len(unused)} imágenes NO se borrarán automáticamente.")
        print("   Revisa la lista antes de borrarlas manualmente.")
    else:
        print("  ¡Todas las imágenes están en uso!")
    
    # Guardar reporte
    report_file = ROOT / "unused_images_report.txt"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("REPORTE DE IMÁGENES NO USADAS\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Total de imágenes analizadas: {len(all_images)}\n")
        f.write(f"Imágenes en uso: {len(used)}\n")
        f.write(f"Imágenes NO usadas: {len(unused)}\n\n")
        
        if unused:
            f.write("IMÁGENES NO USADAS:\n")
            f.write("-" * 50 + "\n")
            for img_name in sorted(unused):
                f.write(f"{img_name}\n")
    
    print(f"\n📄 Reporte guardado en: {report_file.relative_to(ROOT)}")

if __name__ == "__main__":
    main()


#!/usr/bin/env python3
"""
Script para convertir todas las imágenes a WebP y actualizar referencias
"""

from pathlib import Path
from PIL import Image
import re
import os

# Configuración
WORKSPACE = Path("c:/Users/facun/Desktop/denovo-web")
IMG_DIR = WORKSPACE / "img"
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif"}
SKIP_FORMATS = {".webp", ".svg", ".ico", ".mp4"}  # No convertir estos

print("="*60)
print("INICIANDO CONVERSIÓN DE IMÁGENES A WebP")
print("="*60)

# Paso 1: Convertir todas las imágenes a WebP
print("\nPaso 1: Convirtiendo imágenes a WebP...")
converted_images = {}
failed_images = []

for img_file in sorted(IMG_DIR.iterdir()):
    if not img_file.is_file():
        continue
    
    ext = img_file.suffix.lower()
    
    # Si la extensión está en SKIP_FORMATS, saltar
    if ext in SKIP_FORMATS:
        print(f"  ⊘ {img_file.name} (formato {ext}, no se convierte)")
        continue
    
    # Si la extensión es de imagen soportada
    if ext in IMAGE_EXTENSIONS:
        webp_path = img_file.with_suffix(".webp")
        
        try:
            # Abrir imagen original
            with Image.open(img_file) as img:
                # Convertir RGBA a RGB para mejor compresión si es posible
                if img.mode == "RGBA":
                    # Mantener transparencia en WebP, que lo soporta
                    img.save(webp_path, "WEBP", quality=85)
                elif img.mode == "P":
                    # Imágenes indexadas
                    img.convert("RGB").save(webp_path, "WEBP", quality=85)
                else:
                    img.save(webp_path, "WEBP", quality=80, method=6)
            
            # Guardar mapeo: nombre_original -> nombre_webp
            converted_images[img_file.name] = webp_path.name
            
            # Mostrar tamaño original vs webp
            original_size = img_file.stat().st_size
            webp_size = webp_path.stat().st_size
            reduction = (1 - webp_size / original_size) * 100
            
            print(f"  ✓ {img_file.name} → {webp_path.name} ({reduction:.1f}% menor)")
            
        except Exception as e:
            print(f"  ✗ Error al convertir {img_file.name}: {e}")
            failed_images.append(img_file.name)

print(f"\nImágenes convertidas: {len(converted_images)}")
if failed_images:
    print(f"Imágenes con error: {len(failed_images)}")
    for img in failed_images:
        print(f"  - {img}")

# Paso 2: Actualizar referencias en archivos HTML y CSS
print("\nPaso 2: Actualizando referencias en archivos...")

def update_file_references(file_path, conversions):
    """Actualiza todas las referencias de imágenes en un archivo"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Actualizar referencias con rutas relativas
        for old_name, new_name in conversions.items():
            # Patterns para capturar diferentes formas de referencias
            patterns = [
                # src="./img/imagen.jpg" o src="/img/imagen.jpg"
                (f"(['\"])(\\.?/?img/)({re.escape(old_name)})(['\"])", 
                 f"\\1\\2{new_name}\\4"),
                # style="background: url('./img/imagen.jpg')"
                (f"(url\\(['\"]?)(\\.?/?img/)({re.escape(old_name)})(['\"]?\\))",
                 f"\\1\\2{new_name}\\4"),
                # background-image: url('../img/imagen.jpg')
                (f"(url\\(['\"]?)(\\.\\./img/)({re.escape(old_name)})(['\"]?\\))",
                 f"\\1\\2{new_name}\\4"),
                # img/imagen.jpg sin precedente
                (f"(img/)({re.escape(old_name)})",
                 f"\\1{new_name}"),
            ]
            
            for pattern, replacement in patterns:
                content = re.sub(pattern, replacement, content)
        
        # Si hubo cambios, guardar el archivo
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True, True
        return True, False
        
    except Exception as e:
        print(f"  ✗ Error al procesar {file_path}: {e}")
        return False, False

# Encontrar y actualizar todos los HTML, CSS y PHP
html_files = list(WORKSPACE.glob("**/*.html"))
css_files = list(WORKSPACE.glob("**/*.css"))
php_files = list(WORKSPACE.glob("**/*.php"))

all_files = html_files + css_files + php_files
updated_files = []

for file_path in all_files:
    # Saltar archivos en node_modules o .venv
    if '.venv' in str(file_path) or 'node_modules' in str(file_path):
        continue
    
    success, changed = update_file_references(file_path, converted_images)
    if success and changed:
        updated_files.append(file_path.name)
        print(f"  ✓ {file_path.name}")

print(f"\nArchivos actualizados: {len(updated_files)}")

# Paso 3: Eliminar imágenes originales (opcional)
print("\nPaso 3: Eliminando imágenes originales...")
deleted_count = 0

for old_name in converted_images.keys():
    old_path = IMG_DIR / old_name
    if old_path.exists():
        try:
            old_path.unlink()
            deleted_count += 1
            print(f"  ✓ {old_name}")
        except Exception as e:
            print(f"  ✗ No se pudo eliminar {old_name}: {e}")

print(f"\nImágenes eliminadas: {deleted_count}")

# Resumen final
print("\n" + "="*60)
print("RESUMEN DE CONVERSIÓN")
print("="*60)
print(f"Imágenes convertidas: {len(converted_images)}")
print(f"Archivos actualizados: {len(updated_files)}")
print(f"Imágenes eliminadas: {deleted_count}")
print(f"Conversiones fallidas: {len(failed_images)}")
print("="*60)
print("\n✓ ¡Conversión completada!")

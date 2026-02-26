#!/usr/bin/env python3
"""Rename HTML files and update all references across the codebase."""
import os
import re
from pathlib import Path

root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Mapping of old names to new names
RENAMES = {
    'nosotros': 'proposito',
    'constructora': 'construimos',
    'desarrollos': 'desarrollamos',
    'gerenciamiento': 'gerenciamos',
    'casas': 'proyectamos-dirigimos'
}

def update_references_in_file(filepath):
    """Update all href and src references in a file."""
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    original = content
    for old_name, new_name in RENAMES.items():
        # Update hrefs: href="nosotros" → href="proposito"
        content = re.sub(
            rf'href=["\']({old_name})["\']',
            rf'href="{new_name}"',
            content
        )
        # Update paths in src attributes: ./casas/ → ./proyectamos-dirigimos/
        content = re.sub(
            rf'(["\'])\./{old_name}/',
            rf'\1./{new_name}/',
            content
        )
        content = re.sub(
            rf'(["\']){old_name}/',
            rf'\1{new_name}/',
            content
        )
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    # Step 1: Update all HTML files with new references
    for dirpath, dirs, files in os.walk(root):
        for fn in files:
            if fn.lower().endswith('.html'):
                filepath = os.path.join(dirpath, fn)
                if update_references_in_file(filepath):
                    print(f"Updated references in: {filepath}")
    
    # Step 2: Rename files using os.rename
    for old_name, new_name in RENAMES.items():
        # Rename single HTML file
        old_file = os.path.join(root, f"{old_name}.html")
        new_file = os.path.join(root, f"{new_name}.html")
        if os.path.exists(old_file):
            os.rename(old_file, new_file)
            print(f"Renamed: {old_file} → {new_file}")
        
        # Rename directory
        old_dir = os.path.join(root, old_name)
        new_dir = os.path.join(root, new_name)
        if os.path.isdir(old_dir):
            os.rename(old_dir, new_dir)
            print(f"Renamed: {old_dir} → {new_dir}")

if __name__ == '__main__':
    main()

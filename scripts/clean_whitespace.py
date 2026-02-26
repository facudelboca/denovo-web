#!/usr/bin/env python3
"""Remove trailing whitespace and collapse multiple blank lines in text files."""
import os
import re

def clean_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    new_lines = []
    blank_count = 0
    for line in lines:
        # strip trailing spaces
        l = line.rstrip() + '\n'
        if l.strip() == '':
            blank_count += 1
            if blank_count <= 2:
                new_lines.append(l)
        else:
            blank_count = 0
            new_lines.append(l)
    if new_lines != lines:
        with open(path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        print('Cleaned', path)


for dirpath, dirs, files in os.walk(os.path.join(os.path.dirname(__file__), '..')):
    for fn in files:
        if fn.lower().endswith(('.html','.css','.js')):
            clean_file(os.path.join(dirpath, fn))

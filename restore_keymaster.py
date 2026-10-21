#!/usr/bin/env python3
"""Reconstruye keymaster.py desde las partes. Ejecutar una vez: python restore_keymaster.py"""
from pathlib import Path
p1 = Path("km_part1.txt").read_text()
p2 = Path("km_part2.txt").read_text()
Path("keymaster.py").write_text(p1 + p2)
print("keymaster.py restaurado:", len(p1) + len(p2), "chars")

#!/usr/bin/env python3
"""Entrypoint: copy the entry image to the make.fun output directory.

Stdlib only. Writes /output/entry.png (or $MAKEFUN_OUTPUT_DIR/entry.png).
The image itself is pre-rendered by render.py at build time; this program
only copies it, so both grader runs write the same bytes.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")

os.makedirs(OUT_DIR, exist_ok=True)
shutil.copyfile(SRC, os.path.join(OUT_DIR, "entry.png"))
print("wrote entry.png")

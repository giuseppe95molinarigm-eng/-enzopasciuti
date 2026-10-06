#!/usr/bin/env python3
"""Rende un PDF in doppie pagine affiancate (verso | recto) per il controllo visivo.
    python3 tools/spreads.py libro.pdf cartella_out [dpi] [prima] [ultima]
"""
import os, subprocess, sys, glob, tempfile
from PIL import Image

pdf, out = sys.argv[1], sys.argv[2]
dpi = sys.argv[3] if len(sys.argv) > 3 else "60"
first = int(sys.argv[4]) if len(sys.argv) > 4 else 1
last = int(sys.argv[5]) if len(sys.argv) > 5 else 9999
os.makedirs(out, exist_ok=True)
tmp = tempfile.mkdtemp()
subprocess.run(["pdftoppm", "-r", dpi, "-png", "-f", str(first), "-l", str(last), pdf, f"{tmp}/p"], check=True)
files = sorted(glob.glob(f"{tmp}/p-*.png"), key=lambda f: int(f.rsplit("-", 1)[1][:-4]))
pages = {int(f.rsplit("-", 1)[1][:-4]): f for f in files}
w, h = Image.open(files[0]).size
nums = sorted(pages)
spreads = []
for n in nums:
    if n % 2 == 1:
        spreads.append((n - 1 if (n - 1) in pages else None, n))
    elif (n + 1) not in pages:
        spreads.append((n, None))
for l, r in spreads:
    S = Image.new("RGB", (2 * w + 8, h), "#7a7a7a")
    if l: S.paste(Image.open(pages[l]), (0, 0))
    if r: S.paste(Image.open(pages[r]), (w + 8, 0))
    S.save(f"{out}/s{(r or l):04d}.png")
print(len(spreads), "doppie pagine")

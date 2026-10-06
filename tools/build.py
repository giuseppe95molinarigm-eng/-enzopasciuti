#!/usr/bin/env python3
"""Compila il libro (o un campione) in PDF con i font del progetto.

    python3 tools/build.py it            -> output/libro-it.pdf
    python3 tools/build.py it --campione 6   -> output/campione-it.pdf (solo cap. 6)
    python3 tools/build.py it --png 120      -> anche le pagine in PNG (controllo)
"""
import argparse, os, re, subprocess, sys
import typst

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ap = argparse.ArgumentParser()
ap.add_argument("lang")
ap.add_argument("--campione")
ap.add_argument("--out")
a = ap.parse_args()

src = os.path.join(ROOT, a.lang, "main.typ")
os.makedirs(os.path.join(ROOT, "output"), exist_ok=True)
out = a.out or os.path.join(ROOT, "output", f"libro-{a.lang}.pdf")
if a.campione:
    content = open(os.path.join(ROOT, a.lang, "contenuto.typ"), encoding="utf-8").read()
    n = a.campione
    i = content.index(f'#capitolo(numero: "{n}"')
    m = re.search(r'\n#capitolo\(numero: ', content[i + 10:])
    part = content[i: i + 10 + m.start()] if m else content[i:]
    tmp = os.path.join(ROOT, a.lang, "_campione.typ")
    main = open(src, encoding="utf-8").read()
    main = main.replace('#include "contenuto.typ"', '#include "_campione_contenuto.typ"')
    main = re.sub(r'#frontespizio\(.*?\n', '', main)
    main = re.sub(r'#pagina-indice\("Indice"\).*?\n', '', main)
    open(tmp, "w", encoding="utf-8").write(main)
    open(os.path.join(ROOT, a.lang, "_campione_contenuto.typ"), "w", encoding="utf-8").write(
        '#import "../template/libro.typ": *\n' + part)
    src = tmp
    out = a.out or os.path.join(ROOT, "output", f"campione-{a.lang}.pdf")

typst.compile(src, output=out, root=ROOT, font_paths=[os.path.join(ROOT, "fonts")], pdf_standards=None)
print("scritto", out)

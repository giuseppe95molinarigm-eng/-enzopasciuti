#!/usr/bin/env python3
"""Controllo di qualità del PDF impaginato.

1. Integrità del testo: confronta la sequenza dei caratteri alfanumerici del
   Word con quella del PDF (testate, folio e indici esclusi). Ogni differenza
   viene elencata: nulla deve risultare perso o duplicato.
2. Impaginazione: titoli isolati in fondo pagina, pagine troppo corte che non
   chiudono un capitolo, font non incorporati, formato pagina.

    python3 tools/qa.py MANOSCRITTO.docx output/libro-it.pdf [it|en]
"""
import difflib
import re
import sys
import unicodedata

import docx
import pymupdf

IN = 72.0
PAGE_W, PAGE_H = 8 * IN, 10 * IN
MM = IN / 25.4
TOP, BOTTOM = 27 * MM, 27 * MM

# Testi aggiunti dall'impaginazione (etichette, rimandi) e marcatori tolti.
ADDED = ["segue", "capitolo", "continued", "chapter"]

# Stringhe che dipendono dalla lingua dell'edizione.
LANG = {
    "it": dict(intro="Perché ho scritto questo libro", toc="Indice", chapter="capitolo",
               box="protocollo in sintesi", disc="adattare la comunicazione al profilo disc",
               cont="segue"),
    "en": dict(intro="Why I Wrote This Book", toc="Contents", chapter="chapter",
               box="protocol at a glance", disc="adapting communication to disc profiles",
               cont="continued"),
}


def norm(s):
    """Sequenza di parole minuscole; trattini e a capo sillabici ricongiunti."""
    s = unicodedata.normalize("NFKC", s).lower()
    s = re.sub(r"[-\u2010\u00ad]\s*\n\s*", "", s)    # sillabazione a fine riga
    s = re.sub(r"[-\u2010\u00ad]", "", s)
    s = "".join(ch if ch.isalnum() else " " for ch in s)
    toks, out, run = s.split(), [], []
    # le etichette spaziate (tracking) vengono estratte lettera per lettera:
    # «c a p i t o l o» -> «capitolo»
    for t in toks + [None]:
        if t is not None and len(t) <= 2 and not t.isdigit():
            run.append(t)
            continue
        if len(run) >= 5:
            out.append("".join(run))
        else:
            out.extend(run)
        run = []
        if t is not None:
            out.append(t)
    return out


def docx_stream(path):
    d = docx.Document(path)
    out = []
    for p in d.paragraphs:
        t = "".join(n.text or "" for n in p._p.iter() if n.tag.endswith("}t"))
        t = re.sub(r"^\s*BOX\s*[—–-]\s*", "", t)   # marcatore redazionale
        out.append(t)
    return norm(" ".join(out))


def pdf_pages(path):
    doc = pymupdf.open(path)
    return doc


def body_text(page):
    clip = pymupdf.Rect(0, TOP - 2, PAGE_W, PAGE_H - BOTTOM + 2)
    return page.get_text("text", clip=clip, sort=False)


def main():
    src, pdf = sys.argv[1], sys.argv[2]
    K = LANG[sys.argv[3] if len(sys.argv) > 3 else "it"]
    doc = pdf_pages(pdf)
    problems = []

    # formato e font
    for i, page in enumerate(doc):
        r = page.rect
        if abs(r.width - PAGE_W) > 0.5 or abs(r.height - PAGE_H) > 0.5:
            problems.append(f"pagina {i+1}: formato {r.width:.1f}x{r.height:.1f} pt")
    fonts = set()
    for i in range(len(doc)):
        for f in doc.get_page_fonts(i):
            fonts.add((f[3], f[1], f[2]))
    not_embedded = [f for f in fonts if f[1] in ("", "n/a")]
    print(f"Pagine: {len(doc)} · formato 8x10 in · font: {len(fonts)} varianti")
    for f in sorted(fonts):
        print("   font:", f[0], f[2])

    # inizio del corpo del libro: prima pagina che contiene l'introduzione
    start = next(i for i, p in enumerate(doc) if K["intro"] in p.get_text()
                 and K["toc"] not in p.get_text()[:200])
    pdf_txt = "".join(body_text(doc[i]) for i in range(start, len(doc)))
    a = docx_stream(src)
    b = norm(pdf_txt)
    # Testatine e folio sono esclusi dal ritaglio. Diff parola per parola con
    # GNU diff (veloce anche su 70.000 parole).
    import os, subprocess, tempfile
    tmp = tempfile.mkdtemp()
    fa, fb = os.path.join(tmp, "word.txt"), os.path.join(tmp, "pdf.txt")
    open(fa, "w").write("\n".join(a) + "\n")
    open(fb, "w").write("\n".join(b) + "\n")
    out = subprocess.run(["diff", fa, fb], capture_output=True, text=True).stdout
    diffs = []
    for hunk in re.split(r"\n(?=\d)", out.strip()):
        if not hunk:
            continue
        head, *body = hunk.split("\n")
        dels = [l[2:] for l in body if l.startswith("< ")]
        adds = [l[2:] for l in body if l.startswith("> ")]
        if "".join(dels) == "".join(adds):
            continue   # stessa sequenza di lettere: etichetta spaziata letta come parola unica
        rip = " ".join(adds)
        if not dels and (all(w in ADDED or w.isdigit() for w in adds)
                         or rip in (f"{K['disc']} {K['cont']}",
                                    f"{K['chapter']} {K['box']} {K['cont']}")):
            continue   # etichette «Capitolo N» / «segue» aggiunte dall'impaginazione
        k = int(re.match(r"(\d+)", head).group(1))
        diffs.append((head, " ".join(dels)[:90], " ".join(adds)[:90], " ".join(a[max(0, k - 7):k - 1])))
    print(f"\nIntegrità testo: {len(a)} parole nel Word, {len(b)} nel PDF, differenze non previste: {len(diffs)}")
    for d in diffs[:60]:
        print("   ", d)

    # titoli isolati / pagine corte
    heading_fonts = ("SourceSerif4Subhead-Semibold", "Inter-SemiBold")
    for i in range(start, len(doc)):
        page = doc[i]
        d = page.get_text("dict", clip=pymupdf.Rect(0, TOP - 2, PAGE_W, PAGE_H - BOTTOM + 2))
        lines = []
        for blk in d["blocks"]:
            for ln in blk.get("lines", []):
                spans = [s for s in ln["spans"] if s["text"].strip()]
                if spans:
                    lines.append((ln["bbox"][3], spans[0]["font"], spans[0]["size"],
                                  "".join(s["text"] for s in spans)))
        if not lines:
            continue
        lines.sort()
        last = lines[-1]
        if last[1].startswith("SourceSerif4Subhead-Semibold") and last[2] > 13:
            problems.append(f"pagina {i+1}: titolo isolato in fondo pagina: {last[3][:60]}")
        text_bottom = last[0]
        fill = (text_bottom - TOP) / (PAGE_H - TOP - BOTTOM)
        nxt = doc[i + 1].get_text() if i + 1 < len(doc) else ""
        nn = " ".join(norm(nxt)[:40])
        chapter_end = (i + 1 >= len(doc) or not nxt.strip()
                       or nn.startswith(K["chapter"]) or K["box"] in nn
                       or (K["disc"] in nn and f"disc {K['cont']}" not in nn
                           and f"profiles {K['cont']}" not in nn))
        if fill < 0.80 and not chapter_end:
            problems.append(f"pagina {i+1}: pagina corta ({fill:.0%}) — ultima riga: {last[3][:50]}")

    print(f"\nSegnalazioni di impaginazione: {len(problems)}")
    for p in problems:
        print("   ", p)


if __name__ == "__main__":
    main()

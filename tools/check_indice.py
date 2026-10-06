#!/usr/bin/env python3
"""Verifica che ogni voce degli indici (link interni) porti alla pagina giusta e che
il numero stampato accanto alla voce corrisponda al folio di quella pagina."""
import re, sys
import pymupdf

doc = pymupdf.open(sys.argv[1])
start = next(i for i, p in enumerate(doc) if "I N T R O D U Z I O N E" in p.get_text()[:80]
             or p.get_text().lstrip().startswith("INTRODUZIONE"))
flat = lambda s: re.sub(r"\s+", " ", s).strip()
errors = n = 0
for i in range(start):
    page = doc[i]
    words = page.get_text("words")
    for l in page.get_links():
        if l.get("kind") != pymupdf.LINK_GOTO:
            continue
        r = pymupdf.Rect(l["from"])
        cy = (r.y0 + r.y1) / 2
        title = flat(" ".join(w[4] for w in words if r.x0 - 1 <= w[0] and w[2] <= r.x1 + 1
                              and r.y0 - 1 <= (w[1] + w[3]) / 2 <= r.y1 + 1))
        shown = l["page"] - start + 1           # folio della pagina di destinazione
        target = flat(doc[l["page"]].get_text())
        n += 1
        if re.match(r"^(SCRIPT|PROTOCOLLO)\b", title):
            ok = title.endswith(str(shown))
        else:
            # numero più vicino sulla stessa riga, a destra della voce
            cand = [w for w in words if w[0] > r.x1 and re.fullmatch(r"\d+", w[4])]
            cand.sort(key=lambda w: abs((w[1] + w[3]) / 2 - (r.y1 - 4)))
            num_ok = True
            riga = [w[4] for w in words if abs((w[1] + w[3]) / 2 - cy) < 8]
            if "PROTOCOLLO" not in riga:   # indice generale (non l'indice dei protocolli)
                num_ok = bool(cand) and int(cand[0][4]) == shown
            key = title.split(": ")[-1][:22]
            ok = num_ok and key in target
        if not ok:
            errors += 1
            print("ERRORE pag.", i + 1, "|", title, "| folio destinazione", shown)
print(f"voci d'indice controllate: {n} — errori: {errors}")

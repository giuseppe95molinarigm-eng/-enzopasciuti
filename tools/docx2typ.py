#!/usr/bin/env python3
"""Converte il manoscritto Word in un sorgente Typst semantico.

Il Word usa gli stili in modo incoerente (Heading 1 per il testo corrente,
Heading 2 per bibliografie, ecc.), quindi la struttura viene riconosciuta dal
contenuto e dalla formattazione effettiva dei run, non dal nome dello stile.

Uso:
    python3 tools/docx2typ.py MANOSCRITTO.docx it/contenuto.typ [--lang it]
           [--report report.json]

Le stringhe che identificano le sezioni ricorrenti (Bibliografia, Script
operativo, box DISC, ecc.) sono raccolte in TRIGGERS, per lingua: per le
edizioni inglese e spagnola basta aggiungere le chiavi corrispondenti.
"""
import argparse
import json
import re
import sys

import docx
from docx.text.run import Run

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"

TRIGGERS = {
    "it": {
        "chapter": r"^CAPITOLO\s+(\d+)$",
        "intro": r"^Introduzione$",
        "biblio": r"^Bibliografia$",
        "disc": r"^Adattare la comunicazione al profilo DISC$",
        "box": r"^BOX\s*[—–-]\s*(Protocollo in sintesi)$",
        "script": r"^(Lo )?[Ss]cript operativo$",
        "perche": r"^Perché questo protocollo funziona$",
        "disc_profile": r"^([DISC])\s*[—–-]\s*(.+)$",
        "box_labels": ["Quando applicarlo", "Obiettivo", "Cosa fare", "Cosa verificare"],
        "leva": "Leva principale",
    },
    "en": {
        "chapter": r"^(?:CHAPTER|Chapter)\s+(\d+)$",
        "intro": r"^Introduction$",
        "biblio": r"^References$",
        "disc": r"^Adapting Communication to DISC Profiles$",
        "box": r"^BOX\s*[—–-]\s*(Protocol at a Glance)$",
        "script": r"^(The )?Practical Script$",
        "perche": r"^Why This Protocol Works$",
        "disc_profile": r"^([DISC])\s*[—–-]\s*(.+)$",
        "box_labels": ["When to Use It", "Goal", "What to Do", "What to Check"],
        "leva": "Main motivator",
    },
    "es": {
        "chapter": r"^(?:CAPÍTULO|Capítulo)\s+(\d+)$",
        "intro": r"^Introducción$",
        "biblio": r"^Bibliografía$",
        "disc": r"^Adaptar la comunicación al perfil DISC$",
        "box": r"^RECUADRO\s*[—–-]\s*(Resumen del protocolo|El protocolo en resumen|Protocolo en síntesis)$",
        # nel Word il titolo del riquadro varia (capp. 10 e 11): uniformato
        "box_title": "Resumen del protocolo",
        "script": r"^(El )?[Gg]uion operativo$",
        "perche": r"^Por qué funciona este protocolo$",
        "disc_profile": r"^([DISC])\s*[—–-]\s*(.+)$",
        "box_labels": ["Cuándo aplicarlo", "Objetivo", "Qué hacer", "Qué comprobar"],
        "leva": "Palanca principal",
    },
}

# Caratteri che in Typst hanno un significato di markup e vanno protetti.
SPECIAL = set('\\#*_`$<>@[]~/=+-\'"')


def esc(s: str) -> str:
    out = []
    for ch in s:
        if ch in SPECIAL:
            out.append("\\" + ch)
        else:
            out.append(ch)
    return "".join(out)


def norm_text(s: str) -> str:
    # Normalizzazioni esclusivamente tipografiche.
    s = s.replace("\t", " ").replace("\u00a0", " ")
    s = s.replace("'", "\u2019")          # apostrofo dritto -> tipografico
    s = re.sub(r" {2,}", " ", s)
    return s


class Para:
    def __init__(self, idx, p, style_bold):
        self.idx = idx
        self.style = p.style.name
        pPr = p._p.pPr
        self.num = None
        if pPr is not None and pPr.numPr is not None and pPr.numPr.numId is not None:
            self.num = pPr.numPr.numId.val
        runs = []
        # Tutti i run nell'ordine del documento, compresi quelli dentro i link.
        for r_el in p._p.iter(W + "r"):
            r = Run(r_el, p)
            b = r.bold if r.bold is not None else style_bold
            i = bool(r.italic)
            t = ""
            for ch in r_el:
                tag = ch.tag.replace(W, "")
                if tag == "t":
                    t += ch.text or ""
                elif tag in ("br", "cr"):
                    t += "\n"
                elif tag == "tab":
                    t += " "
            if t:
                runs.append([norm_text(t), bool(b), i])
        # unisce run adiacenti con la stessa formattazione
        merged = []
        for t, b, i in runs:
            if merged and merged[-1][1] == b and merged[-1][2] == i:
                merged[-1][0] += t
            else:
                merged.append([t, b, i])
        # rimuove spazi iniziali/finali
        while merged and not merged[0][0].strip():
            merged.pop(0)
        while merged and not merged[-1][0].strip():
            merged.pop()
        if merged:
            merged[0][0] = merged[0][0].lstrip()
            merged[-1][0] = merged[-1][0].rstrip()
        self.runs = merged
        self.text = "".join(t for t, _, _ in merged)
        vis = [(t, b, i) for t, b, i in merged if t.strip()]
        self.all_bold = bool(vis) and all(b for _, b, _ in vis)
        self.all_ital = bool(vis) and all(i for _, _, i in vis)
        n = sum(len(t) for t, _, _ in vis) or 1
        self.ital_ratio = sum(len(t) for t, _, i in vis if i) / n
        self.starts_ital_quote = bool(vis) and vis[0][2] and vis[0][0].lstrip().startswith("«")


def runs_to_typ(runs, drop_bold=False, drop_ital=False, strip_lead=None):
    out = []
    first = True
    for t, b, i in runs:
        if first and strip_lead:
            t = re.sub(strip_lead, "", t, count=1)
        if b and drop_bold:
            b = False
        if i and drop_ital:
            i = False
        lines = t.split("\n")
        parts = []
        for k, line in enumerate(lines):
            e = esc(line)
            if first and k == 0:
                e = re.sub(r"^(\d+)\\?\.", r"\1\\.", e)
            parts.append(e)
        s = " \\\n".join(parts)
        if not s:
            first = False
            continue
        # gli spazi restano fuori dalle funzioni di enfasi
        lead = re.match(r"^\s*", s).group(0)
        trail = re.search(r"\s*$", s).group(0)
        core = s[len(lead):len(s) - len(trail)] if trail else s[len(lead):]
        if core:
            if b and i:
                core = f"#strong[#emph[{core}]];"
            elif b:
                core = f"#strong[{core}];"
            elif i:
                core = f"#emph[{core}];"
        out.append(lead + core + trail)
        first = False
    return "".join(out)


def convert(path, lang="it"):
    T = TRIGGERS[lang]
    d = docx.Document(path)
    style_bold = {}
    for st in d.styles:
        try:
            style_bold[st.name] = bool(st.font.bold)
        except Exception:
            pass
    paras = []
    for idx, p in enumerate(d.paragraphs):
        para = Para(idx, p, style_bold.get(p.style.name, False))
        if para.text.strip():
            paras.append(para)

    out = []          # righe Typst
    report = {"chapters": [], "headings": [], "counts": {}, "paragraphs_in": len(paras)}
    counts = report["counts"]
    used = set()

    def bump(k):
        counts[k] = counts.get(k, 0) + 1

    chapter = None
    mode = "body"
    seen_a = False
    seen_h2 = False
    expect_title = False
    expect_epi = False
    pending_script = []   # paragrafi dello script in attesa di essere raggruppati
    disc = None           # dict in costruzione
    box = None
    last_num = None

    def flush_script():
        nonlocal pending_script
        if pending_script:
            out.append("#script[\n" + "\n\n".join(pending_script) + "\n]\n")
            pending_script = []

    def flush_disc():
        nonlocal disc
        if disc is None:
            return
        rows = []
        for pr in disc["profiles"]:
            body = "\n\n".join(pr["body"])
            rows.append(f'  (lettera: "{pr["letter"]}", nome: [{pr["name"]}], corpo: [\n{body}\n  ]),')
        out.append(f'#disc(titolo: [{disc["title"]}], profili: (\n' + "\n".join(rows) + "\n))\n")
        disc = None

    def flush_box():
        nonlocal box
        if box is None:
            return
        rows = []
        for f in box["fields"]:
            body = "\n".join(f["body"])
            rows.append(f'  (etichetta: [{f["label"]}], corpo: [\n{body}\n  ]),')
        out.append(f'#protocollo(capitolo: "{box["chapter"]}", titolo: [{box["title"]}], campi: (\n'
                   + "\n".join(rows) + "\n))\n")
        box = None

    def flush_all():
        flush_script()
        flush_disc()
        flush_box()

    def close_biblio():
        nonlocal mode
        if mode == "biblio":
            out.append("]\n")

    for p in paras:
        txt = p.text.strip()
        plain = re.sub(r"\s+", " ", txt)
        m_ch = re.match(T["chapter"], plain)
        is_intro = (chapter is None and re.match(T["intro"], plain) and p.all_bold)

        # --- inizio capitolo -------------------------------------------------
        if m_ch or is_intro:
            flush_all(); close_biblio()
            chapter = {"num": m_ch.group(1) if m_ch else "", "label": plain, "title": None,
                       "start_idx": p.idx}
            report["chapters"].append(chapter)
            mode = "body"; seen_a = False; seen_h2 = False
            expect_title = True
            used.add(p.idx)
            continue
        if expect_title:
            chapter["title"] = plain
            chapter["_title_typ"] = runs_to_typ(p.runs, drop_bold=True, drop_ital=True)
            expect_title = False; expect_epi = True
            used.add(p.idx)
            continue
        if expect_epi:
            expect_epi = False
            if "\n" in p.text and p.ital_ratio > 0.5 and (
                    re.search(r"\n\s*[—–-]", p.text)
                    # attribuzione senza trattino (es. cap. 3 spagnolo): riga breve finale
                    or len(p.text.split("\n", 1)[1].strip()) < 60):
                quote, src = p.text.split("\n", 1)
                src = re.sub(r"^\s*[—–-]\s*", "", src)
                out.append(f'#capitolo(numero: "{chapter["num"]}", etichetta: [{esc(chapter["label"])}], '
                           f'titolo: [{chapter["_title_typ"]}], epigrafe: [{esc(quote.strip())}], '
                           f'fonte: [{esc(src.strip())}])\n')
                bump("epigrafi")
                used.add(p.idx)
                continue
            out.append(f'#capitolo(numero: "{chapter["num"]}", etichetta: [{esc(chapter["label"])}], '
                       f'titolo: [{chapter["_title_typ"]}])\n')

        # --- sezioni ricorrenti ----------------------------------------------
        if re.match(T["biblio"], plain):
            flush_all(); close_biblio()
            mode = "biblio"
            out.append(f"#bibliografia(titolo: [{esc(plain)}])[\n")
            bump("bibliografie"); used.add(p.idx)
            continue
        if re.match(T["disc"], plain):
            flush_all(); close_biblio()
            mode = "disc"
            disc = {"title": esc(plain), "profiles": []}
            bump("box_disc"); used.add(p.idx)
            continue
        m_box = re.match(T["box"], plain)
        if m_box:
            flush_all(); close_biblio()
            mode = "box"
            box = {"chapter": chapter["num"], "title": esc(T.get("box_title", m_box.group(1))), "fields": []}
            last_num = None
            bump("box_protocollo"); used.add(p.idx)
            continue
        if re.match(T["script"], plain) and p.all_bold:
            flush_all(); close_biblio()
            mode = "script"
            out.append(f"#script-titolo[{esc(plain)}]\n")
            report["headings"].append(("script", p.idx, plain))
            bump("script"); used.add(p.idx)
            continue
        if re.match(T["perche"], plain) and p.all_bold:
            flush_all(); close_biblio()
            mode = "perche"
            out.append(f"#perche-titolo[{esc(plain)}]\n")
            report["headings"].append(("perche", p.idx, plain))
            bump("perche"); used.add(p.idx)
            continue

        # --- dentro le sezioni ----------------------------------------------
        if mode == "biblio":
            out.append(f"  #voce[{runs_to_typ(p.runs)}]")
            bump("voci_bibliografiche"); used.add(p.idx)
            continue

        if mode == "disc":
            m_pr = re.match(T["disc_profile"], plain)
            if m_pr and p.all_bold:
                disc["profiles"].append({"letter": m_pr.group(1), "name": esc(m_pr.group(2)), "body": []})
                used.add(p.idx)
                continue
            body = disc["profiles"][-1]["body"]
            if p.all_bold and plain.startswith(T["leva"]):
                body.append(f"#leva[{runs_to_typ(p.runs, drop_bold=True)}]")
            elif p.starts_ital_quote or p.all_ital:
                body.append(f"#battuta-disc[{runs_to_typ(p.runs)}]")
            else:
                body.append(runs_to_typ(p.runs))
            used.add(p.idx)
            continue

        if mode == "box":
            if p.all_bold and plain in T["box_labels"]:
                box["fields"].append({"label": esc(plain), "body": []})
                last_num = None
                used.add(p.idx)
                continue
            body = box["fields"][-1]["body"]
            if p.num is not None:
                if p.num != last_num:
                    body.append("#passi-reset()")
                    last_num = p.num
                body.append(f"#passo[{runs_to_typ(p.runs)}]")
                bump("passi")
            elif p.all_ital and len(plain) < 80:
                body.append(f"#sottoetichetta[{runs_to_typ(p.runs, drop_ital=True)}]")
                last_num = None
            else:
                body.append(f"#testo-box[{runs_to_typ(p.runs)}]")
            used.add(p.idx)
            continue

        # --- titoli interni ----------------------------------------------------
        is_heading = (p.all_bold and len(plain) <= 100 and not plain.endswith(".")
                      and (p.style in ("Heading 2", "Heading 3") or not plain.endswith("?")))
        if is_heading:
            flush_script()
            if mode == "perche":
                out.append(f"#perche-voce[{runs_to_typ(p.runs, drop_bold=True)}]\n")
                report["headings"].append(("perche-voce", p.idx, plain))
            elif mode == "script" and p.style == "Heading 3":
                out.append(f"#script-sub[{runs_to_typ(p.runs, drop_bold=True)}]\n")
                report["headings"].append(("script-sub", p.idx, plain))
            else:
                # Heading 3 vale come sezione principale se nel capitolo non
                # compare ancora un Heading 2 (capitoli 1 e 7); altrimenti è
                # una sottosezione (capitolo 13).
                if p.style == "Heading 2" or (p.style == "Heading 3" and not seen_h2):
                    level = "A"
                else:
                    level = "B"
                if p.style == "Heading 2":
                    seen_h2 = True
                if level == "A":
                    seen_a = True
                    mode = "body"
                    out.append(f"#sezione[{runs_to_typ(p.runs, drop_bold=True)}]\n")
                else:
                    out.append(f"#sottosezione[{runs_to_typ(p.runs, drop_bold=True)}]\n")
                report["headings"].append((level, p.idx, plain))
            bump("titoli")
            used.add(p.idx)
            continue

        # --- battute / dialoghi ------------------------------------------------
        speech = p.all_ital or (p.starts_ital_quote and p.ital_ratio > 0.6)
        if mode == "script":
            if speech or (pending_script and p.ital_ratio > 0.6):
                pending_script.append(runs_to_typ(p.runs))
                bump("battute_script"); used.add(p.idx)
                continue
            flush_script()
        if speech:
            out.append(f"#dialogo[{runs_to_typ(p.runs)}]\n")
            bump("dialoghi"); used.add(p.idx)
            continue

        out.append(runs_to_typ(p.runs) + "\n")
        bump("paragrafi"); used.add(p.idx)

    flush_all(); close_biblio()
    missing = [p.idx for p in paras if p.idx not in used]
    report["missing"] = missing
    for c in report["chapters"]:
        c.pop("_title_typ", None)
    return "\n".join(out), report


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("docx")
    ap.add_argument("out")
    ap.add_argument("--lang", default="it")
    ap.add_argument("--report")
    a = ap.parse_args()
    typ, rep = convert(a.docx, a.lang)
    header = ("// GENERATO da tools/docx2typ.py — contenuto del libro, senza stili.\n"
              "// Le funzioni (#capitolo, #sezione, #script, #protocollo, …) sono definite\n"
              "// in template/libro.typ. Correzioni di testo: modificare qui o nel Word e rigenerare.\n\n"
              "#import \"../template/libro.typ\": *\n\n")
    with open(a.out, "w", encoding="utf-8") as f:
        f.write(header + typ)
    if a.report:
        with open(a.report, "w", encoding="utf-8") as f:
            json.dump(rep, f, ensure_ascii=False, indent=1)
    print(json.dumps(rep["counts"], ensure_ascii=False), "missing:", rep["missing"], file=sys.stderr)


if __name__ == "__main__":
    main()

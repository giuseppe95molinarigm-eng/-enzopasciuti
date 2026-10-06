# Impaginazione del libro (KDP · 8 × 10 in · B/N)

Questo progetto produce il PDF di stampa a partire dal manoscritto Word. È pensato per essere riutilizzato con le edizioni inglese e spagnola.

```
template/libro.typ     progetto grafico: stili, box, aperture, indici (comune a tutte le lingue)
it/main.typ            edizione italiana: titolo, autore, colophon, ordine delle pagine iniziali
it/contenuto.typ       testo del libro in markup semantico (generato dal Word, modificabile)
fonts/                 Source Serif 4 e Inter (licenza SIL OFL), incorporati nel PDF
tools/docx2typ.py      Word -> contenuto.typ (riconosce capitoli, script, box, bibliografie…)
tools/build.py         compila il PDF (libro intero o campione di un capitolo)
tools/qa.py            controllo: testo integrale, formato, font, titoli isolati, pagine corte
tools/check_indice.py  controllo: ogni voce d'indice punta alla pagina giusta
tools/spreads.py       anteprime a doppia pagina per il controllo visivo
output/                PDF finali (libro-it.pdf, campione-it.pdf)
NOTE_EDITORIALI.md     struttura riconosciuta, dubbi editoriali, specifiche KDP, scelte grafiche
```

## Compilare

```bash
pip install typst python-docx pymupdf pillow
python3 tools/docx2typ.py "MASTER.docx" it/contenuto.typ     # solo se cambia il Word
python3 tools/build.py it                                     # -> output/libro-it.pdf
python3 tools/build.py it --campione 6                        # -> output/campione-it.pdf
python3 tools/qa.py "MASTER.docx" output/libro-it.pdf
python3 tools/check_indice.py output/libro-it.pdf
```

In alternativa si può usare l'editor web di Typst (typst.app): basta caricare la cartella e aprire `it/main.typ`.

## Modificare

- **Titolo, autore, colophon.** In cima a `it/main.typ`.
- **Testo.** Si corregge direttamente in `it/contenuto.typ`, oppure nel Word, rigenerando poi il file con `docx2typ.py`. Ogni elemento ha la sua funzione semantica:
  - `#capitolo(...)`, `#sezione[...]`, `#sottosezione[...]`, `#dialogo[...]`;
  - `#script-titolo[...]`, `#script[...]`, `#perche-titolo[...]`, `#perche-voce[...]`;
  - `#bibliografia[...]`, `#disc(...)`, `#protocollo(...)`.
- **Aspetto grafico.** Tutto in `template/libro.typ`: corpo, interlinea, gabbia, colori e stili dei box. Una modifica lì si applica a tutto il libro e a tutte le lingue.

## Edizioni inglese e spagnola

1. Copiare `it/` in `en/` (o `es/`).
2. In `tools/docx2typ.py` aggiungere in `TRIGGERS` le stringhe della nuova lingua, per esempio `"en": {"chapter": r"^CHAPTER\s+(\d+)$", "biblio": r"^References$", "script": r"^Operational script$", ...}`.
3. Generare il contenuto: `python3 tools/docx2typ.py EN.docx en/contenuto.typ --lang en`.
4. In `en/main.typ` impostare `lingua: "en"` (sillabazione) e le etichette, passando `etichette: (capitolo: "Chapter", ...)` a `libro.with(...)`. I titoli «Indice» e «Protocolli in sintesi» si cambiano nelle chiamate `#pagina-indice(...)`.
5. Compilare con `python3 tools/build.py en` e ricontrollare con `qa.py`.
6. Ricalcolare il margine interno e il dorso della copertina in base al nuovo numero di pagine (vedi `NOTE_EDITORIALI.md`).

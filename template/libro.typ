// =============================================================================
//  Progetto grafico del libro — stili riutilizzabili (IT / EN / ES)
//  Formato: 8 × 10 in (203,2 × 254 mm), interno in bianco e nero, KDP paperback
//  Caratteri: Source Serif 4 (testo, titoli) · Inter (apparati operativi)
// =============================================================================

// ---- Parametri generali -------------------------------------------------------
#let serif = "Source Serif 4"
#let serif-small = "Source Serif 4 SmText"   // ottica per corpi piccoli
#let serif-sub = "Source Serif 4 Subhead"    // ottica per titoli intermedi
#let serif-display = "Source Serif 4 Display" // ottica per titoli grandi
#let sans = "Inter"

#let nero = luma(0)
#let grigio-testo = luma(38%)     // didascalie, testatine
#let grigio-filetto = luma(70%)
#let fondino = luma(92%)          // ~8% di nero: visibile in stampa, testo leggibile
#let fondino-chiaro = luma(95.5%)

#let corpo = 11pt
#let interlinea = 0.74em

#let gabbia = (
  inside: 25mm,    // KDP: min. 12,7 mm (151–300 pp.) / 15,9 mm (301–500 pp.)
  outside: 36mm,
  top: 27mm,
  bottom: 27mm,
)

#let altezza-gabbia = 10in - gabbia.top - gabbia.bottom

// Etichette di lingua (sostituire per EN / ES)
#let L = state("lingua", (
  capitolo: "Capitolo",
  indice: "Indice",
  protocolli: "Protocolli in sintesi",
  protocolli-sotto: "Consultazione rapida: script operativi e protocolli, capitolo per capitolo.",
  script: "Script",
  box: "Protocollo",
  segue: "segue",
  pagina: "p.",
))

// ---- Utilità ----------------------------------------------------------------
#let marca(body, size: 7.4pt, fill: nero, track: 0.14em, weight: 600) = text(
  font: sans, size: size, weight: weight, tracking: track, fill: fill,
  upper(body),
)

// Marcatori invisibili per testatine e indici
#let capitolo-corrente = state("capitolo", none)

// Apertura su pagina dispari (recto). La pagina bianca eventualmente inserita
// viene riconosciuta dalle testatine: segue un'apertura e non contiene la fine
// del capitolo precedente.
#let apri-a-destra() = {
  [#metadata("fine")<fine-cap>]
  pagebreak(weak: true, to: "odd")
}

#let pagina-vuota() = {
  let p = here().page()
  query(<apertura>).any(m => m.location().page() == p + 1) and not query(<fine-cap>).any(m => m.location().page() == p)
}

#let pagina-speciale(etichetta) = {
  let pag = here().page()
  query(etichetta).any(m => m.location().page() == pag)
}

// ---- Apertura di capitolo ---------------------------------------------------
#let capitolo(numero: "", etichetta: [], titolo: [], epigrafe: none, fonte: none) = {
  apri-a-destra()
  [#metadata("apertura")<apertura>]
  capitolo-corrente.update((numero: numero, titolo: titolo))
  // titolo strutturale (per indice e testatine), reso invisibile qui
  [#metadata((numero: numero, titolo: titolo, etichetta: etichetta))<cap-meta>]
  place(top + left, hide(heading(level: 1, outlined: true, bookmarked: true,
    if numero != "" { [#numero · #titolo] } else { titolo })))
  set par(first-line-indent: 0pt)
  v(30mm)
  // Numero / etichetta
  block(below: 0pt, {
    if numero != "" {
      context marca(L.get().capitolo, size: 7.6pt, fill: grigio-testo, track: 0.32em)
      v(3mm)
      text(font: serif-display, weight: 300, size: 86pt, fill: nero, top-edge: "cap-height",
        bottom-edge: "baseline", numero)
    } else {
      marca(etichetta, size: 7.6pt, fill: grigio-testo, track: 0.32em)
    }
  })
  v(9mm)
  line(length: 22mm, stroke: 1.6pt + nero)
  v(7mm)
  block(width: 132mm, {
    set par(justify: false, leading: 0.32em, first-line-indent: 0pt)
    set text(font: serif-display, weight: 600, size: 25pt, hyphenate: false, tracking: -0.005em)
    titolo
  })
  if epigrafe != none {
    v(11mm)
    block(width: 96mm, inset: (left: 0mm), {
      set par(justify: false, leading: 0.55em, first-line-indent: 0pt)
      text(font: serif-sub, style: "italic", size: 11.2pt, fill: luma(15%), hyphenate: false, epigrafe)
      v(2.6mm)
      text(font: sans, size: 7.2pt, weight: 500, tracking: 0.12em, fill: grigio-testo, [— #upper(fonte)])
    })
  }
  v(14mm)
}

// ---- Titoli interni -----------------------------------------------------------
#let sezione(body) = {
  heading(level: 2, body)
}
#let sottosezione(body) = {
  heading(level: 3, body)
}

// ---- Dialoghi nel testo narrativo -----------------------------------------
#let dialogo(body) = block(
  above: 0.95em, below: 0.95em, inset: (left: 6mm, right: 4mm),
  {
    set par(first-line-indent: 0pt, justify: false)
    set text(hyphenate: false)
    body
  },
)

// ---- Script operativo -------------------------------------------------------
#let script-titolo(body) = {
  block(above: 2.2em, below: 1.1em, sticky: true, breakable: false, {
    box(fill: nero, inset: (x: 2.6mm, y: 1.7mm), baseline: 1.7mm,
      text(font: sans, size: 7.4pt, weight: 600, tracking: 0.18em, fill: white, number-type: "lining", upper(body)))
    [#metadata("script")<script>]
  })
}

#let script-sub(body) = block(above: 1.5em, below: 0.7em, sticky: true, {
  set par(first-line-indent: 0pt, justify: false)
  text(font: sans, size: 9.4pt, weight: 600, body)
})

#let script(body) = block(
  above: 1.05em, below: 1.15em, width: 100%, breakable: true,
  fill: fondino-chiaro,
  stroke: (left: 2.4pt + nero),
  inset: (left: 6.5mm, right: 6mm, top: 4.2mm, bottom: 4.4mm),
  {
    set par(first-line-indent: 0pt, justify: false, spacing: 0.95em, leading: 0.7em)
    set text(size: 10.5pt, hyphenate: false)
    body
  },
)

// ---- «Perché questo protocollo funziona» -----------------------------------
#let perche-titolo(body) = heading(level: 2, outlined: false, body)

#let perche-voce(body) = block(above: 1.25em, below: 0.45em, sticky: true, {
  set par(first-line-indent: 0pt, justify: false)
  grid(columns: (4.2mm, 1fr), column-gutter: 0mm,
    place(dy: 0.18em, square(size: 1.7mm, fill: nero)),
    text(font: sans, size: 9.2pt, weight: 600, body))
})

// ---- Bibliografia ---------------------------------------------------------------
#let voce(body) = par(body)
#let bibliografia(titolo: [Bibliografia], body) = {
  block(above: 2.4em, below: 0.9em, sticky: true, {
    line(length: 100%, stroke: 0.5pt + grigio-filetto)
    v(2.2mm)
    marca(titolo, size: 7pt, fill: grigio-testo, track: 0.22em)
  })
  block({
    set par(justify: false, first-line-indent: 0pt, hanging-indent: 4mm, leading: 0.52em, spacing: 0.62em)
    set text(font: serif-small, size: 8.4pt, hyphenate: true, fill: luma(10%))
    show emph: it => it
    body
  })
}

// ---- Box DISC ----------------------------------------------------------------
#let leva(body) = block(above: 0.3em, below: 0.7em,
  text(font: sans, size: 8.2pt, weight: 600, tracking: 0.01em, body))
#let battuta-disc(body) = block(above: 0.7em, below: 0.7em, inset: (left: 3.5mm),
  stroke: (left: 0.6pt + grigio-filetto), {
    set par(justify: false)
    body
  })

#let disc(titolo: [], profili: ()) = {
  let intestazione(segue) = block(width: 100%, inset: (x: 6mm, top: 5mm, bottom: 3.6mm), {
    grid(columns: (1fr, auto), align: (left + bottom, right + bottom),
      text(font: serif-sub, weight: 600, size: 13pt, hyphenate: false, titolo),
      if segue { text(font: sans, size: 7pt, weight: 500, tracking: 0.12em, fill: grigio-testo,
        context upper(L.get().segue)) },
    )
  })
  let profilo(p, ultimo) = block(breakable: false, width: 100%,
    inset: (x: 6mm, top: 4.2mm, bottom: 4.6mm),
    stroke: if ultimo { none } else { (bottom: 0.5pt + grigio-filetto) }, {
      grid(columns: (12.5mm, 1fr), column-gutter: 0mm,
        box(width: 8.4mm, height: 8.4mm, fill: nero,
          align(center + horizon, text(font: sans, weight: 700, size: 12.5pt, fill: white, p.lettera))),
        {
          set par(first-line-indent: 0pt, justify: false, spacing: 0.7em, leading: 0.62em)
          set text(size: 9.9pt, hyphenate: true)
          block(above: 0.05em, below: 0.5em, text(font: sans, size: 10.4pt, weight: 600, p.nome))
          p.corpo
        })
    })
  // «needspace»: il box non comincia in fondo pagina se non c'è spazio almeno
  // per l'intestazione e il primo profilo.
  layout(spazio => {
    let h = measure(block(width: spazio.width, {
      set par(first-line-indent: 0pt)
      intestazione(false)
      profilo(profili.first(), false)
    })).height + 2pt
    block(above: 2.6em, below: 0pt, height: h, breakable: false, width: 100%)
    v(-h)
  })
  block(above: 0pt, below: 1.4em, width: 100%, breakable: true, {
    set par(first-line-indent: 0pt)
    [#metadata("disc")<disc-inizio>]
    table(columns: 1fr, stroke: (x: 0.8pt + nero), inset: 0pt,
      table.header(repeat: true,
        table.cell(stroke: (top: 0.8pt + nero, bottom: 0.8pt + nero), context {
          // il titolo si ripete con «segue» quando il box continua alla pagina dopo
          let inizio = query(selector(<disc-inizio>).before(here()))
          let segue = inizio.len() > 0 and inizio.last().location().page() < here().page()
          intestazione(segue)
        })),
      ..profili.enumerate().map(((k, p)) => table.cell(profilo(p, k == profili.len() - 1))),
      table.hline(stroke: 0.8pt + nero),
    )
  })
}

// ---- Box «Protocollo in sintesi» ----------------------------------------
#let numero-passo = counter("passo")
#let passi-reset() = numero-passo.update(0)
#let passo(body) = {
  numero-passo.step()
  block(above: 0.55em, below: 0.55em, breakable: false,
    grid(columns: (7mm, 1fr),
      context {
        let n = numero-passo.get().first()
        box(width: 4.6mm, height: 4.6mm, radius: 2.3mm, fill: nero, baseline: 1.15mm,
          align(center + horizon, text(font: sans, size: 7pt, weight: 700, fill: white, str(n))))
      },
      body))
}
#let sottoetichetta(body) = block(above: 0.9em, below: 0.35em, sticky: true,
  text(font: sans, size: 8.6pt, weight: 600, style: "italic", body))
#let testo-box(body) = block(above: 0.55em, below: 0.55em, body)

#let protocollo(capitolo: "", titolo: [], campi: ()) = {
  let intestazione(segue) = block(width: 100%, inset: (x: 6mm, top: 5.2mm, bottom: 1mm), {
    grid(columns: (1fr, auto), align: (left + bottom, right + bottom),
      {
        context marca([#L.get().capitolo #capitolo], size: 6.8pt, fill: grigio-testo, track: 0.2em)
        v(1.6mm)
        text(font: serif-sub, weight: 600, size: 15pt, titolo)
      },
      if segue { text(font: sans, size: 7pt, weight: 500, tracking: 0.12em, fill: grigio-testo,
        context upper(L.get().segue)) },
    )
  })
  let campo(c) = block(breakable: true, width: 100%, inset: (x: 6mm, top: 3.4mm, bottom: 3.4mm), {
    grid(columns: (29mm, 1fr), column-gutter: 3mm,
      block(above: 0pt, inset: (top: 0.25em),
        text(font: sans, size: 6.9pt, weight: 700, tracking: 0.13em, hyphenate: false, upper(c.etichetta))),
      {
        set par(first-line-indent: 0pt, justify: false, leading: 0.66em, spacing: 0.66em)
        set text(font: sans, size: 8.9pt, hyphenate: true, lang: "it")
        passi-reset()
        c.corpo
      })
  })
  let tabella = {
    set par(first-line-indent: 0pt)
    table(columns: 1fr, inset: 0pt, fill: fondino,
      stroke: none,
      table.header(repeat: true,
        table.cell(stroke: (top: 3pt + nero), context {
          let inizio = query(selector(<box-protocollo>).before(here()))
          let segue = inizio.len() > 0 and inizio.last().location().page() < here().page()
          intestazione(segue)
        })),
      ..campi.enumerate().map(((k, c)) => table.cell(
        stroke: if k > 0 { (top: 0.5pt + luma(100%)) } else { none }, campo(c))),
      table.cell(v(2mm)),
    )
  }
  // Il box resta intero se entra in una pagina; altrimenti si spezza tra un
  // campo e l'altro (o tra i passi) con l'intestazione ripetuta e «segue».
  // Ogni protocollo apre una pagina nuova: una «scheda» facile da ritrovare.
  pagebreak(weak: true)
  layout(spazio => {
    let h = measure(block(width: spazio.width, tabella)).height
    block(above: 0pt, below: 1.2em, width: 100%, breakable: h > altezza-gabbia * 0.97, {
      [#metadata(capitolo)<box-protocollo>]
      tabella
    })
  })
}

// ---- Indici ------------------------------------------------------------------
#let indice() = context {
  let voci = query(selector(<cap-meta>).or(heading.where(level: 2, outlined: true)))
  for v in voci {
    let pag = counter(page).at(v.location()).first()
    if v.func() == metadata {
      let c = v.value
      block(above: 1.5em, below: 0.55em, breakable: false, sticky: true,
        grid(columns: (9mm, 1fr, 12mm), align: (left + top, left + top, right + top),
          text(font: sans, size: 8.4pt, weight: 600, fill: grigio-testo, number-type: "lining",
            if c.numero != "" { c.numero }),
          link(v.location(), text(font: serif-sub, weight: 600, size: 11.4pt, hyphenate: false,
            if c.numero == "" { [#c.etichetta: #c.titolo] } else { c.titolo })),
          text(font: sans, size: 8.4pt, weight: 600, number-type: "lining", str(pag))))
    } else {
      block(above: 0.4em, below: 0.4em, breakable: false,
        grid(columns: (9mm, 1fr, 12mm), align: (left, left + top, right + top),
          [],
          link(v.location(), text(size: 9.4pt, hyphenate: false, fill: luma(18%), v.body)),
          text(font: sans, size: 7.8pt, fill: grigio-testo, number-type: "lining", str(pag))))
    }
  }
}

#let indice-protocolli() = context {
  let boxes = query(<box-protocollo>)
  let scripts = query(<script>)
  let capitoli = query(<cap-meta>)
  for b in boxes {
    let cap = capitoli.filter(c => c.location().page() <= b.location().page()).last()
    let sc = scripts.filter(s => s.location().page() >= cap.location().page() and s.location().page() <= b.location().page())
    let pb = counter(page).at(b.location()).first()
    let ps = if sc.len() > 0 { counter(page).at(sc.first().location()).first() } else { none }
    let rif(lbl, loc, n) = link(loc, box(text(font: sans, size: 7.4pt, number-type: "lining",
      [#text(fill: grigio-testo, tracking: 0.1em, upper(lbl))#h(1.4mm)#text(weight: 600, size: 8.4pt, str(n))])))
    block(breakable: false, above: 0pt, below: 0pt, inset: (y: 3.4mm), width: 100%,
      stroke: (bottom: 0.5pt + grigio-filetto),
      grid(columns: (12mm, 1fr, 19mm, 31mm), column-gutter: 2mm, align: (left + horizon, left + horizon, right + horizon, right + horizon),
        text(font: serif-display, weight: 300, size: 20pt, number-type: "lining", cap.value.numero),
        link(cap.location(), text(font: serif-sub, weight: 600, size: 10.6pt, hyphenate: false, cap.value.titolo)),
        if ps != none { rif(L.get().script, sc.first().location(), ps) },
        rif(L.get().box, b.location(), pb),
      ))
  }
}

// ---- Impostazione del documento ----------------------------------------------
#let libro(
  titolo: [],
  sottotitolo: none,
  autore: [],
  lingua: "it",
  colophon: none,
  etichette: none,
  body,
) = {
  set document(title: titolo, author: if type(autore) == str { autore } else { () })
  set text(font: serif, size: corpo, lang: lingua, hyphenate: true, number-type: "old-style",
    costs: (widow: 100%, orphan: 100%, hyphenation: 85%, runt: 100%),
    fallback: false)
  set par(justify: true, leading: interlinea, spacing: interlinea,
    first-line-indent: 1.15em, linebreaks: "optimized")
  if etichette != none { L.update(etichette) }

  // Testatine: verso = capitolo, recto = titolo del capitolo; folio all'esterno
  set page(
    width: 8in, height: 10in,
    margin: gabbia,
    binding: left,
    header-ascent: 9mm,
    footer-descent: 9mm,
    header: context {
      if pagina-vuota() or pagina-speciale(<apertura>) or pagina-speciale(<senza-testatina>) { return }
      let cap = capitolo-corrente.get()
      if cap == none { return }
      let n = counter(page).display()
      let pari = calc.even(here().page())
      set text(font: sans, size: 7pt, weight: 500, tracking: 0.12em, fill: grigio-testo, number-type: "lining")
      if pari {
        grid(columns: (12mm, 1fr), align: (left, left),
          text(fill: nero, weight: 600, n),
          if cap.numero != "" { upper([#L.get().capitolo #cap.numero]) } else { upper(cap.titolo) })
      } else {
        grid(columns: (1fr, 12mm), align: (right, right),
          upper(cap.titolo),
          text(fill: nero, weight: 600, n))
      }
    },
    footer: context {
      if pagina-vuota() or pagina-speciale(<senza-testatina>) { return }
      if pagina-speciale(<apertura>) {
        align(center, text(font: sans, size: 7.4pt, weight: 600, fill: nero, number-type: "lining",
          counter(page).display()))
      }
    },
  )

  // Titoli interni
  show heading.where(level: 2): it => block(above: 2.1em, below: 0.85em, sticky: true, breakable: false, {
    set par(justify: false, first-line-indent: 0pt, leading: 0.4em)
    set text(font: serif-sub, weight: 600, size: 14pt, hyphenate: false, number-type: "lining")
    it.body
  })
  show heading.where(level: 3): it => block(above: 1.6em, below: 0.6em, sticky: true, breakable: false, {
    set par(justify: false, first-line-indent: 0pt)
    set text(font: sans, weight: 600, size: 9.6pt, hyphenate: false, tracking: 0.01em)
    it.body
  })
  show heading: set text(number-type: "lining")

  body
}

// ---- Pagine iniziali ------------------------------------------------------------
#let frontespizio(titolo: [], sottotitolo: none, autore: [], colophon: none) = {
  // Occhietto
  page(header: none, footer: none, {
    [#metadata("x")<senza-testatina>]
    v(62mm)
    align(left, block(width: 120mm, {
      set par(justify: false, leading: 0.35em)
      text(font: serif-display, weight: 400, size: 19pt, titolo)
    }))
  })
  page(header: none, footer: none, [#metadata("x")<senza-testatina>])
  // Frontespizio
  page(header: none, footer: none, {
    [#metadata("x")<senza-testatina>]
    v(38mm)
    marca(autore, size: 9pt, fill: nero, track: 0.28em)
    v(16mm)
    line(length: 22mm, stroke: 1.6pt + nero)
    v(9mm)
    block(width: 130mm, {
      set par(justify: false, leading: 0.3em)
      text(font: serif-display, weight: 600, size: 34pt, hyphenate: false, titolo)
    })
    if sottotitolo != none {
      v(8mm)
      block(width: 120mm, {
        set par(justify: false, leading: 0.5em)
        text(font: serif-sub, style: "italic", size: 14pt, fill: luma(20%), sottotitolo)
      })
    }
  })
  // Colophon
  page(header: none, footer: none, {
    [#metadata("x")<senza-testatina>]
    align(bottom, block(width: 100mm, {
      set par(justify: false, leading: 0.55em, spacing: 0.9em, first-line-indent: 0pt)
      set text(font: serif-small, size: 8pt, fill: luma(20%), number-type: "lining")
      colophon
    }))
  })
}

#let pagina-indice(titolo, sotto: none, body) = {
  apri-a-destra()
  [#metadata("x")<apertura>]
  v(40mm)
  line(length: 22mm, stroke: 1.6pt + nero)
  v(7mm)
  text(font: serif-display, weight: 600, size: 25pt, titolo)
  if sotto != none {
    v(4mm)
    block(width: 110mm, text(font: serif-sub, style: "italic", size: 11pt, fill: luma(25%), sotto))
  }
  v(12mm)
  set par(justify: false, first-line-indent: 0pt)
  body
}

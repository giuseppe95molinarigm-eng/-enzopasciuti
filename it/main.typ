// Edizione italiana — file principale da compilare
//   typst compile --font-path fonts it/main.typ output/libro-it.pdf
// (oppure: python3 tools/build.py it)
#import "../template/libro.typ": *

// ---- Dati del libro (DA CONFERMARE con il cliente) ----------------------------
#let titolo = [Titolo del libro]
#let sottotitolo = none
#let autore = "Enzo Pasciuti"
#let colophon = [
  © #datetime.today().year() #autore \
  Tutti i diritti riservati. Nessuna parte di questo libro può essere riprodotta
  senza l’autorizzazione scritta dell’autore.

  Prima edizione.
]

#show: libro.with(titolo: titolo, autore: autore, lingua: "it")

#set page(numbering: "i")
#frontespizio(titolo: titolo, sottotitolo: sottotitolo, autore: autore, colophon: colophon)

#pagina-indice("Indice")[#indice()]
#pagina-indice("Protocolli in sintesi",
  sotto: [Consultazione rapida: per ogni protocollo, la pagina dello script operativo e del riquadro di sintesi.])[#indice-protocolli()]

#apri-a-destra()
#set page(numbering: "1")
#counter(page).update(1)
#include "contenuto.typ"

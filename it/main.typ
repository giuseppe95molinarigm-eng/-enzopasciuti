// Edizione italiana — file principale da compilare
//   typst compile --font-path fonts it/main.typ output/libro-it.pdf
// (oppure: python3 tools/build.py it)
#import "../template/libro.typ": *

// ---- Dati del libro (dalla copertina italiana) ---------------------------------
#let titolo = [Dicono di averli usati]
#let sottotitolo = [La psicologia nascosta della collaborazione con gli allineatori e~i protocolli clinici che fanno funzionare il trattamento]
#let autore = "Enzo Pasciuti"
#let autore-frontespizio = "Dr. Enzo Pasciuti"
#let editore = "Enzo Pasciuti Academy"
#let colophon = [
  © #datetime.today().year() #autore \
  Tutti i diritti riservati. Nessuna parte di questo libro può essere riprodotta
  senza l’autorizzazione scritta dell’autore.

  Prima edizione.
]

#show: libro.with(titolo: titolo, autore: autore, lingua: "it")

#set page(numbering: "i")
#frontespizio(titolo: titolo, sottotitolo: sottotitolo, autore: autore-frontespizio, editore: editore, colophon: colophon)

#pagina-indice("Indice")[#indice()]

#apri-a-destra()
#set page(numbering: "1")
#counter(page).update(1)
#include "contenuto.typ"

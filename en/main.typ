// English edition — main file to compile
//   python3 tools/build.py en   ->  output/libro-en.pdf
// Same design as the Italian edition (template/libro.typ); only text and labels change.
#import "../template/libro.typ": *

// ---- Book data (from the English cover) ------------------------------------------
#let titolo = [They Say They Wore Them]
#let sottotitolo = [The Hidden Psychology of Clear Aligner Compliance and the Clinical Protocols That Make Treatment~Work]
#let autore = "Enzo Pasciuti"
#let autore-frontespizio = "Dr. Enzo Pasciuti"
#let editore = "Enzo Pasciuti Academy"
#let colophon = [
  © #datetime.today().year() #autore \
  All rights reserved. No part of this book may be reproduced
  without the written permission of the author.

  First edition.
]

#show: libro.with(titolo: titolo, autore: autore, lingua: "en", etichette: (
  capitolo: "Chapter",
  indice: "Contents",
  protocolli: "Protocols at a Glance",
  protocolli-sotto: "",
  script: "Script",
  box: "Protocol",
  segue: "continued",
  pagina: "p.",
))

#set page(numbering: "i")
#frontespizio(titolo: [They Say \ They Wore Them], sottotitolo: sottotitolo, autore: autore-frontespizio, editore: editore, colophon: colophon)

#pagina-indice("Contents")[#indice()]

#apri-a-destra()
#set page(numbering: "1")
#counter(page).update(1)
#include "contenuto.typ"

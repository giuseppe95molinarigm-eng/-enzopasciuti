// Edición española — archivo principal
//   python3 tools/build.py es   ->  output/libro-es.pdf
// Mismo diseño que la edición italiana (template/libro.typ); solo cambian textos y etiquetas.
#import "../template/libro.typ": *

// ---- Datos del libro (de la cubierta española) -----------------------------------
#let titolo = [Dicen que los han usado]
#let sottotitolo = [La psicología oculta de la colaboración con los alineadores y los protocolos clínicos que hacen que el tratamiento~funcione]
#let autore = "Enzo Pasciuti"
#let autore-frontespizio = "Dr. Enzo Pasciuti"
#let editore = "Enzo Pasciuti Academy"
#let colophon = [
  © #datetime.today().year() #autore \
  Todos los derechos reservados. Ninguna parte de este libro puede reproducirse
  sin la autorización por escrito del autor.

  Primera edición.
]

#show: libro.with(titolo: titolo, autore: autore, lingua: "es", etichette: (
  capitolo: "Capítulo",
  indice: "Índice",
  protocolli: "Protocolos",
  protocolli-sotto: "",
  script: "Guion",
  box: "Protocolo",
  segue: "continúa",
  pagina: "p.",
))

#set page(numbering: "i")
#frontespizio(titolo: titolo, sottotitolo: sottotitolo, autore: autore-frontespizio, editore: editore, colophon: colophon)

#pagina-indice("Índice")[#indice()]

#apri-a-destra()
#set page(numbering: "1")
#counter(page).update(1)
#include "contenuto.typ"

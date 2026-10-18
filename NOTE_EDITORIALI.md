# Note editoriali e di produzione — edizione italiana

Impaginazione del file definitivo **«MASTER FINALISSIMO (1)(1).docx»**.

## 1. Struttura riconosciuta nel manoscritto

Il conteggio dei capitoli si basa sul file definitivo, non sulle indicazioni della chat.

| Elemento | Quantità |
|---|---|
| Introduzione («Perché ho scritto questo libro») | 1 |
| Capitoli | 17 |
| Epigrafi d'apertura (citazione + autore) | 17 |
| Titoli di sezione e sottosezione | 127 |
| Dialoghi nel testo narrativo | 59 |
| Sezioni «Script operativo» (capp. 6–16) | 11, con 51 battute |
| Sezioni «Perché questo protocollo funziona» | 11 |
| Box «Adattare la comunicazione al profilo DISC» | 11 |
| Box «Protocollo in sintesi» | 11, con 73 passi numerati |
| Bibliografie | 17, con 107 voci |

**Nota tecnica.** Nel Word gli stili sono usati in modo incoerente: per esempio «Titolo 1» è applicato al testo corrente del capitolo 1 e «Titolo 2» ad alcune voci bibliografiche. Per questo la struttura è stata ricavata dal contenuto e dalla formattazione reale di ogni paragrafo, non dal nome dello stile. Lo script `tools/docx2typ.py` fa questo lavoro in modo ripetibile.

## 2. Integrità del testo — verificata

- **Testo completo, nello stesso ordine.** Il confronto parola per parola tra Word e PDF (`tools/qa.py`) dà **0 differenze**: 69.119 parole su 69.119.
- **Parole in più nel PDF: 142.** Sono solo elementi di impaginazione:
  - l'etichetta «Capitolo N» sopra i box Protocollo;
  - l'intestazione del box DISC ripetuta con «segue» quando il box continua alla pagina successiva.
- **Enfasi conservate.** Grassetti e corsivi sono riportati com'erano nell'originale.

**Normalizzazioni esclusivamente tipografiche:**

- 8 apostrofi dritti (') trasformati in apostrofi tipografici (’), nei capp. 13 e 15;
- eliminati spazi doppi, spazi a inizio e fine paragrafo e le righe vuote usate per andare a pagina nuova.

**Marcatori redazionali resi graficamente:**

- «BOX — Protocollo in sintesi» diventa il riquadro intitolato «Protocollo in sintesi»: la parola «BOX» era un'istruzione per l'impaginazione;
- nei box DISC, «D — Dominante» diventa la lettera **D** in un quadrato nero seguita dal nome del profilo.

## 3. Dubbi editoriali da sottoporre al cliente

1. **Titolo, sottotitolo e autore** presi dalla copertina italiana: «Dicono di averli usati. La psicologia nascosta della collaborazione con gli allineatori e i protocolli clinici che fanno funzionare il trattamento», Dr. Enzo Pasciuti, Enzo Pasciuti Academy. Resta da confermare il **colophon**: anno, eventuale ISBN, crediti. Si modifica in cima a `it/main.typ`.
2. **Posizione delle bibliografie (capp. 6–16).** In ogni capitolo la bibliografia viene *prima* dei due box finali. L'ordine del manoscritto è stato rispettato. Spostare la bibliografia a chiusura del capitolo, dopo i box, renderebbe la lettura più lineare: è una modifica di una riga, se il cliente la approva.
3. **Formato delle bibliografie non uniforme** (non toccato, perché è contenuto):
   - i nomi delle riviste sono in corsivo nei capp. 3–8, 11–14 e 16, ma in tondo nei capp. 2, 9, 10, 15 e 17;
   - nel cap. 1 il corsivo è sul *titolo dell'articolo* invece che sulla rivista;
   - le riviste sono abbreviate in alcuni capitoli (es. *Am J Orthod Dentofacial Orthop*) e scritte per esteso in altri (es. *Journal of Orthodontics*);
   - i DOI compaiono solo nel cap. 8.
   
   Consiglio di uniformare tutto allo stile Vancouver/ICMJE, già prevalente.
4. **Cap. 16.** La sezione si intitola «Lo script operativo», mentre negli altri capitoli è «Script operativo». Il titolo è stato mantenuto com'è.
5. **Box DISC dei capp. 11, 12 e 14.** Hanno una forma più breve degli altri: nessuna riga «Leva principale», un solo paragrafo per profilo. Va bene se è una scelta voluta.
6. **Cap. 14, apertura dello script operativo.** Ripete quasi alla lettera la frase già citata all'inizio del capitolo («Oggi termina la fase che precede…»). Probabilmente è voluto, perché lo script deve essere autonomo: è segnalato solo per verifica.

## 4. Formato e requisiti KDP

I requisiti sono stati verificati sulle guide KDP aggiornate (pagina *Paperback Submission Guidelines*) e su fonti secondarie concordi.

| Voce | Valore |
|---|---|
| Formato | **8 × 10 in** (203,2 × 254 mm): era richiesto dal cliente nell'ordine ed è un formato standard KDP per il paperback |
| Rilegatura | Paperback (brossura). **KDP non offre l'8 × 10 in copertina rigida**: per l'hardcover servirebbero 7 × 10 o 8,25 × 11 |
| Interno | Bianco e nero, **senza abbondanza (no bleed)**: nessun elemento arriva al bordo |
| Carta consigliata | Bianca: i fondini grigi dei box rendono meglio e il tono è più adatto a un testo medico |
| Pagine | **226** (x + 216) |
| Margine interno (gutter) | 25 mm. Il minimo KDP per 151–300 pagine è 12,7 mm (0,5 in); il margine regge anche fino a 828 pagine |
| Margini esterno / alto / basso | 36 / 27 / 27 mm. Il minimo KDP è 6,4 mm (0,25 in) |
| Font | Tutti incorporati (16 varianti, sottoinsiemi), verificato con `pdffonts` |
| Colori | Solo scala di grigi (DeviceGray). Fondini all'8–4,5% di nero; filetti e testo al 100% |

**Copertina (domanda del cliente: «serve anche la copertina?»).** Sì, KDP la richiede: è un PDF separato, unico, con quarta, dorso e prima di copertina, più 3,2 mm di abbondanza per lato. In alternativa si può usare Cover Creator di KDP. Con 226 pagine:

- **dorso**: 0,509 in (12,9 mm) su carta bianca, 0,565 in (14,4 mm) su carta crema;
- **file completo**: 16,759 × 10,25 in su carta bianca.

Il testo sul dorso è ammesso, perché il libro supera le 79 pagine. La copertina non fa parte di questo lavoro: si può preparare una volta confermato il titolo. Le misure del dorso vanno ricalcolate se cambia il numero di pagine.

## 5. Scelte di progetto grafico

- **Caratteri.**
  - *Source Serif 4* per il testo e i titoli, con le ottiche Text, Subhead e Display: autorevole, molto leggibile, con numeri «old style» nel testo corrente.
  - *Inter* per gli apparati operativi: etichette, box, script, testatine.
  
  Il serif accompagna la lettura, il sans segnala ciò che si consulta.
- **Corpo e gabbia.** Testo a 11 pt, giustezza di 140 mm (circa 70–75 battute per riga), giustificato con sillabazione italiana.
- **Aperture di capitolo.** Sempre su pagina dispari, con:
  - l'etichetta «CAPITOLO»;
  - il numero grande in Display Light;
  - un filetto;
  - il titolo;
  - l'epigrafe in corsivo con l'autore in maiuscoletto spaziato.
- **Dialoghi nel testo.** Corsivo rientrato, senza riquadro.
- **Script operativo.** Etichetta nera in negativo e battute su un fondino chiaro con un filetto nero verticale: si ritrovano a colpo d'occhio sfogliando il libro.
- **«Perché questo protocollo funziona».** Voci con un quadratino nero e il titoletto in sans.
- **Box DISC.** Riquadro con filetto nero. Per ogni profilo: lettera in negativo, nome, «Leva principale» e battuta con un filetto grigio. Il box si spezza solo tra un profilo e l'altro, ripete l'intestazione con «segue» e non comincia mai in fondo pagina senza almeno un profilo.
- **Protocollo in sintesi.** È pensato come una *scheda*:
  - comincia sempre in testa di pagina, con fondino grigio e filetto nero spesso;
  - le etichette (Quando applicarlo, Obiettivo, Cosa fare, Cosa verificare) stanno in una colonna a sinistra;
  - i passi sono numerati in cerchi neri.
  
  Se un box superasse la pagina, si spezzerebbe tra un campo e l'altro con «segue». Oggi nessuno lo fa.
- **Indici.**
  - *Indice* generale con capitoli e sezioni.
  - *Protocolli in sintesi*: indice di consultazione rapida con la pagina dello script e della scheda per ogni capitolo dal 6 al 16, pensato per l'uso in studio.
  
  Tutte le voci sono collegamenti cliccabili nel PDF.

## 6. Controllo di qualità eseguito

- **Campione.** È stato realizzato prima su un capitolo intero, il 6, che contiene apertura, testo, dialoghi, script, «Perché funziona», bibliografia, box DISC e box Protocollo (`output/campione-it.pdf`). Sono stati poi corretti:
  - il rientro della prima riga che spostava il numero di capitolo;
  - le voci bibliografiche fuse in un solo paragrafo;
  - un box Protocollo spezzato con un solo passo sulla pagina seguente;
  - l'apertura dei capitoli non su pagina dispari;
  - l'intestazione del box DISC isolata in fondo pagina;
  - «segue» sulla prima pagina del box.
- **Libro intero.** È stato renderizzato e ispezionato a doppie pagine.
- **Controlli automatici** (`tools/qa.py`, `tools/check_indice.py`):
  - integrità del testo: 0 differenze;
  - formato pagina;
  - font incorporati;
  - titoli isolati in fondo pagina: 0;
  - 116 voci d'indice verificate contro le pagine reali: 0 errori.
- **Vedove e orfane.** Il motore di impaginazione le impedisce. I titoli restano sempre agganciati al testo che segue.
- **Pagine corte segnalate (4).** Sono pp. 116, 129, 206 e 216 della numerazione PDF. In ognuna un box DISC, o uno dei suoi profili, passa interamente alla pagina successiva, lasciando bianco il fondo pagina. È il comportamento voluto: un profilo non viene mai spezzato e il box non apre in fondo pagina.

## 7. Altro

Il token API per la generazione di immagini fornito in chat **non è stato usato**: il progetto non richiede immagini. Dato che è stato condiviso in chiaro, consiglio di revocarlo e rigenerarlo.

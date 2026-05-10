# Fase 3 - Piano tecnico operativo per gli oggetti

## Obiettivo della fase

La Fase 3 serve a portare il dominio "oggetti" allo stesso livello minimo di maturita' gia' raggiunto per le magie:

- core Python riusabile
- backend applicativo coerente con `spelldeck/`
- compilazione PDF via servizi Python
- supporto GUI nel flusso principale
- test automatici

L'obiettivo non e' ancora rifinire tutta la UX, ma rendere gli oggetti una parte di prima classe del progetto.

## Stato di partenza

Attualmente il flusso oggetti esiste, ma e' ancora basato su un fork pragmatico del vecchio script magie:

- `generate_items.py` contiene logica di dominio, CLI e output mescolati
- usa ancora nomi e concetti del dominio magie (`SPELLS`, `get_spells`, `LEVEL_STRING`)
- carica `data/spells.json` all'avvio, anche se il dominio e' diverso
- ha lo stesso bug storico sul check di `args.filename`
- non ha test dedicati
- non ha ancora un backend riusabile equivalente a quello magie
- non e' integrato nella GUI

## Problemi principali da risolvere

### 1. Dominio dati poco pulito

I dataset oggetti oggi usano una forma ibrida:

- campi utili al rendering reale
- campi ereditati dalle magie ma poco significativi
- convenzioni testuali non del tutto uniformi

Campi attualmente osservati:

- `availability`
- `itemtype`
- `weight`
- `cost`
- `damage`
- `attunement`
- `damagetype`
- `overlay`
- `overlay_opacity`
- `text`

Più alcuni campi legacy o opzionali:

- `classes`
- `ritual`
- `material`

### 2. Flusso oggetti non separato dalla CLI

Come era successo per le magie prima del refactor, oggi la logica principale sta tutta nello script.

### 3. Mancanza di contratto applicativo per la GUI

La GUI non ha ancora un set chiaro di funzioni da chiamare per:

- caricare dataset oggetti
- filtrare o selezionare record
- generare `tex/items.tex`
- compilare `printable_items.pdf`
- gestire il caso speciale "9 copie dello stesso oggetto"

### 4. Caso speciale one-page non modellato bene

Il flusso "stampa 9 volte lo stesso oggetto" oggi passa da:

- `generate_single_item.sh`
- `tex/printable_onepage.tex`

Funziona, ma non e' ancora incapsulato come funzionalita' applicativa Python.

## Vincoli confermati

- dipendenze minime
- stack interamente Python
- GUI desktop `tkinter`
- nessuna modifica ai dataset dalla GUI
- LaTeX resta esplicito come prerequisito tecnico

## Obiettivo architetturale

Gli oggetti dovrebbero convergere verso la stessa forma usata per le magie.

### Core backend desiderato

Nuovi moduli suggeriti:

- `spelldeck/items_data.py`
- `spelldeck/items_filters.py`
- `spelldeck/items_tex.py`
- `spelldeck/items_service.py`

Ed estensione mirata di:

- `spelldeck/compiler.py`

### GUI desiderata

La GUI attuale dovrebbe evolvere da "solo magie" a "magie + oggetti".

Due opzioni semplici:

1. una finestra con selettore modalita'
2. due tab: `Magie` e `Oggetti`

Raccomandazione:

usare due tab. E' semplice in `tkinter`, mantiene separati i flussi e riduce i branch logici dentro un singolo form.

## Strategia di implementazione

### Step 1. Stabilizzare lo script oggetti esistente

Prima di estrarre il core conviene fare pulizia minima concettuale:

- correggere il check su `args.filename`
- eliminare il caricamento iniziale di `data/spells.json`
- smettere di usare nomi fuorvianti dove la correzione e' locale e sicura

Non serve ancora riscrivere tutto, ma il punto di partenza deve essere meno ambiguo.

### Step 2. Definire il contratto dati oggetti

Serve fissare almeno uno schema operativo minimo.

Schema base suggerito:

- `availability`: stringa
- `itemtype`: stringa
- `weight`: stringa
- `cost`: stringa
- `damage`: stringa
- `attunement`: boolean
- `damagetype`: stringa opzionale
- `overlay`: stringa opzionale
- `overlay_opacity`: numero opzionale
- `text`: stringa

Da valutare:

- se `classes`, `ritual`, `material` vadano tollerati come legacy oppure esclusi dal nuovo contratto

Raccomandazione:

nel backend nuovo vanno tollerati come campi extra, ma non devono piu' guidare la logica applicativa.

### Step 3. Estrarre il core oggetti

#### `spelldeck/items_data.py`

Responsabilita':

- path default dataset oggetti
- caricamento JSON
- validazione minima record

Funzioni candidate:

- `load_items(path)`
- `validate_item_record(name, data)`

#### `spelldeck/items_filters.py`

Responsabilita':

- selezione per nome
- eventuali filtri semplici futuri

Nota:

Per gli oggetti oggi non serve copiare il modello filtri delle magie. Meglio partire minimali.

Funzioni candidate:

- `filter_items(items, names=None)`

#### `spelldeck/items_tex.py`

Responsabilita':

- troncamento testo
- conversione markdown-lite
- costruzione header oggetto
- rendering TeX della singola carta
- rendering TeX di una lista di carte

Funzioni candidate:

- `truncate_string(...)`
- `markdown_lite_to_latex(...)`
- `build_item_header(...)`
- `render_item_tex(...)`
- `render_items_tex(...)`

#### `spelldeck/items_service.py`

Responsabilita':

- orchestrazione applicativa del flusso oggetti
- generazione `tex/items.tex`
- conteggio elementi e troncamenti
- supporto selezione singolo oggetto

Funzioni candidate:

- `generate_items_tex(...)`
- `generate_items_tex_file(...)`

### Step 4. Estendere il compilatore

`spelldeck/compiler.py` va esteso per coprire anche gli oggetti.

Funzioni candidate:

- `compile_spell_pdf(...)`
- `compile_items_pdf(...)`
- `compile_single_page_items_pdf(...)`

Comandi da incapsulare:

```bash
latexmk -xelatex -cd tex/items_cards.tex tex/printable_items.tex
```

e per il caso one-page:

```bash
latexmk -xelatex -cd tex/items_cards.tex tex/printable_onepage.tex
```

Nota importante:

Il vecchio script usa `-f` su `latexmk`. Prima di replicarlo nel backend conviene verificare se e' davvero necessario o se e' solo una tolleranza legacy. Se non serve, meglio evitarlo.

### Step 5. Integrare gli oggetti nella GUI

La GUI dovrebbe offrire almeno:

- scelta modalita' `Magie` / `Oggetti`
- selezione dataset JSON oggetti
- filtro opzionale per nome oggetto
- pulsanti:
  - `Genera TeX`
  - `Genera PDF`
  - `Genera PDF 9 copie`

Per il primo MVP oggetti non servono:

- editor testo
- selezione immagini dalla GUI
- preview embedded

### Step 6. Valutare il destino di `generate_single_item.sh`

Dopo che il backend Python avra' coperto il caso "9 copie", lo script shell dovrebbe essere:

- rimosso
oppure
- mantenuto come wrapper legacy sottilissimo

Raccomandazione:

tenerlo solo se serve compatibilita' manuale; altrimenti il backend Python deve diventare la sorgente principale di verita'.

## Test previsti

### `tests/test_items_data.py`

Coprire:

- caricamento dataset oggetti
- dataset custom
- errore su file mancante
- errore su JSON invalido
- validazione campi minimi

### `tests/test_items_tex.py`

Coprire:

- troncamento testo
- conversione markdown-lite
- rendering con overlay
- rendering senza overlay
- header corretto

### `tests/test_items_service.py`

Coprire:

- generazione `tex/items.tex`
- selezione per nome
- conteggio oggetti
- conteggio troncamenti

### `tests/test_compiler.py`

Estendere per coprire:

- comando compilazione oggetti
- comando compilazione one-page
- successo/fallimento per il ramo oggetti

## GUI: impatto sul design attuale

La GUI attuale e' piccola e si presta a una estensione controllata.

Raccomandazione di design:

- introdurre un `ttk.Notebook`
- spostare l'attuale form magie in un pannello dedicato
- creare un pannello oggetti separato

Vantaggi:

- separazione chiara dei campi
- nessuna logica condizionale invasiva su una singola vista
- estensione piu' semplice dei log e delle azioni

## Ordine di priorita'

### P0

- pulizia minima di `generate_items.py`
- schema dati operativo per oggetti
- estrazione backend oggetti
- test core

### P1

- estensione `compiler.py`
- supporto GUI oggetti base
- supporto caso "9 copie"

### P2

- rifinitura UX
- eventuale normalizzazione piu' forte dei dati legacy
- eventuale dismissione script shell legacy

## Deliverable della Fase 3

Al termine della fase dovremmo avere:

1. backend Python riusabile per gli oggetti
2. test automatici sul dominio oggetti
3. compilazione PDF oggetti via servizi Python
4. supporto GUI per il flusso oggetti
5. copertura del caso "9 copie dello stesso oggetto"

## Criteri di completamento

La fase puo' considerarsi chiusa quando:

- e' possibile generare `tex/items.tex` senza passare da `generate_items.py`
- e' possibile compilare il PDF oggetti dal backend Python
- e' possibile usare gli oggetti dalla GUI
- esiste supporto GUI o backend per il caso one-page
- la suite test copre il nuovo dominio in modo minimo ma reale

## Rischi da tenere sotto controllo

- trascinarsi troppa semantica legacy del dominio magie dentro gli oggetti
- fissare troppo presto uno schema dati che i dataset reali non rispettano
- complicare la GUI con troppe differenze tra i due flussi
- mantenere in parallelo troppi entrypoint legacy senza una gerarchia chiara

## Prossimo passo consigliato

La prossima esecuzione dovrebbe partire da:

1. refactor minimo e stabilizzazione di `generate_items.py`
2. estrazione di `items_data.py`, `items_tex.py` e `items_service.py`
3. primi test

Solo dopo conviene toccare la GUI.

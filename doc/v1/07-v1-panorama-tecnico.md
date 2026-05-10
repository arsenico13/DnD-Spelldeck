# V1 - Panorama tecnico del progetto

## Scopo del documento

Questo documento descrive il progetto allo stato attuale della v1.

Non sostituisce i documenti storici presenti in `doc/`, che restano validi come
traccia dell'evoluzione del lavoro. Questo file ha invece lo scopo di offrire
una vista unica, consolidata e coerente di:

- struttura del repository
- architettura attuale
- flussi applicativi
- backend Python
- GUI
- compilazione LaTeX
- test
- punti legacy ancora presenti

## Obiettivo del progetto

Il progetto genera carte stampabili di D&D partendo da dataset JSON e template
LaTeX.

La v1 supporta due domini:

- magie
- oggetti

Per entrambi esistono:

- un flusso CLI
- un backend Python riusabile
- generazione del TeX

Per entrambi esiste anche la compilazione PDF tramite backend Python.

Per la GUI desktop `tkinter` esiste supporto per:

- magie
- oggetti
- caso speciale one-page per 9 copie dello stesso oggetto

## Stack tecnico

### Linguaggi e runtime

- Python 3
- LaTeX / XeLaTeX

### Librerie Python

- solo libreria standard
- `tkinter` per la GUI

### Tool esterni

- `latexmk`
- `xelatex`

### Filosofia tecnica della v1

- dipendenze minime
- stack interamente Python lato applicazione
- logica applicativa separata dalla CLI
- GUI costruita sopra servizi Python, non sopra shell script

## Struttura del repository

### Entry point principali

- `generate.py`
  CLI per la generazione delle carte magia
- `generate_items.py`
  CLI per la generazione delle carte oggetto
- `gui/app.py`
  entrypoint della GUI desktop

### Package applicativo

La logica riusabile vive in `spelldeck/`.

Moduli lato magie:

- `spelldeck/spells_data.py`
- `spelldeck/spells_filters.py`
- `spelldeck/spells_tex.py`
- `spelldeck/spells_service.py`

Moduli lato oggetti:

- `spelldeck/items_data.py`
- `spelldeck/items_filters.py`
- `spelldeck/items_tex.py`
- `spelldeck/items_service.py`

Moduli condivisi:

- `spelldeck/compiler.py`
- `spelldeck/io_utils.py`

### GUI

La GUI vive in `gui/`.

File principali:

- `gui/app.py`
- `gui/main_window.py`

### Template LaTeX

I template principali vivono in `tex/`.

Per le magie:

- `tex/cards.tex`
- `tex/printable.tex`

Per gli oggetti:

- `tex/items_cards.tex`
- `tex/printable_items.tex`
- `tex/printable_onepage.tex`

### Dataset

I dataset JSON vivono in `data/`.

Dataset di default attuali:

- magie: `data/spells.json`
- oggetti: `data/items_test.json`

Esistono anche altri dataset custom nel repository.

### Test

I test vivono in `tests/`.

Attualmente coprono:

- backend magie
- backend oggetti
- compilatore LaTeX

## Architettura applicativa

## 1. Layer dati

Responsabilita':

- caricare JSON
- validare struttura minima dei record
- definire i dataset di default

Moduli:

- `spells_data.py`
- `items_data.py`

### Magie

`load_spells(path=None)`:

- carica il dataset
- usa `data/spells.json` come default
- valida i campi richiesti

### Oggetti

`load_items(path=None)`:

- carica il dataset
- usa `data/items_test.json` come default
- valida un set minimo di campi richiesti

Nota importante:

nel dominio oggetti il backend e' tollerante verso campi extra legacy presenti
nei dataset, ma la logica core si basa solo sui campi realmente utili al
rendering.

## 2. Layer filtri

Responsabilita':

- trasformare input utente in criteri di selezione
- filtrare i record in memoria

### Magie

`spells_filters.py` gestisce:

- filtro per classe
- filtro per livello
- filtro per scuola
- filtro per nome
- parsing dei range di livelli

### Oggetti

`items_filters.py` gestisce:

- filtro per nome
- filtro opzionale per classi legacy

Per gli oggetti si e' scelta volutamente una modellazione piu' semplice rispetto
alle magie.

## 3. Layer rendering TeX

Responsabilita':

- costruire il testo TeX da una lista di record
- gestire troncamenti
- convertire eventuale formattazione

### Magie

`spells_tex.py` si occupa di:

- troncamento testo
- costruzione header
- costruzione source/page
- rendering della singola carta
- rendering di un set di carte

### Oggetti

`items_tex.py` si occupa di:

- troncamento testo
- conversione markdown-lite -> LaTeX
- costruzione header oggetto
- gestione overlay opzionale
- rendering della singola carta
- rendering di un set di carte

### Markdown-lite oggetti

Nel dominio oggetti e' supportata una mini-sintassi:

- `**testo**` -> grassetto
- `__testo__` -> corsivo
- doppia newline -> paragrafo
- newline singola -> a capo forzato

## 4. Layer servizi applicativi

Responsabilita':

- orchestrare caricamento dati, filtri e rendering
- scrivere i file TeX finali
- esporre risultati strutturati alla GUI o alla CLI

### Magie

`spells_service.py` espone:

- `parse_filter_string(...)`
- `generate_spells_tex(...)`
- `generate_spells_tex_file(...)`

Restituisce:

- path del file generato
- numero magie selezionate
- numero testi troncati

### Oggetti

`items_service.py` espone:

- `generate_items_tex(...)`
- `generate_items_tex_file(...)`

Restituisce:

- path del file generato
- numero oggetti selezionati
- numero testi troncati
- nomi degli oggetti troncati

## 5. Layer compilazione

Responsabilita':

- verificare la disponibilita' di `latexmk`
- costruire il comando corretto
- lanciare la compilazione LaTeX
- restituire un risultato strutturato

Modulo:

- `spelldeck/compiler.py`

Funzioni principali:

- `ensure_latexmk_available()`
- `build_latexmk_command(...)`
- `compile_spell_pdf(...)`
- `compile_items_pdf(...)`
- `compile_single_page_items_pdf(...)`

Il risultato della compilazione e' un `LatexCompileResult` con:

- comando eseguito
- codice di ritorno
- stdout
- stderr
- path del PDF atteso

## CLI attuale

## `generate.py`

`generate.py` e' un wrapper sottile sul backend magie.

Fa solo:

1. parsing argomenti
2. selezione dataset
3. invocazione del core
4. stampa del TeX su stdout
5. stampa statistiche su stderr

## `generate_items.py`

`generate_items.py` e' stato alleggerito rispetto alla versione legacy, ma resta
un wrapper CLI di compatibilita' per gli oggetti.

Fa:

1. parsing argomenti
2. selezione dataset
3. invocazione del core oggetti
4. stampa del TeX su stdout
5. stampa statistiche su stderr

## GUI desktop

La GUI e' implementata in `tkinter` e vive in `gui/main_window.py`.

### Entry point

- `python3 gui/app.py`
- `python3 -m gui.app`

### Struttura

La finestra principale contiene un `ttk.Notebook` con due tab:

- `Magie`
- `Oggetti`

Entrambe derivano da una base comune:

- `BaseGeneratorTab`

Questa base centralizza:

- selezione dataset
- log testuale
- area stato
- gestione errori

### Tab Magie

Campi:

- dataset JSON
- classi
- livelli
- scuole
- nomi

Azioni:

- `Genera TeX`
- `Genera PDF`

### Tab Oggetti

Campi:

- dataset JSON
- nomi
- classi legacy

Azioni:

- `Genera TeX`
- `Genera PDF`
- `Genera PDF 9 copie`

### Modalita' operativa della GUI

La GUI usa chiamate sincrone ai servizi Python e alla compilazione.

Questa scelta e' deliberata nella v1:

- riduce la complessita'
- evita threading o code UI premature
- mantiene il flusso semplice da debuggare

Tradeoff:

durante compilazioni lunghe la finestra puo' apparire temporaneamente bloccata.

## Flussi supportati

## Flusso magie

1. caricare dataset magie
2. applicare i filtri
3. generare `tex/spells.tex`
4. compilare `tex/printable.pdf`

Supportato da:

- CLI
- backend Python
- GUI

## Flusso oggetti standard

1. caricare dataset oggetti
2. filtrare per nome o classi legacy
3. generare `tex/items.tex`
4. compilare `tex/printable_items.pdf`

Supportato da:

- CLI
- backend Python
- GUI

## Flusso oggetti one-page

1. generare `tex/items.tex`
2. compilare `tex/printable_onepage.pdf`

Se il file generato contiene una sola card, `printable_onepage.tex` ripete la
pagina 9 volte nel layout 3x3.

Supportato da:

- backend Python
- GUI
- script legacy ancora presente

## Testing

La suite test usa `unittest`.

### Copertura attuale

Magie:

- caricamento dati
- filtri
- rendering TeX
- servizi

Oggetti:

- caricamento dati
- rendering TeX
- servizi

Compilazione:

- costruzione comandi `latexmk`
- success path con mock
- failure path con mock
- ramo magie
- ramo oggetti standard
- ramo oggetti one-page

### Comando principale

```bash
python3 -m unittest discover
```

## Requisiti e dipendenze

Requisiti per il funzionamento completo:

- Python 3
- `latexmk`
- XeLaTeX

Requisiti per i test:

- Python 3

La GUI non introduce dipendenze esterne aggiuntive oltre a `tkinter`, che fa
parte della libreria standard Python negli ambienti target abituali.

## Stato dei componenti legacy

I seguenti elementi esistono ancora per compatibilita' o storico:

- `generate_items.py`
- `generate_single_item.sh`
- `Makefile`

Situazione attuale:

- `generate_items.py` e' ancora usabile, ma la logica vera e' nel backend
- `generate_single_item.sh` e' legacy: il caso one-page e' gia' coperto da backend e GUI
- il `Makefile` non e' ancora stato riallineato completamente all'architettura v1

## Limiti attuali della v1

- la GUI non include preview embedded del PDF
- la GUI non modifica i dataset JSON
- il dominio oggetti accetta ancora alcuni campi legacy nei dataset
- il `Makefile` e alcuni script shell non sono ancora stati consolidati
- la GUI usa operazioni sincrone

## Cosa definisce la v1

La v1 puo' essere descritta cosi':

- progetto Python + LaTeX funzionante end-to-end
- backend separato dalla CLI
- GUI desktop minima ma completa per i casi d'uso principali
- supporto reale a magie e oggetti
- copertura test concreta sui moduli principali

In pratica la v1 e' il momento in cui il repository smette di essere solo una
raccolta di script e diventa una piccola applicazione strutturata, pur restando
leggera e pragmatica.

# Stato attuale del progetto

## Scopo

Il progetto genera carte stampabili di D&D partendo da dataset JSON e template LaTeX.

Ad oggi il repository supporta:

- generazione carte magia tramite pipeline Python + LaTeX
- generazione carte oggetto tramite script separati
- GUI desktop Python minima per il flusso magie
- backend Python riusabile anche per il dominio oggetti

La parte piu' stabilizzata e preparata per evoluzioni future e' attualmente il dominio "magie".

## Requisiti operativi

Per usare il progetto nello stato attuale servono:

- Python 3
- `latexmk`
- XeLaTeX

I test unitari non richiedono LaTeX.
La generazione del PDF invece si'.

## Struttura del repository

### Root

- `README.md`: documentazione storica e note d'uso originali
- `generate.py`: entrypoint CLI per la generazione delle carte magia
- `generate_items.py`: generatore oggetti, ancora non rifattorizzato come il flusso magie
- `generate_single_item.sh`: utility per stampare 9 copie dello stesso oggetto
- `Makefile`: file legacy, non ancora riallineato alla struttura introdotta nelle Fasi 1 e 2

### Dati

- `data/`: dataset JSON usati come sorgente
- `data/spells.json`: dataset default per le magie
- altri file in `data/`: dataset alternativi, traduzioni e set custom

### Template e output TeX

- `tex/cards.tex`: template LaTeX delle magie
- `tex/items_cards.tex`: template LaTeX degli oggetti
- `tex/printable.tex`: impaginazione stampabile delle magie
- `tex/printable_items.tex`: impaginazione stampabile degli oggetti
- `tex/printable_onepage.tex`: layout per 9 copie della stessa carta oggetto
- `tex/spells.tex`: file generato per il contenuto magie
- `tex/items.tex`: file generato per il contenuto oggetti
- `tex/printable.pdf`: PDF finale delle magie, generato dopo compilazione

### Core Python riusabile

Il package applicativo attuale e':

- `spelldeck/`

Contenuto rilevante:

- `spelldeck/spells_data.py`
- `spelldeck/spells_filters.py`
- `spelldeck/spells_tex.py`
- `spelldeck/spells_service.py`
- `spelldeck/items_data.py`
- `spelldeck/items_filters.py`
- `spelldeck/items_tex.py`
- `spelldeck/items_service.py`
- `spelldeck/compiler.py`
- `spelldeck/io_utils.py`

Questi moduli rappresentano il backend riusabile del progetto. Il ramo magie e'
piu' completo, mentre il ramo oggetti e' in fase di convergenza verso la stessa
architettura.

### GUI

La GUI desktop introdotta in Fase 2 si trova in:

- `gui/app.py`
- `gui/main_window.py`

La GUI e' realizzata con `tkinter` e al momento copre solo il dominio magie.

### Test

- `tests/`

Contenuto attuale:

- `tests/test_spells_data.py`
- `tests/test_spells_filters.py`
- `tests/test_spells_tex.py`
- `tests/test_spells_service.py`
- `tests/test_items_data.py`
- `tests/test_items_tex.py`
- `tests/test_items_service.py`
- `tests/test_compiler.py`

## Organizzazione del codice magie

### `generate.py`

`generate.py` e' un wrapper CLI sottile.

Responsabilita':

- parsing argomenti
- caricamento dataset magia di default o custom
- applicazione filtri
- stampa del TeX generato su stdout
- stampa statistiche di troncamento su stderr

La logica di dominio vera e propria vive nei moduli `spelldeck/`.

### `spelldeck/spells_data.py`

Responsabilita':

- definizione del path default del dataset magie
- caricamento JSON
- validazione minima dei record

Funzioni principali:

- `load_spells(path=None)`
- `validate_spell_record(name, data)`

### `spelldeck/spells_filters.py`

Responsabilita':

- parsing dei livelli
- normalizzazione filtri testuali
- filtraggio delle magie

Funzioni principali:

- `parse_levels(levels)`
- `filter_spells(spells, classes=None, levels=None, schools=None, names=None)`

### `spelldeck/spells_tex.py`

Responsabilita':

- troncamento testo
- costruzione header magia
- composizione source/page
- rendering TeX della singola carta
- rendering TeX di una lista di carte

Funzioni principali:

- `truncate_string(...)`
- `build_spell_header(...)`
- `build_spell_source(...)`
- `build_spell_text(...)`
- `render_spell_tex(...)`
- `render_spells_tex(...)`

### `spelldeck/spells_service.py`

Responsabilita':

- orchestrazione applicativa del flusso magie
- parsing filtri da stringhe GUI-friendly
- generazione del contenuto TeX
- scrittura diretta di `tex/spells.tex`

Funzioni principali:

- `parse_filter_string(raw_value)`
- `generate_spells_tex(...)`
- `generate_spells_tex_file(...)`

### `spelldeck/compiler.py`

Responsabilita':

- verifica disponibilita' di `latexmk`
- costruzione del comando di compilazione
- lancio di `latexmk`
- ritorno di un risultato strutturato

Funzioni principali:

- `ensure_latexmk_available()`
- `build_latexmk_command(...)`
- `compile_spell_pdf(...)`

### `spelldeck/items_data.py`

Responsabilita':

- path default del dataset oggetti
- caricamento JSON
- validazione minima dei record

Funzioni principali:

- `load_items(path=None)`
- `validate_item_record(name, data)`

### `spelldeck/items_filters.py`

Responsabilita':

- filtro per nome
- filtro legacy per classi, quando presente nel dataset

Funzioni principali:

- `filter_items(items, names=None, classes=None)`

### `spelldeck/items_tex.py`

Responsabilita':

- troncamento testo
- conversione markdown-lite in LaTeX
- costruzione header oggetto
- rendering TeX della singola carta
- rendering TeX di una lista di carte

Funzioni principali:

- `truncate_string(...)`
- `markdown_lite_to_latex(...)`
- `build_item_header(...)`
- `build_item_text(...)`
- `render_item_tex(...)`
- `render_items_tex(...)`

### `spelldeck/items_service.py`

Responsabilita':

- orchestrazione applicativa del flusso oggetti
- generazione del contenuto TeX
- scrittura diretta di `tex/items.tex`
- conteggio elementi troncati

Funzioni principali:

- `generate_items_tex(...)`
- `generate_items_tex_file(...)`

### `spelldeck/io_utils.py`

Responsabilita':

- utility minima di scrittura file testuale

Funzioni principali:

- `write_text_file(path, content)`

## Flusso attuale delle magie

Il flusso applicativo attuale per le magie e':

1. caricare il dataset JSON
2. applicare i filtri
3. generare il contenuto TeX
4. scriverlo in `tex/spells.tex`
5. compilare con LaTeX tramite `latexmk`
6. produrre `tex/printable.pdf`

Questo flusso e' disponibile in due modi:

- CLI
- GUI desktop `tkinter`

## Utilizzo da CLI

### Generare tutte le magie

```bash
python3 generate.py > tex/spells.tex
```

### Generare magie filtrate per classe

```bash
python3 generate.py -c bard -c fighter > tex/spells.tex
```

### Generare magie filtrate per livello

```bash
python3 generate.py -l 0 -l 2 -l 5-7 > tex/spells.tex
```

### Generare una magia specifica

```bash
python3 generate.py -n Alarm > tex/spells.tex
```

### Usare un dataset custom

```bash
python3 generate.py -f data/spells_ita.json > tex/spells.tex
```

### Compilare il PDF finale

```bash
latexmk -xelatex -cd tex/cards.tex tex/printable.tex
```

### Esempio completo

```bash
python3 generate.py -f data/spells_ita.json -c wizard -l 1-3 > tex/spells.tex
latexmk -xelatex -cd tex/cards.tex tex/printable.tex
```

## Utilizzo del backend Python

Il backend introdotto nelle Fasi 1 e 2 puo' essere usato anche direttamente da Python.

### Generare `tex/spells.tex`

```bash
python3 -c 'from spelldeck.spells_service import generate_spells_tex_file; print(generate_spells_tex_file(names=["Alarm"]))'
```

### Compilare il PDF

```bash
python3 -c 'from spelldeck.compiler import compile_spell_pdf; r = compile_spell_pdf(); print(r.returncode, r.output_pdf)'
```

## Utilizzo della GUI

### Avvio

Dal root del repository:

```bash
python3 gui/app.py
```

In alternativa funziona anche:

```bash
python3 -m gui.app
```

### Funzioni disponibili nella GUI

- selezione del dataset JSON magie
- uso del dataset default se il campo resta quello precompilato
- filtro per classi
- filtro per livelli
- filtro per scuole
- filtro per nomi
- generazione del solo file TeX
- generazione del PDF completo
- visualizzazione log ed esito finale

### Convenzioni nei campi filtro GUI

Nei campi testuali si usano valori separati da virgola.

Esempi:

- `wizard, bard`
- `1, 2, 5-7`
- `abjuration, evocation`
- `Alarm, Augury`

### Flusso tipico GUI

1. avviare `python3 gui/app.py`
2. selezionare o confermare il dataset JSON
3. inserire eventuali filtri
4. cliccare `Genera TeX` oppure `Genera PDF`
5. leggere stato e log nella parte bassa della finestra

## Stato del dominio oggetti

Il dominio oggetti e' ancora in stato pre-refactor.

Significa che:

- esiste una pipeline funzionante
- esistono template e dataset dedicati
- ora esiste anche un primo core Python dedicato in `spelldeck/items_*`
- `generate_items.py` e' stato alleggerito, ma resta ancora un wrapper CLI legacy
- non esiste ancora supporto GUI per gli oggetti
- non e' ancora stato esteso il compilatore Python al flusso oggetti

## Test automatici

## Requisiti

Per eseguire i test basta Python 3.
Non serve LaTeX per i test unitari attuali.

## Comando principale

Dal root del repository:

```bash
python3 -m unittest discover
```

Questo comando esegue tutti i test presenti nella directory `tests/`.

## Comandi mirati

Eseguire solo i test del caricamento dati:

```bash
python3 -m unittest tests.test_spells_data
```

Eseguire solo i test dei filtri:

```bash
python3 -m unittest tests.test_spells_filters
```

Eseguire solo i test del rendering TeX:

```bash
python3 -m unittest tests.test_spells_tex
```

Eseguire solo i test del servizio magie:

```bash
python3 -m unittest tests.test_spells_service
```

Eseguire solo i test del dominio oggetti:

```bash
python3 -m unittest tests.test_items_data tests.test_items_tex tests.test_items_service
```

Eseguire solo i test della compilazione:

```bash
python3 -m unittest tests.test_compiler
```

## Cosa coprono i test

### `tests/test_spells_data.py`

Copre:

- caricamento dataset di default
- caricamento dataset custom
- errore su file mancante
- errore su JSON invalido

### `tests/test_spells_filters.py`

Copre:

- nessun filtro
- filtro per classe
- filtro per scuola
- filtro per livello
- filtro per nome
- parsing livelli

### `tests/test_spells_tex.py`

Copre:

- troncamento testo
- costruzione header
- costruzione source/page
- aggiunta del materiale nel testo
- rendering TeX della singola carta
- rendering TeX di piu' carte

### `tests/test_spells_service.py`

Copre:

- parsing dei filtri da stringa
- generazione di `spells.tex`
- uso dataset custom
- conteggio magie e troncamenti

### `tests/test_compiler.py`

Copre:

- costruzione del comando `latexmk`
- rilevamento di `latexmk`
- gestione di compilazione riuscita
- gestione di compilazione fallita
- errore se `latexmk` non e' presente

### `tests/test_items_data.py`

Copre:

- caricamento dataset oggetti di default
- caricamento dataset custom
- errore su file mancante
- errore su JSON invalido

### `tests/test_items_tex.py`

Copre:

- troncamento testo
- conversione markdown-lite
- costruzione header
- rendering TeX con e senza overlay

### `tests/test_items_service.py`

Copre:

- generazione di `items.tex`
- selezione per nome
- uso dataset custom
- conteggio oggetti e troncamenti

## Note sui commenti nel codice

I commenti sono stati aggiunti solo nei punti in cui servono davvero:

- compatibilita' con la firma storica dell'environment LaTeX
- compatibilita' della CLI con dataset custom
- mantenimento del comando storico `latexmk`

Il resto del codice punta a essere leggibile tramite struttura dei moduli e nomi di funzione.

## Stato di avanzamento

Completato:

- Fase 1 del refactor magie
- estrazione core Python riusabile
- backend Python per generazione e compilazione magie
- GUI desktop `tkinter` MVP per le magie
- primo refactor del dominio oggetti con backend e test di base
- nuova suite test

Non ancora fatto:

- supporto oggetti nella GUI
- compilazione PDF oggetti nel backend Python
- preview grafica embedded del PDF
- riallineamento del `Makefile`

## Punto di ingresso per il lavoro successivo

La base attuale e' pronta per:

1. rifinitura UX della GUI magie
2. estensione del backend e della GUI al dominio oggetti
3. eventuale aggiornamento del `Makefile` e della documentazione utente generale

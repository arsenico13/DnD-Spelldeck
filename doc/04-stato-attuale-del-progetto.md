# Stato attuale del progetto

## Scopo

Il progetto genera carte stampabili di D&D partendo da dataset JSON e template LaTeX.

Ad oggi il repository supporta:

- generazione carte magia tramite pipeline Python + LaTeX
- generazione carte oggetto tramite script separati

La parte piu' stabilizzata e preparata per la futura GUI e' attualmente il dominio "magie".

## Struttura del repository

### Root

- `README.md`: documentazione storica e note d'uso originali
- `generate.py`: entrypoint CLI per la generazione delle carte magia
- `generate_items.py`: generatore oggetti, ancora non rifattorizzato come il flusso magie
- `generate_single_item.sh`: utility per stampare 9 copie dello stesso oggetto
- `Makefile`: file legacy, non ancora aggiornato alla nuova organizzazione

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

### Core Python riusabile

La Fase 1 ha introdotto il package:

- `spelldeck/`

Contenuto attuale:

- `spelldeck/spells_data.py`
- `spelldeck/spells_filters.py`
- `spelldeck/spells_tex.py`
- `spelldeck/io_utils.py`

Questi moduli rappresentano il nuovo core riusabile per la pipeline magie.

### Test

- `tests/`

Contenuto attuale:

- `tests/test_spells_data.py`
- `tests/test_spells_filters.py`
- `tests/test_spells_tex.py`

## Organizzazione del codice magie

### `generate.py`

`generate.py` e' ora un wrapper CLI sottile.

Responsabilita':

- parsing argomenti
- caricamento dataset magia di default o custom
- applicazione filtri
- stampa del TeX generato su stdout
- stampa statistiche di troncamento su stderr

La logica di dominio non e' piu' concentrata qui.

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
- composizione sorgente/libro + pagina
- rendering TeX della singola carta
- rendering TeX di una lista di carte

Funzioni principali:

- `truncate_string(...)`
- `build_spell_header(...)`
- `build_spell_source(...)`
- `build_spell_text(...)`
- `render_spell_tex(...)`
- `render_spells_tex(...)`

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
5. compilare con LaTeX

Attualmente il passo 4 puo' essere fatto via redirect shell.
Il passo 5 resta esterno al core Python e continua a dipendere dai comandi LaTeX gia' in uso nel progetto.

## Esecuzione della CLI magie

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

### Usare un dataset custom

```bash
python3 generate.py -f data/spells_ita.json > tex/spells.tex
```

### Compilare il PDF finale

```bash
latexmk -xelatex -cd tex/cards.tex tex/printable.tex
```

## Stato del dominio oggetti

Il dominio oggetti e' ancora in stato pre-refactor.

Significa che:

- esiste una pipeline funzionante
- esistono template e dataset dedicati
- la logica e' ancora concentrata in `generate_items.py`
- non esiste ancora un core pulito equivalente a `spelldeck/` per gli oggetti

Questa parte non e' ancora il target della futura GUI MVP.

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

## Note sui commenti nel codice

I commenti sono stati aggiunti solo nei punti in cui servono davvero:

- compatibilita' con la firma storica dell'environment LaTeX
- compatibilita' della CLI con dataset custom

Il resto del codice punta a essere leggibile tramite struttura dei moduli e nomi di funzione.

## Stato di avanzamento

Completato:

- Fase 1 del refactor magie
- estrazione core Python riusabile
- nuova suite test

Non ancora fatto:

- servizio Python per compilazione LaTeX
- GUI desktop `tkinter`
- refactor del dominio oggetti

## Punto di ingresso per la Fase 2

La base attuale e' pronta per:

1. aggiungere un servizio Python che orchestri `latexmk`
2. costruire una GUI minima per il flusso magie
3. far usare alla GUI direttamente il core in `spelldeck/`

# Fase 1 - Piano tecnico operativo

## Obiettivo della fase

La Fase 1 serve a rendere il flusso "carte magia" abbastanza pulito e stabile da poter essere usato da una GUI Python senza dipendere direttamente dagli script CLI attuali.

Il risultato atteso non e' ancora una GUI, ma un piccolo core applicativo Python riusabile, testato e leggibile.

## Scope della Fase 1

Incluso:

- refactor minimo del dominio magie
- correzione delle fragilita' note negli script esistenti
- estrazione di funzioni/moduli richiamabili dalla futura GUI
- aggiunta di test automatici
- aggiunta di commenti solo dove il codice non e' immediato

Escluso:

- supporto GUI
- refactor completo del dominio oggetti
- editor dataset
- redesign dei template LaTeX

## Principi guida

- cambiare il meno possibile nel comportamento funzionale
- separare il dominio dalla CLI
- evitare over-engineering
- mantenere dipendenze a zero o quasi
- scrivere test prima o insieme ai punti piu' delicati del refactor

## Problemi da risolvere in questa fase

### 1. Fragilita' sul caricamento file input

Va corretto il controllo di `args.filename` negli script esistenti, evitando condizioni basate su stringa vuota quando il valore reale puo' essere `None`.

### 2. Logica core mescolata alla CLI

Oggi:

- il parsing argomenti
- il caricamento dati
- il filtraggio
- la generazione TeX
- la stampa su stdout

sono concentrati nello stesso script.

Per la GUI serve separarli.

### 3. Assenza di un contratto Python stabile

La GUI avra' bisogno di chiamare funzioni del tipo:

- carica dataset
- filtra magie
- genera TeX
- salva output

Oggi questo contratto non esiste in modo esplicito.

### 4. Test insufficienti per il futuro refactor

I test esistenti coprono alcune funzioni di `generate.py`, ma non rappresentano ancora un vero punto di appoggio per un refactor strutturale.

## Strategia di refactor

Il refactor consigliato e' incrementale, non distruttivo.

### Step 1. Introdurre un package Python minimo

Creare una directory applicativa, ad esempio:

- `spelldeck/`

Contenuto iniziale suggerito:

- `spelldeck/__init__.py`
- `spelldeck/spells_data.py`
- `spelldeck/spells_filters.py`
- `spelldeck/spells_tex.py`
- `spelldeck/io_utils.py`

Obiettivo:

spostare dentro moduli chiari la logica oggi dispersa in `generate.py`.

### Step 2. Estrarre il caricamento dati

Introdurre una funzione esplicita, ad esempio:

- `load_spells(path: str | None = None) -> dict`

Responsabilita':

- usare `data/spells.json` come default
- permettere path alternativo
- fallire con errore chiaro se il file non esiste o il JSON e' invalido

Nota:

questa e' una funzione che la GUI potra' chiamare direttamente.

### Step 3. Estrarre e isolare il filtraggio

Introdurre una funzione del tipo:

- `get_spells(spells, classes=None, levels=None, schools=None, names=None)`

oppure, meglio ancora:

- `filter_spells(...)`

Obiettivo:

- mantenere il comportamento attuale
- non dipendere da stato globale
- rendere testabile il filtraggio su input espliciti

### Step 4. Estrarre la generazione TeX

Introdurre funzioni del tipo:

- `truncate_text(text, max_len=MAX_TEXT_LENGTH)`
- `render_spell_tex(name, spell_data) -> str`
- `render_spells_tex(spells) -> str`

Obiettivo:

- non stampare direttamente
- ritornare stringhe
- lasciare alla CLI o alla GUI la scelta se scrivere su file, stdout o altro

### Step 5. Ridurre lo script CLI a wrapper sottile

`generate.py` dovrebbe diventare soprattutto:

1. parsing argomenti
2. chiamata al core
3. scrittura su stdout
4. log finale su stderr

Questo permette di preservare la compatibilita' con il flusso attuale senza impedire l'evoluzione dell'applicazione.

## Struttura tecnica consigliata

Una proposta concreta e' questa.

### Modulo `spelldeck/spells_data.py`

Responsabilita':

- path default del dataset magie
- caricamento JSON
- eventuale validazione minima dei campi attesi

Funzioni candidate:

- `load_spells(path=None)`
- `validate_spell_record(name, data)`

### Modulo `spelldeck/spells_filters.py`

Responsabilita':

- parsing livelli
- normalizzazione input filtri
- filtraggio magie

Funzioni candidate:

- `parse_levels(level_specs)`
- `filter_spells(spells, classes=None, levels=None, schools=None, names=None)`

### Modulo `spelldeck/spells_tex.py`

Responsabilita':

- truncation
- formattazione header
- rendering TeX di una carta
- rendering TeX di una lista di carte

Funzioni candidate:

- `truncate_string(text, max_len=MAX_TEXT_LENGTH)`
- `build_spell_header(level, school, ritual)`
- `render_spell_tex(name, spell_data)`
- `render_spells_tex(spell_items)`

### Modulo `spelldeck/io_utils.py`

Responsabilita':

- scrittura file testuale
- utility semplici di I/O riusabili

Funzioni candidate:

- `write_text_file(path, content)`

## Contratto minimo per la futura GUI

Alla fine della Fase 1 la GUI dovrebbe poter fare qualcosa di questo tipo:

1. chiamare `load_spells(path)`
2. chiamare `parse_levels(...)`
3. chiamare `filter_spells(...)`
4. chiamare `render_spells_tex(...)`
5. scrivere il contenuto risultante in `tex/spells.tex`
6. in una fase successiva, lanciare la compilazione LaTeX

Questo e' il contratto applicativo minimo che dobbiamo costruire.

## Strategia test

I test non devono restare un accessorio: in questa fase sono parte del deliverable.

### Obiettivi test

- proteggere il comportamento attuale del dominio magie
- coprire il refactor senza cambiare il risultato finale
- garantire funzioni richiamabili dalla futura GUI

### Aree di test minime

#### 1. Caricamento dati

Testare:

- caricamento dataset di default
- caricamento dataset alternativo
- errore su file inesistente
- errore su JSON invalido

#### 2. Parsing livelli

Testare:

- livello singolo
- piu' livelli
- range
- mix di range e livelli singoli

#### 3. Filtraggio magie

Testare:

- nessun filtro
- filtro per classe
- filtro per scuola
- filtro per livello
- filtro per nome
- combinazioni di filtri

#### 4. Troncamento testo

Testare:

- testo corto invariato
- testo lungo troncato correttamente
- risultato entro lunghezza massima

#### 5. Rendering TeX

Testare:

- presenza di `\\begin{spell}`
- header atteso
- campi fondamentali presenti nel testo generato
- gestione del campo `material`
- gestione del `source_page`

### Organizzazione consigliata dei test

Invece di tenere tutto in `tests.py`, e' preferibile iniziare una struttura piu' chiara, ad esempio:

- `tests/test_spells_data.py`
- `tests/test_spells_filters.py`
- `tests/test_spells_tex.py`

Se pero' vuoi minimizzare al massimo il refactor del layout, si puo' anche partire da un unico file test piu' ordinato e poi spezzarlo nella fase successiva.

Raccomandazione:

creare da subito una directory `tests/`.

## Commenti nel codice

I commenti vanno aggiunti con criterio, non per descrivere l'ovvio.

### Quando commentare

- blocchi con logica non immediata
- compatibilita' con il formato TeX esistente
- scelte deliberate per preservare il comportamento storico
- edge case non evidenti

### Quando non commentare

- assegnazioni banali
- passaggi lineari gia' chiari dal nome di funzione e variabili
- boilerplate

### Regola pratica

Se un commento puo' essere sostituito da un nome migliore di funzione o variabile, meglio migliorare il nome.

## Deliverable della Fase 1

Al termine della fase dovremmo avere:

1. un package Python minimo riusabile per il dominio magie
2. `generate.py` ancora funzionante come CLI
3. test automatici per il core magie
4. codice piu' leggibile, con commenti mirati dove servono
5. base pronta per il piano della Fase 2, cioe' compilazione e GUI MVP

## Sequenza operativa consigliata

1. creare package `spelldeck/`
2. spostare funzioni pure fuori da `generate.py`
3. aggiornare `generate.py` a wrapper
4. creare struttura `tests/`
5. migrare e ampliare i test
6. eseguire test
7. aggiornare la documentazione tecnica se emergono aggiustamenti

## Criteri di completamento

La Fase 1 puo' considerarsi chiusa quando:

- il flusso CLI magie continua a funzionare
- la logica core non dipende da stato globale
- i test coprono i casi essenziali
- esiste un set di funzioni Python che una GUI puo' chiamare direttamente
- il codice e' abbastanza chiaro da estenderlo senza introdurre altro debito inutile

## Nota sulla fase successiva

La compilazione LaTeX vera e propria puo' restare fuori da questa fase oppure entrare come primo tassello della Fase 2.

Scelta consigliata:

tenere in Fase 1 solo il core di generazione TeX, e portare l'orchestrazione `latexmk` nel passo successivo insieme alla GUI. In questo modo il refactor resta piccolo, testabile e focalizzato.

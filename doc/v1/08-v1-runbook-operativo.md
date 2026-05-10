# V1 - Runbook operativo e manutenzione

## Scopo del documento

Questo documento raccoglie le procedure operative principali per usare,
verificare e manutenere il progetto nella sua v1.

L'obiettivo e' pratico:

- come avviare i flussi
- come fare debug
- come aggiungere nuovi dataset
- come validare una modifica
- quali comandi usare per i test
- dove guardare quando qualcosa non funziona

## Prerequisiti

Per usare il progetto in modo completo servono:

- Python 3
- `latexmk`
- XeLaTeX

Per i soli test unitari basta Python 3.

## Directory di riferimento

Cartelle principali:

- `data/`
- `tex/`
- `spelldeck/`
- `gui/`
- `tests/`
- `doc/`

File di ingresso principali:

- `generate.py`
- `generate_items.py`
- `gui/app.py`

## Avvio rapido

## GUI

Dal root del repository:

```bash
python3 gui/app.py
```

Alternativa:

```bash
python3 -m gui.app
```

La GUI espone due tab:

- `Magie`
- `Oggetti`

## CLI magie

Generare `tex/spells.tex`:

```bash
python3 generate.py > tex/spells.tex
```

Generare un sottoinsieme:

```bash
python3 generate.py -c wizard -l 1-3 -n Alarm > tex/spells.tex
```

Compilare il PDF:

```bash
latexmk -xelatex -cd tex/cards.tex tex/printable.tex
```

## CLI oggetti

Generare `tex/items.tex`:

```bash
python3 generate_items.py -f data/items_test.json > tex/items.tex
```

Generare un singolo oggetto:

```bash
python3 generate_items.py -f data/items_test.json -n "Pozione di Cura" > tex/items.tex
```

Compilare il PDF standard:

```bash
latexmk -xelatex -cd tex/items_cards.tex tex/printable_items.tex
```

Compilare il PDF one-page:

```bash
latexmk -xelatex -cd tex/items_cards.tex tex/printable_onepage.tex
```

## Uso del backend Python

## Magie

Generare TeX:

```bash
python3 -c 'from spelldeck.spells_service import generate_spells_tex_file; print(generate_spells_tex_file(names=["Alarm"]))'
```

Compilare PDF:

```bash
python3 -c 'from spelldeck.compiler import compile_spell_pdf; r = compile_spell_pdf(); print(r.returncode, r.output_pdf)'
```

## Oggetti

Generare TeX:

```bash
python3 -c 'from spelldeck.items_service import generate_items_tex_file; print(generate_items_tex_file(names=["Pozione di Cura"]))'
```

Compilare PDF standard:

```bash
python3 -c 'from spelldeck.compiler import compile_items_pdf; r = compile_items_pdf(); print(r.returncode, r.output_pdf)'
```

Compilare PDF one-page:

```bash
python3 -c 'from spelldeck.compiler import compile_single_page_items_pdf; r = compile_single_page_items_pdf(); print(r.returncode, r.output_pdf)'
```

## Flussi di lavoro consigliati

## 1. Verifica veloce di un dataset magie

1. generare `tex/spells.tex` con `generate.py` oppure `spells_service`
2. controllare che il TeX sia stato prodotto
3. compilare `printable.pdf`
4. verificare log e PDF finale

## 2. Verifica veloce di un dataset oggetti

1. generare `tex/items.tex` con `generate_items.py` oppure `items_service`
2. controllare che overlay e testo siano presenti nel TeX
3. compilare `printable_items.pdf`
4. per il caso singolo, compilare anche `printable_onepage.pdf`

## 3. Verifica di una modifica al backend

1. eseguire la suite test
2. generare almeno un caso reale per magie
3. generare almeno un caso reale per oggetti
4. compilare almeno un PDF reale

## Aggiungere un nuovo dataset

## Dove metterlo

Salvare il file JSON in `data/`.

Per oggetti custom singoli o tematizzati, usare una convenzione coerente con i
dataset gia' presenti.

## Nuovo dataset magie

Ogni record deve essere keyed by spell name e includere almeno i campi attesi da
`spelldeck/spells_data.py`, tra cui:

- `classes`
- `components`
- `duration`
- `level`
- `material`
- `range`
- `ritual`
- `school`
- `source`
- `source_page`
- `text`
- `time`

Validazione rapida:

```bash
python3 -c 'from spelldeck.spells_data import load_spells; load_spells("data/NOME_FILE.json"); print("ok")'
```

## Nuovo dataset oggetti

Ogni record deve essere keyed by item name e includere almeno i campi minimi
attesi da `spelldeck/items_data.py`:

- `availability`
- `itemtype`
- `weight`
- `cost`
- `damage`
- `attunement`
- `text`

Campi opzionali ma supportati:

- `damagetype`
- `overlay`
- `overlay_opacity`
- `classes`

Validazione rapida:

```bash
python3 -c 'from spelldeck.items_data import load_items; load_items("data/NOME_FILE.json"); print("ok")'
```

## Convenzioni pratiche per i dataset oggetti

- `overlay` deve puntare a un path valido relativo al contesto TeX, di norma `images/...`
- `overlay_opacity` deve essere un valore numerico compatibile con LaTeX/TikZ
- `text` puo' usare la mini-sintassi markdown-lite
- il filtro `classi legacy` e' tollerato ma non centrale nella modellazione v1

## Come validare una modifica

## Modifica solo Python backend

Eseguire:

```bash
python3 -m unittest discover
```

Poi fare almeno:

```bash
python3 -c 'from spelldeck.spells_service import generate_spells_tex_file; print(generate_spells_tex_file(names=["Alarm"]))'
python3 -c 'from spelldeck.items_service import generate_items_tex_file; print(generate_items_tex_file(names=["Pozione di Cura"]))'
```

## Modifica alla compilazione LaTeX

Eseguire:

```bash
python3 -m unittest tests.test_compiler
```

Poi provare almeno:

```bash
python3 -c 'from spelldeck.compiler import compile_spell_pdf; r = compile_spell_pdf(); print(r.returncode, r.output_pdf)'
python3 -c 'from spelldeck.compiler import compile_items_pdf; r = compile_items_pdf(); print(r.returncode, r.output_pdf)'
```

Se il cambiamento riguarda il one-page:

```bash
python3 -c 'from spelldeck.compiler import compile_single_page_items_pdf; r = compile_single_page_items_pdf(); print(r.returncode, r.output_pdf)'
```

## Modifica alla GUI

Eseguire:

```bash
python3 gui/app.py
```

Verificare almeno:

- apertura della finestra
- accesso ai tab `Magie` e `Oggetti`
- generazione TeX da entrambi i tab
- compilazione PDF da entrambi i tab
- compilazione `9 copie` dal tab oggetti

## Test

## Suite completa

```bash
python3 -m unittest discover
```

## Solo backend magie

```bash
python3 -m unittest tests.test_spells_data tests.test_spells_filters tests.test_spells_tex tests.test_spells_service
```

## Solo backend oggetti

```bash
python3 -m unittest tests.test_items_data tests.test_items_tex tests.test_items_service
```

## Solo compilatore

```bash
python3 -m unittest tests.test_compiler
```

## Check di compilazione Python

Utile per intercettare errori banali di sintassi o import:

```bash
python3 -m compileall gui spelldeck tests
```

## Debug

## 1. La GUI non parte

Controllare:

- di essere nel root del repository
- di usare `python3 gui/app.py` oppure `python3 -m gui.app`
- eventuali errori di import

Comando utile:

```bash
python3 -c 'import gui.app; import gui.main_window; print("imports ok")'
```

## 2. `latexmk` non trovato

Sintomo tipico:

- errore sollevato da `ensure_latexmk_available()`

Controllare:

```bash
which latexmk
```

## 3. Il TeX viene generato ma il PDF fallisce

Controllare:

- stdout/stderr restituiti da `LatexCompileResult`
- file `.log` sotto `tex/`
- correttezza dei path immagini per gli oggetti
- compatibilita' del font/ambiente XeLaTeX

File utili:

- `tex/cards.log`
- `tex/items_cards.log`
- `tex/printable.log`
- `tex/printable_items.log`
- `tex/printable_onepage.log`

## 4. Un dataset non viene caricato

Controllare:

- JSON valido
- campi obbligatori presenti
- encoding corretto
- path giusto

Debug rapido:

```bash
python3 -c 'from spelldeck.spells_data import load_spells; print(load_spells("data/NOME_FILE.json").keys())'
python3 -c 'from spelldeck.items_data import load_items; print(load_items("data/NOME_FILE.json").keys())'
```

## 5. Gli oggetti mostrano testo o overlay strani

Controllare:

- sintassi markdown-lite
- path `overlay`
- valore `overlay_opacity`
- contenuto del file generato `tex/items.tex`

Comando utile:

```bash
python3 generate_items.py -f data/items_test.json -n "Pozione di Cura" | sed -n '1,80p'
```

## 6. Un test passa ma il PDF reale fallisce

Questo e' normale quando il problema e' nel layer LaTeX e non nel backend
Python puro. In quel caso serve una prova reale di compilazione, non solo i mock.

## File di output da conoscere

Magie:

- `tex/spells.tex`
- `tex/printable.pdf`

Oggetti:

- `tex/items.tex`
- `tex/printable_items.pdf`
- `tex/printable_onepage.pdf`

## Pulizia file temporanei

Se serve pulire la directory `tex/` dai file di build:

```bash
rm -f tex/*.aux tex/*.log tex/*.xdv tex/*.out tex/*.pdf tex/*.fls tex/*.fdb_latexmk
```

Usare questo comando con consapevolezza: rimuove anche i PDF gia' generati.

## Componenti legacy

Componenti ancora presenti ma non centrali nella v1:

- `generate_single_item.sh`
- `Makefile`

Uso consigliato:

- preferire backend Python e GUI
- mantenere gli script legacy solo come supporto o riferimento storico

## Procedura consigliata prima di chiudere una modifica

Checklist minima:

1. `python3 -m unittest discover`
2. `python3 -m compileall gui spelldeck tests`
3. generazione TeX magie reale
4. generazione TeX oggetti reale
5. almeno una compilazione PDF reale nel dominio toccato
6. se hai toccato la GUI, avvio manuale della finestra

## Quando aggiornare la documentazione

Aggiornare almeno:

- `README.md` se cambia il flusso utente
- `doc/07-v1-panorama-tecnico.md` se cambia l'architettura v1 consolidata
- questo runbook se cambiano procedure operative, debug o validazione

# Analisi tecnica iniziale

## Scopo del progetto

Il repository genera carte stampabili di D&D partendo da dati JSON e template LaTeX.
Le due linee funzionali oggi presenti sono:

- carte magia
- carte oggetto

Il flusso generale e':

1. lettura dataset JSON
2. generazione file `.tex`
3. compilazione LaTeX in PDF
4. impaginazione finale per la stampa

## Mappa del progetto

- `generate.py`: generatore originale per le magie
- `generate_items.py`: generatore per gli oggetti, nato come fork pragmatico di `generate.py`
- `generate_single_item.sh`: utility per stampare 9 copie dello stesso oggetto
- `tests.py`: test unitari per la pipeline magie
- `tex/cards.tex`: template LaTeX delle magie
- `tex/items_cards.tex`: template LaTeX degli oggetti
- `tex/printable.tex`: impaginazione 3x3 delle magie
- `tex/printable_items.tex`: impaginazione 3x3 degli oggetti
- `tex/printable_onepage.tex`: caso speciale per ripetere una sola carta oggetto 9 volte
- `data/`: dataset JSON per magie e oggetti

## Flusso magie

`generate.py`:

- carica `data/spells.json` di default
- filtra per classe, livello, scuola e nome
- tronca i testi oltre una soglia prefissata
- emette blocchi LaTeX `spell` da includere in `tex/spells.tex`

Punti positivi:

- pipeline chiara
- filtri semplici ma utili
- test automatici di base gia' presenti

## Flusso oggetti

`generate_items.py`:

- genera `tex/items.tex`
- usa un dataset JSON con campi specifici per gli oggetti
- supporta overlay immagine e opacita'
- converte una mini-sintassi tipo markdown in LaTeX

Funzionalita' aggiuntive gia' presenti:

- `**grassetto**`
- `__corsivo__`
- doppio newline come paragrafo
- newline singolo come a capo forzato

## Stato architetturale

La base e' funzionante, ma il ramo "oggetti" mostra diversi segnali di crescita per copia e adattamento:

- `generate_items.py` mantiene nomi e concetti delle magie anche dove non sono piu' corretti
- ci sono variabili e funzioni semanticamente sbagliate, ad esempio `SPELLS` e `get_spells`
- e' rimasto codice morto o non piu' rilevante, come `LEVEL_STRING`
- i template LaTeX funzionano, ma alcuni nomi interni non descrivono bene i dati che mostrano

Questo non blocca l'uso del tool, ma rende piu' fragile ogni estensione futura.

## Problemi tecnici emersi

### 1. Check fragile su `args.filename`

Sia in `generate.py` sia in `generate_items.py` compare:

`if args.filename != "":`

Il controllo e' debole, perche' quando il parametro non viene passato il valore atteso e' `None`, non stringa vuota. Il check corretto deve verificare che il valore sia davvero presente.

### 2. Fork non ripulito della pipeline oggetti

`generate_items.py`:

- apre `data/spells.json` in avvio anche se il dominio e' "oggetti"
- conserva filtri class/level/school che non risultano centrali nel modello dati oggetti
- riusa termini "spell" dove sarebbe meglio usare termini neutrali o specifici

### 3. Script shell con passaggi inutili

`generate_single_item.sh` esegue due volte `generate_items.py`, una delle quali senza impatto reale sulla build finale.

### 4. Makefile incompleto

Il `Makefile`:

- copre solo il caso magie
- ha un target `cleaup` con typo
- non rappresenta piu' l'intero workflow del repo

### 5. Copertura test insufficiente

I test presenti coprono solo `generate.py`.
Mancano test per:

- generazione oggetti
- conversione markdown-lite
- gestione overlay
- dataset oggetto reali

## Incoerenze nei dati

I JSON degli oggetti non sembrano seguire uno schema forte e uniforme.

Esempi osservati:

- campi ereditati dalle magie ma poco significativi per gli oggetti: `classes`, `ritual`, `material`
- `weight` usato anche per contenere metadati misti come `750g | s002`
- `itemtype` a volte descrittivo, a volte abbreviato o poco normalizzato
- testi con convenzioni miste: newline reali, `\r\n`, separatori testuali come `|`

Il parser oggi e' permissivo, ma non c'e' una vera normalizzazione del dato.

## Template LaTeX

### Magie

`tex/cards.tex` e' semplice e coerente con il modello dati delle magie.

### Oggetti

`tex/items_cards.tex` supporta bene overlay e opacita', ma ha rumore semantico interno:

- campi e macro con nomi ereditati dal modello magie
- associazioni non immediatamente intuitive tra dato mostrato ed etichetta visuale

Il risultato visivo puo' essere corretto, ma la manutenzione e' meno chiara del necessario.

## Valutazione complessiva

Il progetto ha una buona base operativa per uso personale o semi-artigianale:

- pipeline end-to-end corta
- dataset modificabili facilmente
- output orientato alla stampa gia' funzionante

Il debito tecnico e' concentrato soprattutto in:

- separazione insufficiente tra dominio magie e dominio oggetti
- schema dati debole per gli oggetti
- assenza di una interfaccia applicativa stabile da cui costruire una GUI

## Direzione consigliata

Prima di aggiungere la GUI conviene consolidare uno strato applicativo Python riusabile, in modo che l'interfaccia grafica non dipenda da script CLI fragili o da dettagli LaTeX sparsi.

In pratica:

1. stabilizzare generatori e input
2. definire schema dati e API interne
3. introdurre test sui casi principali
4. costruire la GUI sopra funzioni/moduli, non sopra script shell

## Domande aperte

- la GUI dovra' essere solo locale desktop o anche esportabile come web app locale?
- il target principale e' uso personale o condivisione ad altri utenti non tecnici?
- i dataset dovranno essere modificabili dalla GUI oppure solo selezionabili?
- la compilazione LaTeX deve restare un requisito esplicito oppure va incapsulata del tutto dentro l'app?

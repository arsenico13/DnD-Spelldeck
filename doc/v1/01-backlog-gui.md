# Backlog tecnico iniziale

## Obiettivo

Portare il repository da insieme di script CLI + LaTeX a tool Python con GUI locale che permetta di:

- generare carte magia
- generare carte oggetto
- scegliere dataset e filtri
- lanciare la compilazione
- ottenere rapidamente i PDF finali

## Assunzioni di partenza

- GUI desktop locale, non web
- stack interamente Python
- LaTeX resta il motore di rendering PDF
- l'utente finale ideale non deve conoscere comandi shell o struttura interna del repo

Queste assunzioni vanno confermate prima di entrare in implementazione della GUI.

## Priorita' P0

### P0.1 Stabilizzare gli script esistenti

Impatto: alto
Sforzo: basso

Attivita':

- correggere il check su `args.filename`
- eliminare codice palesemente morto o fuorviante nei punti critici
- rimuovere la doppia esecuzione inutile in `generate_single_item.sh`
- sistemare il `Makefile` o sostituirlo con entrypoint Python piu' chiari

Motivo:

La GUI non deve poggiare su comportamenti fragili o ambiguamente corretti.

### P0.2 Definire uno schema dati minimo per magie e oggetti

Impatto: alto
Sforzo: medio

Attivita':

- documentare campi obbligatori e opzionali
- chiarire i campi davvero usati dagli oggetti
- separare eventuali metadati misti oggi inseriti in `weight`
- definire convenzioni di testo e formattazione

Motivo:

Una GUI ha bisogno di sapere cosa mostrare, validare e salvare.

### P0.3 Estrarre una API Python interna riusabile

Impatto: molto alto
Sforzo: medio

Attivita':

- spostare la logica core fuori dagli script CLI
- introdurre funzioni/moduli del tipo:
  - carica dataset
  - valida record
  - genera tex
  - compila pdf
- lasciare gli script CLI come wrapper sottili

Motivo:

La GUI deve chiamare codice Python strutturato, non orchestrare shell script.

### P0.4 Aggiungere test minimi sulle pipeline reali

Impatto: alto
Sforzo: medio

Attivita':

- test su `generate_items`
- test sul parsing markdown-lite
- test su selezione dataset
- test su output TeX base

Motivo:

Prima di introdurre la GUI serve ridurre il rischio di regressioni.

## Priorita' P1

### P1.1 Scegliere il framework GUI Python

Impatto: alto
Sforzo: basso

Opzioni candidate:

- `tkinter`: semplice, integrato, poco dipendenze, look limitato
- `PySide6` / `PyQt`: migliore UX e struttura, piu' adatto se la GUI cresce
- `customtkinter`: compromesso rapido, ma meno solido come base a lungo termine

Raccomandazione iniziale:

Se la GUI deve restare utility locale semplice, `tkinter` basta.
Se vuoi un'app piu' rifinita e destinata a crescere, meglio `PySide6`.

### P1.2 Definire il flusso utente della GUI

Impatto: molto alto
Sforzo: medio

Flusso minimo consigliato:

1. scegliere modalita': magie o oggetti
2. scegliere dataset JSON
3. impostare filtri o selezione record
4. scegliere output e opzioni stampa
5. generare `.tex`
6. compilare PDF
7. aprire cartella o file risultante

Motivo:

Serve evitare di progettare la GUI direttamente sui dettagli del codice esistente.

### P1.3 Disegnare il modello applicativo della GUI

Impatto: alto
Sforzo: medio

Componenti suggeriti:

- `services/loader.py`
- `services/generator.py`
- `services/compiler.py`
- `models/spell.py`
- `models/item.py`
- `gui/` con viste e controller

Motivo:

Separare la logica di dominio dalla UI fin dall'inizio.

### P1.4 Gestione errori e prerequisiti

Impatto: alto
Sforzo: medio

Attivita':

- rilevare assenza di `latexmk` o `xelatex`
- mostrare errori leggibili all'utente
- separare errori dati, errori TeX, errori di ambiente

Motivo:

Per una GUI questo e' fondamentale quasi quanto la generazione stessa.

## Priorita' P2

### P2.1 Editor dataset dentro la GUI

Impatto: medio-alto
Sforzo: alto

Possibili scope:

- sola modifica testo dei record
- creazione nuovi oggetti
- gestione overlay immagine
- validazione live del JSON

Motivo:

Molto utile, ma e' meglio costruirlo dopo aver stabilizzato schema e servizi.

### P2.2 Preview parziale prima della compilazione completa

Impatto: medio
Sforzo: medio-alto

Opzioni:

- preview del TeX generato
- preview testuale dei campi
- preview PDF dopo compilazione

Motivo:

Aumenta l'usabilita', ma non e' il primo blocco da risolvere.

### P2.3 Preset di progetto o profili di esportazione

Impatto: medio
Sforzo: medio

Esempi:

- deck magie di una classe
- oggetti di una campagna
- stampa singolo oggetto 9 copie

Motivo:

Buona funzionalita' per evitare ripetizione di passaggi.

## Sequenza consigliata

### Fase 1

- stabilizzazione tecnica
- schema dati
- API interna
- test

### Fase 2

- scelta framework GUI
- definizione UX minima
- prototipo GUI per il solo flusso magie

### Fase 3

- estensione GUI agli oggetti
- supporto overlay
- gestione errori migliore

### Fase 4

- editing dati
- preset
- preview e rifiniture UX

## Primo MVP GUI consigliato

Il primo MVP dovrebbe fare poche cose ma bene:

- selezionare un file JSON
- scegliere se generare magie o oggetti
- applicare i filtri base nel caso magie
- lanciare generazione TeX e compilazione PDF
- mostrare esito e percorso dei file prodotti

Non includerei nel primo MVP:

- editor JSON completo
- drag and drop immagini avanzato
- preview sofisticata in tempo reale

## Decisioni da confermare

1. Vuoi una GUI desktop nativa oppure una mini web-app locale?
2. Preferisci dipendenze minime o un framework GUI piu' solido e moderno?
3. La GUI deve anche modificare i dataset o solo usarli?
4. Vuoi mantenere LaTeX come dipendenza visibile oppure nasconderla del tutto all'utente?
5. Il primo MVP deve coprire sia magie sia oggetti, oppure possiamo partire dalle magie e aggiungere gli oggetti subito dopo?

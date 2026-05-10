# V2 - Pianificazione GUI

## Scopo

Questo documento apre la pianificazione della v2.

Focus iniziale della v2:

- migliorare l'esperienza della GUI
- rendere piu' guidata la selezione dei filtri nel tab `Magie`
- aggiungere una preview esplicita dei record che verranno esportati

Le idee iniziali gia' emerse sono:

1. pulsante `Analizza` nel tab `Magie`
2. pulsante `Preview` nei tab `Magie` e `Oggetti`

## Stato di partenza

La GUI v1 e' funzionale ma ancora spartana.

### Tab `Magie`

Attualmente offre:

- scelta dataset
- campi testo per classi, livelli, scuole, nomi
- `Genera TeX`
- `Genera PDF`

Limite principale:

- i filtri sono solo manuali
- non c'e' alcun supporto guidato dai valori realmente presenti nel dataset
- non c'e' un'anteprima del set selezionato

### Tab `Oggetti`

Attualmente offre:

- scelta dataset
- filtro nome
- filtro classi legacy
- `Genera TeX`
- `Genera PDF`
- `Genera PDF 9 copie`

Limite principale:

- non c'e' una preview esplicita dei nomi che verranno esportati

## Obiettivi v2

### Obiettivo 1

Permettere all'utente di esplorare il dataset magie prima di impostare i filtri.

### Obiettivo 2

Ridurre gli errori di input nei campi `Classi` e `Scuole`.

### Obiettivo 3

Rendere sempre visibile, prima della generazione, quali record verranno usati.

## Feature 1 - Pulsante `Analizza` nel tab `Magie`

## Comportamento desiderato

Flusso previsto:

1. l'utente seleziona un dataset nel campo `Dataset magie`
2. preme `Analizza`
3. la GUI legge il dataset
4. estrae i valori reali di:
   - classi
   - scuole
5. rende questi valori selezionabili tramite UI dedicata

## Dati da estrarre

Dal dataset magie vanno ricavati almeno:

- insieme ordinato delle classi
- insieme ordinato delle scuole
- eventualmente conteggio totale magie

Possibile estensione utile:

- livelli disponibili nel dataset

Ma per ora non e' prioritaria, perche' il campo livelli ha gia' una sintassi
compatta e gestibile a mano.

## Proposte UI per scelta multipla

### Opzione A - `Listbox` multiselezione

Una `tk.Listbox(selectmode="extended")` per:

- classi
- scuole

Vantaggi:

- standard `tkinter`
- nessuna dipendenza extra
- selezione multipla nativa
- implementazione semplice

Svantaggi:

- UX un po' grezza
- meno intuitiva di widget piu' moderni

### Opzione B - Finestra popup di selezione

Pulsante tipo `Seleziona classi...` e `Seleziona scuole...` che apre un popup
con lista multiselezione.

Vantaggi:

- tiene il form principale piu' pulito
- scala meglio se i valori aumentano

Svantaggi:

- piu' codice
- piu' stato UI da gestire

### Opzione C - Checkbutton dinamici

Generare una lista di checkbox.

Vantaggi:

- molto esplicito

Svantaggi:

- poco scalabile
- rischia di occupare troppo spazio

## Raccomandazione

Per la v2 iniziale la scelta consigliata e':

- `Analizza`
- due `Listbox` multiselezione inline oppure dentro un riquadro dedicato

Motivo:

- semplice
- coerente con `tkinter`
- poca logica extra
- abbastanza chiaro per l'utente

## Impatto tecnico

Per implementare `Analizza` servono almeno:

### Backend

Nuova funzione lato magie, ad esempio in `spelldeck/spells_service.py` o
`spelldeck/spells_data.py`, che ritorni metadati del dataset:

- classi disponibili
- scuole disponibili
- numero record

Possibile firma:

- `analyze_spells_dataset(path) -> SpellDatasetAnalysis`

### GUI

Nel tab `Magie`:

- aggiungere pulsante `Analizza`
- aggiungere area UI per mostrare classi e scuole disponibili
- sincronizzare selezione widget -> filtro attivo

## Feature 2 - Pulsante `Preview`

## Comportamento desiderato

Prima della generazione TeX/PDF, l'utente puo' premere `Preview` e vedere:

- la lista dei nomi che verranno esportati
- il conteggio totale dei record selezionati

Questo vale per:

- tab `Magie`
- tab `Oggetti`

## Scopo reale della preview

La preview non deve mostrare il PDF.

Per la v2 iniziale la preview deve essere:

- testuale
- veloce
- basata sul backend gia' esistente

In pratica deve rispondere a:

- "quali record sto per esportare?"
- "quanti sono?"

## Proposte UI per `Preview`

### Opzione A - Popup con lista nomi

Premendo `Preview`, si apre una finestra modale con:

- titolo
- numero record
- lista scrollabile dei nomi

Vantaggi:

- semplice
- non sporca il layout principale
- riusabile per magie e oggetti

Svantaggi:

- aggiunge una finestra extra

### Opzione B - Riquadro preview nel tab

Nel tab c'e' una lista sempre presente che viene popolata quando si preme
`Preview`.

Vantaggi:

- tutto in una finestra

Svantaggi:

- aumenta la complessita' del layout
- sottrae spazio al log

## Raccomandazione

Per la v2 iniziale:

- `Preview` come popup modale con lista scrollabile

Motivo:

- piu' semplice da implementare
- meno invasivo sul layout
- adatto sia a magie che oggetti

## Impatto tecnico

### Backend magie

Riutilizzare il filtro gia' esistente per ottenere:

- lista nomi filtrati
- conteggio totale

Possibile funzione:

- `preview_spells(dataset_path, filters) -> SpellPreviewResult`

### Backend oggetti

Riutilizzare il filtro oggetti gia' esistente per ottenere:

- lista nomi filtrati
- conteggio totale

Possibile funzione:

- `preview_items(dataset_path, filters) -> ItemPreviewResult`

### GUI

In ogni tab:

- aggiungere bottone `Preview`
- aprire una `Toplevel` con lista nomi e conteggio

## Ordine di implementazione consigliato

### Step 1

Introdurre nel backend magie e oggetti funzioni di preview riusabili.

### Step 2

Aggiungere il pulsante `Preview` in entrambi i tab con popup modale.

### Step 3

Aggiungere `Analizza` nel tab `Magie`.

### Step 4

Sostituire o integrare i campi testo `Classi` e `Scuole` con selezione guidata
multi-valore.

## Perche' questo ordine

`Preview` ha:

- impatto backend basso
- UX immediata
- rischio contenuto

`Analizza` con selezione guidata invece tocca:

- struttura del layout
- stato della GUI
- sincronizzazione filtri

Quindi conviene fare prima la feature piu' semplice e a maggior valore immediato.

## Backlog v2 iniziale

### P0

- creare funzioni backend di preview per magie e oggetti
- aggiungere pulsante `Preview` nei due tab
- mostrare popup con nomi e conteggio

### P1

- creare funzione backend di analisi dataset magie
- aggiungere pulsante `Analizza`
- mostrare classi e scuole reali presenti nel dataset

### P2

- sostituire i campi testo `Classi` e `Scuole` con selezione guidata multipla
- rifinire il layout del tab `Magie`

## Test previsti

### Backend

Aggiungere test per:

- analisi dataset magie
- preview magie
- preview oggetti

### GUI

Anche senza test UI completi, fare almeno validazione manuale su:

- apertura popup preview
- correttezza nomi mostrati
- correttezza conteggio
- correttezza classi/scuole emerse da `Analizza`
- selezione multipla e trasferimento ai filtri attivi

## Rischi

- introdurre troppo stato UI nel tab `Magie`
- duplicare logica di filtro tra preview e generazione
- costruire un widget multi-selezione poco chiaro in `tkinter`

## Linea guida importante

Le nuove feature v2 della GUI devono appoggiarsi a funzioni backend dedicate.

Non bisogna implementare in `gui/main_window.py` logica di analisi o filtro
duplicata rispetto a `spelldeck/`.

## Prossimo passo suggerito

Il primo step esecutivo consigliato per la v2 e':

1. implementare la preview backend
2. aggiungere il bottone `Preview` in `Magie` e `Oggetti`
3. solo dopo lavorare su `Analizza`

# Decisioni GUI e piano MVP

## Decisioni confermate

In base alle risposte raccolte, il perimetro del lavoro e' questo:

- la GUI puo' essere desktop nativa oppure web locale, ma la scelta va fatta in base alla soluzione piu' semplice
- la priorita' e' minimizzare dipendenze e complessita'
- la GUI non deve creare o modificare dataset JSON
- il primo MVP puo' coprire solo le magie
- LaTeX puo' restare esplicito come prerequisito tecnico

## Confronto: GUI desktop nativa vs web app locale

### Opzione A: GUI desktop nativa Python

Soluzione piu' coerente con il vincolo di semplicita' e dipendenze minime.

Vantaggi:

- nessun server web da gestire
- nessun frontend separato
- stack interamente Python
- possibile usare `tkinter`, gia' incluso con Python nella maggior parte degli ambienti
- integrazione semplice con file picker, log, pulsanti e campi form

Svantaggi:

- aspetto visivo piu' spartano
- layout e UX meno moderni rispetto a una web app
- preview PDF integrata meno immediata se in futuro la vorrai dentro la GUI

### Opzione B: web app locale lanciata da Python

Possibile, ma meno adatta al vincolo "dipendenze minime e semplicita'".

Vantaggi:

- interfaccia piu' flessibile e gradevole
- facile estendere la UX in futuro
- eventuale preview e componenti piu' ricchi

Svantaggi:

- richiede server locale, routing e frontend HTML
- piu' moving parts
- piu' punti di failure
- per un tool personale di generazione file e' probabile overkill

## Raccomandazione

Per questo repository la scelta consigliata e':

- GUI desktop nativa Python
- framework iniziale: `tkinter`

Motivo:

`tkinter` e' la via piu' pragmatica per ottenere in fretta un MVP utile, con il minor costo architetturale possibile. Se in futuro il progetto richiedera' un'interfaccia piu' rifinita, si potra' rivalutare una migrazione verso `PySide6`, ma oggi non sembra giustificata.

## Obiettivo del primo MVP

Il primo MVP deve permettere a un utente di generare PDF di carte magia senza usare shell manuale.

Funzioni incluse:

1. selezione file dataset JSON
2. scelta dei filtri magie:
   - classe
   - livello
   - scuola
   - nome
3. generazione `tex/spells.tex`
4. compilazione PDF tramite LaTeX
5. visualizzazione esito operazione
6. visualizzazione del comando eseguito o del log principale

Funzioni escluse dal primo MVP:

- supporto oggetti
- modifica dei JSON
- preview grafica live della carta
- gestione immagini overlay
- preset avanzati

## Architettura consigliata

Prima della GUI serve una piccola riorganizzazione del codice Python.

### Strato core

Introdurre moduli riusabili, ad esempio:

- `spelldeck/data_loader.py`
- `spelldeck/spells.py`
- `spelldeck/tex_writer.py`
- `spelldeck/compiler.py`

Responsabilita' attese:

- caricamento file JSON
- validazione minima input
- filtro magie
- generazione stringa TeX
- scrittura file output
- invocazione compilazione LaTeX

### Strato CLI

Gli script esistenti possono restare, ma come wrapper sottili:

- parsing argomenti
- chiamata al core
- stampa output/log

### Strato GUI

Una struttura iniziale semplice potrebbe essere:

- `gui/app.py`
- `gui/main_window.py`
- `gui/forms/spells_form.py`

Responsabilita':

- selezione file
- raccolta parametri utente
- invocazione dei servizi Python
- visualizzazione stato e log

## Flusso utente MVP

1. apertura applicazione
2. scelta del file JSON delle magie
3. impostazione filtri opzionali
4. click su "Genera"
5. generazione del `.tex`
6. compilazione PDF
7. messaggio finale con percorso output o errore

## Backlog aggiornato

### P0

- correggere bug e fragilita' degli script attuali
- estrarre il core Python riusabile per le magie
- aggiungere test minimi sulle funzioni core

### P1

- creare GUI `tkinter` per il flusso magie
- integrare selezione file e filtri
- mostrare output e errori di compilazione

### P2

- estendere il core al dominio oggetti in modo pulito
- aggiungere secondo pannello o seconda modalita' GUI per gli oggetti

## Rischi da tenere sotto controllo

- forte accoppiamento attuale tra script e file path fissi
- scarsa separazione tra logica dominio e logica CLI
- errori LaTeX poco leggibili se non vengono normalizzati nella GUI
- dataset eterogenei che possono creare casi limite quando il filtro diventa UI-driven

## Prossimo passo consigliato

Il prossimo documento di planning dovrebbe essere un piano tecnico operativo per la Fase 1, cioe':

1. refactor minimo del core magie
2. test
3. contratto tra core e futura GUI

Solo dopo conviene iniziare a scrivere la GUI vera e propria.

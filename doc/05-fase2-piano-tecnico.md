# Fase 2 - Piano tecnico operativo

## Obiettivo della fase

La Fase 2 serve a trasformare il core magie introdotto in Fase 1 in un flusso applicativo completo, utilizzabile tramite una GUI desktop Python.

Il risultato atteso e':

- backend Python che generi `tex/spells.tex`
- backend Python che lanci la compilazione LaTeX
- MVP GUI `tkinter` per il dominio magie

## Scope della Fase 2

Incluso:

- servizio Python per generazione file TeX delle magie
- servizio Python per compilazione LaTeX via `latexmk`
- GUI desktop `tkinter` per selezione dataset e filtri magie
- visualizzazione esito operazioni e log essenziale
- test del nuovo backend

Escluso:

- supporto oggetti nella GUI
- editor JSON
- preview grafica embedded del PDF
- packaging/distribuzione desktop

## Vincoli confermati

- dipendenze minime
- stack interamente Python
- GUI desktop nativa, non web
- LaTeX requisito esplicito e non nascosto
- primo MVP limitato alle magie

## Architettura target

### Backend applicativo

Estendere `spelldeck/` con moduli dedicati al flusso applicativo:

- `spelldeck/spells_service.py`
- `spelldeck/compiler.py`

Responsabilita' del backend:

- caricare dataset
- applicare filtri
- generare contenuto TeX
- scrivere `tex/spells.tex`
- lanciare `latexmk`
- restituire risultati strutturati alla GUI

### GUI

Introdurre una directory:

- `gui/`

Contenuto iniziale suggerito:

- `gui/__init__.py`
- `gui/app.py`
- `gui/main_window.py`

La GUI non deve conoscere dettagli interni di LaTeX oltre a:

- prerequisito `latexmk`
- file output generato
- messaggi di errore

## Backend: contratto tecnico

### Servizio magie

Serve una funzione o un piccolo servizio che faccia:

1. caricare dataset
2. applicare filtri
3. generare TeX
4. scrivere file in `tex/spells.tex`
5. restituire statistiche utili

Output minimo utile:

- path file scritto
- numero magie selezionate
- numero testi troncati

### Servizio compilazione

Serve una funzione del tipo:

- `compile_spell_pdf(...)`

Responsabilita':

- verificare che `latexmk` sia disponibile
- lanciare il comando corretto
- raccogliere exit code, stdout e stderr
- restituire un risultato strutturato

## GUI MVP

### Funzioni incluse

- scegliere file dataset JSON
- lasciare il default del dataset standard
- compilare filtri testuali:
  - classe
  - livello
  - scuola
  - nome
- generare solo il file TeX
- generare TeX + compilare PDF
- mostrare log e percorso output

### Layout suggerito

Una singola finestra con:

1. campo dataset + pulsante "Sfoglia"
2. campi filtri
3. pulsanti azione:
   - "Genera TeX"
   - "Genera PDF"
4. area log testuale
5. etichetta stato finale

### Scelte UX

- niente wizard
- niente multi-finestra
- niente preview PDF dentro la GUI
- messaggi chiari ma sintetici
- errori mostrati senza stack trace grezzo, salvo log dettagliato

## Strategia implementativa

### Step 1. Backend generazione TeX

Introdurre un servizio che usi i moduli della Fase 1 e salvi direttamente `tex/spells.tex`.

### Step 2. Backend compilazione LaTeX

Introdurre un wrapper Python sopra:

```bash
latexmk -xelatex -cd tex/cards.tex tex/printable.tex
```

con gestione errori e cattura output.

### Step 3. GUI `tkinter`

Costruire un'interfaccia minimale che chiami il backend.

### Step 4. Test

Copertura minima:

- generazione `spells.tex`
- parsing filtri lato servizio
- compilazione LaTeX simulata con mock
- errore se `latexmk` non e' presente

## Test previsti

### `tests/test_spells_service.py`

Coprire:

- generazione file TeX
- numero magie selezionate
- conteggio troncamenti
- uso dataset custom

### `tests/test_compiler.py`

Coprire:

- comando `latexmk` atteso
- compilazione riuscita
- compilazione fallita
- `latexmk` assente

## Commenti nel codice

I commenti devono restare pochi e mirati.

In Fase 2 servono soprattutto in questi punti:

- costruzione del comando `latexmk`
- motivi per cui la GUI usa operazioni sincrone o semplificate
- compatibilita' con i percorsi storici del repository

## Deliverable della Fase 2

Al termine della fase dovremmo avere:

1. backend Python per generazione e compilazione magie
2. GUI `tkinter` avviabile localmente
3. test sul nuovo backend
4. base pronta per futura estensione agli oggetti

## Criteri di completamento

La Fase 2 puo' considerarsi chiusa quando:

- e' possibile generare `tex/spells.tex` dalla GUI
- e' possibile compilare il PDF finale dalla GUI
- il backend e' testato
- non sono state introdotte dipendenze extra non necessarie

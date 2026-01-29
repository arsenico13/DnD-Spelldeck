Il comando:

```bash
latexmk -f -xelatex -cd tex/cards.tex tex/printable.tex
```

esegue una compilazione di file LaTeX utilizzando lo strumento **`latexmk`**. Vediamo i dettagli di ogni parte del comando:

---

### **`latexmk`**
- **`latexmk`** è un programma che automatizza la compilazione di file LaTeX.
- Gestisce la rigenerazione automatica di file ausiliari (ad esempio, indici o riferimenti incrociati) e garantisce che la compilazione venga ripetuta finché il documento non è completamente aggiornato.

---

### **Opzioni del comando**
1. **`-f`**
   - Forza la compilazione anche in caso di errori durante il processo (non si ferma su errori non gravi).
   - È utile per verificare fino a che punto può essere completata la compilazione.

2. **`-xelatex`**
   - Specifica che il motore di compilazione deve essere **XeLaTeX**.
   - XeLaTeX supporta nativamente i font di sistema e Unicode, rendendolo ideale per documenti con caratteri speciali o font personalizzati (come `Mrs Eaves OT` usato in `cards.tex`).

3. **`-cd`**
   - Cambia la directory di lavoro in quella del file specificato prima di iniziare la compilazione.
   - In questo caso, garantisce che i file e le risorse (ad esempio, immagini di sfondo o PDF inclusi) vengano cercati nella directory `tex/`.

---

### **File specificati**
1. **`tex/cards.tex`**
   - Questo file contiene le definizioni delle carte (probabilmente con l'ambiente `spell` che abbiamo analizzato prima).
   - Verrà compilato per generare un documento PDF con singole carte.

2. **`tex/printable.tex`**
   - Questo file combina il PDF generato da `cards.tex` in un layout stampabile (griglia 3x3) usando il comando `\includepdf`.
   - Anche questo verrà compilato in un file PDF finale.

---

### **Flusso di lavoro**
1. Compila `cards.tex` con XeLaTeX:
   - Genera un PDF delle singole carte.
2. Compila `printable.tex` con XeLaTeX:
   - Utilizza il PDF delle carte (generato al passaggio precedente) per creare un layout compatto stampabile.

### **Risultato finale**
- Il comando produce due file PDF:
  1. **`cards.pdf`**: Contiene tutte le carte come pagine singole.
  2. **`printable.pdf`**: Contiene il layout compatto stampabile con griglie di 9 carte per pagina.

---

### **Vantaggi dell'uso di questo comando**
- Automazione completa: **`latexmk`** si occupa della compilazione in più passaggi.
- Gestione efficiente dei file ausiliari: Riconosce dipendenze come immagini, riferimenti incrociati, e include il PDF delle carte in `printable.tex`.
- Supporto per Unicode e font personalizzati grazie a XeLaTeX.

---

### **Nota sull'ambiente**
- È necessario che i pacchetti richiesti da `cards.tex` e `printable.tex` siano installati nel sistema Debian.
- È essenziale che il file `cards.pdf` venga generato correttamente prima che `printable.tex` possa includerlo. Questo avviene automaticamente grazie a **`latexmk`**.

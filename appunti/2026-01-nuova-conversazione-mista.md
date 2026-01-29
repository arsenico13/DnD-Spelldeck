Ho letto `cards.tex`: in pratica è un “template” per impaginare **carte formato card** (tipo carte da gioco / spell cards) con **uno sfondo a tutta pagina**, **titolo in alto**, **sorgente in basso**, e un layout a blocchi per i campi (Casting time, Range, Components, Duration). Il contenuto vero e proprio delle carte non è in questo file: viene importato da un altro file chiamato `spells.tex` (o `spells` senza estensione).

Di seguito ti spiego cosa fa, sezione per sezione, e soprattutto *dove mettere le mani* per modificarlo.

---

## 1) Impostazioni base e dimensioni della carta

```tex
\documentclass{article}
...
\usepackage[paperheight=8.89cm,paperwidth=6.35cm,margin=0.6cm,top=22mm,bottom=10mm,headheight=1cm]{geometry}
```

* Usa la classe `article`, ma poi con `geometry` imposta una **pagina piccola**:

  * **paperwidth=6.35cm** e **paperheight=8.89cm** = circa **2.5" x 3.5"**, cioè molto vicino al formato *poker card*.
* `margin=0.6cm` imposta margini piccoli (poi però vengono ulteriormente “specializzati” con `top=22mm` e `bottom=10mm`).
* `headheight=1cm` serve a dare spazio all’header gestito da `fancyhdr`.

Se vuoi cambiare formato carta (più grande/piccola), il punto principale è qui: `paperwidth` e `paperheight`.

---

## 2) Sfondo a tutta carta

```tex
\usepackage{background}

\backgroundsetup{
    contents={\includegraphics[width=\paperwidth,height=\paperheight]{images/background}}
}
```

Questa parte disegna **una immagine di sfondo** su ogni pagina/carta.

* L’immagine attesa è `images/background` (senza estensione). LaTeX cercherà un file tipo:

  * `images/background.pdf` oppure `.png` oppure `.jpg` (dipende dal motore e da cosa trova).
* Viene scalata **esattamente** a `\paperwidth` x `\paperheight`.

Se vuoi cambiare lo sfondo: sostituisci quel file, oppure cambia il path.

---

## 3) Font: solo se compili con XeLaTeX

```tex
\usepackage{ifxetex}
\ifxetex
\usepackage{fontspec}
\setmainfont{MrsEavesRoman}
\fi
```

* Se compili con **XeLaTeX**, usa `fontspec` e imposta il font principale a `MrsEavesRoman`.
* Se compili con **pdfLaTeX**, questa parte viene ignorata e userà i font standard di LaTeX.

Se vuoi essere sicuro di vedere quel font, devi compilare con `xelatex` e avere il font installato sul sistema.

---

## 4) Colori e stile generale

```tex
\definecolor{headercolor}{RGB}{88,23,13}
\definecolor{linecolor}{RGB}{201,173,106}

\sloppy
\setlength{\headsep}{3mm}
\setlength{\parindent}{0pt}
```

* `headercolor` è il colore usato per titolo/etichette.
* `linecolor` è definito ma **in questo file non viene usato** (probabilmente in una versione precedente o in `spells.tex`).
* `\parindent` a 0 rende i paragrafi “a blocco” senza rientro.

---

## 5) Header e footer (titolo sopra, source sotto)

```tex
\usepackage{fancyhdr}
\pagestyle{fancy}

\chead{\scshape\scriptsize\spellheader\\[-1.8mm]\Large\color{headercolor}\mbox{\spelltitle}}
\cfoot{\if\relax\spellsource\relax\else\scriptsize\spellsource\fi}
```

* In alto al centro (`\chead`) stampa:

  1. `\spellheader` in piccolo maiuscoletto
  2. a capo, il `\spelltitle` grande e colorato
* In basso al centro (`\cfoot`) stampa `\spellsource` **solo se non è vuoto**.

Questi tre campi (`\spellheader`, `\spelltitle`, `\spellsource`) non sono “globali”: vengono impostati carta per carta dal tuo environment `spell` (vedi sotto).

---

## 6) Il cuore del template: l’environment `spell`

Questa è la parte più importante:

```tex
\newenvironment{spell}[7]{
    \def\spelltitle{#1}
    \def\spellheader{#2}
    \def\castrange{#3}
    \def\casttime{#4}
    \def\duration{#5}
    \def\components{#6}
    \def\spellsource{#7}
    ...
}{ 
    ...
    \newpage
}
```

Vuol dire: ogni carta si scrive così (in `spells.tex`):

```tex
\begin{spell}{Titolo}{Header}{Range}{Casting time}{Duration}{Components}{Source}
  Qui va la descrizione lunga dell’effetto, testo libero, paragrafi, ecc.
\end{spell}
```

### Layout interno della carta

Dentro l’environment, impagina così:

* apre un `minipage` alto **5cm**:

  ```tex
  \begin{minipage}[t][5cm][t]{\textwidth}
  ```

  Questo “costringe” l’area contenuti ad essere alta 5 cm; se il testo è troppo, può andare brutto (sbordare o comprimersi). È una scelta deliberata per tenere le carte uniformi.

* poi fa una griglia 2x2 con i campi:

  * Casting time | Range
  * Components  | Duration

* poi:

  * `\headrule` disegna una riga orizzontale (di `fancyhdr`).
  * passa a `\footnotesize` per il corpo testo.

* alla fine chiude e fa `\newpage`: **ogni spell = una pagina/carta**.

---

## 7) Dove sta il contenuto vero

Alla fine:

```tex
\begin{document}
\input{spells}
\end{document}
```

Questo significa: LaTeX carica un file `spells.tex` (di solito) che contiene tutte le carte, una dopo l’altra.

Quindi tu quasi sicuramente modificherai:

* `cards.tex` per cambiare **grafica/layout/stile**
* `spells.tex` per cambiare **testi e campi delle singole carte**

---

# Modifiche tipiche (con indicazione “dove”)

## A) Cambiare dimensione carta

Nel `geometry`:

* `paperwidth=...`
* `paperheight=...`

Se aumenti la carta, probabilmente vorrai anche ritarare:

* `top=22mm`, `bottom=10mm`
* l’altezza del contenuto: `[5cm]` nel `minipage`

## B) Cambiare sfondo

Cambia:

```tex
{images/background}
```

oppure sostituisci il file in `images/background.(png/pdf/jpg)`.

## C) Cambiare colori del titolo/etichette

Cambia `headercolor`:

```tex
\definecolor{headercolor}{RGB}{...}
```

## D) Aggiungere un nuovo campo (es. “Saving Throw” o “School”)

Devi:

1. aumentare il numero di argomenti dell’environment (`[7]` → `[8]`)
2. aggiungere un `\def\...{#8}`
3. aggiungere un blocco `minipage` nel layout

E poi aggiornare tutte le chiamate in `spells.tex` (ogni `\begin{spell}{...}`).

## E) Se il testo della descrizione è spesso troppo lungo

Hai alcune leve:

* aumentare la dimensione della carta o ridurre margini
* aumentare l’altezza del minipage: `[5cm]` → `[5.5cm]` o simili
* ridurre il font del corpo: `\footnotesize` → `\scriptsize`
* rivedere `\vspace` e spazi verticali

---

## Compilazione (pratica)

* Se vuoi usare il font `MrsEavesRoman`: **XeLaTeX**

  ```bash
  xelatex cards.tex
  ```
* Se non ti interessa quel font: può andare anche `pdflatex cards.tex` (ma lo sfondo deve essere compatibile).

---

Se mi alleghi anche il file `spells.tex` (o mi incolli 2–3 carte di esempio), posso dirti esattamente:

* come sono scritte le carte oggi,
* quali modifiche conviene fare (layout vs contenuto),
* e se ci sono rischi di “overflow” del testo o campi inconsistenti.


---


Perfetto: conferma esattamente la struttura che ti ho descritto. Ogni `\begin{spell}{...}{...}{...}{...}{...}{...}{...}` passa **7 campi** al template, e poi dentro l’environment metti il **testo descrittivo libero**.

Qui sotto ti spiego, in modo operativo, cosa significa ogni parametro e alcune modifiche “pratiche” che quasi sempre servono quando si impaginano carte D&D.

---

## 1) Mappa dei 7 parametri (nell’ordine corretto)

Nel tuo esempio:

```latex
\begin{spell}{Beffa crudele}{enchantment cantrip}{60 feet}{1 action}{Instantaneous}{V}{Vicious Mockery page 285}
```

L’ordine è:

1. **Titolo** (`#1`)

   * `Beffa crudele`
     Va nell’header grande in alto.

2. **Header / sottotitolo** (`#2`)

   * `enchantment cantrip` / `1st level ammaliamento`
     Va sopra al titolo (piccolo maiuscoletto). In genere qui ci sta “Scuola + livello” (o “trucchetto”).

3. **Range / Gittata** (`#3`)

   * `60 feet` / `18m (30ft)`
     Va nel riquadro “Range”.

4. **Casting time / Tempo di lancio** (`#4`)

   * `1 action` / `1 azione`
     Va nel riquadro “Casting time”.

5. **Duration / Durata** (`#5`)

   * `Instantaneous` / `Concentrazione, fino a 1 minuto`
     Va nel riquadro “Duration”.

6. **Components / Componenti** (`#6`)

   * `V` / `S, V, M`
     Va nel riquadro “Components”.

7. **Source / sorgente** (`#7`)

   * `Vicious Mockery page 285` / `Bless page 217`
     Va nel footer in basso (se non vuoto).

Il testo dopo la riga vuota è il **corpo** della carta.

---

## 2) Problemi tipici che vedo già nel tuo esempio (e come risolverli)

### A) Incoerenza lingua/terminologia

Hai un mix (es. “Range”, “Casting time” come etichette stampate e contenuti in italiano/inglese).
Se vuoi uniformare tutto in italiano, la modifica va fatta nel template `cards.tex` (le etichette “Casting time”, “Range”, ecc. sono hardcoded lì).

Nel file `cards.tex`, dentro `\newenvironment{spell}` trovi:

```tex
Casting time
Range
Components
Duration
```

Basta sostituirle con:

* **Tempo di lancio**
* **Gittata**
* **Componenti**
* **Durata**

Operazione semplice e “a rischio zero”.

---

### B) Caratteri speciali e apostrofi tipografici

Nel testo hai `5° liv` ecc. Va bene.
Attenzione invece a caratteri tipo `’` (apostrofo “curvo”) se copi/incolli da Word o web: con pdfLaTeX può dare problemi. Con XeLaTeX (che già potresti usare per il font) di solito è tutto più tollerante.

---

### C) Lunghezza testo vs spazio carta

La carta ha un’area di testo fissa (minipage alta 5 cm). “Beffa crudele” è abbastanza lunga: rischi facilmente che il testo “vada oltre” o venga impaginato male.

Tre soluzioni “standard” (in ordine di intervento):

1. **Ridurre leggermente il font del corpo**: nel template c’è `\footnotesize`. Passa a `\scriptsize`.
2. **Aumentare l’altezza del minipage**: `[5cm]` → ad esempio `[5.6cm]`.
3. **Ridurre margini o aumentare formato carta**.

Se vuoi mantenere il formato poker, in genere la combo migliore è: **aumentare un po’ il minipage** + **portare il corpo a `\scriptsize`**.

---

## 3) Migliorie pratiche per scrivere `spells.tex` senza impazzire

### A) Evitare problemi se nei campi metti parentesi/virgolette

Nei campi parametrici evita `{` e `}` non bilanciati. Parentesi tonde ok, virgole ok.

### B) Macro “più leggibili”

Se ti dà fastidio l’ordine rigido dei 7 parametri, si può migliorare il template per avere comandi “a chiave” (stile `\spellRange{...}` ecc.), ma è una riscrittura un po’ più invasiva. Se ti interessa, te la propongo in modo pulito mantenendo compatibilità.

---

## 4) Esempio di come appariranno le tue due carte (a livello logico)

### “Beffa crudele”

* Header piccolo: `ENCHANTMENT CANTRIP` (in maiuscoletto)
* Titolo grande colorato: `Beffa crudele`
* Box:

  * Casting time: `1 action`
  * Range: `60 feet`
  * Components: `V`
  * Duration: `Instantaneous`
* Footer: `Vicious Mockery page 285`
* Corpo: la descrizione in italiano

### “Benedizione”

Idem, con campi misti IT/EN.

---

## 5) Modifica consigliata immediata (minimo sforzo, massimo beneficio)

1. **Traduci le etichette** nel template (se vuoi tutto italiano).
2. **Uniforma unità** (es. metri o piedi, ma non entrambi; oppure entrambi ma sempre nello stesso formato).
3. Se hai carte “lunghe”, cambia `\footnotesize` → `\scriptsize` e aumenta `[5cm]` un poco.

---

Se mi incolli il blocco del template dove c’è il layout interno (quello con i quattro riquadri “Casting time / Range / …”), ti dico esattamente quali 2–3 righe modificare per:

* italianizzare le etichette,
* aumentare spazio testo,
* e rendere più robusta l’impaginazione (meno “sensibile” alla lunghezza).



---


Prima mi hai scritto questa cosa:

```
margin=0.6cm imposta margini piccoli (poi però vengono ulteriormente “specializzati” con top=22mm e bottom=10mm).
```

Se io volessi abbassare il margine da 0.6cm a 0.4cm... mi basta cambiare quella variabile e basta?
Devo per forza cambiare anche "top" e "bottom" o quelli posso lasciarli così?



Risposta breve: **sì, puoi cambiare solo `margin=0.6cm` in `margin=0.4cm` e lasciare `top` e `bottom` così come sono**. Non è obbligatorio toccarli.
Risposta lunga (che è quella che ti evita sorprese): dipende **da quale margine vuoi davvero ridurre** e **da come `geometry` risolve le priorità**.

---

## Come funziona davvero `geometry` in questo caso

Hai questa riga:

```tex
\usepackage[
  paperheight=8.89cm,
  paperwidth=6.35cm,
  margin=0.6cm,
  top=22mm,
  bottom=10mm,
  headheight=1cm
]{geometry}
```

### Regola fondamentale di `geometry`

* **Le opzioni più specifiche vincono su quelle generiche**.
* `margin=...` è un’impostazione *globale* (tutti i lati).
* `top=...` e `bottom=...` sono *override specifici*.

Quindi, oggi succede questo:

| Lato       | Valore effettivo     |
| ---------- | -------------------- |
| **Top**    | **22 mm** (override) |
| **Bottom** | **10 mm** (override) |
| **Left**   | **0.6 cm**           |
| **Right**  | **0.6 cm**           |

---

## Cosa succede se cambi solo `margin`

Se fai:

```tex
margin=0.4cm
```

otteni:

| Lato       | Valore effettivo     |
| ---------- | -------------------- |
| **Top**    | **22 mm** (immutato) |
| **Bottom** | **10 mm** (immutato) |
| **Left**   | **0.4 cm**           |
| **Right**  | **0.4 cm**           |

Quindi:

* **sì**, è perfettamente valido
* **no**, non sei obbligato a cambiare `top` e `bottom`
* riduci **solo** i margini laterali

---

## Quando *devi* toccare anche `top` e `bottom`

Devi modificarli **solo se** il tuo obiettivo è uno di questi:

### 1) Vuoi più spazio verticale per il testo

Allora `margin` **non basta**, perché:

* il top è fissato a 22 mm
* il bottom a 10 mm

In quel caso devi intervenire qui, ad esempio:

```tex
top=18mm,
bottom=8mm
```

oppure eliminare proprio gli override:

```tex
% togli top e bottom
margin=0.4cm
```

(ma attenzione: così cambiano anche header e footer).

---

### 2) Vuoi che tutti i margini siano coerenti

Se vuoi **simmetria vera**, allora sì:
o usi solo `margin`, oppure solo `top/bottom/left/right`.

Esempio “pulito”:

```tex
\usepackage[
  paperheight=8.89cm,
  paperwidth=6.35cm,
  margin=0.4cm,
  headheight=1cm
]{geometry}
```

---

## Nota importante per il tuo caso specifico (carte)

Nel tuo template:

* lo **spazio verticale** è già molto vincolato da:

  * `top=22mm`
  * header (`fancyhdr`)
  * `minipage` alta 5 cm

👉 **Ridurre i margini laterali (`margin`) è sicuro e non rompe nulla.**
👉 **Ridurre `top` senza ritarare header/minipage può rompere l’allineamento** (titolo che “morde” lo sfondo o collide col contenuto).

---

## Consiglio pratico (sysadmin-style)

Fai una modifica alla volta:

1. Cambia solo:

   ```tex
   margin=0.4cm
   ```
2. Ricompila
3. Guarda:

   * titolo
   * riquadri
   * corpo testo

Se poi serve più aria verticale, **allora** tocchi `top/bottom` *consapevolmente*.

Se vuoi, nel prossimo messaggio posso dirti **quali valori sono “safe”** per `top` e `bottom` *senza rompere il layout attuale*.




---


Ok, passiamo ad un'altra possibile modifica che sto valutando.

La possibilità di poter specificare un'immagine di sfondo da mettere dietro al testo.
Alcune carte potrebbero averla, altre invece no e si potrebbe lasciare l'attuale background.
Vorrei che fosse un'immagine centrata rispetto alla carta e che sia un png con trasparenza in modo che si vada ad aggiungere all'attuale background lasciandolo intravedere dove serve.

Credi sia possibile?



Sì, è assolutamente possibile, ed è una modifica “pulita” da fare: puoi mantenere lo sfondo attuale (quello definito con `backgroundsetup`) e, **solo per alcune carte**, aggiungere un **secondo livello** (overlay) con un PNG trasparente, centrato sulla carta.

L’idea tecnica è:

* lasci `\backgroundsetup{...images/background...}` com’è (sfondo “base” uguale per tutte le pagine);
* per le carte che vuoi “decorate”, aggiungi un’immagine **in sovrimpressione** solo su quella pagina;
* a fine carta, “pulisci” l’overlay così non si trascina sulla carta successiva.

Di seguito ti do una soluzione pronta, minimale e robusta.

---

## Modifica a `cards.tex` (overlay per singola carta)

### 1) Aggiungi questi package

Nel preambolo di `cards.tex` (dove ci sono gli altri `\usepackage`), aggiungi:

```latex
\usepackage{eso-pic}   % per inserire immagini sullo sfondo della singola pagina
\usepackage{xparse}    % per gestire argomenti opzionali in modo comodo
```

(`graphicx` lo hai già, quindi ok.)

---

### 2) Sostituisci la definizione dell’environment `spell` con una versione che accetta un argomento opzionale

Attualmente hai:

```latex
\newenvironment{spell}[7]{ ... }{ ... }
```

Sostituiscila con questa (stesso comportamento, ma in più supporta un overlay PNG opzionale):

```latex
\RenewDocumentEnvironment{spell}{O{} m m m m m m m}
{
    % #1 = overlay (opzionale), default vuoto
    % #2..#8 = i tuoi 7 campi originali

    \def\spelltitle{#2}
    \def\spellheader{#3}
    \def\castrange{#4}
    \def\casttime{#5}
    \def\duration{#6}
    \def\components{#7}
    \def\spellsource{#8}

    % Overlay per questa pagina (se specificato)
    \def\spelloverlay{#1}
    \if\relax\spelloverlay\relax\else
      \AddToShipoutPictureBG*{%
        \AtPageCenter{%
          % Regola qui la dimensione dell’overlay:
          % - width=\paperwidth mantiene proporzioni e lo scala sulla larghezza carta
          % - puoi usare anche width=0.9\paperwidth per lasciarlo “più piccolo”
          \includegraphics[width=\paperwidth]{\spelloverlay}%
        }%
      }%
    \fi

    % ---- da qui in poi: il tuo layout originale (incollalo identico) ----
    \begin{minipage}[t][5cm][t]{\textwidth}
    \begin{minipage}[t]{0.49\textwidth}
    \textbf{\color{headercolor}\footnotesize Casting time}
    \footnotesize\casttime
    \end{minipage}
    \hfill
    \begin{minipage}[t]{0.49\textwidth}
    \textbf{\color{headercolor}\footnotesize Range}
    \footnotesize\castrange
    \end{minipage}

    \vspace{5mm}
    \begin{minipage}[t]{0.49\textwidth}
    \textbf{\color{headercolor}\footnotesize Components}
    \footnotesize\components
    \end{minipage}
    \hfill
    \begin{minipage}[t]{0.49\textwidth}
    \textbf{\color{headercolor}\footnotesize Duration}
    \footnotesize\duration
    \end{minipage}
    \end{minipage}

    \vspace{0.3mm}
    \headrule
    \footnotesize
}
{
    % IMPORTANTISSIMO: pulisce l’overlay per non applicarlo alla pagina successiva
    \ClearShipoutPictureBG

    \vfill\null
    \newpage
}
```

Nota:

* Uso `\RenewDocumentEnvironment` perché con ogni probabilità l’environment `spell` esiste già nel file; così lo “sovrascrivi” senza errori.
* L’argomento opzionale è `[#1]`. Se è vuoto, non mette nulla.

---

## Come si usa in `spells.tex`

### Carta SENZA overlay (come fai ora)

Identica a prima:

```latex
\begin{spell}{Beffa crudele}{enchantment cantrip}{60 feet}{1 action}{Instantaneous}{V}{Vicious Mockery page 285}
...
\end{spell}
```

### Carta CON overlay (PNG trasparente)

Aggiungi un argomento opzionale tra parentesi quadre, con il path del PNG:

```latex
\begin{spell}[images/overlays/vicious-mockery.png]{Beffa crudele}{enchantment cantrip}{60 feet}{1 action}{Instantaneous}{V}{Vicious Mockery page 285}
...
\end{spell}
```

L’immagine viene centrata e “si somma” allo sfondo base grazie alla trasparenza PNG.

---

## Regolazioni comuni (che ti serviranno quasi sicuramente)

### 1) Overlay più piccolo della carta

Nel `\includegraphics[...]` cambia:

```latex
\includegraphics[width=0.9\paperwidth]{\spelloverlay}
```

Oppure imposta anche l’altezza, mantenendo proporzioni:

```latex
\includegraphics[height=0.85\paperheight]{\spelloverlay}
```

### 2) Overlay “dietro” ma non troppo invadente

Se vuoi “alleggerirlo” (renderlo più tenue), in LaTeX puro non è sempre comodissimo. La via più semplice è preparare i PNG già con opacità ridotta (esportandoli con un editor grafico). Se invece vuoi farlo lato LaTeX, si può usare `transparent` o soluzioni PDF/XeLaTeX, ma ti direi di partire con PNG già pronti.

### 3) Assicurati che il base background continui a funzionare

Questa soluzione non tocca `backgroundsetup`: l’overlay è un secondo layer per pagina.

---

## Una cautela importante

`eso-pic` aggiunge l’overlay “a livello pagina”. Se un domani fai carte multi-pagina (non credo, ma lo dico), l’overlay si applicherà a quella singola pagina e poi viene pulito.

---

Se vuoi, incollami il blocco attuale di `cards.tex` dove definisci `\newenvironment{spell}` (solo quella parte) e ti restituisco una patch “diff-like” esatta, così riduci il rischio di errori di copia/incolla.



---

#!/usr/bin/env bash


echo "$0 - script per oggetti singoli, 9 copie su una singola pagina"

# Controllo che sia stato passato un argomento
if [ "$#" -ne 1 ]; then
  echo "Uso: $0 <file>"
  exit 1
fi

FILE="$1"

# Controllo che esista
if [ ! -e "$FILE" ]; then
  echo "Errore: il file '$FILE' non esiste."
  exit 1
fi

# Controllo che non sia una directory
if [ -d "$FILE" ]; then
  echo "Errore: '$FILE' è una directory, non un file."
  exit 1
fi

# Pulizia dei file di compilazione
echo "Pulizia file di compilazione..."
rm -f tex/*.aux tex/*.log tex/*.xdv tex/*.out tex/*.pdf tex/*.fls tex/*.fdb_latexmk


# Esecuzione del comando Python
echo "Generazione documento latex..."
python3 generate_items.py -f "$FILE" > tex/items.tex
python3 generate_items.py -f "$FILE"

# Compilazione con LaTeX
echo "Compilazione..."
latexmk -f -xelatex -cd tex/items_cards.tex tex/printable_onepage.tex

echo "Done."

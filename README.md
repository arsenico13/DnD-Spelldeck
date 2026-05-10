# D&D Spelldeck

Generate printable D&D spell and item cards from JSON datasets using Python and
LaTeX.

The project currently supports:

- spell cards from CLI, backend and GUI
- item cards from CLI, backend and GUI
- standard printable PDFs
- one-page item PDFs for 9 copies of the same generated card


## Preview

A card looks something like this:

![An example of a spell card](http://i.imgur.com/gLl9PwI.png)

Some cards need to truncate text because the available space is limited.


## Requirements

To use the full generation pipeline you need:

- Python 3
- `latexmk`
- XeLaTeX

Unit tests only require Python 3.


## Project Layout

Main entrypoints:

- `generate.py`: CLI for spell cards
- `generate_items.py`: CLI for item cards
- `gui/app.py`: desktop GUI entrypoint

Reusable backend:

- `spelldeck/spells_*`: spell loading, filtering, TeX rendering and services
- `spelldeck/items_*`: item loading, filtering, TeX rendering and services
- `spelldeck/compiler.py`: LaTeX compilation services

Templates and generated files:

- `tex/cards.tex`
- `tex/items_cards.tex`
- `tex/printable.tex`
- `tex/printable_items.tex`
- `tex/printable_onepage.tex`

Datasets:

- `data/spells.json`: default spells dataset
- `data/items_test.json`: default items dataset
- additional custom datasets in `data/`


## Quick Start

### GUI

Start the GUI from the repository root:

```bash
python3 gui/app.py
```

Alternative:

```bash
python3 -m gui.app
```

The GUI has two tabs:

- `Magie`
- `Oggetti`

Current GUI features:

- select a JSON dataset
- filter spells by class, level, school and name
- filter items by name and optional legacy class field
- generate TeX
- compile spell PDFs
- compile item PDFs
- compile one-page item PDFs for 9 copies

Filter fields accept comma-separated values, for example:

- `wizard, bard`
- `1, 2, 5-7`
- `abjuration, evocation`
- `Alarm, Augury`
- `Pozione di Cura, Armor of Resistance`


### CLI: Spells

Generate `tex/spells.tex`:

```bash
python3 generate.py > tex/spells.tex
```

Generate filtered spells:

```bash
python3 generate.py -c wizard -l 1-3 > tex/spells.tex
```

Use a custom dataset:

```bash
python3 generate.py -f data/spells_ita.json -n Alarm > tex/spells.tex
```

Compile the final spell PDF:

```bash
latexmk -xelatex -cd tex/cards.tex tex/printable.tex
```


### CLI: Items

Generate `tex/items.tex`:

```bash
python3 generate_items.py -f data/items_test.json > tex/items.tex
```

Generate a specific item:

```bash
python3 generate_items.py -f data/items_test.json -n "Pozione di Cura" > tex/items.tex
```

Compile the standard item PDF:

```bash
latexmk -xelatex -cd tex/items_cards.tex tex/printable_items.tex
```

Compile the one-page item PDF:

```bash
latexmk -xelatex -cd tex/items_cards.tex tex/printable_onepage.tex
```


## Python Backend Usage

Generate spell TeX from Python:

```bash
python3 -c 'from spelldeck.spells_service import generate_spells_tex_file; print(generate_spells_tex_file(names=["Alarm"]))'
```

Compile the spell PDF:

```bash
python3 -c 'from spelldeck.compiler import compile_spell_pdf; r = compile_spell_pdf(); print(r.returncode, r.output_pdf)'
```

Generate item TeX from Python:

```bash
python3 -c 'from spelldeck.items_service import generate_items_tex_file; print(generate_items_tex_file(names=["Pozione di Cura"]))'
```

Compile the standard item PDF:

```bash
python3 -c 'from spelldeck.compiler import compile_items_pdf; r = compile_items_pdf(); print(r.returncode, r.output_pdf)'
```

Compile the one-page item PDF:

```bash
python3 -c 'from spelldeck.compiler import compile_single_page_items_pdf; r = compile_single_page_items_pdf(); print(r.returncode, r.output_pdf)'
```


## Item Features

The item pipeline supports:

- overlay images
- overlay opacity
- lightweight markdown-like formatting in item text

Supported formatting in item text:

- `**text**` -> bold
- `__text__` -> italic
- blank line -> paragraph break
- single newline -> forced line break


## Fonts and Paper

The cards are designed around XeLaTeX and the `Mrs Eaves` font. If that font is
not available on your system, XeLaTeX may fall back poorly or fail depending on
your setup.

Printable layouts currently target A4. If you need another paper size, adjust:

- `tex/printable.tex`
- `tex/printable_items.tex`
- `tex/printable_onepage.tex`


## Tests

Run the full test suite:

```bash
python3 -m unittest discover
```

Run only spell backend tests:

```bash
python3 -m unittest tests.test_spells_data tests.test_spells_filters tests.test_spells_tex tests.test_spells_service
```

Run only item backend tests:

```bash
python3 -m unittest tests.test_items_data tests.test_items_tex tests.test_items_service
```

Run only compiler tests:

```bash
python3 -m unittest tests.test_compiler
```


## Notes

- `generate_items.py` still exists as a compatibility CLI, but the core logic now lives in `spelldeck/items_*`.
- `generate_single_item.sh` is legacy; the one-page flow is now covered by the backend and GUI.
- More detailed technical planning and project documentation live under `doc/`.

## Copyright and Credit

The spells included in this repository as well as the background for the cards
are property of Wizards of the Coast. The license in this repository covers the
Python and LaTeX code, not the game content assets.

Instrumental in creating this project were reddit user Afluffygrue in
[this thread](https://www.reddit.com/r/DnD/comments/2yirik/after_hours_of_cleaning_here_are_the_complete/)
for providing spell data and the people at
[UnearthedArcana](https://www.reddit.com/r/UnearthedArcana/) for graphical
resources.

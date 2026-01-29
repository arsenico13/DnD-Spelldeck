#! /usr/bin/env python3

import argparse
import sys
import textwrap
import re
import json

MAX_TEXT_LENGTH = 600

ITEMS_TRUNCATED = 0
ITEMS_TRUNCATED_NAMES = []
ITEMS_TOTAL = 0

LEVEL_STRING = {
    0: '{school} cantrip {ritual}',
    1: '1st level {school} {ritual}',
    2: '2nd level {school} {ritual}',
    3: '3rd level {school} {ritual}',
    4: '4th level {school} {ritual}',
    5: '5th level {school} {ritual}',
    6: '6th level {school} {ritual}',
    7: '7th level {school} {ritual}',
    8: '8th level {school} {ritual}',
    9: '9th level {school} {ritual}',
}

with open('data/spells.json') as json_data:
    SPELLS = json.load(json_data)


def truncate_string(string, max_len=MAX_TEXT_LENGTH):
    rv = ""

    for sentence in string.split(".")[:-1]:
        if len(rv + sentence) < MAX_TEXT_LENGTH - 2:
            rv += sentence + "."
        else:
            rv += ".."
            break

    return rv


def markdown_lite_to_latex(text):
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Bold: **text** -> \textbf{text}
    text = re.sub(r"\*\*(.+?)\*\*", r"\\textbf{\1}", text)
    # Italic: __text__ -> \textit{text}
    text = re.sub(r"__(.+?)__", r"\\textit{\1}", text)

    # Paragraphs: blank line -> \par ; single newline -> line break
    paragraphs = text.split("\n\n")
    paragraphs = [p.replace("\n", " \\\\\n") for p in paragraphs]

    return "\n\n\\par\n\n".join(paragraphs)


def print_item(name, availability, itemtype, weight, cost, ritual, damage, attunement,
                material, text, damagetype=None, overlay=None, overlay_opacity=1, **kwargs):

    global ITEMS_TRUNCATED, ITEMS_TOTAL

    # deve essere composto da tipo di oggetto + disponibilità dell'oggetto
    header = "" + itemtype + " - " + availability
    # header = LEVEL_STRING[level].format(school=school.lower(), ritual='ritual' if ritual else '').strip()

    new_text = truncate_string(text)
    new_text = markdown_lite_to_latex(new_text)

    if new_text != text:
        ITEMS_TRUNCATED += 1
        ITEMS_TRUNCATED_NAMES.append(name)

    ITEMS_TOTAL += 1

    overlay = (overlay or "").strip()
    if overlay:
        begin_spell = "\\begin{spell}[%s][%s]" % (overlay, overlay_opacity)
    else:
        begin_spell = "\\begin{spell}"

    print("%s{%s}{%s}{%s}{%s}{%s}{%s}{%s}\n\n%s\n\n\\end{spell}\n" %
        (begin_spell, name, header, damagetype, cost, damage, 'si' if attunement else 'no', weight, new_text))


def get_spells(classes=None, levels=None, schools=None, names=None):
    classes = {i.lower() for i in classes} if classes is not None else None
    schools = {i.lower() for i in schools} if schools is not None else None
    names = {i.lower() for i in names} if names is not None else None

    return [
        (name, spell) for name, spell in sorted(SPELLS.items(), key=lambda x: x[0]) if
        (classes is None or len(classes & {i.lower() for i in spell['classes']}) > 0) and
        (schools is None or spell['school'].lower() in schools) and
        (levels is None or spell['level'] in levels) and
        (names is None or name.lower() in names)
    ]


def parse_levels(levels):
    rv = None

    if levels is not None:
        rv = set()

        for level_spec in levels:
            tmp = level_spec.split('-')
            if len(tmp) == 1:
                rv.add(int(tmp[0]))
            elif len(tmp) == 2:
                rv |= set(range(int(tmp[0]), int(tmp[1]) + 1))

    return rv


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c", "--class", type=str, action='append', dest='classes',
        help="only select spells for this class, can be used multiple times "
             "to select multiple classes."
    )
    parser.add_argument(
        "-l", "--level", type=str, action='append', dest='levels',
        help="only select spells of a certain level, can be used multiple "
             "times and can contain a range such as `1-3`."
    )
    parser.add_argument(
        "-s", "--school", type=str, action='append', dest='schools',
        help="only select spells of a school, can be used multiple times."
    )
    parser.add_argument(
        "-n", "--name", type=str, action='append', dest='names',
        help="select spells with one of several given names."
    )
    parser.add_argument(
        "-f", "--filename", type=str, action='store', dest='filename',
        help="specify a different filename for the spells data."
    )
    args = parser.parse_args()

    if args.filename != "":
        # se viene specificato un filename, allora uso quel file come input dei dati
        with open(args.filename) as json_data:
            SPELLS = json.load(json_data)

    for name, spell in get_spells(args.classes, parse_levels(args.levels), args.schools, args.names):
        print_item(name, **spell)

    print('Ho dovuto troncare il testo di %d su %d items a %d caratteri.' % (ITEMS_TRUNCATED, ITEMS_TOTAL, MAX_TEXT_LENGTH), file=sys.stderr)

    if ITEMS_TRUNCATED:
        print(f"I nomi degli oggetti che sono stati troncati sono: {ITEMS_TRUNCATED_NAMES}", file=sys.stderr)

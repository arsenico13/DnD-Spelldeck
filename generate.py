#! /usr/bin/env python3

import argparse
import sys
from spelldeck.spells_data import load_spells
from spelldeck.spells_filters import filter_spells, parse_levels
from spelldeck.spells_tex import MAX_TEXT_LENGTH, build_spell_text, render_spell_tex, truncate_string

SPELLS = load_spells()
SPELLS_TRUNCATED = 0
SPELLS_TOTAL = 0


def print_spell(name, **spell_data):
    global SPELLS_TRUNCATED, SPELLS_TOTAL

    _, was_truncated = build_spell_text(spell_data.get("material"), spell_data["text"])
    if was_truncated:
        SPELLS_TRUNCATED += 1

    SPELLS_TOTAL += 1
    print(render_spell_tex(name, spell_data))


def get_spells(classes=None, levels=None, schools=None, names=None):
    return filter_spells(
        SPELLS, classes=classes, levels=levels, schools=schools, names=names
    )

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

    if args.filename:
        # A custom dataset keeps the CLI compatible while the reusable core
        # stays independent from argparse and stdout.
        SPELLS = load_spells(args.filename)

    for name, spell in get_spells(args.classes, parse_levels(args.levels), args.schools, args.names):
        print_spell(name, **spell)

    print('Had to truncate %d out of %d spells at %d characters.' % (SPELLS_TRUNCATED, SPELLS_TOTAL, MAX_TEXT_LENGTH), file=sys.stderr)

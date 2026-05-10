#! /usr/bin/env python3

import argparse
import sys
from spelldeck.items_data import DEFAULT_ITEMS_PATH, load_items
from spelldeck.items_service import generate_items_tex, parse_filter_string
from spelldeck.items_tex import MAX_TEXT_LENGTH, build_item_text, render_item_tex

ITEMS_TRUNCATED = 0
ITEMS_TRUNCATED_NAMES = []
ITEMS_TOTAL = 0

ITEMS = load_items(DEFAULT_ITEMS_PATH)


def print_item(name, **item_data):

    global ITEMS_TRUNCATED, ITEMS_TOTAL

    _, was_truncated = build_item_text(item_data["text"], max_len=MAX_TEXT_LENGTH)
    if was_truncated:
        ITEMS_TRUNCATED += 1
        ITEMS_TRUNCATED_NAMES.append(name)

    ITEMS_TOTAL += 1
    print(render_item_tex(name, item_data))


def get_items(names=None, classes=None):
    _, item_items, _ = generate_items_tex(
        dataset_path=DEFAULT_ITEMS_PATH,
        names=names,
        classes=classes,
    )
    return item_items


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c", "--class", type=str, action='append', dest='classes',
        help="select only items that match one of the given classes. "
             "This is mainly kept for legacy datasets."
    )
    parser.add_argument(
        "-n", "--name", type=str, action='append', dest='names',
        help="select items with one of several given names."
    )
    parser.add_argument(
        "-f", "--filename", type=str, action='store', dest='filename',
        help="specify a different filename for the items data."
    )
    args = parser.parse_args()

    if args.filename:
        ITEMS = load_items(args.filename)

    names = parse_filter_string(",".join(args.names)) if args.names else None
    classes = parse_filter_string(",".join(args.classes)) if args.classes else None

    for name, item in generate_items_tex(
        dataset_path=args.filename or DEFAULT_ITEMS_PATH,
        names=names,
        classes=classes,
    )[1]:
        print_item(name, **item)

    print('Ho dovuto troncare il testo di %d su %d items a %d caratteri.' % (ITEMS_TRUNCATED, ITEMS_TOTAL, MAX_TEXT_LENGTH), file=sys.stderr)

    if ITEMS_TRUNCATED:
        print(f"I nomi degli oggetti che sono stati troncati sono: {ITEMS_TRUNCATED_NAMES}", file=sys.stderr)

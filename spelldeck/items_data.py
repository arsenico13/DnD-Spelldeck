import json
from pathlib import Path

from spelldeck.spells_data import PACKAGE_ROOT


DEFAULT_ITEMS_PATH = PACKAGE_ROOT / "data" / "items_test.json"

REQUIRED_ITEM_FIELDS = {
    "availability",
    "itemtype",
    "weight",
    "cost",
    "damage",
    "attunement",
    "text",
}


def validate_item_record(name, data):
    if not isinstance(data, dict):
        raise ValueError(f"Item '{name}' must be a JSON object.")

    missing_fields = REQUIRED_ITEM_FIELDS - set(data)
    if missing_fields:
        missing = ", ".join(sorted(missing_fields))
        raise ValueError(f"Item '{name}' is missing required fields: {missing}")


def load_items(path=None):
    items_path = Path(path) if path is not None else DEFAULT_ITEMS_PATH

    with items_path.open() as json_data:
        items = json.load(json_data)

    if not isinstance(items, dict):
        raise ValueError("The items dataset must be a JSON object keyed by item name.")

    for name, data in items.items():
        validate_item_record(name, data)

    return items


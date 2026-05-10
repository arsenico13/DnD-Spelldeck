import json
from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SPELLS_PATH = PACKAGE_ROOT / "data" / "spells.json"

REQUIRED_SPELL_FIELDS = {
    "classes",
    "components",
    "duration",
    "level",
    "material",
    "range",
    "ritual",
    "school",
    "source",
    "source_page",
    "text",
    "time",
}


def validate_spell_record(name, data):
    if not isinstance(data, dict):
        raise ValueError(f"Spell '{name}' must be a JSON object.")

    missing_fields = REQUIRED_SPELL_FIELDS - set(data)
    if missing_fields:
        missing = ", ".join(sorted(missing_fields))
        raise ValueError(f"Spell '{name}' is missing required fields: {missing}")


def load_spells(path=None):
    spells_path = Path(path) if path is not None else DEFAULT_SPELLS_PATH

    with spells_path.open() as json_data:
        spells = json.load(json_data)

    if not isinstance(spells, dict):
        raise ValueError("The spells dataset must be a JSON object keyed by spell name.")

    for name, data in spells.items():
        validate_spell_record(name, data)

    return spells


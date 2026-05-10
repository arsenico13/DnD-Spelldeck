from dataclasses import dataclass
from pathlib import Path

from spelldeck.io_utils import write_text_file
from spelldeck.items_data import DEFAULT_ITEMS_PATH, load_items
from spelldeck.items_filters import filter_items
from spelldeck.items_tex import MAX_TEXT_LENGTH, build_item_text, render_items_tex
from spelldeck.spells_data import PACKAGE_ROOT
from spelldeck.spells_service import parse_filter_string


DEFAULT_ITEMS_TEX_PATH = PACKAGE_ROOT / "tex" / "items.tex"


@dataclass
class ItemGenerationResult:
    output_path: Path
    item_count: int
    truncated_count: int
    truncated_names: list[str]


def generate_items_tex(dataset_path=None, names=None, classes=None):
    items = load_items(dataset_path or DEFAULT_ITEMS_PATH)
    item_items = filter_items(items, names=names, classes=classes)
    tex_content = render_items_tex(item_items)

    truncated_names = [
        name
        for name, item in item_items
        if build_item_text(item["text"], max_len=MAX_TEXT_LENGTH)[1]
    ]

    return tex_content, item_items, truncated_names


def generate_items_tex_file(
    dataset_path=None,
    names=None,
    classes=None,
    output_path=DEFAULT_ITEMS_TEX_PATH,
):
    tex_content, item_items, truncated_names = generate_items_tex(
        dataset_path=dataset_path,
        names=names,
        classes=classes,
    )
    output_file = Path(output_path)
    write_text_file(output_file, tex_content)

    return ItemGenerationResult(
        output_path=output_file,
        item_count=len(item_items),
        truncated_count=len(truncated_names),
        truncated_names=truncated_names,
    )


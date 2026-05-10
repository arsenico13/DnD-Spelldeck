from dataclasses import dataclass
from pathlib import Path

from spelldeck.io_utils import write_text_file
from spelldeck.spells_data import PACKAGE_ROOT, load_spells
from spelldeck.spells_filters import filter_spells, parse_levels
from spelldeck.spells_tex import MAX_TEXT_LENGTH, build_spell_text, render_spells_tex


DEFAULT_SPELLS_TEX_PATH = PACKAGE_ROOT / "tex" / "spells.tex"


@dataclass
class SpellGenerationResult:
    output_path: Path
    spell_count: int
    truncated_count: int


@dataclass
class SpellPreviewResult:
    names: list[str]

    @property
    def spell_count(self):
        return len(self.names)


def parse_filter_string(raw_value):
    if raw_value is None:
        return None

    values = [value.strip() for value in raw_value.split(",") if value.strip()]
    return values or None


def generate_spells_tex(
    dataset_path=None,
    classes=None,
    levels=None,
    schools=None,
    names=None,
):
    spells = load_spells(dataset_path)
    spell_items = filter_spells(
        spells,
        classes=classes,
        levels=parse_levels(levels),
        schools=schools,
        names=names,
    )
    tex_content = render_spells_tex(spell_items)
    truncated_count = sum(
        1
        for _, spell in spell_items
        if build_spell_text(spell.get("material"), spell["text"], max_len=MAX_TEXT_LENGTH)[1]
    )

    return tex_content, spell_items, truncated_count


def preview_spells(
    dataset_path=None,
    classes=None,
    levels=None,
    schools=None,
    names=None,
):
    _, spell_items, _ = generate_spells_tex(
        dataset_path=dataset_path,
        classes=classes,
        levels=levels,
        schools=schools,
        names=names,
    )
    return SpellPreviewResult(names=[name for name, _ in spell_items])


def generate_spells_tex_file(
    dataset_path=None,
    classes=None,
    levels=None,
    schools=None,
    names=None,
    output_path=DEFAULT_SPELLS_TEX_PATH,
):
    tex_content, spell_items, truncated_count = generate_spells_tex(
        dataset_path=dataset_path,
        classes=classes,
        levels=levels,
        schools=schools,
        names=names,
    )
    output_file = Path(output_path)
    write_text_file(output_file, tex_content)

    return SpellGenerationResult(
        output_path=output_file,
        spell_count=len(spell_items),
        truncated_count=truncated_count,
    )

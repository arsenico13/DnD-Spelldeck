import textwrap


MAX_TEXT_LENGTH = 600

LEVEL_STRING = {
    0: "{school} cantrip {ritual}",
    1: "1st level {school} {ritual}",
    2: "2nd level {school} {ritual}",
    3: "3rd level {school} {ritual}",
    4: "4th level {school} {ritual}",
    5: "5th level {school} {ritual}",
    6: "6th level {school} {ritual}",
    7: "7th level {school} {ritual}",
    8: "8th level {school} {ritual}",
    9: "9th level {school} {ritual}",
}


def truncate_string(string, max_len=MAX_TEXT_LENGTH):
    truncated = ""

    for sentence in string.split(".")[:-1]:
        if len(truncated + sentence) < max_len - 2:
            truncated += sentence + "."
        else:
            truncated += ".."
            break

    return truncated


def build_spell_header(level, school, ritual):
    return LEVEL_STRING[level].format(
        school=school.lower(), ritual="ritual" if ritual else ""
    ).strip()


def build_spell_source(source=None, source_page=None):
    if source_page is None:
        return source or ""

    base_source = source or ""
    return f"{base_source} page {source_page}".strip()


def build_spell_text(material, text, max_len=MAX_TEXT_LENGTH):
    if material is not None:
        text = "Requires " + material + ". " + text

    truncated_text = truncate_string(text, max_len=max_len)
    return textwrap.fill(truncated_text, 80), truncated_text != text


def render_spell_tex(name, spell_data, max_len=MAX_TEXT_LENGTH):
    rendered_text, _ = build_spell_text(
        spell_data.get("material"), spell_data["text"], max_len=max_len
    )
    header = build_spell_header(
        spell_data["level"], spell_data["school"], spell_data["ritual"]
    )
    source = build_spell_source(
        spell_data.get("source"), spell_data.get("source_page")
    )

    # The LaTeX environment signature is historical and is still consumed by
    # the existing card template, so the argument order must stay stable.
    return (
        "\\begin{spell}{%s}{%s}{%s}{%s}{%s}{%s}{%s}\n\n%s\n\n\\end{spell}\n"
        % (
            name,
            header,
            spell_data["range"],
            spell_data["time"],
            spell_data["duration"],
            ", ".join(spell_data["components"]),
            source,
            rendered_text,
        )
    )


def render_spells_tex(spell_items, max_len=MAX_TEXT_LENGTH):
    return "".join(render_spell_tex(name, spell, max_len=max_len) for name, spell in spell_items)


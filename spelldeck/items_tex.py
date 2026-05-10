import re
import textwrap


MAX_TEXT_LENGTH = 600


def truncate_string(string, max_len=MAX_TEXT_LENGTH):
    truncated = ""

    for sentence in string.split(".")[:-1]:
        if len(truncated + sentence) < max_len - 2:
            truncated += sentence + "."
        else:
            truncated += ".."
            break

    return truncated


def markdown_lite_to_latex(text):
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    normalized = re.sub(r"\*\*(.+?)\*\*", r"\\textbf{\1}", normalized)
    normalized = re.sub(r"__(.+?)__", r"\\textit{\1}", normalized)

    paragraphs = normalized.split("\n\n")
    paragraphs = [paragraph.replace("\n", " \\\\\n") for paragraph in paragraphs]
    return "\n\n\\par\n\n".join(paragraphs)


def build_item_header(itemtype, availability):
    return f"{itemtype} - {availability}"


def build_item_text(text, max_len=MAX_TEXT_LENGTH):
    truncated_text = truncate_string(text, max_len=max_len)
    return markdown_lite_to_latex(textwrap.fill(truncated_text, 80)), truncated_text != text


def render_item_tex(name, item_data, max_len=MAX_TEXT_LENGTH):
    rendered_text, _ = build_item_text(item_data["text"], max_len=max_len)
    header = build_item_header(item_data["itemtype"], item_data["availability"])
    overlay = (item_data.get("overlay") or "").strip()
    overlay_opacity = item_data.get("overlay_opacity", 1)

    if overlay:
        begin_item = "\\begin{spell}[%s][%s]" % (overlay, overlay_opacity)
    else:
        begin_item = "\\begin{spell}"

    # The items template reuses the historical `spell` environment, so the
    # argument order must stay aligned with `tex/items_cards.tex`.
    return (
        "%s{%s}{%s}{%s}{%s}{%s}{%s}{%s}\n\n%s\n\n\\end{spell}\n"
        % (
            begin_item,
            name,
            header,
            item_data.get("damagetype") or "",
            item_data["cost"],
            item_data["damage"],
            "si" if item_data["attunement"] else "no",
            item_data["weight"],
            rendered_text,
        )
    )


def render_items_tex(item_items, max_len=MAX_TEXT_LENGTH):
    return "".join(render_item_tex(name, item, max_len=max_len) for name, item in item_items)


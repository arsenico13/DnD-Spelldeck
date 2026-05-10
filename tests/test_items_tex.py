import unittest

from spelldeck.items_data import load_items
from spelldeck.items_tex import (
    MAX_TEXT_LENGTH,
    build_item_header,
    build_item_text,
    markdown_lite_to_latex,
    render_item_tex,
    render_items_tex,
    truncate_string,
)


class TestItemsTex(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.items = load_items()

    def test_truncate(self):
        long_text = self.items["Lilalu"]["text"]
        short_text = self.items["Pozione di Cura"]["text"]

        self.assertLess(len(truncate_string(long_text)), MAX_TEXT_LENGTH)
        self.assertEqual(short_text, truncate_string(short_text))

    def test_markdown_lite_to_latex(self):
        text = "**Bold**\nSecond line\n\n__Italic__"
        rendered = markdown_lite_to_latex(text)

        self.assertIn(r"\textbf{Bold}", rendered)
        self.assertIn(r"Second line", rendered)
        self.assertIn(r"\par", rendered)
        self.assertIn(r"\textit{Italic}", rendered)

    def test_build_item_header(self):
        self.assertEqual("Pozione - comune", build_item_header("Pozione", "comune"))

    def test_build_item_text_reports_truncation(self):
        item_text, was_truncated = build_item_text(self.items["Lilalu"]["text"])
        self.assertTrue(was_truncated)
        self.assertIn("You have resistance", item_text)

    def test_render_item_tex_with_overlay(self):
        rendered = render_item_tex("Pozione di Cura", self.items["Pozione di Cura"])

        self.assertIn(r"\begin{spell}[images/roundpotion.png][0.55]{Pozione di Cura}", rendered)
        self.assertIn("Pozione - non comune", rendered)
        self.assertIn(r"\end{spell}", rendered)

    def test_render_items_tex(self):
        item_items = [
            ("Pozione di Cura", self.items["Pozione di Cura"]),
            ("Armor of Resistance", self.items["Armor of Resistance"]),
        ]
        rendered = render_items_tex(item_items)

        self.assertIn("Pozione di Cura", rendered)
        self.assertIn("Armor of Resistance", rendered)


import unittest

from spelldeck.spells_data import load_spells
from spelldeck.spells_filters import filter_spells
from spelldeck.spells_tex import (
    MAX_TEXT_LENGTH,
    build_spell_header,
    build_spell_source,
    build_spell_text,
    render_spell_tex,
    render_spells_tex,
    truncate_string,
)


class TestSpellsTex(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.spells = load_spells()

    def test_truncate(self):
        animate_objects = self.spells["Animate Objects"]["text"]
        eldritch_blast = self.spells["Eldritch Blast"]["text"]

        self.assertLess(len(truncate_string(animate_objects)), MAX_TEXT_LENGTH)
        if len(eldritch_blast) < MAX_TEXT_LENGTH:
            self.assertEqual(truncate_string(eldritch_blast), eldritch_blast)

    def test_build_spell_header(self):
        self.assertEqual("1st level abjuration ritual", build_spell_header(1, "Abjuration", True))
        self.assertEqual("conjuration cantrip", build_spell_header(0, "Conjuration", False))

    def test_build_spell_source(self):
        self.assertEqual("Player's Handbook page 211", build_spell_source("Player's Handbook", 211))
        self.assertEqual("", build_spell_source(None, None))

    def test_build_spell_text_adds_material_and_reports_truncation(self):
        spell_text, was_truncated = build_spell_text("a tiny bell", "Test sentence.")
        self.assertIn("Requires a tiny bell. Test sentence.", spell_text)
        self.assertFalse(was_truncated)

    def test_render_spell_tex(self):
        alarm_tex = render_spell_tex("Alarm", self.spells["Alarm"])

        self.assertIn("\\begin{spell}{Alarm}", alarm_tex)
        self.assertIn("1st level abjuration ritual", alarm_tex)
        self.assertIn("Player's Handbook page 211", alarm_tex)
        self.assertIn("Requires a tiny bell and a piece of fine silver wire.", alarm_tex)
        self.assertIn("\\end{spell}", alarm_tex)

    def test_render_spells_tex(self):
        spells = filter_spells(self.spells, names={"Alarm", "Augury"})
        tex = render_spells_tex(spells)

        self.assertIn("\\begin{spell}{Alarm}", tex)
        self.assertIn("\\begin{spell}{Augury}", tex)


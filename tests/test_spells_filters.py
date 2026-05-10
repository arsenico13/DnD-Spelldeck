import unittest

from spelldeck.spells_data import load_spells
from spelldeck.spells_filters import filter_spells, parse_levels


class TestSpellsFilters(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.spells = load_spells()

    def test_no_filter(self):
        spells = filter_spells(self.spells)
        self.assertEqual(len(spells), len(self.spells))

    def test_filter_class(self):
        spells = [name for name, _ in filter_spells(self.spells, classes={"Warlock", "Fighter"})]
        self.assertIn("Alarm", spells)
        self.assertIn("Astral Projection", spells)
        self.assertNotIn("Augury", spells)
        self.assertEqual([], filter_spells(self.spells, classes={"NotAClass"}))

    def test_filter_schools(self):
        spells = [name for name, _ in filter_spells(self.spells, schools={"Abjuration"})]
        self.assertIn("Alarm", spells)
        self.assertNotIn("Augury", spells)
        self.assertEqual([], filter_spells(self.spells, schools={"NotASchool"}))

    def test_filter_levels(self):
        level_zero = [name for name, _ in filter_spells(self.spells, levels={0})]
        level_two = [name for name, _ in filter_spells(self.spells, levels={2})]
        level_mix = [name for name, _ in filter_spells(self.spells, levels={0, 2})]

        self.assertIn("Prestidigitation", level_zero)
        self.assertNotIn("Augury", level_zero)
        self.assertIn("Augury", level_two)
        self.assertNotIn("Prestidigitation", level_two)
        self.assertIn("Augury", level_mix)
        self.assertIn("Prestidigitation", level_mix)
        self.assertEqual([], filter_spells(self.spells, levels={9000}))

    def test_filter_names(self):
        single_spell = {name for name, _ in filter_spells(self.spells, names={"Augury"})}
        multiple_spells = {
            name for name, _ in filter_spells(self.spells, names={"Augury", "Prestidigitation"})
        }

        self.assertEqual({"Augury"}, single_spell)
        self.assertEqual({"Augury", "Prestidigitation"}, multiple_spells)
        self.assertEqual(set(), {name for name, _ in filter_spells(self.spells, names={"NotASpell"})})

    def test_parse_levels(self):
        self.assertEqual(parse_levels(["1"]), {1})
        self.assertEqual(parse_levels(["5", "8", "0"]), {0, 5, 8})
        self.assertEqual(parse_levels(["2-3"]), {2, 3})
        self.assertEqual(parse_levels(["2-6"]), {2, 3, 4, 5, 6})
        self.assertEqual(parse_levels(["0", "2-6", "9"]), {0, 2, 3, 4, 5, 6, 9})


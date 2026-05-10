import json
import tempfile
import unittest
from pathlib import Path

from spelldeck.spells_service import (
    generate_spells_tex_file,
    parse_filter_string,
    preview_spells,
)


class TestSpellsService(unittest.TestCase):
    def test_parse_filter_string(self):
        self.assertEqual(["bard", "fighter"], parse_filter_string("bard, fighter"))
        self.assertIsNone(parse_filter_string(""))
        self.assertIsNone(parse_filter_string(None))

    def test_generate_spells_tex_file_default_dataset(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "spells.tex"
            result = generate_spells_tex_file(names=["Alarm"], output_path=output_path)

            self.assertEqual(1, result.spell_count)
            self.assertEqual(output_path, result.output_path)
            self.assertTrue(output_path.exists())
            self.assertIn("\\begin{spell}{Alarm}", output_path.read_text())

    def test_generate_spells_tex_file_custom_dataset(self):
        dataset = {
            "Test Spell": {
                "classes": ["Wizard"],
                "components": ["V"],
                "duration": "Instantaneous",
                "level": 1,
                "material": None,
                "range": "Self",
                "ritual": False,
                "school": "Evocation",
                "source": "Homebrew",
                "source_page": 1,
                "text": "A simple spell.",
                "time": "1 action",
            }
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            dataset_path = Path(tmpdir) / "spells.json"
            output_path = Path(tmpdir) / "spells.tex"
            dataset_path.write_text(json.dumps(dataset))

            result = generate_spells_tex_file(dataset_path=dataset_path, output_path=output_path)

            self.assertEqual(1, result.spell_count)
            self.assertEqual(0, result.truncated_count)
            self.assertIn("\\begin{spell}{Test Spell}", output_path.read_text())

    def test_preview_spells(self):
        result = preview_spells(names=["Alarm", "Augury"])

        self.assertEqual(2, result.spell_count)
        self.assertEqual(["Alarm", "Augury"], result.names)

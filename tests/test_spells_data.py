import json
import tempfile
import unittest
from pathlib import Path

from spelldeck.spells_data import DEFAULT_SPELLS_PATH, load_spells


class TestSpellsData(unittest.TestCase):
    def test_load_default_dataset(self):
        spells = load_spells()
        self.assertTrue(DEFAULT_SPELLS_PATH.exists())
        self.assertIn("Alarm", spells)

    def test_load_custom_dataset(self):
        sample = {
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
            dataset_path.write_text(json.dumps(sample))

            spells = load_spells(dataset_path)

        self.assertEqual(sample, spells)

    def test_load_missing_file_raises(self):
        with self.assertRaises(FileNotFoundError):
            load_spells("/tmp/definitely-missing-spells.json")

    def test_load_invalid_json_raises(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            dataset_path = Path(tmpdir) / "broken.json"
            dataset_path.write_text("{broken")

            with self.assertRaises(json.JSONDecodeError):
                load_spells(dataset_path)


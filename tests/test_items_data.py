import json
import tempfile
import unittest
from pathlib import Path

from spelldeck.items_data import DEFAULT_ITEMS_PATH, load_items


class TestItemsData(unittest.TestCase):
    def test_load_default_dataset(self):
        items = load_items()
        self.assertTrue(DEFAULT_ITEMS_PATH.exists())
        self.assertIn("Pozione di Cura", items)

    def test_load_custom_dataset(self):
        sample = {
            "Test Item": {
                "availability": "comune",
                "itemtype": "Oggetto",
                "weight": "10g",
                "cost": "1 mo",
                "damage": "-",
                "attunement": False,
                "text": "Simple item.",
            }
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            dataset_path = Path(tmpdir) / "items.json"
            dataset_path.write_text(json.dumps(sample))

            items = load_items(dataset_path)

        self.assertEqual(sample, items)

    def test_load_missing_file_raises(self):
        with self.assertRaises(FileNotFoundError):
            load_items("/tmp/definitely-missing-items.json")

    def test_load_invalid_json_raises(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            dataset_path = Path(tmpdir) / "broken.json"
            dataset_path.write_text("{broken")

            with self.assertRaises(json.JSONDecodeError):
                load_items(dataset_path)


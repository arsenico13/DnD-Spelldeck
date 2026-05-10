import json
import tempfile
import unittest
from pathlib import Path

from spelldeck.items_service import generate_items_tex_file, parse_filter_string


class TestItemsService(unittest.TestCase):
    def test_parse_filter_string(self):
        self.assertEqual(["bard", "fighter"], parse_filter_string("bard, fighter"))
        self.assertIsNone(parse_filter_string(""))
        self.assertIsNone(parse_filter_string(None))

    def test_generate_items_tex_file_default_dataset(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "items.tex"
            result = generate_items_tex_file(names=["Pozione di Cura"], output_path=output_path)

            self.assertEqual(1, result.item_count)
            self.assertEqual(output_path, result.output_path)
            self.assertTrue(output_path.exists())
            self.assertIn("\\begin{spell}[images/roundpotion.png][0.55]{Pozione di Cura}", output_path.read_text())

    def test_generate_items_tex_file_custom_dataset(self):
        dataset = {
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
            output_path = Path(tmpdir) / "items.tex"
            dataset_path.write_text(json.dumps(dataset))

            result = generate_items_tex_file(dataset_path=dataset_path, output_path=output_path)

            self.assertEqual(1, result.item_count)
            self.assertEqual(0, result.truncated_count)
            self.assertEqual([], result.truncated_names)
            self.assertIn("\\begin{spell}{Test Item}", output_path.read_text())

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "hooks"))
from persona_manual import block


class PersonaManualTest(unittest.TestCase):
    def test_finds_exactly_one_reviewed_block(self):
        text = "before\n<!-- PERSONA:MANUAL:BEGIN -->\nreviewed\n<!-- PERSONA:MANUAL:END -->\nafter"
        start, end = block(text)
        self.assertEqual(text[start:end].count("reviewed"), 1)

    def test_rejects_missing_markers(self):
        with self.assertRaises(ValueError):
            block("unreviewed")

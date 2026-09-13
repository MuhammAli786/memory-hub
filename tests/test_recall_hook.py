import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "hooks"))
from recall_hook import render


class RecallTest(unittest.TestCase):
    def test_keeps_recent_dated_content(self):
        now = datetime.now(timezone.utc).isoformat()
        result = render({"manual_persona": "Be precise.", "l1": [{"created_at": now, "content": "A verified fact."}]})
        self.assertIn("Be precise.", result)
        self.assertIn("A verified fact.", result)

    def test_rejects_undated_dynamic_content(self):
        result = render({"l2": [{"summary": "Undated scene."}]})
        self.assertNotIn("Undated scene.", result)

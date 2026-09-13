import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "hooks"))
from capture import select_new_turns, turn_id


class CaptureTest(unittest.TestCase):
    def test_deduplicates_by_content_identity(self):
        digest = turn_id("meaningful user request", "meaningful assistant response")
        turns = [{"turn_id": "replacement-id", "content_hash": digest,
                  "user": "meaningful user request", "assistant": "meaningful assistant response"}]
        accepted, skipped = select_new_turns(turns, {digest}, minimum_characters=1)
        self.assertEqual(accepted, [])
        self.assertEqual(skipped["known"], 1)

    def test_caps_before_deduplication(self):
        turns = [{"turn_id": str(index), "content_hash": str(index), "user": "x", "assistant": "y"} for index in range(3)]
        accepted, skipped = select_new_turns(turns, {"2"}, minimum_characters=1, maximum_turns=1)
        self.assertEqual(accepted, [])
        self.assertEqual(skipped["outside_tail"], 2)


if __name__ == "__main__":
    unittest.main()

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "tools"))
from model_router import Router


class RouterTest(unittest.TestCase):
    def test_tiers_outrank_list_position_and_rotate_within_tier(self):
        router = Router([
            {"name": "fallback", "model": "m", "tier": 1},
            {"name": "local-a", "model": "m", "tier": 0},
            {"name": "local-b", "model": "m", "tier": 0},
        ])
        first = [item["name"] for item in router.candidates(100)]
        second = [item["name"] for item in router.candidates(100)]
        self.assertEqual(set(first[:2]), {"local-a", "local-b"})
        self.assertEqual(first[-1], "fallback")
        self.assertNotEqual(first[:2], second[:2])

    def test_context_excludes_too_small_backend(self):
        router = Router([{"name": "small", "model": "m", "max_context": 10}])
        self.assertEqual(router.candidates(11), [])

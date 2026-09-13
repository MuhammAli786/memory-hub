#!/usr/bin/env python3
"""Offline safety-net sweep that emits capture batches for transcript files."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from capture import parse_turns, select_new_turns


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--transcript-dir", type=Path, required=True)
    parser.add_argument("--maximum-sessions", type=int, default=5)
    args = parser.parse_args()
    batches = []
    for path in sorted(args.transcript_dir.glob("*.jsonl"))[-args.maximum_sessions:]:
        accepted, skipped = select_new_turns(parse_turns(path), set())
        batches.append({"session_id": path.stem, "accepted": accepted, "skipped": skipped})
    print(json.dumps({"batches": batches}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

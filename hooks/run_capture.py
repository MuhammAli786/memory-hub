#!/usr/bin/env python3
"""Read a lifecycle envelope from standard input and print an offline capture batch."""
from __future__ import annotations

import json
import sys
from pathlib import Path

from capture import parse_turns, select_new_turns


def main() -> int:
    try:
        envelope = json.load(sys.stdin)
        if envelope.get("event") not in {"session.stop", "session.end"}:
            raise ValueError("unsupported event")
        session_id = str(envelope["session_id"])
        transcript = Path(str(envelope["transcript_path"]))
        turns = parse_turns(transcript)
        accepted, skipped = select_new_turns(turns, set(envelope.get("known_turn_ids", [])))
        print(json.dumps({"session_id": session_id, "accepted": accepted, "skipped": skipped}))
    except Exception:
        print("{}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

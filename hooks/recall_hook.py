#!/usr/bin/env python3
"""Fail-open policy layer for session-start recall.

The private retrieval adapter supplies L0, L1, and L2 records in the input
envelope. This module has no service client and no deployment configuration.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timedelta, timezone


def current(item: dict, cutoff: datetime) -> bool:
    stamp = item.get("updated_at") or item.get("created_at") or item.get("timestamp")
    if not isinstance(stamp, str):
        return False
    try:
        value = datetime.fromisoformat(stamp.replace("Z", "+00:00"))
    except ValueError:
        return False
    return value.tzinfo is not None and cutoff <= value <= datetime.now(timezone.utc)


def render(records: dict, age_hours: int = 24) -> str:
    cutoff = datetime.now(timezone.utc) - timedelta(hours=age_hours)
    lines: list[str] = []
    manual = records.get("manual_persona")
    if isinstance(manual, str) and manual.strip():
        lines.extend(["# Reviewed Working Preferences", manual.strip()])
    for title, key in (("Recent Conversation", "l0"), ("Established Facts", "l1"), ("Work Scenes", "l2")):
        items = [item for item in records.get(key, []) if isinstance(item, dict) and current(item, cutoff)]
        if items:
            lines.append(f"# {title}")
            lines.extend(str(item.get("content") or item.get("summary") or "").strip() for item in items)
    return "\n\n".join(line for line in lines if line)


def main() -> int:
    try:
        records = json.load(sys.stdin)
        print(json.dumps({"additionalContext": render(records)}))
    except Exception:
        print("{}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

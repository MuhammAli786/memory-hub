#!/usr/bin/env python3
"""Report wiki pages whose frontmatter update date is older than a threshold."""
from __future__ import annotations

import argparse
from datetime import date, timedelta
from pathlib import Path


def value(text: str, key: str) -> str:
    for line in text.splitlines():
        if line.startswith(f"{key}:"):
            return line.split(":", 1)[1].strip()
    return ""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--wiki", type=Path, required=True)
    parser.add_argument("--days", type=int, default=30)
    args = parser.parse_args()
    cutoff = date.today() - timedelta(days=args.days)
    stale = []
    for path in sorted(args.wiki.rglob("*.md")):
        if path.name in {"index.md", "activity-log.md", "log.md"}:
            continue
        try:
            updated = date.fromisoformat(value(path.read_text(encoding="utf-8", errors="replace"), "last-updated"))
        except ValueError:
            stale.append((path, "missing-or-invalid-date"))
            continue
        if updated < cutoff:
            stale.append((path, updated.isoformat()))
    for path, reason in stale:
        print(f"STALE {path.as_posix()} {reason}")
    print(f"stale={len(stale)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

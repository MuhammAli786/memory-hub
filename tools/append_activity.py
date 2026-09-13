#!/usr/bin/env python3
"""Append one timestamped fact to a local wiki activity log."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--log", required=True, type=Path)
    parser.add_argument("--message", required=True)
    args = parser.parse_args()
    message = args.message.strip()
    if not message:
        raise SystemExit("message must not be empty")
    if not args.log.is_file():
        raise SystemExit("activity log does not exist")
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    with args.log.open("a", encoding="utf-8") as handle:
        handle.write(f"\n- {stamp} — {message}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

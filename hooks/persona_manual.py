#!/usr/bin/env python3
"""Safely read or replace the reviewed block in a local persona document."""
from __future__ import annotations

import argparse
from pathlib import Path

BEGIN = "<!-- PERSONA:MANUAL:BEGIN -->"
END = "<!-- PERSONA:MANUAL:END -->"


def block(text: str) -> tuple[int, int]:
    start, end = text.find(BEGIN), text.find(END)
    if start < 0 or end < 0 or end <= start or text.count(BEGIN) != 1 or text.count(END) != 1:
        raise ValueError("expected exactly one reviewed persona block")
    return start, end + len(END)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("persona", type=Path)
    parser.add_argument("action", choices=("show", "replace"))
    parser.add_argument("--source", type=Path)
    args = parser.parse_args()
    current = args.persona.read_text(encoding="utf-8")
    start, end = block(current)
    if args.action == "show":
        print(current[start:end])
        return 0
    if not args.source:
        raise SystemExit("replace requires --source")
    replacement = args.source.read_text(encoding="utf-8").strip()
    if BEGIN not in replacement or END not in replacement:
        raise SystemExit("replacement must contain reviewed persona markers")
    block(replacement)
    args.persona.write_text(current[:start] + replacement + current[end:], encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

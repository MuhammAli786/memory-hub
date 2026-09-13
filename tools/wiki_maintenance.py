#!/usr/bin/env python3
"""Rebuild the wiki index or report frontmatter and link defects."""
from __future__ import annotations

import argparse
import re
from pathlib import Path

REQUIRED = ("title", "type", "sources", "related", "created", "last-updated")
LINK = re.compile(r"\[\[([^\]]+)\]\]")


def frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---", 4)
    if end < 0:
        return {}
    return {key.strip(): value.strip() for line in text[4:end].splitlines() if ":" in line for key, value in [line.split(":", 1)]}


def pages(wiki: Path) -> list[tuple[Path, dict[str, str]]]:
    return [(path, frontmatter(path.read_text(encoding="utf-8", errors="replace"))) for path in wiki.rglob("*.md") if path.name not in {"index.md", "log.md", "activity-log.md"}]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=("index", "lint"))
    parser.add_argument("--wiki", type=Path, required=True)
    args = parser.parse_args()
    found = pages(args.wiki)
    names = {path.stem for path, _ in found}
    if args.action == "index":
        grouped: dict[str, list[str]] = {}
        for path, meta in found:
            grouped.setdefault(meta.get("type", "unclassified"), []).append(meta.get("title", path.stem))
        lines = ["# Wiki Index", ""]
        for kind in sorted(grouped):
            lines.extend([f"## {kind.title()}", *[f"- [[{title}]]" for title in sorted(grouped[kind])], ""])
        (args.wiki / "index.md").write_text("\n".join(lines), encoding="utf-8")
        print(f"indexed {len(found)} pages")
        return 0
    defects = []
    for path, meta in found:
        missing = [key for key in REQUIRED if key not in meta or not meta[key]]
        if missing:
            defects.append({"path": path.as_posix(), "kind": "frontmatter", "detail": ", ".join(missing)})
        for target in LINK.findall(path.read_text(encoding="utf-8", errors="replace")):
            if target not in names:
                defects.append({"path": path.as_posix(), "kind": "broken-link", "detail": target})
    for defect in defects:
        print(f"{defect['kind']}: {defect['path']}: {defect['detail']}")
    print(f"defects={len(defects)}")
    return 1 if defects else 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Conservative publication gate for this sanitized reference repository."""
from __future__ import annotations

import re
import sys
from pathlib import Path


RULES = {
    "address": r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
    "network overlay": r"tail" + r"scale",
    "process configuration access": r"(?:os\.(?:environ|getenv)|process\.env)",
    "private home path": r"/(?:Users|home)/",
    "credential assignment": r"(?i)(?:api[_-]?key|password|secret|token)\s*[:=]\s*[^<\s][^\s]*",
    "authorization header": r"(?i)authorization\s*[:=]",
}
SKIP = {".git", "node_modules", "coverage", "local-data", "local-config", "vendor"}
TEXT_SUFFIXES = {".md", ".py", ".ts", ".mjs", ".json", ".toml", ".yaml", ".yml", ".txt", ".gitignore"}


def main(root: Path) -> int:
    findings: list[str] = []
    for path in root.rglob("*"):
        if not path.is_file() or any(part in SKIP for part in path.parts) or path.suffix not in TEXT_SUFFIXES:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for label, expression in RULES.items():
            if re.search(expression, text):
                findings.append(f"{path.relative_to(root)}: {label}")
    if findings:
        print("REJECTED")
        print("\n".join(findings))
        return 1
    print("PASS: no configured credential, address, overlay, home path, or process configuration access found")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(Path(sys.argv[1] if len(sys.argv) == 2 else ".").resolve()))

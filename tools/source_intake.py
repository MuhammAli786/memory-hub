#!/usr/bin/env python3
"""Copy user-selected text sources into raw/ with deterministic deduplication."""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--destination", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    args = parser.parse_args()
    if not args.source.is_dir():
        raise SystemExit("source must be a directory")
    args.destination.mkdir(parents=True, exist_ok=True)
    known = json.loads(args.manifest.read_text(encoding="utf-8")) if args.manifest.exists() else {"items": []}
    hashes = {item["sha256"] for item in known["items"]}
    written = duplicates = 0
    for path in sorted(item for item in args.source.rglob("*") if item.is_file()):
        value = digest(path)
        if value in hashes:
            duplicates += 1
            continue
        target = args.destination / path.name
        suffix = 1
        while target.exists():
            target = args.destination / f"{path.stem}-{suffix}{path.suffix}"
            suffix += 1
        shutil.copy2(path, target)
        known["items"].append({"path": target.as_posix(), "sha256": value, "source_name": path.name})
        hashes.add(value)
        written += 1
    args.manifest.parent.mkdir(parents=True, exist_ok=True)
    args.manifest.write_text(json.dumps(known, indent=2), encoding="utf-8")
    print(json.dumps({"written": written, "duplicates": duplicates}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

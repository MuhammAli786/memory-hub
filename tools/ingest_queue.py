#!/usr/bin/env python3
"""Create a review queue from raw sources without calling a model."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--minimum-bytes", type=int, default=400)
    parser.add_argument("--large-bytes", type=int, default=22000)
    args = parser.parse_args()
    items = []
    for path in sorted(item for item in args.raw.rglob("*") if item.is_file()):
        size = path.stat().st_size
        if size < args.minimum_bytes:
            status = "skip-thin"
        elif size > args.large_bytes:
            status = "review-large"
        else:
            status = "ready"
        items.append({"path": path.as_posix(), "bytes": size, "status": status})
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps({"items": items}, indent=2), encoding="utf-8")
    print(json.dumps({"items": len(items), "ready": sum(item["status"] == "ready" for item in items)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Run the safe local portion of a periodic vault-maintenance cycle."""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def run(command: list[str]) -> int:
    result = subprocess.run(command, check=False)
    return result.returncode


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    args = parser.parse_args()
    root = args.root.resolve()
    local = root / "local-data"
    local.mkdir(exist_ok=True)
    queue = run([sys.executable, str(root / "tools" / "ingest_queue.py"), "--raw", str(root / "raw"), "--output", str(local / "ingest-queue.json")])
    stale = run([sys.executable, str(root / "automation" / "stale_pages.py"), "--wiki", str(root / "wiki")])
    graph = run([sys.executable, str(root / "automation" / "graph_refresh.py"), "--root", str(root), "--output", str(root / "graphify-out" / "graph.json"), "--lock", str(local / "graph-refresh.lock")])
    status = "SUCCESS" if queue == stale == graph == 0 else "PARTIAL"
    print(f"{status} vault cycle queue={queue} stale={stale} graph={graph}")
    return 0 if status == "SUCCESS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

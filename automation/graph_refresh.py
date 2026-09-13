#!/usr/bin/env python3
"""Run one local graph build guarded by an exclusive lock file."""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--lock", type=Path, required=True)
    args = parser.parse_args()
    args.lock.parent.mkdir(parents=True, exist_ok=True)
    try:
        descriptor = os.open(args.lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError:
        print("BLOCKED graph refresh already running")
        return 0
    try:
        os.write(descriptor, str(os.getpid()).encode())
        os.close(descriptor)
        script = Path(__file__).parents[1] / "tools" / "build_code_graph.py"
        result = subprocess.run([sys.executable, str(script), "--root", str(args.root), "--output", str(args.output)], check=False)
        print("SUCCESS graph refresh" if result.returncode == 0 else "FAILED graph refresh")
        return result.returncode
    finally:
        args.lock.unlink(missing_ok=True)


if __name__ == "__main__":
    raise SystemExit(main())

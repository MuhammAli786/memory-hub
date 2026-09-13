#!/usr/bin/env python3
"""Inspect or explicitly reconcile a private container deployment."""
from __future__ import annotations

import argparse
import subprocess
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--compose", type=Path, required=True)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    if not args.compose.is_file():
        raise SystemExit("compose file does not exist")
    command = ["docker", "compose", "--file", str(args.compose)]
    if not args.apply:
        print("PLAN " + " ".join(command + ["ps"]))
        return 0
    result = subprocess.run(command + ["up", "--detach", "--build", "--remove-orphans"], check=False)
    print("SUCCESS container reconcile" if result.returncode == 0 else "FAILED container reconcile")
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())

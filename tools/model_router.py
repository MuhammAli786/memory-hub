#!/usr/bin/env python3
"""Configuration-file model router core with tiered round-robin selection.

This reference intentionally has no process-environment access, address, or
credential value. A private adapter supplies connection details at deployment.
"""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path


class Router:
    def __init__(self, backends: list[dict]):
        self.backends = [item for item in backends if item.get("enabled", True)]
        self.cursor = 0
        self.benched_until: dict[str, float] = {}

    def candidates(self, estimated_tokens: int) -> list[dict]:
        grouped: dict[int, list[dict]] = {}
        for backend in self.backends:
            if not backend.get("name") or not backend.get("model"):
                continue
            context = int(backend.get("max_context", 0))
            if context and estimated_tokens > context:
                continue
            tier = int(backend.get("tier", 0))
            if time.time() < self.benched_until.get(backend["name"], 0):
                continue
            grouped.setdefault(tier, []).append(backend)
        self.cursor += 1
        ordered: list[dict] = []
        for tier in sorted(grouped):
            group = grouped[tier]
            offset = self.cursor % len(group)
            ordered.extend(group[offset:] + group[:offset])
        return ordered

    def mark_transport_failure(self, backend: dict, cooldown_seconds: int) -> None:
        self.benched_until[backend["name"]] = time.time() + cooldown_seconds


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--estimated-tokens", type=int, required=True)
    args = parser.parse_args()
    data = json.loads(args.config.read_text(encoding="utf-8"))
    names = [backend["name"] for backend in Router(data.get("backends", [])).candidates(args.estimated_tokens)]
    print(json.dumps({"candidates": names}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

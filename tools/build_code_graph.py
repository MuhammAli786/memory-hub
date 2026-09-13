#!/usr/bin/env python3
"""Build a deterministic local Python symbol graph without external services."""
from __future__ import annotations

import argparse
import ast
import json
from datetime import datetime, timezone
from pathlib import Path


def dotted(node: ast.AST) -> str | None:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        parent = dotted(node.value)
        return f"{parent}.{node.attr}" if parent else node.attr
    return None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    nodes: list[dict[str, str]] = []
    edges: list[dict[str, str]] = []
    inventory: list[str] = []
    for path in sorted(args.root.rglob("*.py")):
        if any(part in {".git", "__pycache__", "node_modules"} for part in path.parts):
            continue
        relative = path.relative_to(args.root).as_posix()
        inventory.append(relative)
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=relative)
        except SyntaxError:
            continue
        module_id = f"module:{relative}"
        nodes.append({"id": module_id, "kind": "module", "source": relative})
        for item in ast.walk(tree):
            if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                symbol_id = f"symbol:{relative}:{item.name}:{item.lineno}"
                nodes.append({"id": symbol_id, "kind": type(item).__name__, "source": relative})
                edges.append({"source": module_id, "target": symbol_id, "kind": "declares"})
            elif isinstance(item, (ast.Import, ast.ImportFrom)):
                for alias in item.names:
                    edges.append({"source": module_id, "target": f"import:{alias.name}", "kind": "imports"})
            elif isinstance(item, ast.Call):
                name = dotted(item.func)
                if name:
                    edges.append({"source": module_id, "target": f"call:{name}", "kind": "calls"})
    graph = {"generated_at": datetime.now(timezone.utc).isoformat(), "inventory": inventory, "nodes": nodes, "edges": edges}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(graph, indent=2), encoding="utf-8")
    print(f"wrote {len(nodes)} nodes and {len(edges)} edges")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Small model-router server using CLI configuration and tiered candidates."""
from __future__ import annotations

import argparse
import json
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from model_router import Router


def request_backend(backend: dict, request_path: str, body: dict) -> tuple[int, dict, bytes]:
    base = backend.get("base_url")
    if not isinstance(base, str) or not base:
        raise ConnectionError("backend has no private base URL")
    payload = dict(body, model=backend["model"])
    maximum = backend.get("max_tokens")
    if isinstance(maximum, int):
        payload["max_tokens"] = min(int(payload.get("max_tokens", maximum)), maximum)
    headers = {"Content-Type": "application/json"}
    credential_file = backend.get("credential_file")
    if isinstance(credential_file, str) and credential_file:
        credential = Path(credential_file).read_text(encoding="utf-8").strip()
        if credential:
            headers["Authorization"] = f"Bearer {credential}"
    target = base.rstrip("/") + "/" + request_path.lstrip("/").split("/", 1)[-1]
    request = urllib.request.Request(target, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST")
    with urllib.request.urlopen(request, timeout=int(backend.get("timeout_seconds", 120))) as response:
        return response.status, dict(response.headers), response.read()


def serve(config: Path, bind: str, port: int, cooldown_seconds: int) -> None:
    data = json.loads(config.read_text(encoding="utf-8"))
    router = Router(data.get("backends", []))

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *_args) -> None:
            return

        def reply(self, status: int, body: bytes) -> None:
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self) -> None:
            if self.path.split("?", 1)[0] != "/health":
                self.reply(404, b'{"error":"not found"}')
                return
            state = [{"name": item["name"], "model": item["model"], "tier": item.get("tier", 0)} for item in router.backends]
            self.reply(200, json.dumps({"status": "ok", "backends": state}).encode("utf-8"))

        def do_POST(self) -> None:
            try:
                size = int(self.headers.get("Content-Length", "0"))
                body = json.loads(self.rfile.read(size) or b"{}")
                estimate = len(json.dumps(body)) // 4 + int(body.get("max_tokens", 0))
                failures = []
                for backend in router.candidates(estimate):
                    try:
                        status, _headers, payload = request_backend(backend, self.path, body)
                        if 200 <= status < 300:
                            self.reply(status, payload)
                            return
                        failures.append({"name": backend["name"], "status": status})
                        router.mark_transport_failure(backend, cooldown_seconds)
                    except (OSError, urllib.error.URLError, urllib.error.HTTPError) as error:
                        failures.append({"name": backend["name"], "error": str(error)})
                        router.mark_transport_failure(backend, cooldown_seconds)
                self.reply(503, json.dumps({"error": "no backend available", "failures": failures}).encode("utf-8"))
            except (ValueError, json.JSONDecodeError) as error:
                self.reply(400, json.dumps({"error": str(error)}).encode("utf-8"))

    ThreadingHTTPServer((bind, port), Handler).serve_forever()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--bind", required=True)
    parser.add_argument("--port", required=True, type=int)
    parser.add_argument("--cooldown-seconds", default=120, type=int)
    args = parser.parse_args()
    serve(args.config, args.bind, args.port, args.cooldown_seconds)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

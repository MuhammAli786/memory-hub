#!/usr/bin/env python3
"""Offline session capture primitives.

This module intentionally performs no configuration lookup and no service call.
An external, reviewed adapter decides whether and where accepted turns persist.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


def text_of(content: Any) -> str:
    if isinstance(content, str):
        return content.strip()
    if not isinstance(content, list):
        return ""
    return "\n".join(
        item.get("text", "").strip()
        for item in content
        if isinstance(item, dict) and item.get("type") == "text" and item.get("text", "").strip()
    )


def turn_id(user: str, assistant: str) -> str:
    return hashlib.sha256((user + "\0" + assistant).encode("utf-8")).hexdigest()


def parse_turns(transcript: Path) -> list[dict[str, str]]:
    turns: list[dict[str, str]] = []
    pending_user = ""
    for raw in transcript.read_text(encoding="utf-8").splitlines():
        try:
            event = json.loads(raw)
        except json.JSONDecodeError:
            continue
        if event.get("isSidechain"):
            continue
        kind = event.get("type")
        body = text_of((event.get("message") or {}).get("content"))
        if not body:
            continue
        if kind == "user":
            pending_user = body
        elif kind == "assistant" and pending_user:
            digest = turn_id(pending_user, body)
            turns.append({"turn_id": str(event.get("uuid") or digest), "content_hash": digest,
                          "user": pending_user, "assistant": body})
            pending_user = ""
    return turns


def select_new_turns(turns: list[dict[str, str]], known: set[str], *, minimum_characters: int = 80,
                     maximum_turns: int = 25) -> tuple[list[dict[str, str]], dict[str, int]]:
    substantive = [turn for turn in turns if len(turn["user"]) + len(turn["assistant"]) >= minimum_characters]
    window = substantive[-maximum_turns:]
    accepted = [turn for turn in window if turn["turn_id"] not in known and turn["content_hash"] not in known]
    return accepted, {
        "empty": len(turns) - len([turn for turn in turns if turn["user"] and turn["assistant"]]),
        "short": len(turns) - len(substantive),
        "known": len(window) - len(accepted),
        "outside_tail": len(substantive) - len(window),
    }

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


def pending_path(pending_dir: Path, session_id: str, turn_id_value: str) -> Path:
    """Return a safe, stable outbox path for one lifecycle turn."""
    digest = hashlib.sha256(f"{session_id}\0{turn_id_value}".encode("utf-8")).hexdigest()
    return pending_dir / f"{digest}.json"


def save_pending_prompt(pending_dir: Path, *, session_id: str, turn_id_value: str,
                        prompt: str, cwd: str = "") -> Path:
    """Durably stage a prompt before a lifecycle hook can receive its reply."""
    if not prompt.strip():
        raise ValueError("prompt must not be empty")
    path = pending_path(pending_dir, session_id, turn_id_value)
    pending_dir.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({
        "session_id": session_id,
        "turn_id": turn_id_value,
        "prompt": prompt.strip(),
        "cwd": cwd,
    }), encoding="utf-8")
    return path


def save_pending_reply(path: Path, assistant: str) -> dict[str, str]:
    """Complete a staged turn before any external persistence attempt.

    This is deliberately offline: adapters may now retry a fully preserved
    prompt/reply pair after a transport outage without reconstructing content.
    """
    if not assistant.strip():
        raise ValueError("assistant reply must not be empty")
    record = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(record.get("prompt"), str) or not record["prompt"].strip():
        raise ValueError("pending record has no prompt")
    record["assistant"] = assistant.strip()
    path.write_text(json.dumps(record), encoding="utf-8")
    return record


def replayable_pending(pending_dir: Path) -> list[dict[str, str]]:
    """Load only completed outbox records for a caller-owned retry adapter."""
    if not pending_dir.is_dir():
        return []
    completed: list[dict[str, str]] = []
    for path in sorted(pending_dir.glob("*.json"), key=lambda item: item.stat().st_mtime):
        try:
            record = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        required = ("session_id", "turn_id", "prompt", "assistant")
        if all(isinstance(record.get(key), str) and record[key].strip() for key in required):
            completed.append({key: record[key] for key in (*required, "cwd") if isinstance(record.get(key), str)})
    return completed


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

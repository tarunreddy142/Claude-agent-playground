"""Shared helpers for calling Claude and parsing structured JSON replies."""
from __future__ import annotations

import json
import os
import re

from anthropic import Anthropic

_DEFAULT_MODEL = "claude-sonnet-5"


def get_client() -> Anthropic:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError(
            "ANTHROPIC_API_KEY is not set. Copy .env.example to .env and add your key."
        )
    return Anthropic(api_key=api_key)


def get_model() -> str:
    return os.environ.get("CLAUDE_MODEL", _DEFAULT_MODEL)


def ask_for_json(system_prompt: str, user_prompt: str, *, max_tokens: int = 1500) -> dict:
    """Call Claude and parse a JSON object out of its reply.

    Every agent is instructed to reply with a single JSON object, so this
    strips any surrounding markdown fences before parsing.
    """
    client = get_client()
    response = client.messages.create(
        model=get_model(),
        max_tokens=max_tokens,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}],
    )
    text = "".join(block.text for block in response.content if block.type == "text")
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError(f"Expected a JSON object in the model reply, got:\n{text}")
    return json.loads(match.group(0))

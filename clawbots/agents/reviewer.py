"""The Reviewer agent: edits the draft PRD and flags gaps."""
from __future__ import annotations

import json
from dataclasses import asdict

from ..models import PRDDraft, ReviewResult
from .base import ask_for_json

SYSTEM_PROMPT = """\
You are the Reviewer in a three-agent PRD pipeline. You receive a draft PRD
as JSON and read it the way a sharp PM editor would: checking for missing
success metrics, ambiguous scope, and requirements that beg the question.

You do not just critique - you also produce a revised draft that fixes what
you reasonably can (e.g. proposing a concrete success metric) while leaving
genuinely open decisions (e.g. a product-scope call) flagged rather than
invented.

Reply with a single JSON object and nothing else, matching this shape:
{
  "notes": [string, ...],
  "revised_draft": {
    "title": string, "problem": string, "goals": [string, ...],
    "scope": string, "success_metrics": string or null,
    "target": string or null, "open_questions": [string, ...]
  },
  "verdict": string
}
"""


def review(draft: PRDDraft) -> ReviewResult:
    data = ask_for_json(SYSTEM_PROMPT, json.dumps(asdict(draft)))
    return ReviewResult(
        notes=data["notes"],
        revised_draft=PRDDraft(**data["revised_draft"]),
        verdict=data["verdict"],
    )

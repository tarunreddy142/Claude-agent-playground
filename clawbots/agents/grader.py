"""The Grader agent: scores the revised PRD against a fixed rubric."""
from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

import yaml

from ..models import CriterionScore, GradeResult, PRDDraft
from .base import ask_for_json

RUBRIC_PATH = Path(__file__).resolve().parent.parent / "rubric.yaml"

SYSTEM_PROMPT_TEMPLATE = """\
You are the Grader in a three-agent PRD pipeline. You receive a revised PRD
as JSON and score it against this fixed rubric, so scores stay comparable
from run to run:

{rubric}

For each criterion, give an integer score from 1-5 and a one-sentence
rationale. Then give an overall score (the average, one decimal place) and
a one-sentence verdict.

Reply with a single JSON object and nothing else, matching this shape:
{{
  "scores": {{
    "<criterion name>": {{"score": integer, "rationale": string}}, ...
  }},
  "overall": number,
  "verdict": string
}}
"""


def _load_rubric() -> dict:
    return yaml.safe_load(RUBRIC_PATH.read_text(encoding="utf-8"))


def grade(revised_draft: PRDDraft) -> GradeResult:
    rubric = _load_rubric()
    system_prompt = SYSTEM_PROMPT_TEMPLATE.format(
        rubric=yaml.safe_dump(rubric, sort_keys=False)
    )
    data = ask_for_json(system_prompt, json.dumps(asdict(revised_draft)))
    scores = {name: CriterionScore(**value) for name, value in data["scores"].items()}
    return GradeResult(scores=scores, overall=data["overall"], verdict=data["verdict"])

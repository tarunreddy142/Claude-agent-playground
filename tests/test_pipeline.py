"""Pipeline wiring tests. These mock the Claude calls, so no API key is needed."""
from __future__ import annotations

from unittest.mock import patch

from clawbots import pipeline
from clawbots.models import PRDDraft

_DRAFT = {
    "title": "Dark Mode Toggle",
    "problem": "Users have repeatedly requested dark mode across support and social channels.",
    "goals": ["Reduce eye strain", "Increase evening session length"],
    "scope": "Global toggle vs. per-page theming - undecided",
    "success_metrics": None,
    "target": "Before Q3 review",
    "open_questions": ["global vs. per-page?", "effort estimate?"],
}

_REVIEW = {
    "notes": [
        "Added a success metric: 30% of active users enable dark mode within 30 days.",
        "Flagged scope as blocking - needs a design decision before estimation.",
    ],
    "revised_draft": {**_DRAFT, "success_metrics": "30% adoption within 30 days of launch"},
    "verdict": "Needs one more pass before grading.",
}

_GRADE = {
    "scores": {
        "clarity": {"score": 4, "rationale": "Problem and goal are clearly stated."},
        "completeness": {"score": 2, "rationale": "Scope and effort are still open."},
    },
    "overall": 3.0,
    "verdict": "Solid first draft; scope ambiguity is the main blocker.",
}


def test_pipeline_wires_all_three_agents():
    with patch("clawbots.agents.drafter.ask_for_json", return_value=_DRAFT), patch(
        "clawbots.agents.reviewer.ask_for_json", return_value=_REVIEW
    ), patch("clawbots.agents.grader.ask_for_json", return_value=_GRADE):
        result = pipeline.run("dark mode - ppl keep asking on support tix...")

    assert isinstance(result.draft, PRDDraft)
    assert result.draft.title == "Dark Mode Toggle"
    assert result.review.revised_draft.success_metrics is not None
    assert result.grade.overall == 3.0
    assert set(result.grade.scores) == {"clarity", "completeness"}

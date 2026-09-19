"""Wires the three agents into a single draft -> review -> grade run."""
from __future__ import annotations

from dataclasses import dataclass

from .agents import drafter, grader, reviewer
from .models import GradeResult, PRDDraft, ReviewResult


@dataclass
class PipelineResult:
    notes: str
    draft: PRDDraft
    review: ReviewResult
    grade: GradeResult


def run(notes: str) -> PipelineResult:
    """Run notes through the Drafter, then the Reviewer, then the Grader."""
    draft_result = drafter.draft(notes)
    review_result = reviewer.review(draft_result)
    grade_result = grader.grade(review_result.revised_draft)
    return PipelineResult(
        notes=notes, draft=draft_result, review=review_result, grade=grade_result
    )

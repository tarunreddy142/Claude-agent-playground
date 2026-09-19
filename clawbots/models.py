"""Typed data structures shared across the Clawbots pipeline."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class PRDDraft:
    title: str
    problem: str
    goals: list[str]
    scope: str
    success_metrics: Optional[str]
    target: Optional[str]
    open_questions: list[str] = field(default_factory=list)


@dataclass
class ReviewResult:
    notes: list[str]
    revised_draft: PRDDraft
    verdict: str


@dataclass
class CriterionScore:
    score: int
    rationale: str


@dataclass
class GradeResult:
    scores: dict[str, CriterionScore]
    overall: float
    verdict: str

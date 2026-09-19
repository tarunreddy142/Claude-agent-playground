"""Command-line entry point: `python -m clawbots.cli run <notes-file>`."""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path

from dotenv import load_dotenv

from . import pipeline


def _print_report(result: pipeline.PipelineResult) -> None:
    print("=== 01 DRAFTER ===")
    print(json.dumps(asdict(result.draft), indent=2))

    print("\n=== 02 REVIEWER ===")
    for note in result.review.notes:
        print(f"- {note}")
    print(f"verdict: {result.review.verdict}")

    print("\n=== 03 GRADER ===")
    for name, score in result.grade.scores.items():
        print(f"{name}: {score.score}/5 - {score.rationale}")
    print(f"overall: {result.grade.overall}/5 - {result.grade.verdict}")


def _result_to_dict(result: pipeline.PipelineResult) -> dict:
    return {
        "notes": result.notes,
        "draft": asdict(result.draft),
        "review": {
            "notes": result.review.notes,
            "revised_draft": asdict(result.review.revised_draft),
            "verdict": result.review.verdict,
        },
        "grade": {
            "scores": {k: asdict(v) for k, v in result.grade.scores.items()},
            "overall": result.grade.overall,
            "verdict": result.grade.verdict,
        },
    }


def main(argv: list[str] | None = None) -> int:
    load_dotenv()
    parser = argparse.ArgumentParser(prog="clawbots")
    sub = parser.add_subparsers(dest="command", required=True)

    run_cmd = sub.add_parser("run", help="Run the pipeline on a notes file")
    run_cmd.add_argument("notes_file", type=Path)
    run_cmd.add_argument("--output", type=Path, default=None, help="Write JSON result here")

    args = parser.parse_args(argv)

    if args.command == "run":
        notes = args.notes_file.read_text(encoding="utf-8")
        result = pipeline.run(notes)
        _print_report(result)
        if args.output:
            args.output.write_text(
                json.dumps(_result_to_dict(result), indent=2), encoding="utf-8"
            )
        return 0

    return 1


if __name__ == "__main__":
    sys.exit(main())

# Clawbots

A small fleet of Claude-powered agents. One drafts a PRD from messy notes,
one reviews the draft, and a third grades the result against a fixed
rubric — three agents handing work down a line.

```
notes ── Drafter ──▶ draft PRD ── Reviewer ──▶ revised PRD + notes ── Grader ──▶ score card
```

## Why

Most "multi-agent" demos are one prompt wearing three hats. Clawbots is
deliberately a pipeline: each agent has a narrow job, a typed input, and a
typed output, and the next agent only ever sees what the previous one
produced. It's a small, inspectable playground for that hand-off pattern —
not a framework, just three agents and the plumbing between them.

- **Drafter** — turns unstructured notes into a structured PRD, and marks
  what it can't answer as an open question instead of inventing an answer.
- **Reviewer** — reads the draft like an editor: missing metrics, ambiguous
  scope, requirements that beg the question. Produces a revised draft, not
  just a critique.
- **Grader** — scores the revised PRD against a fixed rubric
  (`clawbots/rubric.yaml`), so scores are comparable draft to draft instead
  of one-off verdicts.

## Install

```bash
git clone https://github.com/<your-username>/clawbots.git
cd clawbots
python -m venv .venv && source .venv/bin/activate   # .venv\Scripts\activate on Windows
pip install -r requirements.txt
cp .env.example .env   # then add your own ANTHROPIC_API_KEY
```

Get a key at [console.anthropic.com](https://console.anthropic.com/). `.env`
is gitignored — the key never leaves your machine.

## Run

```bash
python -m clawbots.cli run examples/sample_notes.txt
```

`examples/sample_notes.txt`:

```
dark mode - ppl keep asking on support tix + twitter. check analytics
for dark-hours usage?? maybe not global toggle, per-page? talk to
design. want before Q3 review probably. no clue on effort
```

produces a draft PRD, the reviewer's notes and revision, and a rubric score
card, printed to stdout. Add `--output result.json` to also write the full
result as JSON.

## Test

The pipeline wiring is tested without hitting the API — `tests/test_pipeline.py`
mocks each agent's Claude call and checks that data flows through the three
stages correctly:

```bash
pip install -r requirements-dev.txt
pytest -v
```

## Layout

```
clawbots/
  agents/
    base.py       # shared Claude-call + JSON-parsing helper
    drafter.py     # 01 — notes -> draft PRD
    reviewer.py     # 02 — draft PRD -> revised PRD + notes
    grader.py     # 03 — revised PRD -> rubric score card
  models.py        # PRDDraft / ReviewResult / GradeResult dataclasses
  pipeline.py       # wires the three agents into one run
  cli.py          # `python -m clawbots.cli run <notes-file>`
  rubric.yaml       # the fixed grading rubric
examples/
  sample_notes.txt
tests/
  test_pipeline.py
```

## A note on the name

This project is a personal exploration of Claude-agent hand-off patterns.
"OpenClaw" gets used by a few different open-source multi-agent projects,
not one stable package — so rather than depend on something that might not
build the same way twice, Clawbots calls the Claude API directly through a
small orchestrator of its own. The agent-pipeline shape is the same idea.

## License

MIT — see [LICENSE](LICENSE).

# Prompt Log — Assignment 1: Calorie and Nutrition Tracker

## Entry 1 — Setup (Phase 0)
- Step: Phase 0 (Setup)
- Tool: Spec Kit (`specify init`), uv
- Prompt/command: `specify init sdd-cohort-six-project --ai copilot --script ps`
- Key output: Spec Kit scaffold created (.specify/, .github/)
- Issues hit:
  - `uv tool install specify-cli` initially failed building PyYAML under
    Python 3.15 (no prebuilt wheel, required MSVC build tools). Fixed by
    pinning `uv python install 3.12` and reinstalling specify-cli with
    `--python 3.12`.
  - Windows "python not found" Store alias blocked the bare `python`
    command. Fixed by disabling App Execution Aliases for
    python.exe/python3.exe, and pinning the project to Python 3.12 via
    `uv python pin 3.12`; now using `uv run python` / `uv run pytest`
    for all commands.
- My decision: proceeded with uv-managed Python 3.12 instead of system
  Python, to keep the environment reproducible and avoid PATH issues.
- Screenshot: screenshots/specify-check.png, screenshots/specify-init.png

## Entry 2 — Constitution (Phase 2)
- Step: Phase 2 (Constitution)
- Tool: GitHub Copilot (Spec Kit /speckit.constitution)
- Prompt: requested 7 principles (spec-first, test coverage, input
  validation, simplicity, no secrets, code standards, AI transparency)
  with why/how-applies for each, no implementation detail.
- Key output: constitution.md draft with all 7 principles present.
- My review/changes: added principle IDs (P-1..P-7) and a "How it's
  checked" line to every principle, since the generated draft had
  why/how-applies but no verification criterion. Bumped version to
  1.1.0 to reflect the content change.
- Decision: accepted the generated principles' substance as-is;
  modified structure/traceability only.
- Screenshot: screenshots/speckit-constitution.png

## Entry 3 — Clarification (Phase 3)
- Step: Phase 3 (Clarify)
- Tool: N/A (human mentor interaction, not AI)
- Action: Sent 13 clarification questions (grouped High/Medium/Lower
  impact) to the mentor acting as business owner.
- Mentor's reply (verbatim): "Output can be basic what all things you
  have considered that's our assignment. This is a good example.
  Produce whatever is suitable for you. But create md of all three
  things."
- My interpretation: the mentor authorized resolving each question
  independently via documented product judgment rather than answering
  them individually, with two constraints: (1) keep the implementation
  basic/simple, (2) document the reasoning behind every decision
  considered.
- My decision: converted all 13 questions into 14 assumptions (A-01
  through A-14) in docs/clarification-log.md, each with an explicit
  rationale. No individually mentor-confirmed decisions exist for this
  assignment; all are self-made assumptions under the mentor's general
  authorization, logged as such rather than presented as confirmed
  business rules.
- Screenshot: screenshots/mentor-reply.png (if available)
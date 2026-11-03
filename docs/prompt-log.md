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

## Entry 4 — Feature Specification
- Step: `/speckit.specify`
- Tool: GitHub Copilot (Spec Kit)
- Prompt used (verbatim):

  > Create a feature specification for a Calorie and Nutrition Tracker.
  >
  > Problem: Users want to track their daily food intake and see how it
  > compares with their nutrition goals. The system lets a single user
  > record meals, track calories and protein, set daily targets, and view
  > daily progress.
  >
  > Build the specification strictly from the following decisions. Do not
  > invent any business rule not listed here — if something is still
  > genuinely undecided, mark it [NEEDS CLARIFICATION] instead of guessing.
  >
  > Users:
  > - Single user, no accounts or authentication (A-01).
  > - Command-line interface (A-02).
  >
  > Meal entry:
  > - A meal has: name, calories (number), protein in grams (number), and a
  >   date (defaults to today, can be set to any past or present date, not
  >   future) (A-03, A-07).
  > - Calories and protein accept decimals up to 1 decimal place, rounded
  >   to 1 decimal place for storage and display (A-08).
  > - Zero is a valid value for calories or protein. Reject values above
  >   10,000 kcal or 1,000g protein per meal as implausible input (A-09).
  > - A meal can be deleted by its ID. Editing an existing meal is out of
  >   scope; correcting a mistake means deleting and re-adding (A-10).
  >
  > Targets:
  > - A user sets a daily calorie target and a daily protein target.
  >   Logging meals does not require a target to already be set (A-04).
  > - If a target is changed, it applies from that day forward only; past
  >   days keep whichever target was active on that day (A-05).
  >
  > Day and progress:
  > - A "day" is midnight-to-midnight local system time (A-06).
  > - The progress view for a given day shows: total calories consumed,
  >   total protein consumed, the target for that day (if any), and the
  >   remaining amount for each (target minus consumed, shown as a negative
  >   number when over target).
  > - Each of calories and protein gets a status label: "under", "met", or
  >   "over". "Met" includes a small tolerance: within 5 kcal of the
  >   calorie target, or within 1g of the protein target, counts as "met".
  > - If no meals are logged for a day, consumed totals show as 0 (A-12).
  > - If no target is set for a day, show consumed totals only, with "no
  >   target set" instead of remaining/status (A-12).
  >
  > Validation:
  > - Reject missing required fields, negative calories/protein, non-numeric
  >   input, and values above the stated maximums, with a clear error
  >   message. Reject targets below 0. On any invalid input, no data is
  >   written or changed (ties to constitution P-3).
  >
  > Explicitly out of scope (do not include in the spec):
  > - Micronutrients (fat, carbs, fiber, vitamins).
  > - A food/nutrition database or barcode lookup.
  > - Exercise or calorie-burn tracking.
  > - Weight tracking.
  > - Multiple users, accounts, or sharing.
  > - Editing a meal, history/weekly views beyond a single day (A-13, A-14).
  >
  > Output format:
  > - Users/actors, in scope / out of scope, business rules (BR-##),
  >   functional requirements (FR-### — "The system MUST..."),
  >   non-functional requirements/constraints, a glossary (define "day",
  >   "meal", "target", "progress"), and acceptance criteria.
  > - Every acceptance criterion must have a unique ID (AC-###), be written
  >   as Given/When/Then, describe an observable outcome (not
  >   implementation), and include both normal and negative/edge cases
  >   (e.g. invalid input, no target set, exactly at target, over target).
  > - Do not include any implementation detail (no database schema, no
  >   specific libraries, no file structure) — behavior and outcomes only.

- Initial output: Created a behavior-only specification at
  `specs/001-calorie-nutrition-tracker/spec.md` with business rules,
  functional requirements, uniquely identified acceptance criteria,
  user/scope sections, constraints, glossary, and a quality checklist.
- Follow-up clarification prompt: “Please choose answers, or leave any field
  blank/decline and I will keep its clarification marker in the
  specification.” Asked: (1) target limits/precision — same as meal values,
  non-negative only, or other; (2) target setting — together, independently
  with partial progress, independently with no comparison unless both exist,
  or other; (3) unknown meal ID deletion — clear error or no-op.
- User response: `targetLimits=same_as_meals`,
  `targetSetting=together`, `unknownMealId=clear_error`.
- Final output: Updated the specification and checklist with those decisions.
  The final spec has 12 business rules, 14 functional requirements, and 21
  acceptance criteria. The checklist is complete.
- Decision: Accepted the clarifications and incorporated them into the spec.
- Reasoning: This resolves the genuinely undecided behavior with direct user
  decisions and keeps the final requirements traceable and testable.

## Entry 5 — Implementation Plan (Phase 4)
- Step: `/speckit.plan`
- Tool: GitHub Copilot (Spec Kit)
- Prompt used (verbatim):

  > Create a technical implementation plan for the Calorie and Nutrition
  > Tracker, based on the baselined specification (spec v1.0).
  >
  > Technology: Python 3.12, standard library only where practical, a
  > simple CLI (argparse or typer — pick whichever is more idiomatic for
  > Spec Kit's conventions), SQLite via the built-in sqlite3 module for
  > storage, and pytest for testing. Favor the simplest design that
  > satisfies the spec (constitution P-4) — no web framework, no ORM, no
  > external services.
  >
  > The plan must include:
  > 1. Technology choice and rationale (why this fits a fundamentals-scope
  >    single-user CLI tool).
  > 2. Components/modules and their responsibilities (e.g. a data model
  >    layer, a validation layer, a repository/storage layer, a service
  >    layer with the business logic, and a CLI layer).
  > 3. Data model: tables/entities, fields, types, units, and constraints,
  >    directly reflecting BR-01 through BR-12 in the spec (meals, targets,
  >    their fields, and validation ranges).
  > 4. CLI command surface: the commands needed to add a meal, delete a
  >    meal, set targets, and view progress for a given day.
  > 5. A processing sequence (numbered steps) for each of these three main
  >    flows: (a) recording a meal, (b) setting/changing targets, (c)
  >    viewing progress for a day.
  > 6. Data handling: how dates and the local day boundary (BR-07) are
  >    handled, how values are rounded to one decimal place for storage
  >    and display (BR-03/BR-05), and how the "met" tolerance (BR-11) is
  >    calculated.
  > 7. An error-handling table: condition | detection point | user-facing
  >    response | effect on stored data (should always be "unchanged" per
  >    constitution P-3) | related AC.
  > 8. A mapping from each functional requirement (FR-001 through FR-014)
  >    to the component(s) responsible for satisfying it.
  > 9. Risks and trade-offs of this approach.
  >
  > Do not restate the acceptance criteria — reference them by ID where
  > relevant. Keep the design as simple as the spec allows; do not add
  > speculative features, caching, concurrency handling, or configuration
  > options not required by the spec.

- Clarification prompt: Asked which daily target maximum to use because the
  working spec.md said 20,000 kcal / 2,000 g while the spec v1.0 review
  record said 10,000 kcal / 1,000 g.
- User response: `baseline_10000_1000`.
- Output received: Created `plan.md`, `research.md`, `data-model.md`,
  `contracts/cli.md`, and `quickstart.md`. Chose `argparse`, SQLite via
  `sqlite3`, and integer-tenths storage with `Decimal` validation; mapped
  FR-001–FR-014 to modules and added flow sequences, error handling, AC test
  trace, and design risks.
- Decision: Accepted the baseline selection and plan design. Recorded the
  discrepancy as R-03/R-04 in `docs/review-record.md`, aligned spec v1.0 to
  the reviewed 10,000 kcal / 1,000 g target bounds and AC-006a/AC-006b, and
  marked the spec baseline status.
- Reasoning: The user's explicit choice prioritizes the reviewed baseline
  over a later working-copy drift. Aligning the spec before planning keeps
  the plan, data constraints, and AC references internally consistent.
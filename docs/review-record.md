# Review Record — Calorie and Nutrition Tracker Specification

## Findings

| R-ID | Location | Issue type | Finding | Correction | Verified by |
|------|----------|-----------|---------|------------|-------------|
| R-01 | AC-006 | Untestable (mixed) | AC-006 combined a positive case (meal exactly at max, accepted) and a negative case (meal over max, rejected) in a single Given/When/Then, which doesn't map cleanly to one automated test. | Split into AC-006a (accept at boundary) and AC-006b (reject above maximum). | Self (Anuj Sharma)|
| R-02 | BR-05 / FR-006 / AC-010 | Reviewed, confirmed (not a defect) | Daily target upper bound (10,000 kcal / 1,000 g) equals the per-meal maximum. Initially flagged as a possible unreviewed AI default, but verified against prompt-log Entry 4: this was a deliberate answer (`targetLimits=same_as_meals`) to Spec Kit's own clarification follow-up, not a silent invention. | None — confirmed as an intentional decision; logged as A-15 in the clarification log. | Self (Anuj Sharma) |
| R-03 | BR-05 / FR-006 / AC-010 | Baseline reconciliation | The working spec had diverged from the reviewed v1.0 baseline, showing daily target maximums of 20,000 kcal / 2,000 g, although the baseline record and the user's planning clarification confirm 10,000 kcal / 1,000 g. | Restore the reviewed v1.0 bounds in the specification before planning. | User decision in this planning session |
| R-04 | AC-006 | Baseline reconciliation | The working spec combined acceptance of values at the meal maximum with rejection above the maximum, despite the review finding R-01 documenting the approved split into AC-006a and AC-006b. | Restore the two separately testable acceptance criteria from the baseline review. | Review record R-01 |
| R-05 | plan.md, Processing Sequence A/B, Error Handling table | Plan addition beyond spec | The plan validates malformed date strings (invalid YYYY-MM-DD format), a case not explicitly enumerated in BR-12 or covered by any AC. | Accepted as sensible input-layer robustness; no spec/AC change needed since it falls under FR-013's general "reject invalid input" intent. Will be covered by a test case in the validation plan (Phase 8) without a dedicated AC ID. | Self (Anuj Sharma)  |

| R-06 | tasks.md, T007 | Incorrect completion check | T007's "Done when" check referenced test_repository_schema.py (T004's check) instead of verifying T007's actual deliverable (service/domain error types), making it possible to mark T007 complete without testing it. | Corrected T007's Done-when to defer error-type verification to T012/T017/T021's rejection assertions, matching the pattern already used by T008/T009. | Self (Anuj Sharma) |

| R-07 | cli.py, run() | Missing command handler (false-positive tests) | The set-targets CLI handler was not added to run()'s if/elif chain, so set-targets silently fell through to the "Unknown command" error path. Two of the four T016 tests (invalid-value and above-maximum) initially passed anyway, because an "unknown command" error also returns a non-zero exit code — they were not actually testing validation. | Added the missing set-targets handler to run(). Re-ran tests and confirmed the success-path test (which could only pass with correct routing) now passes, and no test's stderr shows "Unknown command." | Self (Anuj Sharma) |

| R-08 | tests/cli/test_progress_command.py | Test design error — target effective_date postdated the meal date | `test_progress_with_target_shows_calories_and_protein_lines` recorded a meal dated 2026-11-03 but called set-targets with no `today` override, so the target's effective_date became the real system date (2026-11-04) — after the meal date. Per BR-06, a target applies only from its effective date forward, so `get_progress` for 2026-11-03 correctly reported "no target set." The test's expectation, not the code, was wrong. | Rewrote the test to use the real system "today" consistently across the add-meal, set-targets, and progress calls (all default to today when no date/--date is given), removing the hardcoded past date that caused the mismatch. Re-ran and confirmed the test now passes for the right reason — asserting on actual Calories/Protein lines, not just exit code. | Self (Anuj Sharma) |

## Cross-check against clarification log
All of A-01 through A-17 were checked against the spec. Every decision
and assumption in the clarification log is reflected correctly in the
spec's business rules, functional requirements, or acceptance criteria.
No contradictions found.

## Cross-check against Spec Kit's generated quality checklist
Spec Kit's own checklist
(`specs/001-calorie-nutrition-tracker/checklists/`) was reviewed as a
second, independent check. All items pass: no implementation details,
no remaining `[NEEDS CLARIFICATION]` markers, requirements testable,
acceptance criteria unique and Given/When/Then, normal/negative/boundary
scenarios covered, scope bounded, every FR has a corresponding AC. Its
notes line matches the manually-traced decisions A-15/A-16/A-17. No new
issues surfaced that the manual review above did not already cover.

## Baseline
- Previous version: spec v0.1 (initial /speckit.specify output, with
  Entry 4's clarification follow-up incorporated)
- Changes made at review: AC-006 split into AC-006a/AC-006b (R-01)
- **Baseline approved for planning: spec v1.0**
- Date: 2026-11-03
- Approved by: Anuj Sharma(self-review, assignment permits self-verification
  with mentor as available escalation point)
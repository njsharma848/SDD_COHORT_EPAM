# Calorie and Nutrition Tracker Constitution

## Purpose
This constitution defines the operating principles for a small, fundamentals-level calorie and nutrition tracker. It ensures the project remains aligned to its specification, protects correctness, and preserves disciplined, transparent collaboration.

## Core Principles

### P-1. Specification-First
Short statement: The specification is the source of truth.
Why it matters: Without a clear contract, work can drift, duplicate effort, and produce inconsistent results.
How it applies here: All code and tests must trace back to the approved specification. Any change to scope or acceptance criteria is recorded before implementation changes.
How it's checked: Every functional requirement and acceptance criterion in the spec maps to at least one task in `tasks.md`. Any edit to the spec after it is baselined is recorded in `docs/review-record.md` before the corresponding code changes.

### P-2. Test Coverage for Business Rules
Short statement: Every business rule and acceptance criterion must be covered by an automated test.
Why it matters: Business rules define user-visible correctness, and untested rules are easy to break silently.
How it applies here: Rules covering daily targets, meal totals, comparisons against goals, and invalid input must each have explicit automated test coverage.
How it's checked: Every acceptance criterion (AC-###) has at least one corresponding test named `test_tc###_ac###_...`. The traceability matrix in `docs/` shows no acceptance criterion without a linked test.

### P-3. Input Validation and Safe Failure
Short statement: All user input must be validated, and invalid input must fail clearly without changing existing data.
Why it matters: Invalid data can create incorrect nutrition totals and undermine trust in the application.
How it applies here: Missing values, negative numbers, invalid formats, and impossible inputs must be rejected with a clear error. Existing records remain unchanged when invalid input is submitted.
How it's checked: A test exists for each invalid and boundary case per field in `docs/validation-plan.md`. Each such test asserts both the error returned and that prior data is unchanged.

### P-4. Simplicity Appropriate to Scope
Short statement: Prefer the simplest design that satisfies the specification.
Why it matters: Small projects become fragile when they add speculative features or unnecessary complexity.
How it applies here: We will implement only what the current specification requires for daily tracking of calories and protein, and avoid features not justified by the project goals.
How it's checked: No component, dependency, or feature appears in `plan.md` without a corresponding requirement in `spec.md`. The plan is reviewed against the spec before implementation starts.

### P-5. No Secrets in the Repository
Short statement: No passwords, tokens, or API keys are ever committed.
Why it matters: Secret leakage creates serious security risk and undermines the integrity of the project.
How it applies here: Any required configuration values are managed through environment variables or a local .env file that is excluded from version control.
How it's checked: `.gitignore` covers `.env` and any credential files. The repository is scanned for secrets before each push.

### P-6. Code Standards
Short statement: Python code follows PEP 8, uses type hints, and is organized into small, single-responsibility modules.
Why it matters: Clear, consistent code is easier to review, test, and maintain.
How it applies here: All code should be readable, explicit, and structured around a single responsibility rather than broad or mixed-purpose modules.
How it's checked: Code is linted (e.g. `ruff` or `flake8`) and type-checked before each commit. Each module is reviewed for single responsibility.

### P-7. Transparent AI Collaboration
Short statement: All AI-assisted steps are logged with the prompt used, the output received, and whether it was accepted, modified, or rejected.
Why it matters: AI-generated work must remain accountable, reviewable, and understandable.
How it applies here: Any AI-assisted guidance or code contribution is recorded with the prompt, the response, and the reasoning behind the final decision.
How it's checked: `docs/prompt-log.md` has an entry for every AI-assisted step, cross-checked against the commit history for that step.

## Governance
This constitution governs the project's work. Compliance is required before any change is considered complete. If a proposal conflicts with specification integrity, test coverage, safe validation, scope discipline, or transparent collaboration, it must be revised or explicitly approved before implementation continues.

**Version**: 1.1.0 | **Ratified**: 2026-11-03 | **Last Amended**: 2026-11-03
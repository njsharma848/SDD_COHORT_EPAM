\# Prompt Log — Assignment 1: Calorie and Nutrition Tracker



\## Entry 1 — Setup

\- Step: Phase 0 (Setup)

\- Tool: Spec Kit (`specify init`), uv

\- Prompt/command: `specify init sdd-cohort-six-project --ai copilot --script ps`

\- Key output: Spec Kit scaffold created (.specify/, .github/)

\- Issues hit:

&#x20; - `uv tool install specify-cli` initially failed building PyYAML under

&#x20;   Python 3.15 (no prebuilt wheel, required MSVC build tools).

&#x20;   Fixed by pinning `uv python install 3.12` and reinstalling specify-cli

&#x20;   with `--python 3.12`.

&#x20; - Windows "python not found" Store alias blocked bare `python` command.

&#x20;   Fixed by disabling App Execution Aliases for python.exe/python3.exe,

&#x20;   and pinning the project to Python 3.12 via `uv python pin 3.12`;

&#x20;   now using `uv run python` / `uv run pytest` for all commands.

\- My decision: proceeded with uv-managed Python 3.12 instead of system

&#x20; Python, to keep the environment reproducible and avoid PATH issues.

\- Screenshot: screenshots/specify-check.png, screenshots/specify-init.png


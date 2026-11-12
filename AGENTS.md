# AGENTS.md

steerwright: one skill, `skills/steerwright/`. `scripts/sw.py` is the whole tool (registry, discover, pages, reviews, up/down). Design: `ai-docs/plans/2026-11-09-design.md`. State: `ai-docs/HANDOFF.md`, log `ai-docs/log.md`.

- Public repo (since 2026-11-12). No hosted CI; run the tests locally: `python -m unittest discover -s tests`.
- Scripts: standard library only, Python 3.9+, UTF-8, LF. Every change gets a test. Tests use scratch homes (`STEERWRIGHT_HOME`, `ASKWRIGHT_HOME`, `CHAINWRIGHT_HOME`, `GRINDWRIGHT_HOME`), never the real ones.
- Read-only over sibling plugins' state. Kill processes by PID only.
- Plain short sentences, no em dashes, relative links. No AI attribution anywhere.

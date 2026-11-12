## Layout

- `skills/steerwright/SKILL.md`: the skill.
- `skills/steerwright/scripts/sw.py`: the script, standard library only.
- `skills/steerwright/references/`: notes on project management history, terms, charts, rituals, creative and solo work, AI tools and books.
- `tests/test_sw.py`: unit tests.
- `evals/`: skill evals.
- `ai-docs/`: handoff, log and plans.

## Tests

```sh
python -m unittest discover -s tests
```

On 0.4.0 this runs 14 tests, all passing.

## Rules

- Read-only over sibling plugins.
- Stop processes by PID only.
- Pages bind 127.0.0.1.
- No AI attribution in commits or files.

The skill is an evergreen unit: its research state is in `evergreen.json`, `RESEARCH.md`, `CHANGELOG.md` and `LEARNINGS.md` beside SKILL.md.

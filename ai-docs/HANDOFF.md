# steerwright HANDOFF

Status: in progress (step 3 of the kickoff order partly done)

## Where things are
- Plugin folder: D:/m4bwa/Claude/Projects/Ai/steerwright (no git yet).
- Script: skills/steerwright/scripts/sw.py 0.1.0. Design: ai-docs/plans/2026-11-09-design.md. Log: ai-docs/log.md.
- References written (citations unverified): skills/steerwright/references/{history,glossary,charts,rituals,ai-and-pm-now,creative-and-solo,books}.md.
- Test registry only: a session scratchpad STEERWRIGHT_HOME; the real ~/.steerwright is untouched.

## Waiting on Mark
- askwright set D:/m4bwa/Claude/Projects/Ai/steerwright/ask/steerwright-setup (7 questions: unit, wip, stall, home, name, repo, schedule). Read with `ask.py read`. Unanswered or "not sure" answers are never filled with the guess; keep using the guess only where the work can be redone cheaply.

## Next (in order)
1. Read the setup answers; apply them (grouping into portfolios, WIP limit, stall weeks, home, name).
2. Speed: cache gather() results (per project, keyed on mtimes, TTL ~5 min) so the main page loads in under 2 s.
3. `sw.py apply-review` reading review answers; milestones and risks in the registry; flow charts from git/log for projects without a ledger.
4. Run `up`, `down`, `shortcut` for real; then `discover --apply` into the real registry.
5. Unit tests (tests/test_sw.py: flow, monte_carlo, health, discover folding with fake homes).
6. Verification pass on references (open every URL, fix dates and facts); make the skill an evergreen unit (evergreen.json, RESEARCH.md search plan, volatile claims).
7. SKILL.md hub (full), evals (evergreen-test), worth check, README with banner, SECURITY.md, LICENSE, wiki.
8. everscout beat project-management (private).
9. Repo: private m4bwav/steerwright, PRs merged after checks, tag and release, add to mark-local, update installed plugin. Add to plugin-backlog existing-plugins.md.

## Stop and ask (askwright) before
Making the repo public, writing into another plugin's state, adding a scheduled task, publishing to any registry.

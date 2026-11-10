# steerwright HANDOFF

Status: in progress (Next items 1, 2, 4 and most of 5 done in session 2)

## Where things are
- Plugin folder: D:/m4bwa/Claude/Projects/Ai/steerwright, local git repo (main), no GitHub remote yet.
- Script: skills/steerwright/scripts/sw.py 0.2.0. Design: ai-docs/plans/2026-11-09-design.md. Log: ai-docs/log.md. Tests: tests/test_sw.py (`python -m unittest tests/test_sw.py`).
- Real registry: ~/.steerwright/projects.json (22 projects, 21 active, WIP 8, stall 8 weeks). Desktop shortcut D:/m4bwa/OneDrive/Desktop/steerwright.cmd.
- References written (citations unverified): skills/steerwright/references/*.md.

## Waiting on Mark
- Nothing blocking. Setup answers (ask/steerwright-setup) are all in and applied.

## Next (in order)
1. Rename command (`sw.py rename`), then fix "Tiny Colony" (SpaceDeckBuilder2) and "tiny-colony-2" (voicewright-lab/ask_pilot); diagnose the ~12 s first load of the detached server.
2. `sw.py apply-review` reading review answers; milestones and risks in the registry; flow charts from git/log for projects without a ledger.
3. More tests: discover folding with fake sibling homes, review set build.
4. Verification pass on references (open every URL, fix dates and facts); make the skill an evergreen unit (evergreen.json, RESEARCH.md search plan, volatile claims).
5. SKILL.md hub (full), evals (evergreen-test), worth check, README with banner, SECURITY.md, LICENSE, wiki.
6. everscout beat project-management (private).
7. Repo: private m4bwav/steerwright, PRs merged after checks, tag and release, add to mark-local, update installed plugin. Add to plugin-backlog existing-plugins.md.
8. First real weekly reviews: 21 active vs WIP 8; put the table/keep calls on askwright review pages (manual trigger only, per Mark).

## Stop and ask (askwright) before
Making the repo public, writing into another plugin's state, adding a scheduled task, publishing to any registry.

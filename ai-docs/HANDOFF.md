# steerwright HANDOFF

Status: in progress (session 4: evals file written, first four reviews served-ready)

## Where things are
- Plugin folder: D:/m4bwa/Claude/Projects/Ai/steerwright, private GitHub repo m4bwav/steerwright (main), v0.3.0 released, installed as steerwright@mark-local, listed in plugin-backlog existing-plugins.md.
- Script: skills/steerwright/scripts/sw.py 0.3.0. Design: ai-docs/plans/2026-11-09-design.md. Log: ai-docs/log.md. Tests: `python -m unittest tests/test_sw.py` (10, pass). Evals: evals/evals.json (7 cases, not yet run).
- Real registry: ~/.steerwright/projects.json (22 projects, 21 active, WIP 8, stall 8 weeks). Desktop shortcut D:/m4bwa/OneDrive/Desktop/steerwright.cmd.

## Waiting on Mark
- Review sets (askwright, open with `sw.py up` or the desktop shortcut): ~/.steerwright/reviews/steer-get-title-at-url-2026-11-09, steer-dotnetrandomnamegenerator-2026-11-09, steer-universegenerator-2026-11-09, steer-seeded-random-utilities-2026-11-09. Next session: `sw.py apply-review` on any answered ones.
- Flag only: "tiny-colony-2" renamed "voicewright-lab ask pilot" (small ruling).

## Next (in order)
1. `sw.py apply-review` for answered review sets; if still 21 active vs WIP 8, review the quiet ones (Sammy homework) next.
2. Run evals/evals.json with evergreen-test (scratch STEERWRIGHT_HOME fixture), then evergreen-worth.
3. everscout beat project-management (private): read the everscout-beat skill first.
4. Wiki for the private repo.
5. README banner only if the repo goes public (ask first).

## Stop and ask (askwright) before
Making the repo public, writing into another plugin's state, adding a scheduled task, publishing to any registry.

# steerwright HANDOFF

Status: in progress (session 3: Next 1-4 done, 5 partly)

## Where things are
- Plugin folder: D:/m4bwa/Claude/Projects/Ai/steerwright, private GitHub repo m4bwav/steerwright (main), v0.3.0 released, installed as steerwright@mark-local, listed in plugin-backlog existing-plugins.md.
- Script: skills/steerwright/scripts/sw.py 0.3.0. SKILL.md hub, plugin.json, README, SECURITY, LICENSE, evergreen unit files in place. Design: ai-docs/plans/2026-11-09-design.md. Log: ai-docs/log.md. Tests: tests/test_sw.py (`python -m unittest tests/test_sw.py`).
- Real registry: ~/.steerwright/projects.json (22 projects, 21 active, WIP 8, stall 8 weeks). Desktop shortcut D:/m4bwa/OneDrive## Waiting on Mark
- Nothing blocking. Flag: "tiny-colony-2" renamed "voicewright-lab ask pilot" (small ruling).

## Next (in order)
1. Evals: evals/evals.json (triggers, decoys, action cases) run with evergreen-test; worth check.
2. everscout beat project-management (private): read the everscout-beat skill first.
3. Wiki for the private repo.
4. First real weekly reviews: 21 active vs WIP 8; `sw.py review` the stalled ones (get-title-at-url, DotNetRandomNameGenerator, UniverseGenerator, seeded-random-utilities), tell Mark, `apply-review` next session.
5. README banner if the repo goes public (ask first).

es) and tell Mark; `sw.py apply-review` next session.
5. README banner when/if the repo goes public.

## Stop and ask (askwright) before
Making the repo public, writing into another plugin's state, adding a scheduled task, publishing to any registry.

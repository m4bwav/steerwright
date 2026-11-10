# steerwright HANDOFF

Status: in progress (session 3: Next 1-4 done, 5 partly)

## Where things are
- Plugin folder: D:/m4bwa/Claude/Projects/Ai/steerwright, local git repo (main), no GitHub remote yet.
- Script: skills/steerwright/scripts/sw.py 0.3.0. SKILL.md hub, plugin.json, README, SECURITY, LICENSE, evergreen unit files in place. Design: ai-docs/plans/2026-11-09-design.md. Log: ai-docs/log.md. Tests: tests/test_sw.py (`python -m unittest tests/test_sw.py`).
- Real registry: ~/.steerwright/projects.json (22 projects, 21 active, WIP 8, stall 8 weeks). Desktop shortcut D:/m4bwa/OneDrive/Desktop/steerwright.cmd.
- References verified 2026-11-09 (about 16 lines still marked unverified).

## Waiting on Mark
- Creating the private GitHub repo: `gh repo create m4bwav/steerwright --private --source . --push` was refused by the auto-mode classifier (2026-11-09). Mark runs it or allows it; private was his answer on ask/steerwright-setup.
- Flag: "tiny-colony-2" was renamed "voicewright-lab ask pilot" (small ruling).

## Next (in order)
1. Evals: evals/evals.json (triggers, decoys, action cases) and run them with evergreen-test; worth check (evergreen-worth).
2. everscout beat project-management (private): read the everscout-beat skill first.
3. Repo: after the repo exists, push, add to mark-local marketplace, install, add to plugin-backlog existing-plugins.md; tag v0.3.0 and release. Wiki after that.
4. First real weekly reviews: 21 active vs WIP 8; run `sw.py review` for the quietest (stalled: get-title-at-url, DotNetRandomNameGenerator, UniverseGenerator, seeded-random-utilities) and tell Mark; `sw.py apply-review` next session.
5. README banner when/if the repo goes public.

## Stop and ask (askwright) before
Making the repo public, writing into another plugin's state, adding a scheduled task, publishing to any registry.

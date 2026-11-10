# steerwright HANDOFF

Status: in progress (session 6: six reviews served, sw.py fixes, first beat scan)

## Where things are
- Plugin folder: D:/m4bwa/Claude/Projects/Ai/steerwright, private GitHub repo m4bwav/steerwright (main), v0.3.0 released, installed as steerwright@mark-local, listed in plugin-backlog existing-plugins.md.
- Script: skills/steerwright/scripts/sw.py 0.3.0. Design: ai-docs/plans/2026-11-09-design.md. Log: ai-docs/log.md. Tests: `python -m unittest tests/test_sw.py` (10, pass). Evals: skills/steerwright/evals/evals.json 7/7 pass (single run each, subagent proxy; skills/steerwright/TESTS.md T-20261109-1). Worth: UNPROVEN (lite only).
- Real registry: ~/.steerwright/projects.json (backup projects.pre-collectives.json). 14 active vs WIP 8, stall 8 weeks.
- everscout beat project-management (private): D:/m4bwa/Claude/Projects/Ai/indie-ai-scout/beats/project-management/, data ~/.everscout/data/project-management/. First scan done 2026-11-09 (3 notes); 12 books as leads, no Open Library ids yet.
- Wiki drafts: wiki-draft/ (8 pages). Repo has no .wiki.git yet.

## Rulings
- 2026-11-09 (Mark): projects grouped into two collectives, each counting as ONE active project: "AI plugins" (all *wright and evergreen/Claude plugin projects, plus evergreen-upkeep) and "Open source software" (seeded-random-utilities, get-title-at-url, DotNetRandomNameGenerator, UniverseGenerator, universe-generator-ts, package-backlog/jsr-publish, package-modernization). Done with existing `sw.py merge` + `rename`. A stall inside a collective is a note, not a review.
- The four OSS stall reviews are superseded (superseded.json in each set under ~/.steerwright/reviews); do not apply them.

## Waiting on Mark
- Save a first wiki page at https://github.com/m4bwav/steerwright/wiki/_new so the drafts can be pushed.
- Answer six review sets in ~/.steerwright/reviews (steer-*-2026-11-09 except the four superseded OSS ones); restart pages with `ask.py serve` if the servers have stopped.
- Flag only: four labs package repos added to Open source software.
- Flag only: "tiny-colony-2" renamed "voicewright-lab ask pilot" (small ruling).

## Next (in order)
1. Apply answered review sets (`sw.py apply-review`); if still unanswered, carry on.
2. evergreen-worth A/B against a no-skill baseline (needs a runner the classifier allows).
3. everscout-library pass on the project-management books (ids, sources); retry the three failed Reddit threads.
4. Push wiki drafts once the wiki exists.
5. Release 0.3.1 with the session-6 fixes (bump plugin.json, CHANGELOG, tag) when 1 lands or sooner.
6. README banner only if the repo goes public (ask first).

## Stop and ask (askwright) before
Making the repo public, writing into another plugin's state, adding a scheduled task, publishing to any registry.

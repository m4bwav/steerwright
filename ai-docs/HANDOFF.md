# steerwright HANDOFF

Status: in progress (session 8: 0.3.2 hides tabled/done/abandoned, favicon; sibling backlinks)

## Where things are
- Plugin folder: D:/m4bwa/Claude/Projects/Ai/steerwright, private GitHub repo m4bwav/steerwright (main), v0.3.2 released, installed as steerwright@mark-local, listed in plugin-backlog existing-plugins.md.
- Script: skills/steerwright/scripts/sw.py 0.3.2. Design: ai-docs/plans/2026-11-09-design.md. Log: ai-docs/log.md. Tests: `python -m unittest tests/test_sw.py` (13, pass). Evals: skills/steerwright/evals/evals.json 7/7 pass (single run each, subagent proxy; skills/steerwright/TESTS.md T-20261109-1). Worth: UNPROVEN (lite only).
- Real registry: ~/.steerwright/projects.json (backup projects.pre-collectives.json). Active below the old 14 after session 7 (3 tabled indefinitely, krea2 abandoned), WIP 8, stall 8 weeks. Repo traffic: registry `traffic_dashboard` = repo-traffic/data/dashboard.html, served at http://127.0.0.1:47630/traffic.
- everscout beat project-management (private): D:/m4bwa/Claude/Projects/Ai/indie-ai-scout/beats/project-management/, data ~/.everscout/data/project-management/. First scan done 2026-11-09 (3 notes); 12 books as leads, no Open Library ids yet.
- Wiki drafts: wiki-draft/ (8 pages). Repo has no .wiki.git yet.

## Rulings
- 2026-11-09 (Mark, review notes): tabling can be indefinite (no wake date); applied to Blackberry Blossom, Book learnings round 5, Sammy homework. Mark asked for the repo traffic site inside the dashboard: done as /traffic.
- 2026-11-09 (Mark): projects grouped into two collectives, each counting as ONE active project: "AI plugins" (all *wright and evergreen/Claude plugin projects, plus evergreen-upkeep) and "Open source software" (seeded-random-utilities, get-title-at-url, DotNetRandomNameGenerator, UniverseGenerator, universe-generator-ts, package-backlog/jsr-publish, package-modernization). Done with existing `sw.py merge` + `rename`. A stall inside a collective is a note, not a review.
- The four OSS stall reviews are superseded (superseded.json in each set under ~/.steerwright/reviews); do not apply them.

## Waiting on Mark
- Save a first wiki page at https://github.com/m4bwav/steerwright/wiki/_new so the drafts can be pushed.
- Flag only: four labs package repos added to Open source software.
- Flag only: "tiny-colony-2" renamed "voicewright-lab ask pilot" (small ruling).

## Next (in order)
1. Next weekly review round when due (`sw.py review`); apply answers with `sw.py apply-review`.
2. evergreen-worth A/B against a no-skill baseline (needs a runner the classifier allows).
3. everscout-library pass on the project-management books (ids, sources); retry the three failed Reddit threads.
4. Push wiki drafts once the wiki exists.
5. Optional: a per-project repo traffic panel (match a project's GitHub repo to repo-traffic's CSV rows) if Mark wants more than the full dashboard page.
6. README banner only if the repo goes public (ask first).

## Stop and ask (askwright) before
Making the repo public, writing into another plugin's state, adding a scheduled task, publishing to any registry.

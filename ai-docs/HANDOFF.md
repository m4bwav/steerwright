# steerwright HANDOFF

Status: in progress (session 14: idle until a review is due)

## Where things are
- 2026-11-13: v0.5.0 released and installed; live, steerwright runs inside askwright's server at http://127.0.0.1:47631/steer/ (server.json hosted_by askwright). The old standalone server on 47630 is gone.
- 2026-11-13: 0.5.0 serves its pages inside askwright's shared server (127.0.0.1:47631/steer/) when askwright is installed; otherwise its own server on 47630 or a free port. See the log.
- Plugin folder: D:/m4bwa/Claude/Projects/Ai/steerwright, PUBLIC GitHub repo m4bwav/steerwright (since 2026-11-12; wiki live at 0.4.0, banner, social preview, Discussions) (main), v0.4.0 released, installed as steerwright@mark-local, listed in plugin-backlog existing-plugins.md.
- Script: skills/steerwright/scripts/sw.py 0.4.0. Design: ai-docs/plans/2026-11-09-design.md. Log: ai-docs/log.md. Tests: `python -m unittest tests/test_sw.py` (14, pass). Evals: skills/steerwright/evals/evals.json 7/7 pass (single run each, subagent proxy; skills/steerwright/TESTS.md T-20261109-1). Worth: UNPROVEN (lite only).
- Real registry: ~/.steerwright/projects.json (backup projects.pre-collectives.json). Active below the old 14 after session 7 (3 tabled indefinitely, krea2 abandoned), WIP 8, stall 8 weeks. Repo traffic: registry `traffic_dashboard` = repo-traffic/data/dashboard.html, served at http://127.0.0.1:47630/traffic.
- everscout beat project-management (private): D:/m4bwa/Claude/Projects/Ai/indie-ai-scout/beats/project-management/, data ~/.everscout/data/project-management/. First scan done 2026-11-09 (3 notes); 12 books as leads, no Open Library ids yet.
- Wiki: https://github.com/m4bwav/steerwright/wiki pushed from wiki-draft/ (clone .wiki.git, copy, push).

## Rulings
- 2026-11-09 (Mark, review notes): tabling can be indefinite (no wake date); applied to Blackberry Blossom, Book learnings round 5, Sammy homework. Mark asked for the repo traffic site inside the dashboard: done as /traffic.
- 2026-11-09 (Mark): projects grouped into two collectives, each counting as ONE active project: "AI plugins" (all *wright and evergreen/Claude plugin projects, plus evergreen-upkeep) and "Open source software" (seeded-random-utilities, get-title-at-url, DotNetRandomNameGenerator, UniverseGenerator, universe-generator-ts, package-backlog/jsr-publish, package-modernization). Done with existing `sw.py merge` + `rename`. A stall inside a collective is a note, not a review.
- The four OSS stall reviews are superseded (superseded.json in each set under ~/.steerwright/reviews); do not apply them.

## Waiting on Mark
- Flag only: which films are in the parking lot (lancers stays the active Films project). Add more with `sw.py park NAME --lot "Video projects"`.
- Flag only: four labs package repos added to Open source software.
- Flag only: "tiny-colony-2" renamed "voicewright-lab ask pilot" (small ruling).
- Flag only: musicwright merged into AI plugins (session 11). New project arvum-guitar-song (session 13) left standalone; merge into Arvum Electrum with `sw.py merge` if wanted. Active 10 vs WIP 8: pick ones to table or park when convenient.

## Next (in order)
1. Next weekly review round when due (`sw.py review`); apply answers with `sw.py apply-review`.
2. evergreen-worth A/B against a no-skill baseline (needs a runner the classifier allows).
3. everscout beat project-management: done through session 10 (indie-ai-scout 07610ee); next scan when the beat is due.
4. Keep the wiki in step with each release (wikiwright).
5. Optional: a per-project repo traffic panel (match a project's GitHub repo to repo-traffic's CSV rows) if Mark wants more than the full dashboard page.
6. Optional: list steerwright in plugin-backlog existing-plugins.md as public.

## Stop and ask (askwright) before
Making the repo public, writing into another plugin's state, adding a scheduled task, publishing to any registry.

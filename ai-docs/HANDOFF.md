# steerwright HANDOFF

Status: in progress (session 5: evals 7/7, beat created, wiki drafted, collectives applied)

## Where things are
- Plugin folder: D:/m4bwa/Claude/Projects/Ai/steerwright, private GitHub repo m4bwav/steerwright (main), v0.3.0 released, installed as steerwright@mark-local, listed in plugin-backlog existing-plugins.md.
- Script: skills/steerwright/scripts/sw.py 0.3.0. Design: ai-docs/plans/2026-11-09-design.md. Log: ai-docs/log.md. Tests: `python -m unittest tests/test_sw.py` (10, pass). Evals: evals/evals.json 7/7 pass (single run each, subagent proxy; skills/steerwright/TESTS.md T-20261109-1). Worth: UNPROVEN (lite only).
- Real registry: ~/.steerwright/projects.json (backup projects.pre-collectives.json). 14 active vs WIP 8, stall 8 weeks.
- everscout beat project-management (private): D:/m4bwa/Claude/Projects/Ai/indie-ai-scout/beats/project-management/, data ~/.everscout/data/project-management/. First scan not run; book list empty.
- Wiki drafts: wiki-draft/ (8 pages). Repo has no .wiki.git yet.

## Rulings
- 2026-11-09 (Mark): projects grouped into two collectives, each counting as ONE active project: "AI plugins" (all *wright and evergreen/Claude plugin projects, plus evergreen-upkeep) and "Open source software" (seeded-random-utilities, get-title-at-url, DotNetRandomNameGenerator, UniverseGenerator, universe-generator-ts, package-backlog/jsr-publish, package-modernization). Done with existing `sw.py merge` + `rename`. A stall inside a collective is a note, not a review.
- The four OSS stall reviews are superseded (superseded.json in each set under ~/.steerwright/reviews); do not apply them.

## Waiting on Mark
- Save a first wiki page at https://github.com/m4bwav/steerwright/wiki/_new so the drafts can be pushed.
- Flag only: "tiny-colony-2" renamed "voicewright-lab ask pilot" (small ruling).

## Next (in order)
1. 14 active vs WIP 8: run `sw.py review` on the quietest non-collective projects (sammy-homework, krea2, technique-harvest, blackberry-blossom, voicewright-lab-ask-pilot, book-learnings-round-5) and serve them; apply answered sets next session.
2. Add JsonPrettyPrinter (Ai/labs/DotNetJsonPrettyPrinter) and other package repos to "Open source software" if discover finds them.
3. sw.py fixes from evals: status reads the real askwright home under a scratch STEERWRIGHT_HOME ("asks 4"); review text "unknown days" for projects with no history; evergreen-worth looks for evals/ inside the skill folder (move or link the suite).
4. evergreen-worth A/B against a no-skill baseline.
5. First everscout-scan of project-management; add books to the beat.
6. Push wiki drafts once the wiki exists.
7. README banner only if the repo goes public (ask first).

## Stop and ask (askwright) before
Making the repo public, writing into another plugin's state, adding a scheduled task, publishing to any registry.

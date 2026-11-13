# steerwright log

## 2026-11-09
- Kickoff session (prompt: plugin-backlog/ai-docs/plans/2026-11-09-steerwright-kickoff-prompt.md). Name steerwright kept for now (small ruling, also on ask/steerwright-setup).
- Research pass by three subagents wrote skills/steerwright/references: history.md, glossary.md, charts.md, rituals.md, ai-and-pm-now.md, creative-and-solo.md, books.md. Caveat: the history/glossary and charts/rituals agents ran one search between them and opened no pages; only ai-and-pm-now.md rests on search results (summaries, not pages). Every "checked 2026-11-09" line is unverified until a verification pass opens the URLs. PMBOK 8 (Nov 2025, 6 principles, 7 domains) needs confirming on pmi.org. Height shut down 2025-09-24. Suggested WIP limit from research: 3 (+ about 5 items waiting on Mark).
- Built skills/steerwright/scripts/sw.py 0.1.0 (stdlib): discover, add, status, item, forecast, review, table, abandon, done, activate, wip, serve, up, down, shortcut. Tested against real state with a scratch STEERWRIGHT_HOME: discover found 63 projects after folding worktrees and clones; pages render (main 17 s, needs a cache); Arvum forecast 22 items left, 50 % 2027-01-04, 85 % ~2027-04; review set lints clean. `up`, `down` and `shortcut` not yet run.
- Design note: ai-docs/plans/2026-11-09-design.md.
- Open questions on ask/steerwright-setup (what counts as a project, WIP limit, stall weeks, registry home, name, repo visibility, scheduled review). Guesses in use meanwhile: group, 5, 4, ~/.steerwright, steerwright, private, manual.
- No git repo yet; no registry written to the real ~/.steerwright yet (waits on question `unit`).

## 2026-11-09 (session 2)
- Read ask/steerwright-setup: all 7 answered. group (matched guess), WIP 8 (guess was 5), stall 8 weeks (guess was 4), ~/.steerwright, keep name, private repo, manual reviews.
- sw.py 0.2.0: DEFAULT_WIP 8, STALL_WEEKS 8 (stored as registry `stall_weeks`, `sw.py stall [N]`); discover groups by GROUP_RULES (Plugins = .claude-plugin or skills/*/SKILL.md or plugin-backlog; Arvum Electrum; Films under D:/ComfyUI/output/video), `--no-group` to skip; `sw.py merge NAME... --into NAME`.
- gather() cache: in-process, keyed on name+paths, fingerprint of path/ai-docs/.git mtimes and sibling homes, TTL 300 s, RLock; the server warms it in a background thread at start. Direct main page: cold 2.3 s, warm 0.03 s. Known issue: the detached server's first load after start still takes ~12 s even after a 20 s wait (warm thread slower inside the detached process; not diagnosed).
- Real registry written: ~/.steerwright/projects.json, 23 projects, 22 after merging steerwright and finwright into Plugins by hand (small ruling). 21 active against WIP 8, so the first reviews should table some.
- Small ruling to flag: SpaceDeckBuilder2 shows as "Tiny Colony" (its askwright project name) and voicewright-lab/ask_pilot as "tiny-colony-2"; left as discovered, needs a rename command or Mark's word.
- Ran `up` (steerwright on 127.0.0.1:47630, askwright already up, chainwright and grindwright indexes built), `down`, `shortcut` (D:\m4bwa\OneDrive\Desktop\steerwright.cmd). All worked.
- tests/test_sw.py: 5 unittest cases (flow, monte_carlo, health bands, grouping, registry defaults + merge), all pass.
- git init (main), first commit; no GitHub repo yet.

## 2026-11-09 (session 3)
- sw.py 0.3.0: `rename` (old name kept as askwright alias), `apply-review` (keep stores next actions, table parses date + wake, abandon writes post-mortem, done; marks sets applied.json; unanswered sets left alone), `milestone`, `risk`, project-page sections for both, cumulative commits/log-entries proxy chart for projects without a ledger.
- Slow first load fixed: git subprocesses now use CREATE_NO_WINDOW (a DETACHED_PROCESS server opened a console per git call) and gather locks per project instead of one global lock. Detached first load 2.6 s (was ~12 s), then 0.04 s.
- Real registry: renamed "Tiny Colony" -> SpaceDeckBuilder2 and "tiny-colony-2" -> "voicewright-lab ask pilot" (small ruling on the second name; flag for Mark).
- Tests: 10 (added rename, review+apply, keep next actions, milestone/risk page, discover with fake sibling homes). All pass.
- Subagent verified references: 76 URLs checked; corrected METR, Asana, Notion, Kanban Guide (v2025.5), SAFe 6.0 (Mar 2023), PMBOK 8 (40 processes; 7th on sale to 2026-07-08), PRINCE2 7; ~16 lines marked (unverified). Wrote evergreen.json (7 volatile claims), RESEARCH.md, CHANGELOG.md, LEARNINGS.md, MAINTENANCE.md.
- Added SKILL.md hub, .claude-plugin/plugin.json 0.3.0, README (no banner yet; private), SECURITY.md, LICENSE (MIT), AGENTS.md, CLAUDE.md.
- `gh repo create m4bwav/steerwright --private` was refused by the auto-mode permission classifier; needs Mark to allow it or run it.
- Mark switched to manual mode; created private m4bwav/steerwright and pushed, added to mark-local marketplace, installed, tagged and released v0.3.0.

## 2026-11-09 (session 4)
- Fixed garbled HANDOFF.md (a path had been spliced into the Waiting section).
- Ran `sw.py review --no-serve` for the four stalled projects (get-title-at-url 25 d, DotNetRandomNameGenerator 28 d, UniverseGenerator 28 d, seeded-random-utilities 26 d); sets in ~/.steerwright/reviews, waiting on Mark.
- Wrote evals/evals.json: 3 triggers, 2 decoys (grindwright, one-off chart), 2 action cases on a scratch STEERWRIGHT_HOME. Not run yet. Registry shape note: projects is a dict keyed by slug with a `status` field.

## 2026-11-09 eval run
evergreen-test: 7/7 cases pass (one tester run each, scratch STEERWRIGHT_HOME); details in skills/steerwright/TESTS.md T-20261109-1. evergreen-worth --lite: UNPROVEN (no baseline A/B; worth expects evals/ in the skill folder). Next: baseline arm via `worth --ab` once a runner is allowed.

## 2026-11-09 (session 5)
- Review sets still unanswered. Subagents: evals 7/7 pass (54527a0, worth lite UNPROVEN), wiki drafted in wiki-draft/ (fbff2c3; .wiki.git missing), everscout beat project-management created (evergreen.json linked).
- Mark ruling (via coordinator): two collectives, "AI plugins" and "Open source software", each one active project. Applied with merge + rename; the four OSS reviews are marked superseded. Active 21 -> 14.
- Small ruling: evergreen-upkeep, package-backlog (jsr-publish) and package-modernization were placed in the collectives; Ai/Music (musicwright music projects) and blackberry-blossom were left standalone.
- Wrap-up: little to harvest; the eval oddities are on the Next list. The headless `claude -p` eval runner is refused by the auto-mode classifier, so evergreen-tester subagents stand in.

## 2026-11-09 (session 6)
- Served six review sets (sammy-homework, krea2, technique-harvest, blackberry-blossom, voicewright-lab-ask-pilot, book-learnings-round-5) in ~/.steerwright/reviews; each on its own askwright port (59164-59363). Unanswered.
- sw.py: review text says "No activity on record" instead of "unknown days"; evals moved to skills/steerwright/evals/ so evergreen-worth finds them; SKILL.md notes that STEERWRIGHT_HOME does not move sibling homes (small ruling: keep siblings independent rather than redirect them). Tests 10 pass.
- Small ruling: added labs/DotNetJsonPrettyPrinter, CachingServiceWithAOPSupport, IsImageUrlDotNet, TrailerClipperLib to "Open source software" (packages with wikis). Active still 14.
- Subagent ran the first everscout scan of project-management: 39 items, 16 sources, 3 notes; 12 books added to literature.md as leads (indie-ai-scout 6d2dd3e). Three Reddit threads failed in fetchwright.
- Worth A/B skipped: headless runner still refused. Wrap-up: own account only, nothing passed the gate beyond this log.

## 2026-11-09 (session 7)
- Applied all six answered review sets: Blackberry Blossom, Book learnings round 5 and Sammy homework tabled indefinitely (no wake date, per Mark's notes); krea2 abandoned ("we learned what we could for now"); Technique harvest kept; voicewright-lab ask pilot kept, next action "generate 32 distinguishable voices, 12 accents".
- Technique harvest's "next actions" answer was feedback, not actions: Mark could not see the project's docs in askwright. Small ruling: next action set to its continue prompt (run now and then). Fix in steerwright: review one-pagers now carry the HANDOFF head and continue prompt. The general askwright request (a tab that shows a project's docs) went to plugin-backlog as owed askwright work.
- sw.py 0.3.1: indefinite tabling (`table` without `--revisit`; review option "Table indefinitely"; a table answer with no date is indefinite instead of the old 6-week default); `sw.py traffic PATH` serves repo-traffic's built data/dashboard.html at /traffic with a back bar, linked from every page (Mark's request this session); apply-review skips superseded sets; `down` also stops steerwright's own server when `up` did not start it (the old server kept running old code). Tests 12 pass. Real registry points at D:/m4bwa/Claude/Projects/Ai/repo-traffic.
- The traffic page shows the last build; it does not run a capture. Rebuild with the repo-traffic skill.

## 2026-11-09 (session 8)
- Mark's request: filter out inactive or finished projects, add a favicon, backlinks from sibling plugin pages when steerwright is installed.
- sw.py 0.3.2: dashboard and `status` hide tabled, done and abandoned (closed list on the page, `/?all=1`, `status --all`); a tabled project whose revisit date is reached still shows (wake). SVG favicon at /favicon.svg. Tests 13 pass. Server restarted on 47630.
- Small ruling: "inactive" read as status tabled/abandoned, not active-but-idle; idle active projects stay visible because the stall review needs them seen.
- Backlinks: askwright 0.24.1, chainwright 0.7.1, grindwright 0.8.2 show a "steerwright" link when ~/.steerwright/server.json has a url; all released (tests pass). askwright ask.py section dividers shortened to stay under its 360 KB budget.

## 2026-11-09 (session 9)
- Not due: no stalled project, so no review round. Wiki still missing. Worth A/B still blocked. Subagent sent on the everscout-library pass (Next item 3).
- Mark's request: a project parking lot tab with a video projects sub-tab holding the Gray King film and his other major films, so he can pick one to keep improving. sw.py 0.4.0: status `parked` (`lot`, `note`), `sw.py park NAME --lot LOT --note`, Projects / Parking lot tabs, `/parking?lot=` sub-tabs; parked work stays off the main table, WIP count and stall reviews. Tests 14 pass.
- Real registry (backup projects.pre-parking.json): 14 films parked in lot "Video projects": Locke vs the Gray King, The Old Crash Site, Mentos Drop, The No-God Falls, The Sky Duel, Follow the Grain, Sempis Delta and Anwurat, The Library, Cartwheel, Siege news report, Dummy 13 brawl, Lovecraft shorts, Knight vs Hollow Knight, Cola flood. Small ruling: lancers ("The Charge") stays the active "Films" project; test folders (spear_sranc, depth tests) left out; notes come from the film memories and READMEs.
- Library pass (subagent): 12 books got Open Library ids, 3 Reddit threads recovered via fetchwright (indie-ai-scout 9b19ff5 after rebase, pushed). Left: second evidence per book, searches.md queries, latest tier. Wrap-up: nothing beyond this log passed the gate.

## 2026-11-09 (session 10)
- Not due: no stalled project. Wiki still missing. Worth A/B still blocked.
- Beat evidence pass (subagent, resumed after a restart): second source per book in literature.md, all 8 searches.md queries run (3 web notes; two from search summaries with estimated dates), latest tier empty and latest_checked 2026-11-09 (indie-ai-scout 07610ee). Next item 3 done. Wrap-up: nothing beyond this log passed the gate.

## 2026-11-09 (session 11)
- Not due: no stalled project. Wiki still missing. Worth A/B still blocked.
- Small ruling: musicwright merged into the "AI plugins" collective (Mark's rule covers every *wright plugin); its paths include Ai/Music. Backup ~/.steerwright/projects.pre-musicwright.json. Active now 9 against WIP 8 (still over by one; shown on the dashboard, Mark's call).
- Wrap-up: nothing beyond this log passed the gate.

## 2026-11-10 (session 12)
- Idle: no stalled project (all 9 active within 2 d), wiki .wiki.git still missing, worth A/B still blocked. Wrap-up: nothing beyond this log passed the gate.

## 2026-11-11 Works with

At the owner's request: a README "Works with" section, each entry naming the real handoff with a partner plugin (taken from the skills that name each other) and why the pair helps.

## 2026-11-12 (session 13)
- Idle: no stalled project, .wiki.git still missing, worth A/B still blocked. New active project discovered: arvum-guitar-song (active 10 vs WIP 8); left standalone, flagged for Mark (could join Arvum Electrum). Wrap-up: nothing beyond this log passed the gate.
- Mark asked: make public, create the wiki and hero images. Done: secrets scan clean; repo public with wiki and Discussions on; wiki created (placeholder Home via browser, then 8 drafts updated to 0.4.0 pushed, all live); README banner (Z-Image Turbo 1536x640, seed 41103, workflow and prompt in .github/images) and social preview (1280x640 centre crop) uploaded in Settings.

## 2026-11-12 (session 14)
- Idle: all 10 active projects green (newest activity 0-4 d), no review due. Worth A/B still blocked. Wrap-up: nothing beyond this log passed the gate.

## 2026-11-13 · one server (0.5.0)
- Mark asked for steerwright on askwright's single server, still running without askwright, and choosing another port when 47630 is taken. `render(path, query, base)` now builds every page without a server; askwright 0.29.0 mounts it at `/steer/`. `sw.py serve` registers there when askwright is installed (server.json `hosted_by: askwright`, and `down` leaves that process alone), else binds its own port exclusively (Windows SO_REUSEADDR had let it share a taken port) and falls back to a free one. Tests: OneServer (3).

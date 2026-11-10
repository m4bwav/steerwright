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

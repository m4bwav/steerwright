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

# steerwright log

## 2026-11-09
- Kickoff session (prompt: plugin-backlog/ai-docs/plans/2026-11-09-steerwright-kickoff-prompt.md). Name steerwright kept for now (small ruling, also on ask/steerwright-setup).
- Research pass by three subagents wrote skills/steerwright/references: history.md, glossary.md, charts.md, rituals.md, ai-and-pm-now.md, creative-and-solo.md, books.md. Caveat: the history/glossary and charts/rituals agents ran one search between them and opened no pages; only ai-and-pm-now.md rests on search results (summaries, not pages). Every "checked 2026-11-09" line is unverified until a verification pass opens the URLs. PMBOK 8 (Nov 2025, 6 principles, 7 domains) needs confirming on pmi.org. Height shut down 2025-09-24. Suggested WIP limit from research: 3 (+ about 5 items waiting on Mark).
- Built skills/steerwright/scripts/sw.py 0.1.0 (stdlib): discover, add, status, item, forecast, review, table, abandon, done, activate, wip, serve, up, down, shortcut. Tested against real state with a scratch STEERWRIGHT_HOME: discover found 63 projects after folding worktrees and clones; pages render (main 17 s, needs a cache); Arvum forecast 22 items left, 50 % 2027-01-04, 85 % ~2027-04; review set lints clean. `up`, `down` and `shortcut` not yet run.
- Design note: ai-docs/plans/2026-11-09-design.md.
- Open questions on ask/steerwright-setup (what counts as a project, WIP limit, stall weeks, registry home, name, repo visibility, scheduled review). Guesses in use meanwhile: group, 5, 4, ~/.steerwright, steerwright, private, manual.
- No git repo yet; no registry written to the real ~/.steerwright yet (waits on question `unit`).

# steerwright inbox handoff

Status: in progress (session 2 done: step B collectors)
Prompt: [steerwright-inbox-continue-prompt.md](../plans/steerwright-inbox-continue-prompt.md)

Step: C inbox page next (`/steer/inbox` in askwright's server, built on `inbox.collect()` in skills/steerwright/scripts/inbox.py), then release. Askwright set: none yet. Grind state: still not set up (do it first next session or drop it; one step per session has worked without it).
- 2026-11-19 session 1: survey written (ai-docs/notes/inbox-sources.md). Findings worth Mark's eye later, not acted on: chainwright has 96 dead test ledgers in Temp (`chain_index.py prune`), ~/.steerwright/server.json pid is stale, 74 empty wt folders.
Grant: 2026-11-19, Mark asked to chain these changes 20x; read as a bounded unattended run of up to 20 sessions (section 9 of the prompt).
- 2026-11-19 session 2: step B merged (PR #6, 7d2fdb2). `sw.py inbox` real run: 113 items, ~720 Mark-minutes (65 backlog, 21 unanswered ask sets, 14 handoff bullets, 7 stopped chains, 4 ask unused, 1 PR). 35 items map to no project (backlogs, PRs by repo): mapping PR repos and backlog folders to projects is open for C.

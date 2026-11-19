# steerwright inbox handoff

Status: in progress (session 3 done: step C page, released 0.7.2)
Prompt: [steerwright-inbox-continue-prompt.md](../plans/steerwright-inbox-continue-prompt.md)

Step: D one-click clearing next (buttons on /steer/inbox that call the owning tool's verb: open PR, open askwright set, ask.py consume). Live page: http://127.0.0.1:47631/steer/inbox. Askwright set: none yet. Grind state: still not set up (do it first next session or drop it; one step per session has worked without it).
- 2026-11-19 session 1: survey written (ai-docs/notes/inbox-sources.md). Findings worth Mark's eye later, not acted on: chainwright has 96 dead test ledgers in Temp (`chain_index.py prune`), ~/.steerwright/server.json pid is stale, 74 empty wt folders.
Grant: 2026-11-19, Mark asked to chain these changes 20x; read as a bounded unattended run of up to 20 sessions (section 9 of the prompt).
- 2026-11-19 session 2: step B merged (PR #6, 7d2fdb2). `sw.py inbox` real run: 113 items, ~720 Mark-minutes (65 backlog, 21 unanswered ask sets, 14 handoff bullets, 7 stopped chains, 4 ask unused, 1 PR). 35 items map to no project (backlogs, PRs by repo): mapping PR repos and backlog folders to projects is open for C.
- 2026-11-19 session 3: step C merged and released: PR #7 (page, 0.7.0), #8 and #9 (0.7.1, 0.7.2: askwright execs sw.py by path without sys.modules; `sw.sibling_module()` loads inbox.py). Installed 0.7.2, live page 200. 25 tests pass. Open: 19 'no project' decisions (backlog lines, PR repos) still unmapped; the tab count shows only once the cache exists.

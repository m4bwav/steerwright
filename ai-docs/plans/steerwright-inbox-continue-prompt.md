# steerwright inbox continue prompt

Work from `D:/m4bwa/Claude/Projects/Ai/steerwright` (make a worktree per the global rule before editing). State lives in `ai-docs/inbox/HANDOFF.md`, never in this file. The idle main chain (`ai-docs/plans/steerwright-continue-prompt.md`, `ai-docs/HANDOFF.md`) is separate: do not edit its HANDOFF except to add one pointer line to this chain.

chainwright-report: on

## Goal

Make steerwright the one place where Mark sees everything waiting on him and everything sessions left behind, across all his projects, and can clear it fast. This was ruled a steerwright feature, not a new plugin (see `D:/m4bwa/Claude/Projects/Ai/plugin-backlog/new-plugins.md`, entry "Waiting-on-Mark inbox (and leftover cleanup) -> steerwright"). Scope is deliberately large; build it in the order of section 4 so each step ships on its own.

The chain ends when steps A to J are released and installed, or Mark closes the rest. HANDOFF.md then says `Status: finished`.

## 1. Load state

1. Read `ai-docs/inbox/HANDOFF.md`, the end of `ai-docs/log.md`, the main `ai-docs/HANDOFF.md` (rulings and the live server), and `ai-docs/plans/2026-11-09-design.md`. Trust commits and logs over an older HANDOFF.
2. Read the skills that run this chain: chainwright, grindwright, steerwright, askwright, releasewright, quirkwright. Find their scripts through `installPath` in `C:/Users/m4bwa/.claude/plugins/installed_plugins.json`; never glob the plugin cache.
3. Standing rules are not repeated here. Sources: `C:/Users/m4bwa/.claude/CLAUDE.md` (PRs, merging, releases, attribution, worktrees, links, wrap-up, continue prompts), `D:/m4bwa/.claude/CLAUDE.md`, the chainwright SKILL.md, and the memory index `C:/Users/m4bwa/.claude/projects/d--m4bwa-Claude-Projects-Ai/memory/MEMORY.md` (package size budget, small rulings, tests always allowed, local servers over Artifacts, open status pages unasked, askwright full paths, no step letters in questions, don't relay the stale askwright hook line, kill by PID only, update installed plugins after a release).

## 2. Read answers

For the askwright set HANDOFF.md names, run `ask.py read`, act on answers, then `ask.py consume <set> --note "<what you did>"`. Unanswered and "not sure" stay open.

## 3. How the chain runs

- **chainwright**: one master session per run hands each item (a collector, a page, tests, an eval run) to a subagent in its own worktree, keeps the short report, and ends when context runs low. Run `chain.py check` on this file after any edit. At stop: `chain_report.py from-session`, then `chain_index.py build`, and name the page. Mark asked for an unattended run of up to 20 sessions; the driver line in section 9 is his go-ahead for exactly that bound.
- **grindwright** picks the work. State folder `ai-docs/inbox/grind` (pass `--state`). If no profile exists, set it up once with lanes collect, page, cleanup, tests, evals, docs, release, `"ask_route": "askwright"`, and one milestone per step in section 4. Loop `session start`, `next --claim`, do, `done` with evidence and oracle rung, until `session check` allows stopping.
- **steerwright** is the thing being built; its own registry, reviews and weekly ritual are Mark's. Never change project status from this chain.
- **askwright** carries questions: one set `steerwright-inbox` under `ai-docs/ask/`, real guesses with confidence, at most twelve, full paths, plain words (no step letters).

## 4. Order of work

Each step: design note paragraph in `ai-docs/plans/inbox-design.md`, tests first (`tests/`, stdlib unittest), build in `sw.py` (or a sibling module if `sw.py` passes ~1500 lines), docs in SKILL.md references, a PR merged per the global rule. Release after C, F and J at least.

**A. Survey.** Every source of "waiting on Mark" and its format: open PRs assigned to m4bwav or labelled needs-review (`gh search prs`), askwright sets unanswered and answered-but-unconsumed (`ask.py sweep`), chain HANDOFF "Waiting on Mark" sections and stop points (chainwright ledgers and `~/.chainwright/index.html` data), grindwright `WAITING.md` files, everkeep escalations, registry publishes and deploys awaiting go-ahead, the plugin and package backlogs' `#needs-mark` items, evergreen units due. And every kind of leftover: git worktrees whose branch is merged or gone (e.g. the `Ai/comfyui-gen-wt-*` folders), `_wt` folders, stale local branches, orphaned local dev servers, scratch dirs. Write `ai-docs/notes/inbox-sources.md` with path, format, owner plugin and a sample. Overlap check against chainwright's index, grindwright, askwright sweep, everkeep, releasewright: steerwright reads their state, never duplicates their logic.
**B. Collectors.** `sw.py inbox --json`: one normalised item per decision (source, project mapped to the registry, kind, age, link or full path, the one action that clears it, cost in Mark-minutes). Read-only, cached, each collector failing soft with a note.
**C. Inbox page** at `/steer/inbox` in the shared askwright server: oldest first, grouped by project and kind, filters, counts in the dashboard header, a "clears in under 2 minutes" lane. Opened in the browser unasked, with a copyable link (the server address is in the main HANDOFF). Release.
**D. One-click clearing** where the owning tool already has the verb: open the PR, open the askwright set, mark consumed. Buttons call the owning script; steerwright never writes another plugin's state itself.
**E. Leftover scan.** `sw.py tidy` dry run: worktrees (merged, clean, older than N days), branches, servers by PID with their owning session if known, scratch folders; each with why it is safe or why it is kept. Uses quirkwright for PIDs.
**F. Tidy apply.** `sw.py tidy --apply` removes only items whose dry-run verdict was safe, with a log and an undo note (branch SHAs kept). Never deletes uncommitted work, never kills by image name. Release.
**G. Weekly ritual hook-in.** The inbox and tidy summary join steerwright's weekly review page (counts, oldest items, what aged past a threshold); no new review questions without Mark.
**H. Age and load metrics.** Decisions waiting per week, median age, Mark-minutes queued, per project; feeds the existing flow charts.
**I. Evals and worth.** evergreen-test with a baseline for the new triggers ('what is waiting on me', 'clean up leftover worktrees'), evergreen-worth, tokenwright-skills on the grown SKILL.md.
**J. Docs and release.** README, wiki pages (wikiwright), CHANGELOG, release, install, `existing-plugins.md` and the backlog entry updated, log line.

## 5. Stop before anything that needs the owner

Question on the set, recorded in HANDOFF.md, carry on. These wait on Mark: running `tidy --apply` on real folders for the first time (show him the dry run first; after his yes, later runs need none); deleting a branch that exists on a remote; stopping a server that is not a leftover of this chain; changing his registry, collectives or review rules; a hook or scheduled task; any registry publish; a worth CUT.

## 6. Stop early

If HANDOFF.md says `Status: finished`, go straight to the end of section 7. If nothing is selectable and the rest waits on Mark, name the set and stop.

## 7. Hand over

End the grind session, run evergreen-wrapup if installed (failure reported, never blocking), add a line to `ai-docs/log.md`, update `ai-docs/inbox/HANDOFF.md`, then print the start command `Execute D:/m4bwa/Claude/Projects/Ai/steerwright/ai-docs/plans/steerwright-inbox-continue-prompt.md` and the folder to start in (`D:/m4bwa/Claude/Projects/Ai/steerwright`). State goes in HANDOFF.md, never in this file.

When this chain is finished (HANDOFF.md says `Status: finished`), it ends by continuing the existing idle steerwright chain: add a line to the main `ai-docs/HANDOFF.md` saying the inbox and tidy are released (version, what changed for the weekly review), set this HANDOFF's last line to `Next: the main chain`, then run the main chain prompt `ai-docs/plans/steerwright-continue-prompt.md` in this same session (or, if context is low, print the start command the main prompt's own hand-over step gives, instead of this chain's). The unattended driver also stops on finished; the next session it would start belongs to the main chain.

## 8. Unattended driver

Mark's bound: at most 20 sessions. Run from `D:/m4bwa/Claude/Projects/Ai/steerwright`:

```
python <chainwright installPath>/skills/chainwright/scripts/chain_loop.py ai-docs/plans/steerwright-inbox-continue-prompt.md --handoff ai-docs/inbox/HANDOFF.md --max-sessions 20 --max-hours 24 --log ai-docs/inbox/chain-loop.log --go
```

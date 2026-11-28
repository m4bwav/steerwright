# Changelog: steerwright

Every change to SKILL.md and its companions, newest first, each with the reason. Reasons cite findings in [RESEARCH.md](RESEARCH.md) (`R-`) and lessons in [LEARNINGS.md](LEARNINGS.md) (`L-`). State in `evergreen.json`. Protocol: MAINTENANCE.md.

Entry shape: `### C-20261123-1 · 2026-11-23 · 0.12.0: loading, paging and data UI on every page
because: Mark 2026-11-23 asked for loading indicators, paging and data presentation best practices on all internal plugin pages.
files: scripts/sw.py, scripts/inbox.py, tests/test_sw.py.
While the first cache warm pass runs, page routes return a loading shell (spinner, skeleton, role=status, aria-busy, elapsed seconds) that fetches the page with full=1 and shows Retry plus server-down text on failure. One table helper sorts headers (aria-sort), adds a filter and 25-row paging with "showing X-Y of N" and the page in the URL hash, shows relative dates with the absolute date in the tooltip, and clips long cells with a more button. Sticky headers, right-aligned tabular numbers, visible focus, reduced motion, a generated-at stamp, an empty state on the projects table and a Retry on the error page.

### C-YYYYMMDD-n · date · one-line summary`, then `because:`, `files:`, and a sentence on what changed.

### C-20261127-1 · 2026-11-27 · 0.12.1: read the per-event log
because: everlast 0.8.0 split ai-docs/log.md into ai-docs/log/, one file per event, so open PRs stop conflicting on the log.
files: scripts/sw.py, AGENTS.md.
Activity dates now also come from each event file in ai-docs/log/, and the cache fingerprint watches that folder.

### C-20261119-10 · 2026-11-19 · 0.11.0: inbox age and load metrics
because: inbox chain step H (ai-docs/plans/inbox-design.md).
files: scripts/inbox.py, scripts/sw.py, SKILL.md, tests/test_inbox.py.
Each fresh inbox run keeps a daily snapshot in inbox-history.jsonl. `sw.py inbox --metrics`, a folded section on /inbox and a chart on each project page show decisions waiting per week, Mark-minutes queued and median age, per project. Weeks before the first snapshot are backfilled from today's ages.

### C-20261119-9 · 2026-11-19 · 0.10.0: inbox and tidy on the weekly review
because: inbox chain step G (ai-docs/plans/inbox-design.md).
files: scripts/inbox.py, scripts/tidy.py, scripts/sw.py, SKILL.md, tests/test_inbox.py, tests/test_tidy.py.
Each review set's findings page gains a block with the project's waiting items, all projects' counts and aged items, and the last tidy dry run's counts. No new questions.

### C-20261119-8 · 2026-11-19 · 0.9.0: sw.py tidy --apply
because: inbox chain step F (ai-docs/plans/inbox-design.md).
files: scripts/tidy.py, scripts/sw.py, SKILL.md, tests/test_tidy.py.
`tidy --apply` removes only safe items, rechecking each first, and logs every step with its undo note to tidy-log.jsonl. It stays off until Mark sets tidy_apply_ok after seeing the dry run.

### C-20261119-7 · 2026-11-19 · sw.py tidy: leftover scan, dry run
because: inbox chain step E (ai-docs/plans/inbox-design.md).
files: scripts/tidy.py, scripts/sw.py, SKILL.md, tests/test_tidy.py.
New `sw.py tidy` lists leftover worktrees, wt folders, branches, local servers and scratch folders, each safe, ask or keep with the reason and an undo note. It deletes and kills nothing.

### C-20261119-6 · 2026-11-19 · 0.8.1: inbox code reloads after a plugin update
- because: 0.8.0 installed but askwright's long-lived server kept 0.7.2's inbox module (sys.modules cache), so the page showed no buttons
- files: scripts/sw.py (sibling_module), tests/test_inbox.py
A sibling module is reloaded when its file is in another folder or its mtime changed.

### C-20261119-5 · 2026-11-19 · 0.8.0: one-click clearing on the inbox page
- because: inbox step D: clear an item through the tool that owns it, without steerwright writing that tool's state
- files: scripts/inbox.py (ask_urls, clear_controls), SKILL.md, tests/test_inbox.py
Rows get an Open button (PR link, or the set's /s/<key>/ page read from askwright's session records and dashboard server.json) and copy buttons for `ask.py consume` and `ask.py dismiss`. The under-2-minutes lane now follows the filters.

### C-20261119-4 · 2026-11-19 · 0.7.2: inbox page loads when sw.py is not in sys.modules
- because: 0.7.1 still gave 500 live (KeyError 'steerwright_mounted'): askwright execs sw.py without registering the module
- files: scripts/sw.py (sibling_module), tests/test_inbox.py
The sibling gets this module as `sw` (a snapshot module when it is not registered), reset on every call so a reload of sw.py reaches it.

### C-20261119-3 · 2026-11-19 · 0.7.1: inbox page loads inside askwright's server
- because: /steer/inbox returned 500 (No module named 'inbox'): askwright loads sw.py by path, off sys.path
- files: scripts/sw.py (sibling_module), tests/test_inbox.py
Sibling modules load through `sibling_module()`, which puts the script folder on sys.path and registers the hosted sw as `sw`.

### C-20261119-2 · 2026-11-19 · 0.7.0: inbox page (`/steer/inbox`)
- because: user request 2026-11-19 (inbox chain step C)
- files: scripts/inbox.py (inbox_page), scripts/sw.py (route, tab), SKILL.md, tests/test_inbox.py
A Waiting on you tab and page: oldest first, grouped by project and kind, filter chips for project, kind and source, a lane of items that clear in under 2 minutes, counts in the tab from the cache only.

### C-20261119-1 · 2026-11-19 · inbox collectors (`sw.py inbox`)
- because: user request 2026-11-19 (one place for everything waiting on Mark; survey in ai-docs/notes/inbox-sources.md)
- files: scripts/inbox.py, scripts/sw.py, SKILL.md, tests/test_inbox.py
New read-only `sw.py inbox` gathers eight sources into one normalised list mapped to registry projects. Released in 0.7.0.

### C-20261116-1 · 2026-11-16 · 0.6.0: project page shows who is running and links askwright and grindwright
- because: user request 2026-11-16 (running-agents: Jennifer wants to see every agent at work in a project before she starts one; one click between the plugins' project pages)
- files: scripts/sw.py (askwright_project, askwright_page_links, who_is_running, project_page, askwright_projects), tests/test_sw.py
A project page has a Who is running section from askwright's agents.py (status, task, branch and folder, evidence; a failed read or missing askwright says so instead of an empty list) and links to the matching askwright project page and grindwright page when the askwright hub answers. askwright project records get their slug from the file name.

### C-20261114-1 · 2026-11-14 · 0.5.1: apply-review marks the review set used in askwright
- because: askwright's answer sweep (askwright 0.31.0) found all six applied 2026-11-09 weekly reviews still listed as unprocessed: apply-review wrote applied.json but never ran `ask.py consume`, so the week warning kept naming them
- files: scripts/sw.py (mark_consumed), tests/test_sw.py
apply-review now runs askwright's `consume` on each set it applies, with the decision as the note; it records `consumed` in its output and carries on when ask.py is absent. Pair: askwright answer-sweep chain.

### C-20261109-4 · 2026-11-09 · 0.4.0: parking lot tab
- because: Mark asked for a project parking lot tab with a video projects sub-tab (the Gray King film and his other major films) so he can choose one to keep improving
- files: scripts/sw.py, SKILL.md, tests/test_sw.py
New status `parked` with a `lot` and `note`; `sw.py park`; Projects / Parking lot tabs; `/parking?lot=` sub-tabs. Parked projects stay off the main table, the WIP count and stall reviews.

### C-20261109-3 · 2026-11-09 · 0.3.2: hide inactive and finished projects, favicon
- because: Mark asked that steerwright filter out inactive or finished projects and have a favicon
- files: scripts/sw.py, tests/test_sw.py
The dashboard and `sw.py status` show only live projects (active, or tabled with its revisit date reached); tabled, done and abandoned fold into a closed list on the page (`/?all=1` or `status --all` shows everything). Pages carry an SVG ship's-wheel favicon served at /favicon.svg.

### C-20261109-2 · 2026-11-09 · 0.3.1: indefinite tabling, repo traffic page, docs in reviews, down fix
- because: Mark's review answers (blackberry-blossom note "add indefinite tabling"; technique-harvest "make a tab where you can see the docs"); Mark's request to put the repo traffic site in the dashboard
- files: scripts/sw.py, SKILL.md, tests/test_sw.py
- Tabling without a date now parks a project with no revisit date (new review option "Table indefinitely"); `sw.py traffic` serves repo-traffic's built dashboard at /traffic with a link on every page; review one-pagers include the HANDOFF head and continue prompt; apply-review skips superseded sets; `down` also stops a steerwright server that `up` did not start.

### C-20261109-1 · 2026-11-09 · Verified reference facts; made the skill an evergreen unit
- because: R-20261109-1; user request
- files: references/ai-and-pm-now.md, references/history.md, references/charts.md, references/rituals.md; new evergreen.json, RESEARCH.md, CHANGELOG.md, LEARNINGS.md, MAINTENANCE.md
- Fixed wrong or loose facts, replaced dead links, and marked every source line "opened", "via search" or "(unverified)".

# Changelog: steerwright

Every change to SKILL.md and its companions, newest first, each with the reason. Reasons cite findings in [RESEARCH.md](RESEARCH.md) (`R-`) and lessons in [LEARNINGS.md](LEARNINGS.md) (`L-`). State in `evergreen.json`. Protocol: MAINTENANCE.md.

Entry shape: `### C-20261119-1 · 2026-11-19 · inbox collectors (`sw.py inbox`)
- because: user request 2026-11-19 (one place for everything waiting on Mark; survey in ai-docs/notes/inbox-sources.md)
- files: scripts/inbox.py, scripts/sw.py, SKILL.md, tests/test_inbox.py
New read-only `sw.py inbox` gathers eight sources into one normalised list mapped to registry projects. Unreleased; ships with the inbox page.

### C-YYYYMMDD-n · date · one-line summary`, then `because:`, `files:`, and a sentence on what changed.

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

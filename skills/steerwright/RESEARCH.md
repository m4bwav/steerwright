# Research: steerwright

Findings that back SKILL.md and the files in `references/`. Changes they caused are logged in [CHANGELOG.md](CHANGELOG.md); procedural lessons live in [LEARNINGS.md](LEARNINGS.md); schedule and state in `evergreen.json`. Protocol: MAINTENANCE.md.

Topic: Project management methods, flow metrics, AI-for-PM tools, solo/creative production practice. Tier `moderate`. Last refresh 2026-11-09; next due 2026-12-09.

## Current understanding

- Trackers now treat agents as assignees (Linear, Jira, Asana, Notion, monday.com, GitHub). A person stays the owner; review is the bottleneck.
- Evidence on AI speed-up is weak: METR found 19% slower in early 2025 and could not get a clean late-2025 number.
- Method standards moved recently: PMBOK 8 (Nov 2025), Kanban Guide v2025.5, PRINCE2 7 (2023). Scrum Guide is still 2020.
- Trackers die (Height, 2025-09-24); keep state in plain files.

## Open questions

- Has PMI published a PMBOK 8 page that can be fetched (pmi.org blocks bots)?
- Height's own shutdown notice; years active and money raised.
- Asana prebuilt-agent count; Notion Custom Agents GA date; a live replacement for the TC 25-20 After-Action Review PDF.

## Search plan

Scope every query to the time since the last refresh and add the year. Open primary pages (vendor changelog, standard body) before secondary coverage. pmi.org, gartner.com, framework.scaledagile.com and alternativeto.net block fetches; confirm through search results.

- **ai-and-pm-now.md** (most volatile, run every refresh):
  - `linear.app/changelog agents <month> <year>`
  - `Atlassian Rovo "agents in Jira" <year>`
  - `Asana AI Teammates release <year>`; `Notion Custom Agents <year>`; `ClickUp Brain agents pricing <year>`; `monday.com AI agents <year>`
  - `github.blog changelog Copilot agent Linear OR Jira <year>`; `GitHub Agent HQ <year>`
  - `Todoist AI MCP <year>`
  - `"project management" tool shutting down OR sunset OR acquired <year>`
  - `METR developer productivity AI study <year>`; `Gartner agentic AI prediction <year>`; `PMI generative AI project management survey <year>`; `Smartsheet PPM priorities report <year>`
- **history.md**: `PMBOK Guide 8th edition <year>` and `PMBOK 9`; `Scrum Guide update <year>`; `Kanban Guide kanbanguides.org version`; `PRINCE2 new edition <year>`; `SAFe 6.0 OR "SAFe 7" <year>`; `Shape Up Basecamp update`.
- **glossary.md**: same standards as history.md; `WSJF cost of delay definition`.
- **charts.md**: `Jira cumulative flow diagram control chart docs`; `actionableagile Monte Carlo forecasting <year>`; `Focused Objective forecasting spreadsheets github`.
- **rituals.md**: `Scrum Guide events timeboxes`; `Atlassian Team Playbook retrospective premortem`; `After Action Review Army TC 25-20 pdf`; `GTD weekly review gettingthingsdone.com`; `Stage-Gate Cooper <year>`.
- **creative-and-solo.md**: `personal kanban`; `Annie Duke Quit kill criteria`; `solo game developer production scope <year>`; `indie film production schedule practice <year>`.
- **books.md**: check that each listed book has a current edition and that free online editions (Shape Up) still load.
- Link check every refresh: curl every URL in `references/`; replace 404s with primary pages, mark blocked ones "via search".

Best sources: vendor changelogs (linear.app/changelog, github.blog/changelog, atlassian.com blog), scrumguides.org, kanbanguides.org, PMI and PeopleCert press pages, metr.org. Noisy: SEO "best alternatives" listicles, Skywork pages.

## Findings log

Newest first.

### R-20261109-1 · 2026-11-09 · Verification pass on reference files
- Summary: 76 URLs status-checked; key facts confirmed by opening pages or search. Corrected: METR "18% faster" is METR's own late-2025 raw estimate (marked unreliable by METR), not a blog number; Asana "30+ agents / chief of AI staff June 2026" unconfirmed (Asana Dash is "AI chief of staff"); Notion Custom Agents launched 24 Feb 2026, credits from 4 May 2026; monday.com relaunch 6 May 2026; Agent HQ Claude/Codex 4 Feb 2026; Kanban Guide current v2025.5; PMBOK 8 has 40 processes, 7th sold until 2026-07-08. Dead links: GTD episode 43, TOCICO BoK page, TC 25-20 PDF, workmanagementhub roundup.
- Track: subject
- Sources: metr.org/blog/2026-02-24-uplift-update, linear.app/changelog (three entries), github.blog/changelog/2026-07-23, asana.com/inside-asana/spring-release-2026, smartsheet.com/ppm-priorities-report-2026-mobile, kanbanguides.org/english, scrumguides.org
- Magnitude: minor
- Applied: C-20261109-1

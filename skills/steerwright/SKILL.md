---
name: steerwright
description: "Project management for one maker with many projects: keeps a registry of every project (software, game, film, music, art, writing), shows local pages with health, burn-up, cumulative flow, throughput, aging work and a Monte Carlo forecast over askwright, chainwright and grindwright state, and runs weekly keep / table / abandon reviews on askwright pages so each project ends as done, tabled or abandoned. Use on 'how are my projects doing', 'what's my portfolio look like', 'review my projects', 'should I table X', 'how do I get X unstuck', 'when will X be done', 'too many projects', 'start the dashboards', 'add a milestone or risk', or any project management question (Gantt, PERT, Scrum, Kanban, Shape Up, flow metrics, rituals, PM history and terms). Not for picking the next game task (grindwright) or chaining sessions (chainwright)."
---

# Steerwright

Every project should be moving, parked on purpose with a wake condition, or closed. Steerwright keeps the list, shows the evidence, and asks Mark the keep / table / abandon question. Mark decides; steerwright never changes a project's status without his answer.

Script: `scripts/sw.py` (Python 3.9+, standard library). Registry: `~/.steerwright/projects.json` (override with `STEERWRIGHT_HOME`). It reads askwright, chainwright and grindwright homes and project folders and never writes them.

## Commands

| Task | Command |
|---|---|
| Find projects (askwright, chainwright, grindwright, HANDOFF.md) | `sw.py discover [--root DIR] [--since 30] [--apply]` |
| Add, rename, merge | `sw.py add NAME --path P --kind game --goal ... --done-when ...`, `sw.py rename OLD NEW`, `sw.py merge A B --into C` |
| Portfolio and one project | `sw.py status [NAME] [--json]` |
| Items, milestones, risks | `sw.py item NAME add "title"`, `sw.py milestone NAME add "Vertical slice" --date 2026-12-01`, `sw.py risk NAME add "GPU busy" --likelihood high --impact med --plan ...` |
| Forecast | `sw.py forecast NAME` (Monte Carlo on weekly throughput: 50/85/95 % dates) |
| Weekly review | `sw.py review NAME` writes and serves an askwright set; `sw.py apply-review [NAME]` applies answered sets |
| Close or park by hand | `sw.py table NAME --revisit DATE --wake "..."`, `sw.py abandon NAME --why ... --keep ...`, `sw.py done NAME`, `sw.py activate NAME` |
| Limits | `sw.py wip [N]` (Mark: 8), `sw.py stall [WEEKS]` (Mark: 8) |
| Pages | `sw.py up` starts steerwright, askwright and the chainwright/grindwright indexes and opens the main page; `sw.py down` stops only what `up` started; `sw.py shortcut` writes a desktop `.cmd` |

## Weekly review

Manual only (Mark's ruling). For each active project, quietest first when over the WIP limit:
1. `sw.py review NAME`. It flags kill criteria: no progress for `stall_weeks`, 85 % forecast past the target, over the WIP limit, no definition of done, open asks. Its guess is low confidence.
2. Tell Mark the set is up. Never fill an unanswered question with the guess.
3. Later, `sw.py apply-review`. Keep stores the next three actions; table writes revisit date and wake condition; abandon writes the post-mortem; then harvest anything reusable from an abandoned project into the right plugin or note.

## Advice on demand

Answer from the references and name the method: "Personal Kanban says...", "Annie Duke's kill criteria...". Use real numbers from `sw.py status --json` and `forecast`, and give forecasts as a range with confidence, never one date.

- [history.md](references/history.md): Gantt to Shape Up and flow metrics.
- [glossary.md](references/glossary.md): terms.
- [charts.md](references/charts.md): which chart for which question and how to read it.
- [rituals.md](references/rituals.md): which rituals fit a solo maker with agents.
- [creative-and-solo.md](references/creative-and-solo.md): film, game, music, art, writing production; finish-or-kill and stall patterns.
- [ai-and-pm-now.md](references/ai-and-pm-now.md): AI in PM tools and research, 2026.
- [books.md](references/books.md): the reading list and what each book is for.

## Rules

- Read-only over sibling plugins. Kill by PID only. Pages bind 127.0.0.1.
- Status changes come from Mark's answers or his explicit word.
- Item counts come from grindwright ledgers and `sw.py item`; projects without a ledger get a git and log proxy chart, which is activity, not scope.

## Step 0: freshness (every use, one read)

Read `evergreen.json` next to this file. If `verify_at_use` is true, re-check the due `volatile_claims` before relying on them, then stamp them (`evergreen.py claims <unit> --stamp due`). If `contradiction` is set or today is on or after `next_due`, tell the user in one line, do the task with the current content, then run `evergreen-refresh` in the same session. If `tests.failing` is non-empty, say so and run `evergreen-tune` after the task.

## While working: capture learnings

If the user corrects you, the same error happens twice, a workaround is found, or an environment fact is discovered, write it to `LEARNINGS.md` (format in MAINTENANCE.md). If a learning proves a claim wrong, fix it, log it in `CHANGELOG.md`, and set `contradiction` in `evergreen.json`.

## Maintenance

Evergreen unit (tier `moderate`, every 30 days). Files: `evergreen.json`, [RESEARCH.md](RESEARCH.md), [CHANGELOG.md](CHANGELOG.md), [LEARNINGS.md](LEARNINGS.md), MAINTENANCE.md. Refresh with `evergreen-refresh`; test with `evergreen-test`.

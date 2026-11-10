# steerwright

Project management for one maker with many projects. Steerwright keeps a list of every project, shows how each one is moving, and asks the keep, table or abandon question once a week, so projects end as done, tabled or abandoned instead of drifting.

It sits on top of three sibling plugins and only reads their files:

- **askwright** decision pages: open and answered questions, and where the weekly review asks its question.
- **chainwright** chained sessions: running chains, continue prompts, HANDOFF.md.
- **grindwright** ledgers: items by lane and state, which feed the flow charts and forecast.

## What you get

- A registry at `~/.steerwright/projects.json`, filled by `sw.py discover` and kept by hand.
- A local main page: every project with a health colour, last activity, open asks, running chains, grind counts and next action, a WIP warning and tabled projects whose revisit date has come.
- A page per project: burn-up, cumulative flow, throughput, cycle time, aging work, a Monte Carlo forecast as a date range, milestones, risks and the decision log.
- `sw.py up` and a desktop shortcut that start all the page servers; `sw.py down` stops only what it started.
- Reference notes on project management from Gantt to flow metrics and AI tools in 2026, used for advice.

## Quick start

```
python skills/steerwright/scripts/sw.py discover            # proposals only
python skills/steerwright/scripts/sw.py discover --apply    # write them
python skills/steerwright/scripts/sw.py up                  # open the pages
python skills/steerwright/scripts/sw.py review "My game"    # weekly review on an askwright page
python skills/steerwright/scripts/sw.py apply-review        # apply the answers
```

Python 3.9 or later, standard library only. Tests: `python -m unittest discover -s tests`.

## Licence

MIT. See [LICENSE](LICENSE). Security: [SECURITY.md](SECURITY.md).

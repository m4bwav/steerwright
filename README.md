# steerwright

![A ship's brass helm wheel facing a calm sea of small islands with lighthouses, one glowing route on the water leading ahead](https://raw.githubusercontent.com/m4bwav/steerwright/main/.github/images/banner.jpg)

Project management for one maker with many projects. Steerwright keeps a list of every project, shows how each one is moving, and asks the keep, table or abandon question once a week, so projects end as done, tabled or abandoned instead of drifting.

It sits on top of three sibling plugins and only reads their files:

- **askwright** decision pages: open and answered questions, and where the weekly review asks its question.
- **chainwright** chained sessions: running chains, continue prompts, HANDOFF.md.
- **grindwright** ledgers: items by lane and state, which feed the flow charts and forecast.

## What you get

- A registry at `~/.steerwright/projects.json`, filled by `sw.py discover` and kept by hand.
- A local main page: every project with a health colour, last activity, open asks, running chains, grind counts and next action, a WIP warning and tabled projects whose revisit date has come.
- A page per project: burn-up, cumulative flow, throughput, cycle time, aging work, a Monte Carlo forecast as a date range, milestones, risks and the decision log.
- Your repo-traffic dashboard on the same site: `sw.py traffic PATH` once, then a "repo traffic" link on every page opens it at `/traffic`.
- Weekly reviews show the project's HANDOFF and continue prompt, and a project can be tabled indefinitely (no wake date).
- `sw.py up` and a desktop shortcut that start all the page servers; `sw.py down` stops what it started plus steerwright's own server.
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

## Works with

steerwright is the hub: it reads what its siblings leave on disk and links to their pages.

- [askwright](https://github.com/m4bwav/askwright): steerwright lists every open askwright set across projects, starts the askwright server if it isn't running, and puts "answer N questions" at the top of your actions. One place shows what is waiting on you.
- [grindwright](https://github.com/m4bwav/grindwright): it shows the grind ledger by lane and rebuilds grindwright's index, so you can see where each project's work is going.
- [chainwright](https://github.com/m4bwav/chainwright): it lists chain runs with their sessions and ledgers. chainwright and grindwright pages link back to the hub when it is installed.

## Licence

MIT. See [LICENSE](LICENSE). Security: [SECURITY.md](SECURITY.md).

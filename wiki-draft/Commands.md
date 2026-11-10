All commands run as `python skills/steerwright/scripts/sw.py COMMAND`. This list matches `sw.py --help` for 0.3.0. Most commands print JSON.

## Registry

| Command | What it does |
|---|---|
| `discover [--root DIR] [--since DAYS] [--no-group] [--apply]` | Proposes registry entries from sibling plugin state. `--root` can be given more than once. `--since` defaults to 30. Nothing is written without `--apply`. |
| `add NAME --path DIR [--kind K] [--goal G] [--done-when D] [--target YYYY-MM-DD]` | Adds a project. Kinds: software, game, film, art, music, writing, engineering, other (the default). |
| `rename NAME NEW` | Renames a project. |
| `merge NAME... --into NAME` | Folds projects into one. A group counts once against the WIP limit. |

## Status and forecast

| Command | What it does |
|---|---|
| `status [NAME] [--json]` | The portfolio, or one project: health, activity, open asks, flow. |
| `forecast NAME [--trials N] [--weeks N]` | Monte Carlo finish range from weekly throughput, as 50, 85 and 95 % dates. Defaults: 10000 trials, 12 weeks. |

## Items, milestones, risks

| Command | What it does |
|---|---|
| `item NAME add TITLE`, `item NAME done ID`, `item NAME drop ID` | Steerwright's own list of remaining items, for projects with no grindwright ledger. |
| `milestone NAME add TITLE [--date YYYY-MM-DD]`, also `done` and `drop` | Milestones shown on the project page. |
| `risk NAME add TEXT [--likelihood low/med/high] [--impact low/med/high] [--plan TEXT]`, `risk NAME close ID` | The risk list. Likelihood and impact default to med. |

## Reviews and status changes

| Command | What it does |
|---|---|
| `review NAME [--weeks N] [--no-serve]` | Writes the weekly review as an askwright set and serves it. It flags no progress for the stall period, an 85 % forecast past the target, going over the WIP limit, a missing definition of done, and open asks. |
| `apply-review [NAME] [--dry-run]` | Applies answered review sets. Keep stores the next three actions, table stores the revisit date and wake condition, abandon writes the post-mortem. |
| `table NAME --revisit YYYY-MM-DD --wake TEXT` | Parks a project until a date or condition. |
| `abandon NAME --why TEXT [--keep TEXT]` | Closes a project with a short post-mortem. |
| `done NAME [--note TEXT]` | Marks a project finished. |
| `activate NAME` | Makes a project active again. |

## Limits

| Command | What it does |
|---|---|
| `wip [N]` | Shows or sets the limit on active projects. Default 8. |
| `stall [WEEKS]` | Shows or sets how many weeks without progress a review flags. Default 8. |

On a fresh registry with one project added, `wip` printed `{"wip_limit": 8, "active": 1}` and `stall` printed `{"stall_weeks": 8}`.

## Pages

| Command | What it does |
|---|---|
| `serve [--port P] [--detach] [--open]` | Serves the main page and one page per project on 127.0.0.1, port 47630 unless set. |
| `up [--no-open]` | Starts steerwright, the askwright dashboard and the chain and grind indexes, and opens the main page. |
| `down` | Stops only the processes `up` started, by PID. |
| `shortcut` | Writes a desktop `.cmd` that runs `up`. |
| `--version` | Prints the version. |

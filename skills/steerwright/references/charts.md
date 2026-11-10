# Project charts: what each shows, what it needs, how to read it

Purpose: pick the right chart for a solo maker's project and compute it from a plain item log with stdlib Python.

Sources checked 2026-11-09 (from the literature; URLs are the canonical pages):
- Daniel Vacanti, *Actionable Agile Metrics for Predictability* (2015) and *When Will It Be Done?* (2020): https://actionableagile.com/books/
- The Kanban Guide (Vacanti and Coleman, 2020): https://kanbanguides.org/english/
- Scrum Guide 2020: https://scrumguides.org/scrum-guide.html
- Atlassian Agile Coach, burndown, burnup, CFD, control chart: https://www.atlassian.com/agile/tutorials/burndown-charts , https://support.atlassian.com/jira-software-cloud/docs/view-and-understand-the-cumulative-flow-diagram/ , https://support.atlassian.com/jira-software-cloud/docs/view-and-understand-the-control-chart/
- Donald Reinertsen, *The Principles of Product Development Flow* (2009)
- PMI, PMBOK Guide and the Earned Value standard: https://www.pmi.org/standards/pmbok
- Basecamp, *Shape Up*, chapter "Show Progress" (hill charts): https://basecamp.com/shapeup/3.4-chapter-13
- Troy Magennis, Focused Objective forecasting spreadsheets: https://github.com/FocusedObjective/FocusedObjective.Resources

## The data model

Every flow chart below comes from one log. Each item needs:

- `id`, `title`, `type` (optional), `size` (optional; points or 1)
- `created` date
- one date per workflow state it entered: e.g. `started`, `review`, `done`
- `dropped` date if abandoned (counts as leaving the system, not as throughput)

Keep dates as ISO `YYYY-MM-DD`. Use calendar days. Count both ends: cycle time = `done - started + 1` days (Vacanti's convention, so same-day work is 1 day).

For schedule charts (Gantt, PERT, EVM) you also need planned start, duration and dependencies per task, and a budget per task.

---

## Gantt chart

- **Shows:** tasks as bars on a calendar, with dependencies and milestones.
- **Data:** task, planned start, duration or end, dependencies, optional percent done.
- **Read it:** the longest chain of dependent bars sets the end date. A bar slipping on that chain moves the end.
- **Misreadings:** treating the plan as a forecast. Percent-complete bars look precise but are guesses. Bars hide that a task may be blocked, not merely long.
- **Solo maker:** use for work with hard dates and real dependencies: a film shoot schedule, a release with store review lead time, a print run. Skip for open-ended creative work.

## PERT / network diagram

- **Shows:** tasks as nodes, dependencies as arrows, the critical path.
- **Data:** tasks, dependencies, and three estimates each: optimistic `o`, most likely `m`, pessimistic `p`.
- **Compute:** expected `E = (o + 4m + p) / 6`; variance `((p - o) / 6)^2`. Forward pass: earliest start = max earliest finish of predecessors. Backward pass: latest finish = min latest start of successors. Slack = latest start - earliest start. Critical path = tasks with zero slack. Project variance = sum of variances on the critical path.
- **Read it:** zero-slack tasks are where delay hurts. Parallel paths with little slack can become critical.
- **Misreadings:** summing the critical path ignores merge bias (when paths join, the later of several uncertain paths wins, so the real end is later than PERT says). A Monte Carlo over the network fixes this.
- **Solo maker:** rarely. One person does tasks serially, so the "path" is mostly your queue. Useful when agents or outside parties (render farm, printer, reviewer) run in parallel.

## Burn-down chart

- **Shows:** work remaining over time against an ideal line to zero.
- **Data:** total scope at start; daily remaining (items or points).
- **Compute:** `remaining[d] = scope[d] - done_cumulative[d]`. Ideal line: straight from start scope to 0 at end date.
- **Read it:** above the ideal line = behind. Flat stretches = nothing finishing.
- **Misreadings:** scope added mid-way looks like no progress, because burn-down mixes scope and completion in one line. A smooth line can hide that nothing is truly done (many items 90 percent). A line that drops on the last day means work was batched.
- **Solo maker:** only inside a fixed timebox. Burn-up is usually better.

## Burn-up chart

- **Shows:** two lines: total scope and cumulative done.
- **Data:** per day, total scope (items not dropped, created on or before that day) and cumulative done.
- **Compute (per day d):**
  - `scope[d] = count(items where created <= d and not (dropped and dropped <= d))`
  - `done[d] = count(items where done and done <= d)`
  - Optional projection: fit average daily throughput over the last N weeks and extend `done` until it meets `scope`. Better: draw Monte Carlo 50/85 percent lines.
- **Read it:** the gap is remaining work. Lines converging = heading to finish. A rising scope line that keeps pace with done = never finishing.
- **Misreadings:** a straight-line projection looks like a promise. Points-based burn-ups shift when you re-estimate.
- **Solo maker:** yes. Best single chart for "is this project finishing or growing?"

## Cumulative flow diagram (CFD)

- **Shows:** stacked bands, one per workflow state, of cumulative arrivals over time.
- **Data:** state entry dates per item.
- **Compute:** for states in order S1 (backlog) ... Sk (done), for each day d:
  - `arrivals[s][d] = count(items whose date for state s, or any later state, is <= d)`. (An item that skipped a state counts as having passed it.)
  - Plot the lines bottom to top: done, then each earlier state. Band height for state s = `arrivals[s][d] - arrivals[s+1][d]`.
  - Approximate average WIP = band height of in-progress states; approximate average cycle time = horizontal distance between the "started" line and the "done" line at the same height (Little's Law: avg cycle time = avg WIP / avg throughput, valid only when the system is roughly stable).
- **Read it:** bands of steady width = stable flow. A widening band = a queue growing in that state (bottleneck or blocked). A flat top line = no new work; a flat done line = nothing finishing.
- **Misreadings:** lines in a CFD never go down. If they do, the data is wrong (items moved backwards). Reading cycle time off the chart is an average, not a forecast for one item. Little's Law fails when WIP is growing.
- **Solo maker:** monthly, on a project with 30+ items. Shows where work piles up (often "review" or "waiting on Mark").

## Cycle time scatterplot (control chart)

- **Shows:** one dot per finished item: x = finish date, y = cycle time in days, with percentile lines.
- **Data:** `started` and `done` dates.
- **Compute:**
  - `ct = (done - started).days + 1`
  - Percentile with the nearest-rank method (Vacanti's usage): sort ascending; `k = ceil(p/100 * n)`; value = `sorted[k-1]`. Report 50th, 70th, 85th, 95th.
  - Atlassian's Jira control chart instead draws a rolling average and standard deviation band. Prefer percentiles: cycle time is skewed, not normal.
- **Read it:** "85 percent of items finish in X days or less." Use the 85th as the service level for a new item. Dots far above the 95th line are outliers worth a look.
- **Misreadings:** using mean and sigma on skewed data. Treating the percentile as a promise for a large item (it applies to items like the ones in the sample). Mixing very different item types in one plot.
- **Solo maker:** yes, once you have about 20 finished items. Gives a plain answer to "how long does one of these take me?"

## Aging WIP chart

- **Shows:** each item still in progress as a dot in its current state column, y = age in days, with the cycle time percentile lines behind it.
- **Data:** `started` date and current state of open items, plus the historical percentiles above.
- **Compute:** `age = (today - started).days + 1`. Flag items whose age exceeds the 85th percentile cycle time; warn at the 50th or 70th.
- **Read it:** an item crossing the 85th line is now slower than most of your history. Act on it: unblock, split, or drop. Vacanti calls age the leading indicator; cycle time only arrives when an item finishes.
- **Misreadings:** an old item is not a failure by itself. It is a prompt to look. Comparing against percentiles from a different kind of work.
- **Solo maker:** yes, weekly. This is the chart that catches the stalled project lane.

## Throughput run chart and histogram

- **Shows:** items finished per week (or day). The run chart plots it over time; the histogram shows how often each count occurs.
- **Data:** `done` dates.
- **Compute:** bucket `done` dates by ISO week (`date.isocalendar()[:2]`). Include weeks with zero. Use the range from the first to the last week of the sample window, not only weeks that had finishes.
- **Read it:** variation is normal. Trends (several weeks up or down) matter more than one bad week. The histogram is the input to Monte Carlo.
- **Misreadings:** dropping zero weeks inflates the forecast. Comparing points across people or projects. Counting "dropped" as throughput.
- **Solo maker:** yes, weekly, in the review.

## Monte Carlo forecasts

Two questions. Both resample past throughput. Source: Vacanti, *When Will It Be Done?*; Magennis's throughput forecaster.

**Inputs:** a sample of daily (or weekly) throughput counts from a recent stable window, zeros included. 6 to 12 weeks is typical; at least 10 data points. Remaining items `R` or a target date.

**"When will it be done?" (how long for R items):**

```
import random, math
def when(samples, remaining, trials=10000):
    results = []
    for _ in range(trials):
        done, periods = 0, 0
        while done < remaining:
            done += random.choice(samples)
            periods += 1
            if periods > 10000: break      # guard: all-zero samples
        results.append(periods)
    results.sort()
    return {p: results[math.ceil(p/100*trials)-1] for p in (50, 85, 95)}
```

Read: "50 percent chance within X periods, 85 percent within Y, 95 within Z." Add periods to today for dates. Higher percentile = later date = more confidence.

**"How many by a date?" (N periods until the date):**

```
def how_many(samples, periods, trials=10000):
    results = sorted(sum(random.choice(samples) for _ in range(periods))
                     for _ in range(trials))
    # confidence that AT LEAST this many finish: read from the low end
    return {p: results[math.floor((100-p)/100*trials)] for p in (50, 85, 95)}
```

Note the direction: for "how many", 85 percent confidence is the 15th percentile of outcomes (a smaller number). For "when", 85 percent is the 85th percentile (a later date).

- **Misreadings:** the forecast assumes the future looks like the sample. New scope is not included unless you add it (multiply `R` by a split/growth factor from history). It forecasts count, not size; split big items first or forecast them separately. Re-run weekly; never freeze a forecast.
- **Solo maker:** yes. Use daily samples for short projects, weekly for long ones. Agent sessions make throughput lumpy; weekly sampling smooths it.

## Earned value chart (PV, EV, AC)

- **Shows:** three cumulative curves over time. PMI terms.
- **Data:** budget per task (hours or money), planned schedule, percent complete, actual cost.
- **Compute:** PV = budgeted cost of work scheduled to date. EV = sum(budget x percent complete). AC = actual cost to date. SV = EV - PV; CV = EV - AC; SPI = EV/PV; CPI = EV/AC; EAC = BAC / CPI (one common formula); ETC = EAC - AC.
- **Read it:** CPI below 1 = over budget per unit of work. SPI below 1 = behind plan.
- **Misreadings:** EV depends on honest percent-complete; use 0/100 or 50/50 rules to avoid optimism. SPI drifts back to 1 at the end even for late projects (it measures value, not time; "earned schedule" fixes this).
- **Solo maker:** skip, unless spending real money with a budget (paid renders, contractors, hardware). Then track AC against a simple budget instead.

## Risk matrix

- **Shows:** risks placed on a grid of likelihood x impact (often 5x5).
- **Data:** risk list with likelihood, impact, owner, response.
- **Read it:** top-right gets a response now. Review monthly.
- **Misreadings:** the grid makes ordinal guesses look like math; multiplying scores is weak (Tony Cox, "What's Wrong with Risk Matrices?", Risk Analysis 2008, https://doi.org/10.1111/j.1539-6924.2008.01030.x). Rare, huge risks get understated.
- **Solo maker:** adapt. Keep a short list of top 5 risks with a trigger and a response; skip the grid.

## Roadmap (now / next / later)

- **Shows:** three columns of themes or outcomes, no dates.
- **Data:** the bets you have and their order.
- **Read it:** "now" is committed; "next" is likely; "later" is a wish.
- **Misreadings:** "later" read as a promise. Adding dates turns it back into a Gantt.
- **Solo maker:** yes, across the portfolio. Cap "now" at what you can actually finish (one or two projects).

## Kanban board

- **Shows:** items as cards in columns for workflow states, with WIP limits.
- **Data:** items and their current state.
- **Read it:** read right to left (finish before you start). A full column at its limit means pull nothing new in. Kanban Guide practices: visualize, limit WIP, actively manage items in progress, improve the workflow.
- **Misreadings:** a board with no WIP limits is a to-do list. Too many columns hide that work is just waiting.
- **Solo maker:** yes. Columns: Options, Next, Doing (limit 2-3), Waiting (on a person or a render), Done. Waiting counts toward WIP or it grows without bound.

## Hill chart

- **Shows:** each scope as a dot on a hill. Left side uphill = figuring out what to do. Right side downhill = known work, just doing it.
- **Data:** a manual position per scope, updated by the maker, with history.
- **Read it:** dots that stay uphill for weeks are the risk. Downhill work is predictable.
- **Misreadings:** it is self-reported, not measured. Dots on the right can still hide unknowns.
- **Solo maker:** yes for creative work (film, music, game design) where most risk is in "do I know how to do this yet?" Fits Shape Up cycles.

---

## Which chart when (solo maker)

| Question | Chart |
|---|---|
| Is this project finishing or growing? | Burn-up |
| How long does one item usually take? | Cycle time scatterplot, 85th percentile |
| What is stuck right now? | Aging WIP |
| When will these R items be done? | Monte Carlo "when", 85 percent |
| How much can I ship by date D? | Monte Carlo "how many", 85 percent |
| Where does work pile up? | CFD |
| What matters across all projects? | Now/next/later roadmap |
| Do I know how to do this yet? | Hill chart |
| Hard dates and dependencies | Gantt, maybe PERT |

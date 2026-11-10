# Project rituals: what each is for and whether a solo maker should keep it

Purpose: choose which planning and review rituals a solo maker working with AI agent sessions should run, and how often.

Sources checked 2026-11-09:
- Scrum Guide 2020 (events and timeboxes): https://scrumguides.org/scrum-guide.html
- The Kanban Guide 2020: https://kanbanguides.org/english/
- Atlassian Team Playbook and Agile Coach (standups, retrospectives, backlog refinement, pre-mortem): https://www.atlassian.com/team-playbook/plays , https://www.atlassian.com/agile/scrum/backlog-refinement
- Gary Klein, "Performing a Project Premortem", Harvard Business Review, Sept 2007: https://hbr.org/2007/09/performing-a-project-premortem
- US Army, *A Leader's Guide to After-Action Reviews* (TC 25-20, 1993): https://www.acq.osd.mil/dpap/ccap/cc/jcchb/Files/Topical/After_Action_Report/resources/tc_25-20.pdf
- Google SRE book, "Postmortem Culture: Learning from Failure": https://sre.google/sre-book/postmortem-culture/
- David Allen, GTD weekly review: https://gettingthingsdone.com/2018/08/episode-43-the-weekly-review/
- Basecamp, *Shape Up* (betting table, cool-down, circuit breaker): https://basecamp.com/shapeup/2.2-chapter-08 , https://basecamp.com/shapeup/2.1-chapter-07
- John Doerr, *Measure What Matters*, and https://www.whatmatters.com/faqs/okr-meaning-definition-example
- Robert Cooper, Stage-Gate: https://www.stage-gate.com/blog/the-stage-gate-model-an-overview/
- Annie Duke, *Quit: The Power of Knowing When to Walk Away* (2022): https://www.annieduke.com/books/

Verdict key: **fits** (run as is), **adapt** (keep the purpose, change the form), **skip** (ceremony with no audience when you work alone).

---

## Daily standup (Daily Scrum)

- **Purpose:** inspect progress toward the goal and adapt the plan for the next day. Not a status report.
- **Steps:** what moved toward the goal; what is next; what blocks it. Kanban variant: walk the board right to left, item by item.
- **Timing:** daily, 15 minutes max.
- **Verdict: adapt.** No team to sync with. Keep a 2-minute start-of-session check: read HANDOFF.md, look at aging WIP, pick the one item to finish, note what waits on a person. An agent session can do this from the log.

## Sprint planning

- **Purpose:** choose a goal for a timebox and the work that serves it.
- **Steps:** why is this sprint valuable (goal); what can be done (pick items); how (break into tasks).
- **Timing:** start of each sprint; up to 8 hours for a one-month sprint.
- **Verdict: adapt.** Fold into the weekly review: pick one goal per active project for the coming week. Use the Monte Carlo "how many by date" to size it, not story points.

## Sprint review

- **Purpose:** inspect the outcome with stakeholders and adjust the backlog.
- **Steps:** show what was done; discuss what changed; update the backlog and forecast.
- **Timing:** end of sprint; up to 4 hours for a month.
- **Verdict: adapt.** Stakeholders are you, maybe a tester or audience. Replace with "show it": publish a build, a cut, a track, a page, and record reactions. Real feedback beats a meeting.

## Retrospective

- **Purpose:** improve how the work is done.
- **Steps:** set the stage; gather data; find causes; decide one or two changes; close. Formats: start/stop/continue, 4Ls.
- **Timing:** end of sprint; up to 3 hours for a month.
- **Verdict: fits, small.** Five minutes in the weekly review: one thing that slowed you, one change to try. Session wrap-ups already harvest tool and process lessons; the retro looks at the project level.

## Backlog refinement

- **Purpose:** keep upcoming items small, clear and ordered.
- **Steps:** split, clarify, add acceptance criteria, re-order, delete stale items.
- **Timing:** ongoing; Scrum suggests it takes no more than about 10 percent of capacity.
- **Verdict: fits.** Agents can draft splits and criteria. Delete freely; a long backlog is a cost. Refine only the next 1 to 2 weeks of items.

## Pre-mortem (Klein)

- **Purpose:** find failure risks before starting by assuming the project already failed.
- **Steps:** brief the plan; "imagine it is a year from now and the project failed badly"; everyone writes reasons independently (2 minutes); share them round-robin; pick the top risks and change the plan.
- **Timing:** once, at kickoff of anything more than a few weeks long.
- **Verdict: fits.** Cheap and works alone. An AI session can play extra "participants" from different angles (tech, audience, licence, time). Turn each top risk into a kill criterion or a plan change.

## Post-mortem / after-action review

- **Purpose:** learn from an outcome without blame.
- **Steps (AAR):** what was supposed to happen; what actually happened; why the difference; what to keep and what to change. SRE version adds timeline, impact, root causes and owned action items.
- **Timing:** AAR right after a milestone or event; post-mortem at project end or after a serious incident.
- **Verdict: fits.** Write it to the project's ai-docs so the next project starts from it. Include forecast vs actual dates: that calibrates future forecasts.

## GTD weekly review

- **Purpose:** get clear, get current, get creative.
- **Steps:** collect loose notes and inboxes; process to zero; review next actions, calendar (past and coming weeks), waiting-for, project list, someday/maybe; ask what new could be started.
- **Timing:** weekly, about 1 to 2 hours.
- **Verdict: fits.** The core of a solo cadence. Add the keep/table/abandon check (see below) and the flow charts.

## Shape Up betting table and cool-down

- **Purpose:** decide what to bet a fixed cycle on, from shaped pitches; then rest and clean up.
- **Steps:** pitches have a problem, appetite (time you are willing to spend), solution sketch, rabbit holes and no-gos. Bet on a few for the cycle (6 weeks). Circuit breaker: if not done at the end, it does not get extended by default. Cool-down (2 weeks): fix bugs, explore, decide next bets. No backlog: unbet pitches are not kept centrally.
- **Timing:** every 6 + 2 weeks.
- **Verdict: adapt.** Appetite and the circuit breaker fit a solo maker very well, because they cap creative sprawl. Use shorter cycles (1 to 3 weeks) for agent-paced work. Keep cool-down as the slack week each month.

## Quarterly planning / OKR check-in

- **Purpose:** set a few ambitious objectives with measurable key results; check them weekly or monthly; grade at quarter end (0.0 to 1.0; around 0.7 is a good score for stretch goals).
- **Steps:** pick 1 to 3 objectives; 2 to 4 key results each (outcomes, not tasks); check confidence regularly; grade and reflect.
- **Timing:** quarterly, with check-ins.
- **Verdict: adapt.** Full OKRs exist to align teams. Alone, keep one objective per quarter with one or two measures (shipped, downloads, finished film length), reviewed in the monthly portfolio review.

## Stage-gate review

- **Purpose:** a go/kill/hold/recycle decision before funding the next stage.
- **Steps:** deliverables for the gate; criteria (must-meet and should-meet); decision; resources for the next stage.
- **Timing:** at each gate (idea, scoping, business case, development, testing, launch).
- **Verdict: adapt.** Drop the committee. Keep gates at natural points: after a prototype, before a big render or spend, before a public release. Use kill criteria as the must-meet list.

## Kill criteria and the quitting review (Annie Duke)

- **Purpose:** decide in advance when to stop, because in the moment we persist too long (sunk cost, endowment, identity).
- **Steps:** at kickoff, write "if by [date] I have not reached [state], I stop or change course" (state + date pairs). Monkeys first: do the hardest, most uncertain part first (the "monkey" not the "pedestal"). At each review compare against the criteria; ask "if I were starting fresh today, would I start this?" Use a quitting coach (for a solo maker, an AI session told to argue for quitting).
- **Timing:** criteria at kickoff; checked weekly and at each gate.
- **Verdict: fits.** The most useful ritual for someone with many parallel projects. Abandoning is a valid outcome; record it in the post-mortem.

---

## Recommended solo cadence

**Daily (start of each session, 2 to 5 minutes)**
- Read HANDOFF.md and the log. Look at aging WIP; anything past the 85th percentile cycle time gets acted on first.
- Pick one item to finish. Respect the WIP limit (2 to 3 in Doing; waiting items count).
- End of session: update HANDOFF.md and the item log.

**Weekly review (30 to 60 minutes)**
1. Collect: inboxes, notes, agent outputs, decision pages.
2. Update the log; check the throughput run chart, burn-up and aging WIP.
3. Re-run Monte Carlo for each active project (50/85 percent).
4. **Keep / table / abandon** each active project: keep (on track or worth it), table (pause with a written restart condition), abandon (kill criteria hit, or "would not start this today"). Write the decision to the log.
5. Refine next week's items; pick one goal per kept project.
6. Mini retro: one friction, one change.

**Monthly portfolio review (60 minutes)**
- Now/next/later roadmap across all projects; cap "now" at one or two.
- CFD per larger project to find where work piles up.
- Quarterly objective check; stage-gate decisions due; top risks list.
- One slack/cool-down stretch per month for bugs, maintenance and exploration.

**End of project (or abandonment)**
- Post-mortem / AAR: intended vs actual, forecast vs actual dates, keep/change list.
- Archive the log and charts in the project's ai-docs so later forecasts can use the data.

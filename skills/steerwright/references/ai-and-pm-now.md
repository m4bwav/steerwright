# AI and project management now (checked 2026-11-09; per source: "opened" = page or search result read, "(unverified)" = not confirmed)

What the main tools do with AI, what the research says, and what it means for one person running agents. Everything in the tools section is **volatile**: vendors ship monthly, so recheck before quoting a feature. Some claims come from vendor pages and press, not independent tests; those are marked.

## The big shift: agents as assignees

In 2025-2026 the trackers stopped treating AI as a chat box and started treating agents as workers you assign issues to. The unit of work moved from "a task a person does" to "a task an agent session does, and a person reviews".

- **Linear.** "Linear for Agents" (May 2025) made agents workspace members: assign them issues, add them to teams, @mention them. Codex delegation came in Dec 2025, with parallel runs and inbox pings when the agent needs input or work is ready to review. In June 2026 "coding sessions" let Linear's own agent write code through Claude Code or Codex. Linear's docs split *assign* (the human owner) from *delegate* (the agent doing it), so a person stays accountable. Volatile.
  - https://linear.app/changelog/2025-05-20-linear-for-agents (checked 2026-11-09, opened)
  - https://linear.app/changelog/2025-12-04-openai-codex-agent (checked 2026-11-09, opened)
  - https://linear.app/changelog/2026-06-11-coding-sessions (checked 2026-11-09, opened)
  - https://linear.app/docs/assigning-issues.md (unverified)
- **Jira (Atlassian Rovo).** "Agents in Jira" opened in beta in late Feb 2026 and went GA for Jira Cloud Standard, Premium and Enterprise in May 2026 (Team '26). From 15 July 2026 Jira work can also be assigned to Claude Code, Cursor and GitHub Copilot (Futurum report). Rovo agents and third-party agents (GitHub Copilot coding agent, MCP partners) appear in the assignee dropdown, can be called into comments, and can be fired when an item reaches a workflow status. Rovo Dev takes work items to merge-ready PRs. Volatile; dates from Atlassian press and community posts.
  - https://businesswire.com/news/home/20260224033792/en/Atlassian-Introduces-Agents-in-Jira-to-Drive-Human-AI-Collaboration-at-Enterprise-Scale (checked 2026-11-09 via search results; page did not load)
  - https://community.atlassian.com/forums/Jira-articles/Introducing-Agents-in-Jira/ba-p/3194583 (checked 2026-11-09, opened)
- **Asana.** "AI Teammates" announced Sept 2025, broader rollout through 2026 with a gallery of prebuilt and custom no-code teammates (spring release, 20 May 2026). Asana Dash is billed as "your AI chief of staff". The "30+ prebuilt agents" count and its date are (unverified). They live in Asana's Work Graph, so they see projects, owners and history. Volatile.
  - https://asana.com/inside-asana/fall-release-2025 (unverified)
  - https://asana.com/inside-asana/spring-release-2026 (checked 2026-11-09, opened)
  - https://www.computerworld.com/article/4063082/asana-puts-ai-teammate-agents-to-work.html (unverified)
- **Notion.** Notion 3.0 (Sept 2025) added an agent that works across pages and databases. Custom Agents launched 24 Feb 2026 (Notion 3.3, Business and Enterprise) and run on a schedule or trigger; from 4 May 2026 they use Notion credits, sold as an add-on. GA date (unverified). Volatile.
  - https://www.notion.com/releases/2026-02-24 (checked 2026-11-09 via search)
- **ClickUp.** "Brain" with Super Agents and Autopilot Agents; a paid AI add-on on top of a paid plan. Standups, summaries and task creation from chat. Volatile (unverified).
- **monday.com.** Relaunched as an "AI Work Platform" (6 May 2026, agents for every customer) with agents on the boards; a Risk Analyzer watches schedule, dependency and workload risk and alerts people when work drifts. Volatile; from monday's own blog and roundups.
  - https://siliconangle.com/2026/05/06/monday-com-relaunches-ai-work-platform-native-agents/ (checked 2026-11-09 via search)
  - https://monday.com/w/use-cases/risk-management (Risk Analyzer; checked 2026-11-09 via search)
- **Todoist.** Personal-scale AI: natural-language task capture, task breakdown (AI Assist), and an official MCP server so outside agents can read and write tasks (the Todoist connector in this environment exposes project-health and productivity-stats tools). Not checked in detail this pass. Volatile (unverified).
- **GitHub Projects / Copilot.** Assign an issue to the Copilot coding agent and it opens a draft PR. Agent HQ (announced Universe, Oct 2025) adds "mission control" across web, VS Code, mobile and CLI; Claude and Codex were added as assignable agents on 4 Feb 2026 (public preview, Copilot Pro+ and Enterprise; each session uses one premium request). The same issue can go to several agents to compare PRs. Copilot's agent also works from Linear (GA July 2026) and Jira. Volatile.
  - https://github.blog/ai-and-ml/github-copilot/how-to-orchestrate-agents-using-mission-control/ (unverified)
  - https://github.blog/2026-02-04-pick-your-agent-use-claude-and-codex-on-agent-hq/ (checked 2026-11-09 via search)
  - https://github.blog/changelog/2026-07-23-copilot-cloud-agent-for-linear-is-now-generally-available/ (checked 2026-11-09, opened)
  - Copilot for Jira GA 25 June 2026: https://github.blog/changelog/2026-06-25-github-copilot-for-jira-is-now-generally-available (checked 2026-11-09 via search)

### Common AI features across tools
1. **Status summaries.** Draft weekly updates from issue activity. Good at "what changed", weak at "why it matters" and at noticing what did *not* happen.
2. **Triage.** Suggest labels, duplicates, owners and priority on intake (Linear Triage Intelligence, Jira, ClickUp).
3. **Forecasts and risk.** Flag slipping dates and overloaded people from history (monday Risk Analyzer, Asana). Only as good as the data; most solo projects have too little history for this to be meaningful.
4. **Agents as assignees.** Hand an issue to an agent; it works in the background and comes back for review.
5. **Capture.** Turn notes, meetings or voice into tasks.

## Height's shutdown
Height marketed itself as an "autonomous project manager" with AI built in. It announced its shutdown in March 2025 (20 or 22 March; sources differ) and closed on 24 Sept 2025. The "3.5 years" and "$18M raised" figures are (unverified). Lesson: an AI-first tracker is not a moat, and tools die. Keep project state in plain files you own, so a tool's death costs nothing.
- https://alternativeto.net/news/2025/3/height-project-management-tool-to-shut-down-by-september-2025 (checked 2026-11-09 via search; site blocks fetches; Height's own notice not found)

## Agentic work tracking
- The unit of work is now a **session**: a bounded run by an agent with a goal, a result and a handback. Trackers record who delegated, which agent ran, and what came back (Linear's agent sessions, GitHub mission control, Jira assignee agents).
- **A person stays accountable.** Every vendor keeps a human owner separate from the agent doing the work.
- **Review is the bottleneck.** Agents can open more PRs than a person can read. GitHub and Linear both pitch "inbox when the agent needs you" as the core feature, which tells you where the constraint is.
- **Human attention is the scarce resource.** When doing is cheap, the costly steps are deciding what to do, answering the agent's questions, and judging the output. A good system batches those, makes each one quick (one decision, a default guess), and never asks a person something an agent could answer itself.

## What the research says

- **METR RCT (July 2025).** 16 experienced open-source developers, 246 tasks in their own large repos, Cursor with Claude 3.5/3.7 Sonnet. With AI allowed, tasks took **19% longer**. Developers expected 24% faster and afterwards still believed they were 20% faster. Time shifted from coding to prompting, waiting, reviewing and idling. Small sample, mature codebases, early-2025 tools.
  - https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/ (19% slower confirmed via the 2026 update, checked 2026-11-09, opened)
- **METR update (Feb 2026).** The follow-up could not give a clean number: 30-50% of developers held back tasks they did not want to do without AI, which biases the estimate. Late-2025 raw estimates: original developers 18% faster (CI -38% to +9%), new developers 4% faster (CI -15% to +9%); METR calls these very weak evidence, likely biased low, and is redesigning the study. So "18% faster" is METR's number but not a finding it stands behind. **Volatile.**
  - https://metr.org/blog/2026-02-24-uplift-update/ (checked 2026-11-09, opened)
  - Takeaway: people misjudge their own speed with AI. Measure finished outcomes, not felt speed.
- **Gartner (June 2025).** Predicts over 40% of agentic AI projects will be cancelled by end of 2027 (cost, unclear value, weak risk controls). Warns of "agent washing"; estimates about 130 real agentic vendors. Also predicts 15% of day-to-day work decisions made autonomously by 2028 and 33% of enterprise apps including agentic AI by 2028. Predictions, not measurements.
  - https://www.gartner.com/en/newsroom/press-releases/2025-06-25-gartner-predicts-over-40-percent-of-agentic-ai-projects-will-be-canceled-by-end-of-2027 (checked 2026-11-09 via search: 40% by end of 2027 and about 130 real vendors confirmed; the two 2028 figures (unverified); gartner.com blocks fetches)
- **PMI.** PMI's GenAI reports ("First Movers' Advantage", 500 GenAI-using project professionals; "The Project Professional's GenAI Journey", about 2,000 people in 12 countries) find use concentrated in drafting, summaries and reports, with leaders seeing gains where data and governance are in place. Exact figures (unverified).
  - https://www.pmi.org/about/press-media/press-releases/genai-adoption-research (unverified; pmi.org blocks fetches)
- **Smartsheet 2026 PPM Priorities Report.** 1,651 PPM professionals: 97% experimenting with AI, only 46% trust it to act without human supervision. Vendor survey, seven countries, Aug-Sept 2025.
  - https://www.smartsheet.com/ppm-priorities-report-2026-mobile (checked 2026-11-09, opened)
- **Global AIPM Survey 2025** (Vargas and Nieto-Rodriguez, not PMI): 870 respondents in 97 countries; over 70% expect AI to co-pilot portfolios within three years. Self-report (unverified).
- **AI status reports.** No strong independent study found on whether AI-written status reports improve outcomes. Vendor claims are about time saved writing them. The known risk is "watermelon" status: green outside, red inside. A summary built from activity hides work that stalled silently, because stalled work makes no activity.

## What this means for a solo maker running agents
- Treat yourself as the reviewer and decider, not the doer. Your minutes are the budget; agent hours are cheap.
- Make the agent session the unit of work. Each one gets a goal, a done check, and a handback written to disk.
- Keep state in plain files in the repo (HANDOFF, log, plans). Trackers die (Height); files survive.
- Count finished things, not activity or felt speed. METR shows people overrate their AI speed-up.
- Limit work waiting on you, not just work in progress. A queue of unreviewed agent output is the real WIP.
- Batch your decisions: one page, one question each, a default guess, quick to answer.
- Watch for silent stalls. A project with no commits and no log entries is not "on track"; flag it by date of last real progress.
- Be sceptical of forecasts on thin data. A solo project has too little history for tool-made risk scores to mean much; use simple age and last-touched dates instead.
- Many agent projects get cancelled (Gartner's 40%). Decide kill criteria at the start, so cancelling is a planned outcome, not a failure.

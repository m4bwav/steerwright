# AI and project management now (checked 2026-11-09)

What the main tools do with AI, what the research says, and what it means for one person running agents. Everything in the tools section is **volatile**: vendors ship monthly, so recheck before quoting a feature. Some claims come from vendor pages and press, not independent tests; those are marked.

## The big shift: agents as assignees

In 2025-2026 the trackers stopped treating AI as a chat box and started treating agents as workers you assign issues to. The unit of work moved from "a task a person does" to "a task an agent session does, and a person reviews".

- **Linear.** "Linear for Agents" (May 2025) made agents workspace members: assign them issues, add them to teams, @mention them. Codex delegation came in Dec 2025, with parallel runs and inbox pings when the agent needs input or work is ready to review. In June 2026 "coding sessions" let Linear's own agent write code through Claude Code or Codex. Linear's docs split *assign* (the human owner) from *delegate* (the agent doing it), so a person stays accountable. Volatile.
  - https://linear.app/changelog/2025-05-20-linear-for-agents
  - https://linear.app/changelog/2025-12-04-openai-codex-agent
  - https://linear.app/changelog/2026-06-11-coding-sessions
  - https://linear.app/docs/assigning-issues.md
- **Jira (Atlassian Rovo).** "Agents in Jira" opened in beta Feb 2026 and is reported GA for Cloud Standard and up from May 2026. Rovo agents and third-party agents (GitHub Copilot coding agent, MCP partners) appear in the assignee dropdown, can be called into comments, and can be fired when an item reaches a workflow status. Rovo Dev takes work items to merge-ready PRs. Volatile; dates from Atlassian press and community posts.
  - https://businesswire.com/news/home/20260224033792/en/Atlassian-Introduces-Agents-in-Jira-to-Drive-Human-AI-Collaboration-at-Enterprise-Scale
  - https://community.atlassian.com/forums/Jira-articles/Introducing-Agents-in-Jira/ba-p/3194583
- **Asana.** "AI Teammates" announced Sept 2025, broader rollout through 2026 with 30+ prebuilt role agents by the Q3 2026 release and a "chief of AI staff" per user announced June 2026. They live in Asana's Work Graph, so they see projects, owners and history. Volatile.
  - https://asana.com/inside-asana/fall-release-2025
  - https://asana.com/inside-asana/spring-release-2026
  - https://www.computerworld.com/article/4063082/asana-puts-ai-teammate-agents-to-work.html
- **Notion.** Notion 3.0 (Sept 2025) added an agent that works across pages and databases. Custom Agents reached GA in May 2026 and run on a schedule or trigger. Extra agents use credits. Volatile; GA date from a third-party roundup.
- **ClickUp.** "Brain" with Super Agents and Autopilot Agents; a paid AI add-on on top of a paid plan. Standups, summaries and task creation from chat. Volatile.
- **monday.com.** Relaunched as an "AI Work Platform" (May 2026) with agents on the boards; a Risk Analyzer watches schedule, dependency and workload risk and alerts people when work drifts. Volatile; from monday's own blog and roundups.
  - https://monday.com/blog/ai-agents/ai-agents-for-project-management/
  - https://workmanagementhub.com/ai-agents-work-management-comparison-2026/
- **Todoist.** Personal-scale AI: natural-language task capture, task breakdown (AI Assist), and an official MCP server so outside agents can read and write tasks (the Todoist connector in this environment exposes project-health and productivity-stats tools). Not checked in detail this pass. Volatile.
- **GitHub Projects / Copilot.** Assign an issue to the Copilot coding agent and it opens a draft PR. Agent HQ (announced Universe, Oct 2025) adds "mission control" across web, VS Code, mobile and CLI; Claude and Codex were added as assignable agents in Feb 2026 for Pro+ and Enterprise. The same issue can go to several agents to compare PRs. Copilot's agent also works from Linear (GA July 2026) and Jira. Volatile.
  - https://github.blog/ai-and-ml/github-copilot/how-to-orchestrate-agents-using-mission-control/
  - https://github.blog/changelog/2026-07-23-copilot-cloud-agent-for-linear-is-now-generally-available/

### Common AI features across tools
1. **Status summaries.** Draft weekly updates from issue activity. Good at "what changed", weak at "why it matters" and at noticing what did *not* happen.
2. **Triage.** Suggest labels, duplicates, owners and priority on intake (Linear Triage Intelligence, Jira, ClickUp).
3. **Forecasts and risk.** Flag slipping dates and overloaded people from history (monday Risk Analyzer, Asana). Only as good as the data; most solo projects have too little history for this to be meaningful.
4. **Agents as assignees.** Hand an issue to an agent; it works in the background and comes back for review.
5. **Capture.** Turn notes, meetings or voice into tasks.

## Height's shutdown
Height marketed itself as an "autonomous project manager" with AI built in. It announced its shutdown in March 2025 and closed on 24 Sept 2025 after about 3.5 years, with about $18M raised. Lesson: an AI-first tracker is not a moat, and tools die. Keep project state in plain files you own, so a tool's death costs nothing.
- https://alternativeto.net/news/2025/3/height-project-management-tool-to-shut-down-by-september-2025

## Agentic work tracking
- The unit of work is now a **session**: a bounded run by an agent with a goal, a result and a handback. Trackers record who delegated, which agent ran, and what came back (Linear's agent sessions, GitHub mission control, Jira assignee agents).
- **A person stays accountable.** Every vendor keeps a human owner separate from the agent doing the work.
- **Review is the bottleneck.** Agents can open more PRs than a person can read. GitHub and Linear both pitch "inbox when the agent needs you" as the core feature, which tells you where the constraint is.
- **Human attention is the scarce resource.** When doing is cheap, the costly steps are deciding what to do, answering the agent's questions, and judging the output. A good system batches those, makes each one quick (one decision, a default guess), and never asks a person something an agent could answer itself.

## What the research says

- **METR RCT (July 2025).** 16 experienced open-source developers, 246 tasks in their own large repos, Cursor with Claude 3.5/3.7 Sonnet. With AI allowed, tasks took **19% longer**. Developers expected 24% faster and afterwards still believed they were 20% faster. Time shifted from coding to prompting, waiting, reviewing and idling. Small sample, mature codebases, early-2025 tools.
  - https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/
- **METR update (Feb 2026).** The follow-up could not give a clean number: 30-50% of developers held back tasks they did not want to do without AI, which biases the estimate. METR says developers are probably sped up more now than in early 2025, but the size is uncertain. The "18% faster" figure in blogs is not METR's headline. **Volatile.**
  - https://metr.org/blog/2026-02-24-uplift-update/
  - Takeaway: people misjudge their own speed with AI. Measure finished outcomes, not felt speed.
- **Gartner (June 2025).** Predicts over 40% of agentic AI projects will be cancelled by end of 2027 (cost, unclear value, weak risk controls). Warns of "agent washing"; estimates about 130 real agentic vendors. Also predicts 15% of day-to-day work decisions made autonomously by 2028 and 33% of enterprise apps including agentic AI by 2028. Predictions, not measurements.
  - https://www.gartner.com/en/newsroom/press-releases/2025-06-25-gartner-predicts-over-40-percent-of-agentic-ai-projects-will-be-canceled-by-end-of-2027 (press release URL not fetched this pass; figures confirmed via Reuters-based coverage such as https://www.thestar.com.my/tech/tech-news/2025/06/25/over-40-of-agentic-ai-projects-will-be-scrapped-by-2027-gartner-says)
- **PMI.** PMI's GenAI reports ("First Movers' Advantage", 500 GenAI-using project professionals; "The Project Professional's GenAI Journey", about 2,000 people in 12 countries) find use concentrated in drafting, summaries and reports, with leaders seeing gains where data and governance are in place. Exact figures not re-verified this pass.
  - https://www.pmi.org/about/press-media/press-releases/genai-adoption-research
- **Smartsheet 2026 PPM Priorities Report.** 1,651 PPM professionals: 97% experimenting with AI, only 46% trust it to act without human supervision. Vendor survey.
  - https://www.smartsheet.com/ppm-priorities-report-2026-mobile
- **Global AIPM Survey 2025** (Vargas and Nieto-Rodriguez, not PMI): 870 respondents in 97 countries; over 70% expect AI to co-pilot portfolios within three years. Self-report.
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

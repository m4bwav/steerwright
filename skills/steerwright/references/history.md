# Project management history

Purpose: a dated timeline of how project management grew, so the skill can explain where each tool came from and what a solo maker should keep from it.

Sources checked 2026-11-09. Each entry names its main source. Dates are the commonly cited ones; where sources differ, the entry says so.

## 1910s: Gantt chart

Henry Gantt drew bar charts of work against time around 1910-1915, first for factory and munitions work in the First World War. Karol Adamiecki drew a similar "harmonogram" in Poland in 1896 but published it in Polish only, so Gantt got the name.
The chart is still the default way to show a schedule. It shows when, not why or how much is left.
Source: https://www.gantt.com/ and https://en.wikipedia.org/wiki/Gantt_chart

## 1911-1916: Taylor and Fayol

Frederick Taylor's *The Principles of Scientific Management* (1911) broke work into measured tasks and timed them. Henri Fayol's *Administration industrielle et générale* (1916) named five functions of management: plan, organise, command, coordinate, control.
Both treat work as something planned by a manager and done by others. Modern methods keep the measuring and drop most of the top-down control.
Source: https://en.wikipedia.org/wiki/Scientific_management and https://en.wikipedia.org/wiki/Henri_Fayol

## 1957-1958: CPM and PERT

DuPont and Remington Rand developed the Critical Path Method (Kelley and Walker) in 1957 for plant maintenance shutdowns. The US Navy's Special Projects Office built PERT in 1958 for the Polaris missile programme, using three time estimates (optimistic, most likely, pessimistic) per task.
Both draw tasks as a network. The longest chain of dependent tasks sets the finish date. That chain is the critical path.
Source: https://en.wikipedia.org/wiki/Critical_path_method and https://en.wikipedia.org/wiki/Program_evaluation_and_review_technique

## 1960s: Apollo and systems engineering

NASA's Apollo programme ran hundreds of thousands of people through phased reviews, configuration control and work breakdown structures. The US Department of Defense and NASA wrote the WBS into guidance in 1962 (DoD and NASA PERT/Cost guide). Earned value also starts here (C/SCSC, 1967).
Systems engineering adds requirements traced to tests and formal change control.
Source: https://www.nasa.gov/reference/systems-engineering-handbook/ and https://en.wikipedia.org/wiki/Work_breakdown_structure

## 1970: Royce and "waterfall"

Winston Royce's paper "Managing the Development of Large Software Systems" (1970) drew the cascade of phases, then said the plain version "is risky and invites failure". He argued for feedback between steps, for building a pilot version first ("do it twice"), for heavy documentation, for involving the customer and for planned testing.
The word "waterfall" came later (Bell and Thayer, 1976). The paper is a warning against what it is famous for.
Source: https://www.praxisframework.org/files/royce1970.pdf (copy of the original paper)

## 1969 onward: PMI and the PMBOK Guide

The Project Management Institute was founded in 1969 in Pennsylvania. Its PMBOK Guide editions: 1st 1996 (after a 1987 white paper), 2nd 2000, 3rd 2004, 4th 2008, 5th 2013, 6th 2017 (added an agile practice guide), 7th 2021.
The 7th edition dropped the 49 processes for 12 principles and 8 performance domains. The 8th edition was published in November 2025 (print January 2026). It cuts the principles to 6, sets 7 performance domains (governance, scope, schedule, finance, stakeholders, resources, risk), and brings back about 40 non-prescriptive processes grouped into 5 focus areas, plus material on AI and PMOs. Check PMI's page for exact wording.
Source: https://www.pmi.org/about and https://www.pmi.org/pmbok-guide-standards/foundational/pmbok/about

## 1989 onward: PRINCE2

PRINCE came from the UK government's CCTA in 1989, built on PROMPT II. PRINCE2 followed in 1996, with major revisions in 2009, 2017 (6th edition) and 2023 (7th edition, now owned by PeopleCert/AXELOS).
It is built on stages, management by exception, a business case checked at each stage and clear roles. The 7th edition adds a "people" element, sustainability and digital and data management.
Source: https://www.axelos.com/certifications/propath/prince2-project-management

## 1990s: Lean and the Toyota Production System

Taiichi Ohno built TPS at Toyota from the 1950s: just-in-time, pull, kanban cards, stopping the line on a defect, removing waste. Womack, Jones and Roos named it "lean" in *The Machine That Changed the World* (1990).
Mary and Tom Poppendieck carried it into software with *Lean Software Development* (2003): eliminate waste, build quality in, defer commitment, deliver fast, optimise the whole.
Source: https://global.toyota/en/company/vision-and-philosophy/production-system/ and https://www.poppendieck.com/

## 1995-2020: Scrum

Ken Schwaber and Jeff Sutherland presented Scrum at OOPSLA in 1995. The first Scrum Guide came out in 2010. The 2020 Scrum Guide is shorter, drops "development team" for one Scrum Team with no sub-teams, adds the Product Goal, and makes commitments explicit: Product Goal, Sprint Goal, Definition of Done.
Sprints are one month or less. Events: sprint, planning, daily scrum, review, retrospective.
Source: https://scrumguides.org/scrum-guide.html

## 1996-1999: Extreme Programming

Kent Beck ran XP on the Chrysler C3 payroll project from 1996 and wrote *Extreme Programming Explained* (1999). Practices: pair programming, test-first, continuous integration, small releases, refactoring, the planning game with user stories.
Many of its practices outlived the name.
Source: http://www.extremeprogramming.org/ and https://en.wikipedia.org/wiki/Extreme_programming

## 1997: Critical Chain

Eliyahu Goldratt's novel *Critical Chain* (1997) applied his Theory of Constraints to projects. Cut padding from each task, pool it into a project buffer at the end, and watch how fast the buffer burns. Avoid multitasking.
Source: https://www.tocico.org/page/TOCBodyofKnowledge and https://en.wikipedia.org/wiki/Critical_chain_project_management

## 2001: Agile Manifesto

Seventeen people met at Snowbird, Utah in February 2001 and wrote four values and twelve principles. Individuals and interactions over processes and tools; working software over documentation; customer collaboration over contract negotiation; responding to change over following a plan.
Source: https://agilemanifesto.org/

## 2007-2010: Kanban method

David J. Anderson applied kanban to software at Microsoft and Corbis (2004-2007) and wrote *Kanban* (2010). Visualise the work, limit work in progress, manage flow, make policies explicit, improve by small steps. Start with what you do now.
Source: https://djaa.com/ and https://kanban.university/

## 2011 onward: scaling frameworks

SAFe (Dean Leffingwell, 2011; now SAFe 6.0, 2023) adds teams of teams (Agile Release Trains), PI planning every 8-12 weeks and lean portfolio management. LeSS (Craig Larman and Bas Vodde, around 2013) keeps one product backlog and one product owner for many teams. Nexus (Schwaber, Scrum.org, 2015) links 3-9 Scrum teams with an integration team.
None of these matter for one person. They matter only as warnings about coordination cost.
Source: https://framework.scaledagile.com/ , https://less.works/ , https://www.scrum.org/resources/online-nexus-guide

## 1970s-2018: OKRs

Andy Grove set Objectives and Key Results at Intel in the 1970s, building on Drucker's management by objectives (1954). John Doerr took them to Google in 1999 and wrote *Measure What Matters* (2018).
One qualitative objective, two to five measurable results. Ambitious ones are expected to land at about 70%.
Source: https://www.whatmatters.com/faqs/okr-meaning-definition-example

## 2012 onward: #NoEstimates

Woody Zuill started the #NoEstimates hashtag in 2012. Vasco Duarte wrote *No Estimates* (2015). The idea: slice work into similar small pieces, count them, and forecast from past throughput instead of estimating each one.
Source: https://woodyzuill.com/ and https://oikosofyseries.com/no-estimates-book-order

## 2015-2021: flow metrics

Daniel Vacanti's *Actionable Agile Metrics for Predictability* (2015) built on Little's Law: track WIP, cycle time, throughput and work item age, and forecast with Monte Carlo runs over real history. The Kanban Guide (Vacanti and Coleman, 2020, revised 2025) names those four as the minimum.
Source: https://kanbanguides.org/english/ and https://actionableagile.com/

## 2019: Shape Up

Ryan Singer of Basecamp published *Shape Up* free online in 2019. Six-week cycles and two-week cool-downs. Work is shaped first, then pitched at a betting table with a fixed appetite (time budget) and variable scope. No backlogs. Hill charts show unknowns versus known work. If a project misses its cycle, it is not extended by default (the circuit breaker).
Source: https://basecamp.com/shapeup

## Portfolio management

PMI publishes *The Standard for Portfolio Management* (4th edition 2017) and runs the PfMP credential (since 2014). Portfolio work asks which projects to fund, pause or stop, as a set. Lean portfolio management (SAFe, and Jim Highsmith's work) funds value streams rather than projects and limits how many start at once.
Source: https://www.pmi.org/certifications/portfolio-management-pfmp and https://framework.scaledagile.com/lean-portfolio-management/

## What a solo maker should take from each

| Idea | Take this | Leave this |
|---|---|---|
| Gantt chart | A rough timeline for fixed dates (festival, jam, release) | Detailed bars for every task |
| Taylor and Fayol | Measure how long things really take | Planning by one person, doing by another |
| CPM / PERT | Know which chain of tasks sets the end date; use three-point estimates on big unknowns | Full network diagrams |
| Apollo / systems engineering | A WBS to see the whole job; reviews before costly steps | Formal configuration control |
| Royce 1970 | Build a throwaway pilot first; loop back between phases | Strict one-way phases |
| PMBOK | Principles as a checklist: value, risk, stakeholders, finance | Process volumes and certification |
| PRINCE2 | A business case checked at each stage; stop when it no longer holds | Board roles and documents |
| Lean / TPS | Cut waste, pull work, fix defects at once | Factory vocabulary |
| Scrum | Short timeboxes, a goal per cycle, a retrospective | Roles and ceremonies for a team |
| XP | Small releases, tests, refactor often | Pairing (unless pairing with an AI) |
| Critical Chain | One shared buffer instead of padding every task; no multitasking | Buffer accounting detail |
| Agile Manifesto | Working output over plans; change is normal | Treating it as a method |
| Kanban | A board, a WIP limit, finish before starting | Classes of service tables |
| SAFe / LeSS / Nexus | Coordination is costly; keep one backlog | Almost everything else |
| OKRs | One objective per quarter with measurable results | Cascading goals |
| #NoEstimates | Slice small and count; forecast from history | Arguing about points |
| Flow metrics | Watch work item age; Monte Carlo for dates | Dashboards nobody reads |
| Shape Up | Appetite, fixed time with variable scope, cool-down, kill unfinished bets | Betting meetings with yourself as theatre |
| Portfolio management | Limit active projects; decide what to pause or kill as a set | Formal governance boards |

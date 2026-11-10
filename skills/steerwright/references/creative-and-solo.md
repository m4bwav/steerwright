# Creative productions and solo practice (checked 2026-11-09)

How film, games, music, art and books get made to done, and how one person keeps a portfolio of projects moving, kills the dead ones, and tables the rest. Most of this is stable practice; few items are volatile. Sources are books and long-standing industry practice; URLs given where a primary source is online.

## (a) How creative productions are managed

### Film
- **Phases:** development (idea, rights, script, financing) -> pre-production (breakdown, casting, locations, schedule, budget) -> production (the shoot) -> post (edit, sound, music, colour, VFX, delivery) -> distribution.
- **Script breakdown and stripboard.** Each scene is broken down into its needs (cast, props, location, day or night). Each scene becomes a strip; strips are reordered by location and cast, not story order, to get the cheapest shooting order. The ordered board becomes the **shooting schedule** and the **call sheets**. Lesson: plan in the order that is cheapest to make, not the order it is watched.
- **Dailies.** Each day's footage is reviewed the next day, so problems are caught while the set still exists. Lesson: short review loops; look at output while redoing it is still cheap.
- **Picture lock.** A hard gate: after lock, the cut does not change and sound, music and colour work on a fixed target. Lesson: freeze one layer before polishing the next.
- For AI film work: shot list = strips, renders = dailies, a locked cut before music and sound.

### Games
- **Phases:** concept -> pre-production (prototypes, find the fun, tech choices) -> **vertical slice** (one short piece at final quality, proving the whole pipeline and the feel) -> production (make all the content) -> **alpha** (feature complete, all systems in, rough) -> **beta** (content complete, bug fixing only) -> **gold / release candidate** -> live ops or patches.
- **Milestones** with stated acceptance criteria, often tied to publisher payments (Chandler, *The Game Production Handbook*).
- **Feature cuts** are normal. Scope is cut to save the date and the quality.
- **Crunch lessons (Schreier, *Blood, Sweat, and Pixels*, 2017).** Across ten games, crunch came from late design decisions, tools that were not ready, and scope that never got cut. Games often found their shape very late. Crunch did not make the games better in a planned way; it burned out teams. Lessons for one person: decide the core early (vertical slice), cut scope instead of extending effort, and expect the "it finally works" moment late.

### Music albums
- Write and demo many songs -> choose the track list -> pre-production (arrangements, tempos, keys) -> tracking -> overdubs -> mixing -> mastering -> artwork, metadata, release.
- Common practice: write more songs than the album needs and pick the best. Mixing and mastering are separate gates. A release date set by distribution lead times (typically several weeks for streaming pitches) forces the finish.

### Art series
- A series is defined up front: a theme, a format, a count (say 12 pieces), a deadline or show date. Studies and thumbnails come first, then finals. The fixed count and the show date are what end it.

### Books
- Outline (or not) -> **first draft** (often "zero" or "vomit" draft; finish before revising) -> structural revision -> line edit -> copy edit -> proofread.
- **Word-count targets** are the main tracker: daily quotas (NaNoWriMo's 50,000 words in a month, about 1,667 a day, made this famous; the NaNoWriMo organisation itself closed in 2025, volatile).
- Lesson: separate drafting from revising. Revising an unfinished draft is a classic stall.

### Common pattern
Every craft has: a cheap exploration phase, a gate that proves the core (slice, demo, picture lock, finished draft), a production phase with fixed scope, and a finishing phase with its own gates. Projects stall most often between exploration and the first gate, and in the last 10%.

## (b) Solo and portfolio practice

### Personal Kanban (Benson and Barry, 2011)
Two rules only: **visualise your work** and **limit your work in progress**. A board with Backlog / Doing / Done, and a small cap on Doing. https://www.personalkanban.com/

### GTD (David Allen, 2001; rev. 2015)
Capture everything, clarify (is it actionable? what is the next action?), organise (projects list, next actions, waiting-for, someday/maybe), **weekly review**, engage. Useful pieces for this skill: every active project has a defined next action; a **someday/maybe** list is where tabled projects go; the weekly review is when they are revisited. https://gettingthingsdone.com/

### Kanban and flow (Anderson, Reinertsen, Vacanti)
- Little's Law: average cycle time = WIP / throughput. More things in progress means each one takes longer, with the same effort.
- Reinertsen: queues are the hidden cost in product development; cost of delay should drive priority.
- Vacanti: forecast from your own throughput history (Monte Carlo), not from estimates.

### Finish or kill
- **Annie Duke, *Quit* (2022).** People quit too late, almost never too early. Set **kill criteria** in advance: "if by date X I have not reached state Y, I quit." Pair a state with a date. Use a "quitting coach" (someone, or something, outside you who says when). Track what you would need to believe to keep going. Being "on the cusp" is the most common reason people do not quit. https://www.annieduke.com/books/
- **Sunk cost research.** Arkes and Blumer (1985), "The psychology of sunk cost", *Organizational Behavior and Human Decision Processes* 35(1): people continue an endeavour once money, effort or time is invested. Staw (1976) on escalation of commitment: people add more to a failing course they chose themselves. Lesson: judge a project only on the cost to finish and the value at finish, never on what is already spent. https://doi.org/10.1016/0749-5978(85)90049-4
- **Jon Acuff, *Finish* (2017).** Perfectionism kills finishing. Cut the goal in half (smaller goal or longer time), choose what to bomb (deliberately neglect other things), make it fun, use private rewards, and beware "the day after perfect", when one missed day becomes quitting. Acuff cites a Dominican University study (Gail Matthews) on writing goals down; it is small and not peer reviewed, so treat it lightly.
- **Shape Up (Basecamp, 2019).** Fixed time, variable scope ("appetite"). Six-week cycles; if a project does not ship in its cycle, it is not extended by default (the "circuit breaker"); it must be re-pitched. Good model for tabling. https://basecamp.com/shapeup

### Side-project portfolios
- Makers with many side projects describe the same failure: many started, few finished, and a backlog that makes each new idea feel more urgent than finishing.
- Common practice: one main project, one or two background ones, an ideas list that is not a commitment. "Ship small" (finish something tiny) beats "start big".
- Treat the portfolio like an investor: few active bets, regular review, kill or table the rest.

### WIP limits for one person
- Context switching costs focus time; Gerald Weinberg's rule of thumb (*Quality Software Management*, 1992) put the loss at roughly 20% per extra concurrent project. It is an estimate, not a measurement, but the direction is well supported by task-switching research (e.g., Rubinstein, Meyer and Evans, 2001, *J. Exp. Psychology: Human Perception and Performance*).
- Personal Kanban practitioners usually suggest a Doing limit of 2-3 for one person.

### Motivation and stall patterns
Common stall points:
1. **After the fun part.** Exploration is done; production is grind.
2. **The last 10%.** Polish, packaging, release chores.
3. **Waiting on a decision.** A question only the maker can answer sits unanswered.
4. **Perfectionism.** The work is "not good enough to show".
5. **A new shiny idea.** Novelty pulls attention away.
6. **A blocking unknown.** A technical or creative problem with no next step.

What restarts a stalled project:
- A **tiny next action** written down (GTD), small enough to do in one sitting or one agent session.
- **Cutting scope** to a version that can ship (Acuff, Shape Up).
- A **visible deadline or audience** (a show, a release date, someone waiting).
- **Answering the blocking decision**, even with a default.
- **Progress made visible** (Amabile and Kramer, *The Progress Principle*, 2011: small wins are the strongest day-to-day motivator in their diary study of knowledge workers).
- A **fresh look**: a short review of what exists, which often shows it is closer to done than it feels.

### Tabling with revisit dates
- Tabling is not quitting. A tabled project leaves the active list, gets a note (why tabled, what state, what would bring it back), and a **revisit date**.
- On the revisit date: restart, re-table with a new date, or kill. A project tabled three times without a restart should be killed or archived by default.
- GTD's someday/maybe list and Shape Up's "no backlog, re-pitch" both support this: the idea must earn its way back.

## Concrete kill and table criteria

Decide these when a project starts or is first reviewed. Write them in the project file.

**Kill (abandon) when any holds:**
1. The kill criterion set at the start is met: by date X, state Y not reached.
2. Cost to finish now exceeds the value at finish, judged without spent effort (sunk cost check).
3. The reason it existed is gone (the game jam passed, the tool it served is dead, someone else shipped it better).
4. It has been tabled three times without real progress in between.
5. The maker, asked "would you start this today, knowing what you know?", says no.

**Table (park with a revisit date) when:**
1. It is waiting on something outside your control (a model, a tool, a person) for more than two weeks.
2. No real progress in 30 days while other projects are moving, but the reason for it still holds.
3. A WIP slot is needed for a higher-value project.
4. A blocking unknown has no next step yet.
Default revisit: 30 days for things waiting on a tool or person; 90 days for things parked for priority.

**Done means:** shipped to its audience (released, published, shown, merged and tagged), with a short close note of what was learned.

## Suggested default WIP limit for a solo maker with AI agents

**Three active projects, of which at most one is the "main" project, plus a review queue limit of about five items awaiting the maker.**

Reasoning:
- With agents, doing is cheap, so the limit is not on agent work but on the maker's attention: deciding, answering questions, reviewing output.
- Personal Kanban practice puts one person at 2-3 in progress. Weinberg's context-switching estimate makes a fourth project cost about as much attention as it adds.
- Agents can push several projects at once, which tempts a higher number. But each active project creates questions and review items; the review queue fills faster than it empties. Little's Law says more WIP means longer cycle time to done, not more done.
- Three lets one project wait on the maker or on a long render while two others move, so agent time is not wasted, without spreading the maker thin.
- The separate review-queue cap (about five open items waiting for the maker across all projects) is the real throttle. When it is full, agents finish or stop, they do not start new work.
- Raise the limit only if finished projects per month go up after raising it. Lower it if projects keep stalling waiting on decisions.

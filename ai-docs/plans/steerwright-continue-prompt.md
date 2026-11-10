# steerwright continue prompt

Start in `D:/m4bwa/Claude/Projects/Ai`. This prompt never changes; state lives in `D:/m4bwa/Claude/Projects/Ai/steerwright/ai-docs/HANDOFF.md`.

## Goal
Build steerwright, the evergreen project management plugin that drives each of Mark's projects to done, tabled or abandoned. The full brief is the kickoff prompt: `D:/m4bwa/Claude/Projects/Ai/plugin-backlog/ai-docs/plans/2026-11-09-steerwright-kickoff-prompt.md` (read its "What to build" and "Books" sections once per session; its order of work is replaced by HANDOFF.md's "Next" list).

## Load state
1. Read HANDOFF.md, `ai-docs/log.md` and `ai-docs/plans/2026-11-09-design.md` in the steerwright folder. Compare HANDOFF.md's age with the log, git history and the askwright answers; trust the newer evidence.
2. Read the chainwright skill (`D:/m4bwa/Claude/Projects/Ai/chainwright/skills/chainwright/SKILL.md`) and follow its rules for this chain.
3. Read the askwright sets HANDOFF.md names with `ask.py read` (`D:/m4bwa/Claude/Projects/Ai/askwright/skills/askwright/scripts/ask.py`). Act on answers; never fill an unanswered or "not sure" question with its guess.
4. Read sibling formats only as needed: askwright, chainwright and grindwright under `D:/m4bwa/Claude/Projects/Ai/`.

## How to work
- Run this as a master session: hand independent batches (reference verification, tests, README/wiki, the everscout beat) to subagents in parallel and keep only their short reports. Hand on to a fresh session only when context runs low.
- Work HANDOFF.md's "Next" list in order, skipping items that wait on Mark and carrying on with the rest.
- Major decisions go on an askwright page (a new set under `steerwright/ask/`, named in HANDOFF.md) while other work carries on. Small rulings: decide, flag them in the log.
- Test sw.py against Mark's real sibling state with a scratch `STEERWRIGHT_HOME` until the setup answers allow writing `~/.steerwright`.
- Standing rules: follow Mark's CLAUDE.md files (`C:/Users/m4bwa/.claude/CLAUDE.md`, `D:/m4bwa/.claude/CLAUDE.md`) and his memory index; they cover attribution, PRs, releases, registries, killing processes and page hosting.

## Stop and ask (askwright page) before
Making the repo public, writing into another plugin's state, adding any scheduled task, publishing to any registry. If nothing can move without Mark, say what waits and stop early.

## Hand-over (fixed order)
1. Run evergreen-wrapup on this session (skip quietly if absent; report a failure, never let it block).
2. Append to `steerwright/ai-docs/log.md`; update HANDOFF.md (status, what waits on Mark, Next list; `Status: finished` when the plugin is released, installed and in existing-plugins.md). Add a line to `plugin-backlog/log.md`.
3. Run `python D:/m4bwa/Claude/Projects/Ai/chainwright/skills/chainwright/scripts/chain.py check` on this prompt and fix findings.
4. Print the same start command as the last lines, with the folder to start in:
   `Execute D:/m4bwa/Claude/Projects/Ai/steerwright/ai-docs/plans/steerwright-continue-prompt.md` (start in `D:/m4bwa/Claude/Projects/Ai`).

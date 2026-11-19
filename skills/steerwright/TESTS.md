# Tests

## T-20261109-1
- harness: evergreen-tester subagents, one fresh run per case (a `claude -p` runner was refused by the auto-mode classifier; `claude plugin eval` needs WSL2 for Bash cases). Trigger results are a subagent proxy for the main loop. Windows 11, Claude Code 2.1.281. No llm judge.
- fixture: per-case scratch STEERWRIGHT_HOME with demo-proj registered active.
- passed 7/7: trigger-status (Skill + `sw.py status`), trigger-wip (`status`, `wip`), trigger-forecast (`forecast` ran; Arvum not in scratch registry, so no dates), decoy-grind (grindwright only), decoy-gantt (chartwright only), action-table (registry check command passed: tabled, revisit 2027-03-01), action-review (questions.json written under reviews/steer-demo-proj-2026-11-09; agent did not decide).
- not covered: 3 runs per case; baseline arm without the skill; forecast dates with real throughput; apply-review.
- observed: `status` in a scratch home showed "asks 4" (open askwright questions read from the real askwright home); review said "No progress for unknown days" for a project with no history.
- worth (lite): UNPROVEN, listing ~211 tokens, body ~1,143; worth looks for evals/ inside the skill folder and found none (the suite lives at repo-root evals/).
- led to: none

## T-20261119-1
- harness: evergreen-tester subagents, one run per case, read-only (same proxy as T-20261109-1). Description edited in this PR; runs saw the installed 0.9.0 text.
- passed 3/3: trigger-inbox (`sw.py inbox`: 116 waiting, 746 min), trigger-tidy (`sw.py tidy` dry run only: 4202 safe, 20 ask, 72 keep; nothing deleted, apply gate quoted), decoy-dependabot (everkeep only).
- baseline arms (skill absent): inbox found ~8 items from a HANDOFF grep plus `gh search prs` (~12.8k noisy tokens; no askwright, chains or backlogs; could not tell stale from open). Tidy found 151 worktrees and judged them by ancestry and PR state, but had no liveness check, no gone-branch or server or scratch view, and no log or undo.
- observed: steerwright is parked in the user CLAUDE.md, so the agents read SKILL.md instead of calling the Skill tool. Trigger evidence is the sw.py call.
- worth: UNPROVEN by the script (no `worth --ab` run); the manual baseline arms favour KEEP. tokenwright: description cut from 958 to 651 chars.
- not covered: 3 runs per case, `worth --ab`.

# Inbox sources: what waits on Mark, what sessions leave behind

Read-only survey, 2026-11-19. Plugin root below is `P = C:/Users/m4bwa/.claude/plugins/cache/mark-local`.
Counts are from today's run. Nothing was changed.

## Part 1: things waiting on Mark

### 1. Pull requests (owner: GitHub, rule from user CLAUDE.md)
- Command: `gh search prs --assignee m4bwav --state open --json repository,number,title,labels,url --limit 100`
  and `gh search prs --label needs-review --owner m4bwav --state open --json repository,number`.
- Format: JSON list; fields `repository.nameWithOwner`, `number`, `title`, `labels[].name`, `url`.
- Count: 1 assigned (`jennyfofenny/arvumelectrum#123` "Construction strips: Mill, Firewood Station, Camp Site, Farm"). 0 labelled needs-review in m4bwav repos.
- Note: the label search with `--owner m4bwav` misses PRs in other owners' repos. Run the label search without `--owner` too and dedupe by url.
- Cleared: PR merged or closed, or assignee removed.
- Verb: none in a plugin. `gh pr merge` / `gh pr review`. releasewright `rw.py merge` only advises (read-only).

### 2. askwright answer sets (owner: askwright 0.43.0)
- Command: `python P/askwright/0.43.0/skills/askwright/scripts/ask.py sweep` (JSON on stdout by default; no `--json` flag).
  Flags: `--apply`, `--prompts FILE`, `--by`, `--min-days N`. Never pass `--apply` from a collector.
- Format: `{ok, warning, counts{used,check,todo,fresh,gone}, used[], check[], todo[], fresh[], gone[], applied, next}`.
  Each item: `set` (folder path), `title`, `project` (askwright project name), `waiting_days`, `read`, `answered[]`, `unsure[]`, `note_only[]`, `stale[]`, `evidence[{kind,detail}]` (kinds seen: `named`, `later_round`).
- Sample: `{"set": "D:\\ComfyUI\\output\\video\\lovecraft\\ask\\zann-part1", "title": "Erich Zann: part one rework", "project": "lovecraft-shorts", "waiting_days": 8.7, "read": true, "answered": ["cut11"], "evidence": []}`
- Counts today: used 0, check 9, todo 3, fresh 2, gone 4. Warning: 2 sets over 7 days.
- Sets live in each project's `ask/<set>/` folder (also vault `.../private/ask/`). Registry: `~/.askwright/sessions/<sha>.json` (one per set), `~/.askwright/projects/<slug>.json`, `~/.askwright/session-state/`, `~/.askwright/sessions-gone/`.
- Unanswered sets (questions Mark has not answered yet) are not in sweep output; sweep covers answered-but-unconsumed. Unanswered ones need the sessions registry (or the askwright dashboard data).
- Cleared: set consumed or dismissed (drops out of sweep).
- Verbs: `ask.py consume <set>` (answers used), `ask.py dismiss <set>`, `ask.py sweep --apply` (marks the "used" pile).
- Mark-facing items: `todo` (no evidence a session used them) and unanswered sets. `check` items are mostly agent work (consume with evidence), not Mark's.

### 3. chainwright (owner: chainwright 0.12.0)
- Registry: `~/.chainwright/runs.json` `{runs: {<ledger path>: {added, report}}}`. Config `~/.chainwright/config.json` `{report, usd_per_mtok}`. Page `~/.chainwright/index.html` is built from runs.json.
- Command: `python P/chainwright/0.12.0/skills/chainwright/scripts/chain_index.py list` prints one JSON line per ledger: `{ledger, exists, added, report}`. Subcommands: add, scan, list, prune, build.
- Count: 108 ledgers registered, only 12 exist. 96 are dead test ledgers in `C:/Users/m4bwa/AppData/Local/Temp/tmp*/grind/logs/` (test pollution; `chain_index.py prune` clears them; Mark-free).
- Ledger `chains.json` fields: `project, name, manager, manager_prompt, parent, report, session, managers, sessions_total, reports_this_manager`, plus per chain `{name, agent_id, prompt, handoff, state, sessions, history[{outcome, seconds, tokens, model}]}`. `state` values seen: `finished`. A non-finished state with a stop reason is a candidate for Mark.
- HANDOFF "Waiting on Mark": 36 `ai-docs/HANDOFF.md` files under `D:/m4bwa/Claude/Projects/Ai/*/` have a `## Waiting on Mark` heading (e.g. arwright, cinewright-gaps, cinewright-mentos). Format: markdown bullets under that heading until the next `##`.
  Sample (arwright): "- Webcam calibration needs a printed board (`arw.py marker`/calibrate) and the Depstech plugged in."
- Cleared: bullet gone from the section, or section empty / "nothing". No verb; the next session edits HANDOFF.
- Also check continue prompts in `ai-docs/plans/*continue-prompt.md` for "stop points" (prose; low value to parse).

### 4. grindwright (owner: grindwright 0.19.7)
- Global index: `~/.grindwright/runs.jsonl` lines `{state: <state dir>, run: <logs/run-*.json>}`; `~/.grindwright/index.html` built by `grind_index.py build`; `~/.grindwright/sessions-cache.json`.
- Distinct state dirs come from `runs.jsonl` (better than a disk search: depth-4 find took over 2 minutes and found only 2).
- State dir files: `ledger.jsonl`, `WAITING.md` (generated), `BOARD.md`, `HANDOFF.md`, `road.json`, `session.json`, `events.jsonl`, `profile.json`.
- WAITING.md found: `D:/Desktop/Create With Code Mark/grind-state/spacedeckbuilder2/WAITING.md` (2 items), `D:/Desktop/Create With Code Mark/ArvumElectrum-anim-work/ai-docs/grind/WAITING.md` (0 items).
  Format: `# Waiting on a person (generated)` then `- <person>: <goal> (<item id>), answers on <where>, <path>; unblocks N`.
  Sample: "- Mark: Card art for the 9 flight deck cards (burn, brake, turn, coast...) (gde7ace), answers on the askwright set, D:/Desktop/Create With Code Mark/SpaceDeckBuilder2/ArtCandidates/ask/cards-2026-11-08-ship-p1-2; unblocks 0"
- ledger.jsonl item fields: `id, goal, lane, cost, human_min, created, finished, evidence, oracle, checkpoints[]`. No `status` field in lines (event style); read WAITING.md or `grw.py --state DIR list`/`board` instead of replaying.
- Cleared: line gone from regenerated WAITING.md.
- Verbs: `grw.py resolve`, `done`, `drop`, `approve`; `wait-human` puts items there.
- Many WAITING lines point at askwright sets; dedupe by set path against source 2.

### 5. everkeep (owner: everkeep 0.2.0)
- Home: `~/.everkeep/` with `state/github/m4bwav/<repo>.json`, `runs/<stamp>/`, `overlay/`.
- State file fields: `repo, duties{prs,vulns,gaps,kb,...: {last_run, run}}, decisions[], inventory`.
- Escalations: 0 state files mention "escalat"; `decisions` was empty in the sample. Last runs are 2026-10-14, so the data is stale.
- Command: `python P/everkeep/0.2.0/skills/everkeep/scripts/keep.py state show <repo> --json`; `keep.py report` / `prs` for live data (dry run by default; prs calls GitHub).
- Cleared: no escalation in latest run report. Verb: `keep.py act` (with --apply, not for collectors).

### 6. Registry publishes and deploys (owner: releasewright 0.2.0, package-modernize)
- releasewright has no state home (`~/.releasewright` absent). `rw.py check|after|merge` are read-only checks per repo, nothing recorded.
- Publishes waiting on go-ahead are recorded only as prose: backlog `#needs-mark` lines (source 7) and HANDOFF "Waiting on Mark" bullets (source 3). Collector: grep those for "publish", "npm", "NuGet", "OpenUPM", "deploy".

### 7. Backlogs `#needs-mark` (owner: none, plain markdown)
- Paths: `D:/m4bwa/Claude/Projects/Ai/plugin-backlog/*.md`, `.../package-backlog/*.md`, `.../server-backlog/*.md`. Skip `ai-docs/archive/`.
- Format: `- [ ] <text> #S|#M|#L #needs-mark`.
- Open counts: plugin-backlog 41 (beats 1, existing-plugins 17, new-plugins 23); package-backlog 5 (existing 3, ports 2); server-backlog 19.
- Sample: "- [ ] Decide engage: probably read-only, since many pixel art spaces ban or attack AI art #S #needs-mark"
- Cleared: `- [x]` or tag removed. No verb.
- The `#S/#M/#L` size tag is a ready Mark-minutes guess.

### 8. evergreen units due (owner: evergreen 1.1.5)
- Command: `python P/evergreen/1.1.5/scripts/evergreen.py audit --json` (also `--brief`, `--fetch`).
- Format: `{home, stale: <int>, units: [{path, name, kind, tier, last, due, status, flags[], claims_due, source_state, tests{last_run, harness, env, cases}}]}`.
- Count: 117 units, 41 stale. Flags seen: `verify-at-use`, `failing-tests:1`, `tests-overdue`.
- Cleared: `evergreen.py checked <unit>` after a refresh. Mostly agent work, not Mark's; treat as low-priority leftovers.

### 9. steerwright registry (owner: steerwright)
- `~/.steerwright/projects.json`: `{steerwright: 1, wip_limit, projects: {<id>: {name, paths[], kind, status, goal, done_when, target, revisit, wake, created, updated, sources{askwright: [<askwright project names>]}, history[]}}}`.
- Mapping rule: an item maps to a project when its path starts with one of `paths[]` (normalise slashes and case), or its askwright `project` string is in `sources.askwright`. Grindwright state dirs and chain ledgers map by path prefix. PR repos map by matching a git remote of a project path (needs a lookup).

## Part 2: leftovers

### 10. Worktrees
- Folders in `D:/m4bwa/Claude/Projects/Ai` matching `*-wt-*`, `_wt*`, `wt-*`, `*-wt`: 123. Only 49 have a `.git` file; 74 are empty or near-empty leftovers (e.g. `readwright-wt-race`, 8 KB, no .git) from removed worktrees.
- `_wt/` is a container of more worktrees (e.g. `_wt/readwright-pages`); list them with `git -C <repo> worktree list --porcelain`.
- Of the 49: 31 have HEAD contained in `origin/HEAD` (merged), 18 not, 4 with upstream gone, 1 dirty.
- Detect: `git -C D merge-base --is-ancestor HEAD origin/HEAD` (exit 0 = merged); `git -C D status -sb` first line contains `[gone]`; `git -C D status --porcelain` non-empty = dirty (never offer removal then). Squash merges are not ancestors: also check `gh pr list --head <branch> --state merged`.
- Clear: `git worktree remove <dir>` then `git branch -d`; for empty non-git folders a plain delete. Mark-free unless dirty.

### 11. Stale local branches
- `git -C <repo> for-each-ref --format='%(refname:short) %(upstream:track)' refs/heads` and `git branch --merged origin/HEAD`.
- Sample repo readwright: 33 branches merged into origin/HEAD, 17 with upstream gone.
- Clear: `git branch -d` (merged) or `-D` after a squash-merge check. Mark-free.

### 12. Local dev servers and pid files
- `netstat -ano` LISTENING lines joined with `tasklist /FO CSV /NH` on pid. 17 python.exe listeners on 127.0.0.1 today: 18765 (3 pids on one port), 18841, 18950, 55454, 56247, 62110, 8765, 8766, 8767, 8779, 8790, 8841, 8893, 8199 (ComfyUI, keep), 47631 (askwright shared server).
- Known keepers: 8199 ComfyUI, 11434 Ollama, 47631 askwright host. Others are probably askwright/review page servers from old sessions.
- `~/.steerwright/server.json`: `{url, port, pid, started, hosted_by}`. Today it says pid 62864 on 47631, but 47631 is held by pid 21380. The pid record is stale (hosted by askwright, which restarted).
- askwright keeps its own state in `~/.askwright/session-state/` and `dashboard/`; read those for its server pids.
- Clear: kill by pid only (quirkwright `qw.py pid` to confirm), never by name. Collector only reports.

### 13. Scratch dirs
- `C:/Users/m4bwa/AppData/Local/Temp/claude/`: 4046 entries, 6.0 GB. One folder per project slug, then one per session id, each with `scratchpad/` and `tasks/`.
- `C:/Users/m4bwa/AppData/Local/Temp/tmp*`: 3148 folders (many are test homes from plugin test suites).
- Use `du -s` per folder with a timeout; skip the running session's own folder. Clear: delete folders older than N days. Mark-free.

## Overlap: read their output, do not redo it
- chainwright index: `chain_index.py list` already resolves ledgers and existence. Read it plus each ledger's chain `state`. Do not rescan disks for ledgers.
- grindwright: WAITING.md is generated by grw with the person, item id and askwright path. Read WAITING.md for every state dir in `~/.grindwright/runs.jsonl`. Do not replay ledger.jsonl.
- askwright sweep: already classifies answered sets into used/check/todo/fresh/gone with age and evidence, and maps each to an askwright project. Read its JSON; do not parse answer files.
- everkeep: per-repo duties and decisions in `~/.everkeep/state/github/m4bwav/*.json`. Read those files (cheap, offline). Do not call GitHub for PR triage; flag the state as stale when `last_run` is old.
- releasewright: nothing stored. `rw.py check` is per repo and live; call it only on demand for one project, not in the inbox sweep.
- evergreen: `audit --json` gives stale count and flags; read it as is.

## Collector plan
- `prs`: gh search (assignee m4bwav; label needs-review, any owner). About 10 min per PR.
- `ask-todo`: `ask.py sweep` JSON, piles todo + check over 7 days. About 1 min per set to say used or dismiss.
- `ask-unanswered`: `~/.askwright/sessions/*.json` with no answers. About 3 to 10 min per set.
- `grind-waiting`: WAITING.md per state dir from `~/.grindwright/runs.jsonl`. About 5 min per line, deduped against ask sets.
- `handoff-waiting`: `## Waiting on Mark` bullets in `ai-docs/HANDOFF.md` under registered project paths. About 5 min per bullet.
- `chain-stopped`: `chain_index.py list` plus ledgers with chains not finished. About 2 min each.
- `backlog-needs-mark`: open `#needs-mark` lines in the three backlogs. S=2, M=10, L=30 min.
- `publish-goahead`: needs-mark and handoff lines mentioning publish, npm, NuGet, OpenUPM, deploy. About 5 min each.
- `everkeep-escalations`: state json decisions and run reports. About 10 min each; flag stale runs.
- `evergreen-due`: `evergreen.py audit --json` stale units. 0 min for Mark (agent work).
- `worktrees`: merged, gone or empty wt folders, dirty ones flagged. 0 min (agent), 2 min if dirty.
- `branches`: merged or gone local branches per repo. 0 min.
- `servers`: python/node listeners minus keepers, plus stale server.json pids. 1 min to confirm a kill.
- `scratch`: Temp/claude and Temp/tmp* folders by age and size. 0 min.
- `chain-index-junk`: dead ledgers in runs.json (`chain_index.py prune`). 0 min.

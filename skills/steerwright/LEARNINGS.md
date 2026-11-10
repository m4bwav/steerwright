# Learnings: steerwright

Procedural lessons for SKILL.md. Research findings live in [RESEARCH.md](RESEARCH.md); every change is logged in [CHANGELOG.md](CHANGELOG.md); state in `evergreen.json`. Format and write-time gate: MAINTENANCE.md (LEARNINGS-FORMAT). Retired entries go to LEARNINGS-ARCHIVE.md with a reason.

Write an entry the moment a real signal happens: a user correction, the same error twice, a workaround, an environment fact, a stated preference, or a failure in use. Trigger and Hypothesis are required. Promote after three confirmations; retire when harmful > helpful.

## Active

### L-001 · 2026-11-09 · "Checked" lines written by agents that did not open sources are not checks
- Trigger: 2026-11-09 verification pass found the reference files marked "checked 2026-11-09" though most sources were never opened; several facts were wrong (METR 18%, Asana agent count)
- Hypothesis: research agents write the check date from the task date, not from what they fetched
- Rule: mark each source line "opened", "via search" or "(unverified)"; a bare date proves nothing
- Evidence: C-20261109-1
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-11-09

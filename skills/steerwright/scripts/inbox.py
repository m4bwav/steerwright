"""steerwright inbox: everything waiting on Mark, read from the owning tools' state. Stdlib only.

Each collector returns normalised items and fails soft: an error becomes a note, never a crash.
Read-only: it calls other plugins' read commands (ask.py sweep, evergreen.py audit, gh search) and reads
their files, and never writes their state. Results are cached in <steerwright home>/inbox-cache.json.
"""
import hashlib
import json
import urllib.parse
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

import sw

CACHE_SECONDS = 15 * 60
AGED_DAYS = 14
SIZE_MINUTES = {"S": 2, "M": 10, "L": 30}
DEFAULT_BACKLOGS = [r"D:\m4bwa\Claude\Projects\Ai\plugin-backlog", r"D:\m4bwa\Claude\Projects\Ai\package-backlog",
                    r"D:\m4bwa\Claude\Projects\Ai\server-backlog"]


def run(cmd, timeout=60):
    """Run a read-only command and return stdout; raises on failure. Tests replace this."""
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    if r.returncode != 0:
        raise RuntimeError((r.stderr or r.stdout or "exit %d" % r.returncode).strip()[:200])
    return r.stdout


def config():
    return sw.read_json(sw.home() / "config.json", {}) or {}


def item_id(source, key):
    return source + ":" + hashlib.sha1(str(key).encode("utf-8")).hexdigest()[:10]


def age_days(ts):
    dt = sw.parse_ts(ts) if isinstance(ts, str) else ts
    if not dt:
        return None
    return round((datetime.now() - dt).total_seconds() / 86400, 1)


def mtime_days(path):
    try:
        return round((time.time() - os.path.getmtime(path)) / 86400, 1)
    except OSError:
        return None


def make(source, key, title, kind, action, minutes, age=None, link=None, path=None, project_hint=None):
    return {"id": item_id(source, key), "source": source, "kind": kind, "title": title.strip(), "age_days": age,
            "link": link, "path": str(path) if path else None, "action": action, "minutes": minutes,
            "project_hint": project_hint}


# ---------- collectors ----------

def c_prs():
    seen, out = set(), []
    queries = [["gh", "search", "prs", "--assignee", "m4bwav", "--state", "open"],
               ["gh", "search", "prs", "--label", "needs-review", "--owner", "m4bwav", "--state", "open"],
               ["gh", "search", "prs", "--review-requested", "m4bwav", "--state", "open"]]  # a label search with no owner returns strangers' PRs
    for q in queries:
        rows = json.loads(run(q + ["--json", "repository,number,title,url,createdAt", "--limit", "100"]) or "[]")
        for r in rows:
            if r["url"] in seen:
                continue
            seen.add(r["url"])
            repo = (r.get("repository") or {}).get("nameWithOwner", "")
            out.append(make("prs", r["url"], "%s#%s %s" % (repo, r["number"], r["title"]), "review",
                            "review and merge or close the PR", 10, age_days(r.get("createdAt")), link=r["url"],
                            project_hint={"repo": repo}))
    return out


def c_ask():
    script = sw.ask_script()
    if not script:
        raise RuntimeError("askwright not installed")
    data = json.loads(run([sys.executable, script, "sweep"]))
    out = []
    for pile, action, minutes in (("todo", "say whether the answers were used: ask.py consume or dismiss", 1),
                                  ("check", "consume with evidence (agent work) or dismiss", 1)):
        for s in data.get(pile) or []:
            if pile == "check" and (s.get("waiting_days") or 0) < 7:
                continue
            out.append(make("ask", s["set"], s.get("title") or Path(s["set"]).name, "answers-unused", action, minutes,
                            s.get("waiting_days"), path=s["set"], project_hint={"path": s["set"], "ask": s.get("project")}))
    return out


def c_ask_unanswered():
    out = []
    for path, q, a in sw.askwright_sets():
        if a or (Path(path) / "consumed.json").exists():
            continue
        n = len(q.get("questions") or [])
        out.append(make("ask-unanswered", path, q.get("title") or Path(path).name, "answer",
                        "answer the askwright set", max(3, min(10, n)), mtime_days(Path(path) / "questions.json"),
                        path=path, project_hint={"path": path, "ask": sw.set_project_name(q)}))
    return out


def c_grind():
    out = []
    for st in sw.grind_states():
        f = Path(st) / "WAITING.md"
        if not f.exists():
            continue
        for line in f.read_text(encoding="utf-8").splitlines():
            m = re.match(r"-\s*Mark:\s*(.+)", line.strip())
            if not m:
                continue
            text = m.group(1)
            ask = re.search(r"askwright set, (.+?); unblocks", text)
            out.append(make("grind", st + "|" + text, text.split(", answers on")[0], "decision",
                            "answer it where the line says", 5, mtime_days(f), path=f,
                            project_hint={"path": st, "ask_set": ask.group(1) if ask else None}))
    return out


def handoff_bullets(text):
    m = re.search(r"^##\s+Waiting on Mark\s*$(.*?)(?=^##\s|\Z)", text, re.M | re.S)
    if not m:
        return []
    return [b.strip()[2:].strip() for b in m.group(1).splitlines() if re.match(r"\s*[-*]\s+\S", b)]


def c_handoff():
    out, seen = [], set()
    for p in sw.load()["projects"].values():
        if p.get("status") != "active":
            continue
        for root in p.get("paths") or []:
            f = Path(root) / "ai-docs" / "HANDOFF.md"
            if sw.norm(f) in seen or not f.exists():
                continue
            seen.add(sw.norm(f))
            for b in handoff_bullets(f.read_text(encoding="utf-8")):
                if re.match(r"(nothing|none)\b", b.lower()):
                    continue
                pub = re.search(r"\b(publish|npm|nuget|openupm|deploy)\b", b, re.I)
                out.append(make("handoff", str(f) + "|" + b, b, "go-ahead" if pub else "decision",
                                "decide and tell the next session", 5, mtime_days(f), path=f,
                                project_hint={"path": root}))
    return out


def c_backlog():
    out = []
    for root in config().get("inbox_backlogs") or DEFAULT_BACKLOGS:
        for f in sorted(Path(root).glob("*.md")):
            for line in f.read_text(encoding="utf-8").splitlines():
                if not line.lstrip().startswith("- [ ]") or "#needs-mark" not in line:
                    continue
                size = re.search(r"#([SML])\b", line)
                text = re.sub(r"#\S+", "", line.split("- [ ]", 1)[1]).strip()
                pub = re.search(r"\b(publish|npm|nuget|openupm|deploy)\b", text, re.I)
                out.append(make("backlog", str(f) + "|" + text, text, "go-ahead" if pub else "decision",
                                "decide, then tick it or drop #needs-mark", SIZE_MINUTES[size.group(1)] if size else 10,
                                mtime_days(f), path=f, project_hint={"path": root}))
    return out


def c_chains():
    out = []
    for ledger, data, _info in sw.chain_ledgers():
        for ch in data.get("chains") or []:
            if ch.get("state") in (None, "finished", "running"):
                continue
            hist = ch.get("history") or []
            out.append(make("chain", ledger + "|" + ch.get("name", ""), "chain %s %s" % (ch.get("name", "?"), ch["state"]),
                            "unblock", "read the chain HANDOFF and unblock or close it", 2, mtime_days(ledger),
                            path=ch.get("handoff") or ledger, project_hint={"path": data.get("project") or ledger}))
            if hist:
                out[-1]["title"] += " (%s)" % (hist[-1].get("outcome") or "")
    return out


def c_evergreen():
    script = sw.sibling_script("evergreen", "scripts/evergreen.py")
    if not script:
        raise RuntimeError("evergreen not installed")
    data = json.loads(run([sys.executable, str(script), "audit", "--json"], timeout=120))
    n = sum(1 for u in data.get("units") or [] if str(u.get("status", "")).upper().startswith("STALE"))
    if not n:
        return []
    return [make("evergreen", "stale", "%d evergreen units due for refresh" % n, "agent-work",
                 "run evergreen-refresh in a session (no Mark time)", 0)]


COLLECTORS = {"prs": c_prs, "ask": c_ask, "ask-unanswered": c_ask_unanswered, "grind": c_grind,
              "handoff": c_handoff, "backlog": c_backlog, "chain": c_chains, "evergreen": c_evergreen}


# ---------- project mapping ----------

def map_project(it, projects):
    hint = it.pop("project_hint", None) or {}
    for key, p in projects.items():
        if hint.get("ask") and hint["ask"] in ((p.get("sources") or {}).get("askwright") or []):
            return key
    for k in ("path", "ask_set"):
        if hint.get(k):
            for key, p in projects.items():
                if any(sw.under(hint[k], root) for root in p.get("paths") or []):
                    return key
    return None


def dedupe(items):
    """A grind line that points at an askwright set already listed is the same decision."""
    sets = {sw.norm(i["path"]) for i in items if i["source"] in ("ask", "ask-unanswered") and i["path"]}
    return [i for i in items if not (i["source"] == "grind" and i.get("_ask_set") and sw.norm(i["_ask_set"]) in sets)]


def collect(only=None, fresh=False):
    cache = sw.home() / "inbox-cache.json"
    if not fresh and not only:
        c = sw.read_json(cache, None)
        if c and time.time() - c.get("at", 0) < CACHE_SECONDS:
            c["cached"] = True
            return c
    projects = sw.load()["projects"]
    items, notes = [], []
    for name, fn in COLLECTORS.items():
        if only and name not in only:
            continue
        try:
            got = fn()
        except Exception as e:  # each collector fails soft
            notes.append("%s: %s" % (name, str(e)[:200]))
            continue
        for it in got:
            ask_set = (it.get("project_hint") or {}).get("ask_set")
            it["project"] = map_project(it, projects)
            if ask_set:
                it["_ask_set"] = ask_set
            items.append(it)
    items = dedupe(items)
    for it in items:
        it.pop("_ask_set", None)
    items.sort(key=lambda i: -(i["age_days"] or 0))
    out = {"at": time.time(), "generated": sw.now_iso(), "count": len(items),
           "minutes": sum(i["minutes"] for i in items), "items": items, "notes": notes, "cached": False}
    if not only:
        sw.write_json(cache, out)
        record_history(out)
    return out


# ---------- age and load metrics ----------

def median(xs):
    xs = sorted(xs)
    if not xs:
        return None
    m = len(xs) // 2
    return xs[m] if len(xs) % 2 else round((xs[m - 1] + xs[m]) / 2, 1)


def stat(items):
    return {"count": len(items), "minutes": sum(i["minutes"] for i in items),
            "median_age": median([i["age_days"] for i in items if i["age_days"] is not None])}


def snapshot(out):
    """One line of inbox history: totals, and per project counts, minutes and median age."""
    per = {}
    for i in out["items"]:
        per.setdefault(i["project"] or "-", []).append(i)
    return dict(stat(out["items"]), date=sw.today().isoformat(), projects={k: stat(v) for k, v in per.items()})


def record_history(out):
    """Append today's snapshot to inbox-history.jsonl; a later run the same day replaces it."""
    path = sw.home() / "inbox-history.jsonl"
    snap = snapshot(out)
    rows = [r for r in sw.read_jsonl(path) if r.get("date") != snap["date"]] + [snap]
    path.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")


def metrics(out, weeks=12, project=None):
    """Weekly series: decisions waiting, Mark-minutes queued and median age at each week's last snapshot.
    Weeks with no snapshot are backfilled from today's items' ages (items still open then; a lower bound)."""
    hist = {}
    for r in sw.read_jsonl(sw.home() / "inbox-history.jsonl"):
        try:
            d = datetime.strptime(r.get("date") or "", "%Y-%m-%d").date()
        except ValueError:
            continue
        hist[sw.week_start(d)] = r  # rows are in date order, so each week keeps its last one
    items = [i for i in out["items"] if project is None or (i["project"] or "-") == project]
    now = sw.today()
    rows = []
    for k in range(weeks - 1, -1, -1):
        ws = sw.week_start(now) - timedelta(weeks=k)
        r = hist.get(ws)
        if r and project is not None:
            r = (r.get("projects") or {}).get(project) or {"count": 0, "minutes": 0, "median_age": None}
        if r:
            rows.append({"week": ws.isoformat(), "count": r["count"], "minutes": r["minutes"],
                         "median_age": r.get("median_age"), "source": "snapshot"})
            continue
        back = (now - min(ws + timedelta(days=6), now)).days
        then = [dict(i, age_days=round(i["age_days"] - back, 1)) for i in items
                if i["age_days"] is not None and i["age_days"] >= back]
        rows.append(dict(stat(then), week=ws.isoformat(), source="backfill"))
    return rows


def per_project(out):
    """Today's load per project, heaviest first."""
    return sorted(snapshot(out)["projects"].items(), key=lambda kv: (-kv[1]["minutes"], kv[0]))


def review_summary(key, aged_days=None):
    """Text block for a project's weekly review: its waiting items, all projects' counts, and the last tidy dry run.
    Reads the inbox (cached) and the tidy summary file only; asks nothing new."""
    aged_days = aged_days or config().get("inbox_aged_days") or AGED_DAYS
    lines = []
    try:
        c = collect()
    except Exception as e:  # the review never fails on the inbox
        c = None
        lines.append("Inbox unavailable: %s" % str(e)[:200])

    def oldest(items):
        return "; ".join("%s (%.0f d)" % (i["title"][:80], i["age_days"] or 0) for i in items[:3])

    if c:
        mine = [i for i in c["items"] if i.get("project") == key]
        aged = [i for i in c["items"] if (i["age_days"] or 0) > aged_days]
        lines.append("This project: %d waiting on you, about %d minutes%s" % (
            len(mine), sum(i["minutes"] for i in mine), (". Oldest: " + oldest(mine)) if mine else ""))
        lines.append("All projects: %d waiting, about %d minutes; %d older than %d days%s" % (
            c["count"], c["minutes"], len(aged), aged_days, (". Oldest: " + oldest(c["items"])) if c["items"] else ""))
    t = sw.read_json(sw.home() / "tidy-summary.json", None)
    if t:
        n = t.get("counts") or {}
        lines.append("Leftovers (tidy dry run %s): %d safe to remove, %d need you, %d kept" % (
            (t.get("generated") or "")[:10], n.get("safe", 0), n.get("ask", 0), n.get("keep", 0)))
    else:
        lines.append("Leftovers: no tidy dry run yet (sw.py tidy)")
    return {"type": "text", "text": "Waiting on you and leftovers:\n- " + "\n- ".join(lines)}


def cmd_inbox(a):
    out = collect(only=a.source, fresh=a.fresh)
    if getattr(a, "metrics", False):
        m = {"weeks": metrics(out), "projects": dict(per_project(out))}
        if a.json:
            print(json.dumps(m, indent=1, ensure_ascii=False))
            return
        for w in m["weeks"]:
            print("%s  %4d waiting  %5d min  median %s d  (%s)" % (w["week"], w["count"], w["minutes"], w["median_age"], w["source"]))
        for k, v in m["projects"].items():
            print("  %-28s %4d  %5d min  median %s d" % (k[:28], v["count"], v["minutes"], v["median_age"]))
        return
    if a.json:
        print(json.dumps(out, indent=1, ensure_ascii=False))
        return
    print("%d waiting, about %d Mark-minutes%s" % (out["count"], out["minutes"], " (cached)" if out.get("cached") else ""))
    for i in out["items"]:
        age = "%5.1fd" % i["age_days"] if i["age_days"] is not None else "    ?"
        print("%s  %-14s %-22s %s" % (age, i["source"], (i["project"] or "-")[:22], i["title"][:90]))
    for n in out["notes"]:
        print("note: " + n)


# ---------- clearing ----------

def ask_urls():
    """askwright set path -> its page on askwright's shared server, from askwright's own records. {} when it is down."""
    ah = sw.sib_home("askwright")
    base = (sw.read_json(ah / "dashboard" / "server.json", {}) or {}).get("dashboard_url")
    if not base:
        return {}
    out = {}
    for f in (ah / "sessions").glob("*.json"):
        path = (sw.read_json(f, {}) or {}).get("path")
        if path:
            out[sw.norm(path)] = base.rstrip("/") + "/s/%s/" % f.stem[:12]
    return out


def clear_controls(i, urls):
    """The owning tool's verbs for one item: an Open link, and askwright's consume and dismiss as commands to copy.
    steerwright runs none of them; writing askwright's state stays askwright's job."""
    esc = sw.esc
    target = i["link"] or (urls.get(sw.norm(i["path"])) if i["source"] in ("ask", "ask-unanswered") and i["path"] else None)
    out = f"<a class='btn' href='{esc(target)}' target='_blank'>Open</a>" if target else ""
    if i["source"] == "ask":
        script = sw.ask_script() or "ask.py"
        for verb in ("consume", "dismiss"):
            cmd = 'python "%s" %s "%s" --note ""' % (script, verb, i["path"])
            out += (f" <button class='btn' title='{esc(cmd)}' data-cmd='{esc(cmd)}' "
                    f"onclick='navigator.clipboard.writeText(this.dataset.cmd);this.textContent=&quot;copied&quot;'>{verb}</button>")
    return out


# ---------- page ----------

QUICK_MINUTES = 2


def load_section(out, names):
    """Age and load: weekly charts and today's per project table, folded under the tiles."""
    esc = sw.esc
    m = metrics(out)
    labels = [w["week"] for w in m]
    back = sum(1 for w in m if w["source"] == "backfill")
    charts = ("<div class='charts'>"
              + sw.svg_bars([w["count"] for w in m], labels, title="Decisions waiting on you, per week")
              + sw.svg_lines([("Mark-minutes", [w["minutes"] for w in m])], labels, title="Mark-minutes queued")
              + sw.svg_lines([("median age", [w["median_age"] or 0 for w in m])], labels, title="Median age of waiting items (days)")
              + "</div>")
    rows = "".join(f"<tr><td>{esc(names.get(k, 'no project' if k == '-' else k))}</td><td>{v['count']}</td><td>{v['minutes']}</td>"
                   f"<td>{v['median_age'] if v['median_age'] is not None else '?'}</td></tr>" for k, v in per_project(out))
    return (f"<details><summary>Age and load per week and per project</summary>{charts}"
            f"<p class='mut'>{back} of {len(m)} weeks are backfilled from today's ages, so items cleared since are missing there; "
            f"the rest are daily snapshots in inbox-history.jsonl.</p>"
            f"<table><tr><th>Project</th><th>Waiting</th><th>Mark-minutes</th><th>Median age (d)</th></tr>{rows}</table></details>")


def inbox_page(data, q):
    """/inbox: oldest first, grouped by project then kind, filters by query (project, kind, source, quick=1, fresh=1)."""
    esc = sw.esc
    out = collect(fresh=q.get("fresh", ["0"])[0] not in ("0", ""))
    pick = {k: q.get(k, [""])[0] for k in ("project", "kind", "source")}
    quick = q.get("quick", ["0"])[0] not in ("0", "")
    items = [i for i in out["items"]
             if (not pick["project"] or (i["project"] or "-") == pick["project"])
             and (not pick["kind"] or i["kind"] == pick["kind"])
             and (not pick["source"] or i["source"] == pick["source"])
             and (not quick or i["minutes"] <= QUICK_MINUTES)]
    names = {k: p["name"] for k, p in data["projects"].items()}
    urls = ask_urls()

    def link(**kw):
        cur = dict(pick, quick="1" if quick else "")
        cur.update(kw)
        qs = urllib.parse.urlencode({k: v for k, v in cur.items() if v})
        return "/inbox" + ("?" + qs if qs else "")

    def chips(key, values):
        on = pick.get(key, "")
        return (f"<a class='{'on' if not on else ''}' href='{esc(link(**{key: ''}))}'>all</a>"
                + "".join(f"<a class='{'on' if on == v else ''}' href='{esc(link(**{key: v}))}'>{esc(names.get(v, v))} ({n})</a>"
                          for v, n in values))

    def counts(field):
        c = {}
        for i in out["items"]:
            v = (i[field] or "-") if field == "project" else i[field]
            c[v] = c.get(v, 0) + 1
        return sorted(c.items(), key=lambda kv: (-kv[1], kv[0]))

    def row(i):
        where = i["link"] or i["path"] or ""
        target = (f"<a href='{esc(where)}'>{esc(where)}</a>" if where.startswith("http")
                  else f"<code>{esc(where)}</code>") if where else ""
        age = "%.1f d" % i["age_days"] if i["age_days"] is not None else "?"
        return (f"<tr><td>{age}</td><td>{esc(i['title'])}<div class='mut'>{esc(i['source'])} &middot; {target}</div></td>"
                f"<td>{esc(i['action'])}<div>{clear_controls(i, urls)}</div></td><td class='num'>{i['minutes']}</td></tr>")

    groups = {}
    for i in items:  # already oldest first; groups keep their oldest item first too
        groups.setdefault((i["project"] or "-", i["kind"]), []).append(i)
    order = sorted(groups, key=lambda g: -(groups[g][0]["age_days"] or 0))
    head = "<tr><th>Age</th><th>What</th><th>Clears it</th><th class='num'>Min</th></tr>"
    quick_items = [i for i in items if i["minutes"] <= QUICK_MINUTES]  # the lane follows the filters
    lane = ("" if quick or not quick_items else
            f"<h2>Clears in under {QUICK_MINUTES} minutes ({len(quick_items)})</h2><table>{head}"
            + "".join(row(i) for i in quick_items[:15]) + "</table>"
            + (f"<p><a href='{esc(link(quick='1'))}'>all {len(quick_items)}</a></p>" if len(quick_items) > 15 else ""))
    style = ("<style>.btn{display:inline-block;margin:4px 4px 0 0;padding:2px 9px;font:inherit;font-size:12px;"
             "border:1px solid var(--line);border-radius:6px;background:var(--card);color:var(--blue);"
             "text-decoration:none;cursor:pointer}</style>")
    body = (style + f"<div class='top'><h1>steerwright</h1><span>{sw.today()}</span><span>{sw.sibling_links()}</span></div>"
            + sw.tabs("inbox", data)
            + f"<div class='tiles'><div class='tile'><b>{out['count']}</b><span>waiting</span></div>"
              f"<div class='tile'><b>{out['minutes']}</b><span>Mark-minutes</span></div>"
              f"<div class='tile'><b>{len(quick_items)}</b><span>under {QUICK_MINUTES} min</span></div></div>"
            + f"<p class='mut'>Built {esc(out['generated'])}{' (cached)' if out.get('cached') else ''}. "
              f"<a href='{esc(link(fresh='1'))}'>refresh</a> &middot; <a href='{esc(link(quick='' if quick else '1'))}'>"
              f"{'show everything' if quick else 'quick ones only'}</a></p>"
            + "".join(f"<div class='warn'>collector failed: {esc(n)}</div>" for n in out["notes"])
            + f"<nav class='tabs'>{chips('project', counts('project'))}</nav>"
            + f"<nav class='tabs'>{chips('kind', counts('kind'))}</nav>"
            + f"<nav class='tabs'>{chips('source', counts('source'))}</nav>"
            + load_section(out, names)
            + lane
            + ("".join(f"<h2>{esc(names.get(p, 'no project' if p == '-' else p))} &middot; {esc(k)} ({len(groups[(p, k)])})</h2>"
                       f"<table>{head}" + "".join(row(i) for i in groups[(p, k)]) + "</table>" for p, k in order)
               if items else "<p class='mut'>Nothing waiting on you here. Clear a filter above or <a href='/inbox?fresh=1'>refresh</a> to check again.</p>"))
    return sw.page("waiting on you: steerwright", body)

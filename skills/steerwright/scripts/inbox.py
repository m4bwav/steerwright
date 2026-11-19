"""steerwright inbox: everything waiting on Mark, read from the owning tools' state. Stdlib only.

Each collector returns normalised items and fails soft: an error becomes a note, never a crash.
Read-only: it calls other plugins' read commands (ask.py sweep, evergreen.py audit, gh search) and reads
their files, and never writes their state. Results are cached in <steerwright home>/inbox-cache.json.
"""
import hashlib
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

import sw

CACHE_SECONDS = 15 * 60
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
    return out


def cmd_inbox(a):
    out = collect(only=a.source, fresh=a.fresh)
    if a.json:
        print(json.dumps(out, indent=1, ensure_ascii=False))
        return
    print("%d waiting, about %d Mark-minutes%s" % (out["count"], out["minutes"], " (cached)" if out.get("cached") else ""))
    for i in out["items"]:
        age = "%5.1fd" % i["age_days"] if i["age_days"] is not None else "    ?"
        print("%s  %-14s %-22s %s" % (age, i["source"], (i["project"] or "-")[:22], i["title"][:90]))
    for n in out["notes"]:
        print("note: " + n)

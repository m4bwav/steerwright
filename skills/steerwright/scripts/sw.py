#!/usr/bin/env python3
"""steerwright: drive every project to done, tabled or abandoned. Stdlib only.

Registry: ~/.steerwright/projects.json (STEERWRIGHT_HOME moves it). Read-only over askwright, chainwright and
grindwright state: this script never writes their files.

  sw.py discover [--root DIR ...] [--apply]   propose registry entries from sibling state (askwright projects,
                                              chain ledgers, grind states, ai-docs/HANDOFF.md); --apply adds them
  sw.py add NAME --path DIR [--kind K] [--goal G] [--done-when D] [--target YYYY-MM-DD]
  sw.py status [NAME] [--json]                portfolio or one project: health, activity, open asks, flow
  sw.py item NAME add TITLE | done ID | drop ID   steerwright's own remaining-items list (for projects with no grind ledger)
  sw.py forecast NAME [--trials 10000]        Monte Carlo finish range from weekly throughput (50/85/95 %)
  sw.py review NAME [--weeks N] [--no-serve]  weekly review: progress, stalls, next actions, keep/table/abandon check
                                              written as an askwright set under ~/.steerwright/reviews and served
  sw.py table NAME --revisit YYYY-MM-DD --wake TEXT
  sw.py abandon NAME --why TEXT [--keep TEXT]  closes it with a short post-mortem
  sw.py done NAME [--note TEXT] | sw.py activate NAME
  sw.py wip [N]                               show or set the WIP limit on active projects (default 8)
  sw.py stall [WEEKS]                         show or set the stall rule for reviews (default 8 weeks)
  sw.py merge NAME... --into NAME             fold projects into one (a group counts once against the WIP limit)
  sw.py serve [--port P] [--detach] [--open]  local pages on 127.0.0.1 (main + one per project)
  sw.py up | down                             start steerwright + askwright dashboard, build chain/grind indexes, open;
                                              down stops only the PIDs up started
"""
import argparse
import html
import json
import os
import random
import re
import subprocess
import sys
import threading
import time
import urllib.parse
import urllib.request
import webbrowser
from datetime import date, datetime, timedelta
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

VERSION = "0.2.0"
STATUSES = ("active", "tabled", "abandoned", "done")
KINDS = ("software", "game", "film", "art", "music", "writing", "engineering", "other")
DEFAULT_PORT = 47630
DEFAULT_WIP = 8
STALL_WEEKS = 8
CACHE_TTL = 300
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", "Library", "Temp", "obj", "bin", "Logs"}


# ---------- paths and io ----------

def home():
    return Path(os.environ.get("STEERWRIGHT_HOME") or Path.home() / ".steerwright")


def sib_home(name):
    env = {"askwright": "ASKWRIGHT_HOME", "chainwright": "CHAINWRIGHT_HOME", "grindwright": "GRINDWRIGHT_HOME"}[name]
    return Path(os.environ.get(env) or Path.home() / ("." + name))


def today():
    fixed = os.environ.get("STEERWRIGHT_TODAY")
    return date.fromisoformat(fixed) if fixed else date.today()


def now_iso():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def read_json(path, default=None):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def read_jsonl(path):
    out = []
    try:
        for line in Path(path).read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line:
                try:
                    out.append(json.loads(line))
                except ValueError:
                    pass
    except OSError:
        pass
    return out


def write_json(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def norm(p):
    return os.path.normcase(os.path.abspath(str(p))).rstrip("\\/")


def under(child, parent):
    c, p = norm(child), norm(parent)
    return c == p or c.startswith(p + os.sep)


def is_temp(p):
    t = norm(os.environ.get("TEMP") or os.environ.get("TMPDIR") or "/tmp")
    return norm(p).startswith(t)


def slug(name):
    s = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return s or "project"


def parse_ts(text):
    if not text:
        return None
    try:
        dt = datetime.fromisoformat(str(text).replace("Z", "+00:00"))
        return dt.replace(tzinfo=None) if dt.tzinfo is None else dt.astimezone().replace(tzinfo=None)
    except ValueError:
        m = re.match(r"(\d{4}-\d{2}-\d{2})", str(text))
        return datetime.fromisoformat(m.group(1)) if m else None


# ---------- registry ----------

def registry_path():
    return home() / "projects.json"


def load():
    data = read_json(registry_path(), None) or {"steerwright": 1, "wip_limit": DEFAULT_WIP, "projects": {}}
    data.setdefault("projects", {})
    data.setdefault("wip_limit", DEFAULT_WIP)
    data.setdefault("stall_weeks", STALL_WEEKS)
    return data


def save(data):
    write_json(registry_path(), data)


def get(data, name):
    key = slug(name)
    if key in data["projects"]:
        return key, data["projects"][key]
    for k, p in data["projects"].items():
        if p.get("name", "").lower() == name.lower():
            return k, p
    sys.exit(f"no project named {name!r}; sw.py status lists them")


def new_project(name, paths, kind="other", goal="", done_when="", target=None, sources=None):
    return {"name": name, "paths": [str(p) for p in paths], "kind": kind, "status": "active", "goal": goal,
            "done_when": done_when, "target": target, "revisit": None, "wake": "", "created": now_iso(),
            "updated": now_iso(), "sources": sources or {}, "history": [], "items": []}


def log_event(p, event, note=""):
    p.setdefault("history", []).append({"ts": now_iso(), "event": event, "note": note})
    p["updated"] = now_iso()


# ---------- sibling readers (read-only) ----------

def askwright_sets():
    """Every askwright set the inbox knows: (path, questions, answers)."""
    out = []
    for f in sorted((sib_home("askwright") / "sessions").glob("*.json")):
        rec = read_json(f, {}) or {}
        path = rec.get("path")
        if not path or not Path(path, "questions.json").exists():
            continue
        q = read_json(Path(path, "questions.json"), {}) or {}
        a = (read_json(Path(path, "answers.json"), {}) or {}).get("answers", {})
        out.append((path, q, a))
    return out


def askwright_projects():
    out = []
    for f in sorted((sib_home("askwright") / "projects").glob("*.json")):
        rec = read_json(f, None)
        if isinstance(rec, dict) and rec.get("name"):
            out.append(rec)
    return out


def set_project_name(q):
    pr = q.get("project")
    return (pr.get("name") if isinstance(pr, dict) else pr) or ""


def chain_ledgers():
    runs = (read_json(sib_home("chainwright") / "runs.json", {}) or {}).get("runs", {})
    out = []
    for ledger, info in runs.items():
        if is_temp(ledger) or not Path(ledger).exists():
            continue
        out.append((ledger, read_json(ledger, {}) or {}, info))
    return out


def grind_states():
    seen, out = set(), []
    for row in read_jsonl(sib_home("grindwright") / "runs.jsonl"):
        st = row.get("state")
        if st and not is_temp(st) and Path(st).exists() and norm(st) not in seen:
            seen.add(norm(st))
            out.append(st)
    return out


def project_root(path):
    p = Path(path).resolve()
    for cand in [p] + list(p.parents):
        if (cand / ".git").exists() or (cand / "ai-docs").is_dir() and cand.name != "ai-docs":
            return cand
    return p


def scan_handoffs(roots, depth=3):
    found = []
    for root in roots:
        root = Path(root)
        if not root.is_dir():
            continue
        base = len(root.parts)
        for dirpath, dirs, files in os.walk(root):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith(".")]
            if len(Path(dirpath).parts) - base >= depth:
                dirs[:] = []
            if Path(dirpath).name == "ai-docs" and "HANDOFF.md" in files:
                found.append(Path(dirpath).parent)
    return found


def git_identity(path):
    """Fold worktrees and side clones into one project: origin URL, else the shared git dir."""
    try:
        url = subprocess.run(["git", "-C", str(path), "config", "--get", "remote.origin.url"],
                             capture_output=True, text=True, timeout=10).stdout.strip()
        if url:
            return re.sub(r"(\.git)?/?$", "", url.lower())
        common = subprocess.run(["git", "-C", str(path), "rev-parse", "--path-format=absolute", "--git-common-dir"],
                                capture_output=True, text=True, timeout=10).stdout.strip()
        return norm(Path(common).parent) if common else None
    except (OSError, subprocess.SubprocessError):
        return None


def is_side_copy(path):
    """Worktree or scratch clone folders by Mark's naming: _wt/x, x-wt-y, wt-x, or a .git file."""
    n = Path(path).name
    return Path(path).parent.name == "_wt" or "-wt-" in n or n.startswith("wt-") or (Path(path) / ".git").is_file()


def guess_kind(text):
    t = text.lower()
    for kind, words in (("film", ("film", "video", "movie", "duel", "trailer")), ("music", ("music", "song", "album")),
                        ("game", ("game", "unity", "roblox", "arvum", "deck")), ("art", ("art", "sprite", "pixel")),
                        ("writing", ("book", "story", "novel", "writing")), ("software", ("wright", "plugin", "lib", "app"))):
        if any(w in t for w in words):
            return kind
    return "other"


# ---------- per-project gather ----------

def git_dates(path, weeks=26):
    try:
        out = subprocess.run(["git", "-C", str(path), "log", f"--since={weeks} weeks ago", "--format=%cI"],
                             capture_output=True, text=True, timeout=20)
        return [d for d in (parse_ts(x) for x in out.stdout.split()) if d]
    except (OSError, subprocess.SubprocessError):
        return []


def log_dates(path):
    out = []
    for f in (Path(path, "ai-docs", "log.md"), Path(path, "log.md")):
        try:
            text = f.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for m in re.finditer(r"^(?:##\s*|-\s*)(\d{4}-\d{2}-\d{2})", text, re.M):
            out.append(datetime.fromisoformat(m.group(1)))
    return out


_CACHE = {}
_LOCK = threading.RLock()


def _stamp(p):
    """Cheap fingerprint of a project's sources: mtimes of its paths' ai-docs, .git and the sibling homes."""
    parts = []
    for x in p.get("paths", []):
        for sub in ("", "ai-docs", "ai-docs/log.md", "ai-docs/HANDOFF.md", ".git/HEAD", ".git/index", ".git/refs/heads"):
            q = Path(x, sub)
            try:
                parts.append(q.stat().st_mtime_ns)
            except OSError:
                parts.append(0)
    for sib in ("askwright", "chainwright", "grindwright"):
        try:
            parts.append(sib_home(sib).stat().st_mtime_ns)
        except OSError:
            parts.append(0)
    return (json.dumps(p.get("paths")), json.dumps(p.get("items", []), default=str), tuple(parts))


def gather(p, fresh=False):
    """Cached gather_raw: in-process for CACHE_TTL seconds while the source fingerprint is unchanged."""
    key = json.dumps([p.get("name"), p.get("paths")])
    with _LOCK:
        st = _stamp(p)
        hit = _CACHE.get(key)
        if hit and not fresh and hit[0] == st and time.time() - hit[1] < CACHE_TTL:
            return hit[2]
        g = gather_raw(p)
        _CACHE[key] = (st, time.time(), g)
        return g


def warm_cache():
    """Fill and keep refreshing the gather cache so page loads stay fast."""
    while True:
        try:
            for p in load()["projects"].values():
                gather(p)
        except Exception:
            pass
        time.sleep(CACHE_TTL - 30)


def gather_raw(p):
    """Everything the pages and review need about one project, from disk. Never writes."""
    paths = [x for x in p.get("paths", []) if Path(x).exists()]
    names = {p.get("name", "").lower()} | {n.lower() for n in p.get("sources", {}).get("askwright", [])}
    g = {"asks_open": 0, "asks_answered": 0, "ask_sets": [], "chains": [], "grind": [], "prompts": [], "handoff": None,
         "activity": [], "items": []}
    # askwright
    for path, q, a in askwright_sets():
        if set_project_name(q).lower() not in names and not any(under(path, x) for x in paths):
            continue
        open_q = [x for x in q.get("questions", []) if x.get("status", "open") == "open"]
        unanswered = [x for x in open_q if (a.get(x.get("id"), {}) or {}).get("state") != "answered"]
        g["asks_open"] += len(unanswered)
        g["asks_answered"] += len(open_q) - len(unanswered)
        srv = read_json(Path(path, "server.json"), {}) or {}
        g["ask_sets"].append({"path": path, "title": q.get("title", Path(path).name), "open": len(unanswered),
                              "total": len(open_q), "url": srv.get("url"), "updated": q.get("updated")})
        for ans in a.values():
            d = parse_ts((ans or {}).get("updated"))
            if d:
                g["activity"].append(("ask", d))
    # chainwright
    for ledger, d, info in chain_ledgers():
        if not any(under(ledger, x) for x in paths) and (d.get("project") or "").lower() not in names:
            continue
        chains = d.get("chains", [])
        g["chains"].append({"ledger": ledger, "name": d.get("name") or Path(ledger).parent.name,
                            "running": sum(1 for c in chains if c.get("state") not in ("finished", "stopped", "done")),
                            "total": len(chains), "sessions": d.get("sessions_total", 0), "report": info.get("report")})
        g["activity"].append(("chain", datetime.fromtimestamp(Path(ledger).stat().st_mtime)))
    # grindwright
    for st in grind_states():
        if not any(under(st, x) for x in paths):
            continue
        ledger = read_jsonl(Path(st, "ledger.jsonl"))
        events = read_jsonl(Path(st, "events.jsonl"))
        by_state, by_lane = {}, {}
        for it in ledger:
            by_state[it.get("state", "?")] = by_state.get(it.get("state", "?"), 0) + 1
            lane = by_lane.setdefault(it.get("lane", "?"), {})
            lane[it.get("state", "?")] = lane.get(it.get("state", "?"), 0) + 1
        g["grind"].append({"state": st, "by_state": by_state, "by_lane": by_lane, "items": len(ledger)})
        claims = {}
        for e in events:
            d = parse_ts(e.get("ts"))
            if not d:
                continue
            if e.get("type") in ("add", "claim", "done", "drafted"):
                g["activity"].append(("grind", d))
            if e.get("type") == "claim" and e.get("id"):
                claims.setdefault(e["id"], d)
        for it in ledger:
            g["items"].append({"id": it.get("id"), "title": it.get("title", ""), "lane": it.get("lane", ""),
                               "created": parse_ts(it.get("created")), "started": claims.get(it.get("id")),
                               "done": parse_ts(it.get("finished") or (it.get("updated") if it.get("state") == "done" else None)),
                               "state": {"done": "done", "dropped": "dropped"}.get(it.get("state"),
                                         "doing" if it.get("id") in claims or it.get("state") in ("running", "drafted") else "todo")})
    # steerwright's own items
    for it in p.get("items", []):
        g["items"].append({"id": it["id"], "title": it["title"], "lane": "steer", "created": parse_ts(it.get("created")),
                           "started": None, "done": parse_ts(it.get("done")), "state": it.get("state", "todo")})
    # continue prompts, handoff, git, log
    for x in paths:
        for pat in ("ai-docs/plans/*continue-prompt*.md", "ai-docs/plans/*next-session-prompt*.md"):
            for f in Path(x).glob(pat):
                g["prompts"].append({"path": str(f), "mtime": datetime.fromtimestamp(f.stat().st_mtime)})
        h = Path(x, "ai-docs", "HANDOFF.md")
        if h.exists() and not g["handoff"]:
            g["handoff"] = {"path": str(h), "mtime": datetime.fromtimestamp(h.stat().st_mtime),
                            "head": h.read_text(encoding="utf-8", errors="replace")[:1500]}
            g["activity"].append(("handoff", g["handoff"]["mtime"]))
        g["activity"] += [("git", d) for d in git_dates(x)]
        g["activity"] += [("log", d) for d in log_dates(x)]
    g["prompts"].sort(key=lambda r: r["mtime"], reverse=True)
    g["last"] = max((d for _, d in g["activity"]), default=None)
    g["idle_days"] = max(0, (datetime.combine(today(), datetime.min.time()) - g["last"]).days) if g["last"] else None
    return g


def health(p, g):
    if p.get("status") == "tabled":
        rv = p.get("revisit")
        return ("wake", "revisit date reached") if rv and date.fromisoformat(rv) <= today() else ("tabled", "parked")
    if p.get("status") in ("done", "abandoned"):
        return (p["status"], p["status"])
    idle = g["idle_days"]
    if idle is None:
        return ("red", "no activity found")
    if idle <= 7:
        return ("green", f"active {idle} d ago")
    if idle <= 21:
        return ("amber", f"quiet {idle} d")
    return ("red", f"stalled {idle} d")


# ---------- flow metrics ----------

def week_start(d):
    d = d.date() if isinstance(d, datetime) else d
    return d - timedelta(days=d.weekday())


def flow(items, weeks=12):
    """Weekly burn-up, cumulative flow, throughput, cycle times and aging from item dates."""
    end = week_start(today())
    starts = [end - timedelta(weeks=i) for i in range(weeks - 1, -1, -1)]
    live = [i for i in items if i["state"] != "dropped" and i["created"]]
    rows = []
    for s in starts:
        t = datetime.combine(s + timedelta(days=7), datetime.min.time())
        scope = sum(1 for i in live if i["created"] < t)
        done = sum(1 for i in live if i["done"] and i["done"] < t)
        doing = sum(1 for i in live if i["created"] < t and not (i["done"] and i["done"] < t)
                    and i["started"] and i["started"] < t)
        thru = sum(1 for i in live if i["done"] and week_start(i["done"]) == s)
        rows.append({"week": s.isoformat(), "scope": scope, "done": done, "doing": doing,
                     "todo": scope - done - doing, "throughput": thru})
    cycles = sorted(((i["done"] - (i["started"] or i["created"])).total_seconds() / 86400)
                    for i in live if i["done"])
    def pct(xs, q):
        return round(xs[min(len(xs) - 1, int(q * len(xs)))], 1) if xs else None
    now = datetime.combine(today(), datetime.min.time()) + timedelta(days=1)
    aging = sorted(({"id": i["id"], "title": i["title"], "age": round((now - (i["started"] or i["created"])).total_seconds() / 86400, 1),
                     "state": i["state"]} for i in live if not i["done"]), key=lambda r: -r["age"])
    remaining = sum(1 for i in live if not i["done"])
    return {"weeks": rows, "cycle": {"n": len(cycles), "p50": pct(cycles, .5), "p85": pct(cycles, .85), "p95": pct(cycles, .95)},
            "aging": aging, "remaining": remaining, "done": sum(1 for i in live if i["done"])}


def monte_carlo(throughput, remaining, trials=10000, seed=None):
    """Weeks until `remaining` items are done, resampling weekly throughput. Returns percentiles and finish dates."""
    sample = [t for t in throughput]
    if remaining <= 0:
        return {"remaining": 0, "note": "nothing left"}
    if not sample or sum(sample) == 0:
        return {"remaining": remaining, "note": "no throughput in the sample window; no forecast"}
    rng = random.Random(seed)
    results = []
    for _ in range(trials):
        left, w = remaining, 0
        while left > 0 and w < 520:
            left -= rng.choice(sample)
            w += 1
        results.append(w)
    results.sort()
    out = {"remaining": remaining, "trials": trials, "sample_weeks": len(sample)}
    for q in (50, 85, 95):
        wk = results[min(trials - 1, int(q / 100 * trials))]
        out[f"p{q}"] = {"weeks": wk, "date": (today() + timedelta(weeks=wk)).isoformat()}
    return out


# ---------- review ----------

def review_findings(p, g, f, wip_over, stall_weeks=STALL_WEEKS):
    flags, guess = [], "keep"
    idle = g["idle_days"]
    if idle is None or idle >= stall_weeks * 7:
        flags.append(f"No progress for {idle if idle is not None else 'unknown'} days (kill criterion: {stall_weeks} weeks).")
        guess = "table"
    if p.get("target") and f["remaining"]:
        mc = monte_carlo([w["throughput"] for w in f["weeks"]], f["remaining"], seed=1)
        if "p85" in mc and mc["p85"]["date"] > p["target"]:
            flags.append(f"85 % forecast {mc['p85']['date']} is past the target {p['target']}.")
    if wip_over:
        flags.append("Active projects exceed the WIP limit; this one is among the quietest.")
        if guess == "keep":
            guess = "table"
    if not p.get("done_when"):
        flags.append("No definition of done recorded.")
    if g["asks_open"]:
        flags.append(f"{g['asks_open']} askwright questions are waiting on you.")
    return flags, guess


def next_actions(g, n=3):
    acts = [i["title"] for i in sorted((i for i in g["items"] if i["state"] == "doing"), key=lambda i: i["created"] or datetime.min)]
    acts += [i["title"] for i in g["items"] if i["state"] == "todo"]
    if g["asks_open"]:
        acts.insert(0, f"Answer {g['asks_open']} open askwright question(s)")
    if not acts and g["prompts"]:
        acts.append(f"Run the continue prompt {g['prompts'][0]['path']}")
    return acts[:n]


def ask_script():
    cfg = read_json(home() / "config.json", {}) or {}
    cands = [cfg.get("ask_py")]
    inst = read_json(Path.home() / ".claude" / "plugins" / "installed_plugins.json", {}) or {}
    for key, recs in (inst.get("plugins") or {}).items():
        if key.startswith("askwright@"):
            for r in recs:
                cands.append(str(Path(r.get("installPath", ""), "skills", "askwright", "scripts", "ask.py")))
    cands.append(str(Path(__file__).resolve().parents[4] / "askwright" / "skills" / "askwright" / "scripts" / "ask.py"))
    return next((c for c in cands if c and Path(c).exists()), None)


def build_review_set(key, p, g, f, flags, guess, acts):
    stamp = today().isoformat()
    sid = f"steer-{key}-{stamp}"
    facts = [f"Last activity: {g['last']:%Y-%m-%d} ({g['idle_days']} d ago)" if g["last"] else "No activity found",
             f"Items: {f['done']} done, {f['remaining']} remaining",
             f"Throughput last 4 weeks: {sum(w['throughput'] for w in f['weeks'][-4:])}"]
    why = "Keeps the portfolio honest: a project is either moving, parked on purpose with a wake condition, or closed."
    q = {"askwright": 1, "id": sid, "title": f"Weekly review: {p['name']}", "project": {"name": p["name"], "path": (p.get("paths") or [""])[0]},
         "asked_by": f"steerwright review, {stamp}", "context": p.get("goal") or "",
         "questions": [
             {"id": "decision", "kind": "choice", "title": "Keep, table or abandon",
              "question": f"What should happen to {p['name']} now?", "why": why,
              "one_pager": [{"type": "text", "text": "Findings:\n- " + "\n- ".join(flags or ["No kill criterion met."])},
                            {"type": "text", "text": "Facts:\n- " + "\n- ".join(facts)}],
              "options": [{"id": "keep", "label": "Keep going", "consequence": "Stays active; next actions below."},
                          {"id": "table", "label": "Table it", "consequence": "Parked with a revisit date and wake condition."},
                          {"id": "abandon", "label": "Abandon it", "consequence": "Closed with a short post-mortem."},
                          {"id": "done", "label": "It is done", "consequence": "Closed as done."}],
              "guess": {"option": guess, "why": "; ".join(flags) or "moving, no criterion met", "confidence": "low"}},
             {"id": "next", "kind": "text", "title": "Next three actions",
              "question": "Are these the right next three actions, and if not, what are?", "why": "They become the project's next actions.",
              "hint": " | ".join(acts) or "none found", "guess": {"text": "; ".join(acts) or "none", "why": "from in-progress and ready work", "confidence": "low"},
              "show_if": {"question": "decision", "option": ["keep"]}},
             {"id": "wake", "kind": "text", "title": "Wake condition and date",
              "question": "When should it be revisited, and what would wake it sooner?", "why": "Written to the registry; the main page surfaces it on that date.",
              "guess": {"text": f"{(today() + timedelta(weeks=6)).isoformat()}; when a slot frees", "why": "six weeks is the default parking time", "confidence": "low"},
              "show_if": {"question": "decision", "option": ["table"]}},
             {"id": "postmortem", "kind": "text", "title": "Post-mortem",
              "question": "Why is it ending, and what is worth keeping from it?", "why": "Recorded with the project; reusable parts get harvested.",
              "guess": {"text": "; ".join(flags) or "no longer wanted", "why": "the review findings", "confidence": "low"}, "show_if": {"question": "decision", "option": ["abandon"]}}]}
    d = home() / "reviews" / sid
    write_json(d / "questions.json", q)
    return d


# ---------- SVG charts (no CDN) ----------

PAL = ["#3b6fd8", "#c9821f", "#2f9e5a", "#8a6fd1", "#d04848"]


def svg_lines(series, labels, w=560, h=200, title="", stacked_area=False):
    """series: [(name, values)]; labels: x labels. Line chart or stacked area (cumulative flow)."""
    n = len(labels)
    if n == 0:
        return ""
    pad_l, pad_b, pad_t = 34, 22, 18
    if stacked_area:
        tops, acc = [], [0] * n
        for name, vals in series:
            acc = [a + v for a, v in zip(acc, vals)]
            tops.append((name, acc[:]))
        ymax = max(max(acc), 1)
    else:
        ymax = max([max(v) for _, v in series] + [1])
    X = lambda i: pad_l + (w - pad_l - 8) * (i / max(n - 1, 1))
    Y = lambda v: pad_t + (h - pad_t - pad_b) * (1 - v / ymax)
    parts = [f'<svg viewBox="0 0 {w} {h}" class="chart" role="img" aria-label="{html.escape(title)}">',
             f'<text x="{pad_l}" y="12" class="ct">{html.escape(title)}</text>']
    for t in (0, ymax // 2, ymax):
        parts.append(f'<line x1="{pad_l}" x2="{w-8}" y1="{Y(t):.1f}" y2="{Y(t):.1f}" class="grid"/><text x="{pad_l-4}" y="{Y(t)+4:.1f}" class="ax" text-anchor="end">{t}</text>')
    for i in (0, n // 2, n - 1):
        parts.append(f'<text x="{X(i):.1f}" y="{h-6}" class="ax" text-anchor="middle">{labels[i][5:]}</text>')
    if stacked_area:
        prev = [0] * n
        for k, (name, top) in enumerate(tops):
            pts = [f"{X(i):.1f},{Y(top[i]):.1f}" for i in range(n)] + [f"{X(i):.1f},{Y(prev[i]):.1f}" for i in range(n - 1, -1, -1)]
            parts.append(f'<polygon points="{" ".join(pts)}" fill="{PAL[k % 5]}" opacity=".75"><title>{html.escape(name)}</title></polygon>')
            prev = top
    else:
        for k, (name, vals) in enumerate(series):
            pts = " ".join(f"{X(i):.1f},{Y(v):.1f}" for i, v in enumerate(vals))
            parts.append(f'<polyline points="{pts}" fill="none" stroke="{PAL[k % 5]}" stroke-width="2"><title>{html.escape(name)}</title></polyline>')
    leg = " ".join(f'<tspan fill="{PAL[k % 5]}">■</tspan> {html.escape(nm)}' for k, (nm, _) in enumerate(series))
    parts.append(f'<text x="{w-8}" y="12" class="ax" text-anchor="end">{leg}</text></svg>')
    return "".join(parts)


def svg_bars(values, labels, w=560, h=160, title=""):
    n = len(values)
    if n == 0:
        return ""
    ymax = max(values + [1])
    bw = (w - 42) / n
    parts = [f'<svg viewBox="0 0 {w} {h}" class="chart" role="img" aria-label="{html.escape(title)}"><text x="34" y="12" class="ct">{html.escape(title)}</text>']
    for i, v in enumerate(values):
        bh = (h - 40) * v / ymax
        x = 34 + i * bw
        parts.append(f'<rect x="{x+2:.1f}" y="{h-22-bh:.1f}" width="{bw-4:.1f}" height="{bh:.1f}" fill="{PAL[0]}"><title>{labels[i]}: {v}</title></rect>')
        if v:
            parts.append(f'<text x="{x+bw/2:.1f}" y="{h-25-bh:.1f}" class="ax" text-anchor="middle">{v}</text>')
    for i in (0, n // 2, n - 1):
        parts.append(f'<text x="{34+i*bw+bw/2:.1f}" y="{h-6}" class="ax" text-anchor="middle">{labels[i][5:]}</text>')
    return "".join(parts) + "</svg>"


# ---------- pages ----------

CSS = """
:root{--bg:#f7f7f5;--fg:#1d1d1f;--mut:#6b6b70;--card:#fff;--line:#e2e2e0;--green:#2f9e5a;--amber:#c9821f;--red:#d04848;--grey:#8a8a90;--blue:#3b6fd8}
@media (prefers-color-scheme:dark){:root{--bg:#161618;--fg:#ececee;--mut:#9a9aa2;--card:#202024;--line:#33333a}}
body{background:var(--bg);color:var(--fg);font:14px/1.45 system-ui,Segoe UI,sans-serif;margin:0;padding:16px;max-width:1100px;margin:auto}
a{color:var(--blue)}h1{font-size:20px;margin:4px 0 12px}h2{font-size:15px;margin:22px 0 8px}
.top{display:flex;gap:14px;flex-wrap:wrap;align-items:center;color:var(--mut)}.top a{font-weight:600}
table{border-collapse:collapse;width:100%;background:var(--card);border:1px solid var(--line);border-radius:8px;overflow:hidden}
td,th{padding:7px 9px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}th{font-size:12px;color:var(--mut);font-weight:600}
.dot{display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:6px}
.green{background:var(--green)}.amber{background:var(--amber)}.red{background:var(--red)}.tabled,.done,.abandoned{background:var(--grey)}.wake{background:var(--blue)}
.tiles{display:flex;gap:10px;flex-wrap:wrap}.tile{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:10px 14px;min-width:120px}
.tile b{display:block;font-size:22px}.tile span{color:var(--mut);font-size:12px}
.strip{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:8px 12px}
.warn{background:#fff3e0;color:#7a4a00;border-radius:8px;padding:8px 12px;margin:8px 0}@media (prefers-color-scheme:dark){.warn{background:#3a2a10;color:#f0c890}}
.chart{width:100%;max-width:560px;background:var(--card);border:1px solid var(--line);border-radius:8px;margin:4px 8px 8px 0}
.chart .grid{stroke:var(--line)}.chart .ax{fill:var(--mut);font-size:10px}.chart .ct{fill:var(--fg);font-size:11px;font-weight:600}
.charts{display:flex;flex-wrap:wrap}pre{white-space:pre-wrap;background:var(--card);border:1px solid var(--line);padding:10px;border-radius:8px;font-size:12px}
.mut{color:var(--mut)}@media (max-width:640px){td:nth-child(n+5),th:nth-child(n+5){display:none}}
"""


def esc(x):
    return html.escape(str(x if x is not None else ""))


def page(title, body):
    return (f"<!doctype html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>"
            f"<title>{esc(title)}</title><style>{CSS}</style></head><body>{body}</body></html>")


def sibling_links():
    out = []
    srv = read_json(sib_home("askwright") / "dashboard" / "server.json", {}) or {}
    if srv.get("url") and port_open(srv.get("port")):
        out.append(f'<a href="{esc(srv["url"])}">askwright</a>')
    else:
        out.append('<span class="mut">askwright (not running: sw.py up)</span>')
    for name in ("chainwright", "grindwright"):
        if (sib_home(name) / "index.html").exists():
            out.append(f'<a href="/sib/{name}">{name}</a>')
    return " · ".join(out)


def main_page(data):
    rows, strip, warns = [], [], []
    projects = list(data["projects"].items())
    gs = {k: gather(p) for k, p in projects}
    active = [k for k, p in projects if p.get("status") == "active"]
    if len(active) > data["wip_limit"]:
        warns.append(f"{len(active)} active projects, WIP limit {data['wip_limit']}: table or finish some (sw.py review).")
    order = {"wake": 0, "red": 1, "amber": 2, "green": 3, "tabled": 4, "done": 5, "abandoned": 6}
    hs = {k: health(p, gs[k]) for k, p in projects}
    for k, p in sorted(projects, key=lambda kp: (order.get(hs[kp[0]][0], 9), kp[1]["name"].lower())):
        g, (h, why) = gs[k], hs[k]
        if h == "wake":
            warns.append(f"{p['name']}: revisit date {p.get('revisit')} reached. Wake condition: {p.get('wake') or '-'}")
        running = sum(c["running"] for c in g["chains"])
        gl = {}
        for gr in g["grind"]:
            for s, n in gr["by_state"].items():
                gl[s] = gl.get(s, 0) + n
        acts = next_actions(g, 1)
        if p.get("status") == "active" and (running or g["asks_open"] or (g["idle_days"] is not None and g["idle_days"] <= 2)):
            strip.append(f'<a href="/p/{k}">{esc(p["name"])}</a>' + (f" ({running} chain running)" if running else "")
                         + (f" ({g['asks_open']} asks)" if g["asks_open"] else ""))
        rows.append(f"<tr><td><span class='dot {h}'></span><a href='/p/{k}'>{esc(p['name'])}</a><div class='mut'>{esc(p.get('kind'))}</div></td>"
                    f"<td>{esc(p.get('status'))}<div class='mut'>{esc(why)}</div></td>"
                    f"<td>{g['last']:%Y-%m-%d}</td>" if g["last"] else
                    f"<tr><td><span class='dot {h}'></span><a href='/p/{k}'>{esc(p['name'])}</a><div class='mut'>{esc(p.get('kind'))}</div></td>"
                    f"<td>{esc(p.get('status'))}<div class='mut'>{esc(why)}</div></td><td>-</td>")
        rows[-1] += (f"<td>{g['asks_open'] or ''}</td><td>{running or ''}</td>"
                     f"<td>{esc(', '.join(f'{s} {n}' for s, n in sorted(gl.items())))}</td><td>{esc(acts[0] if acts else '')}</td></tr>")
    body = (f"<div class='top'><h1>steerwright</h1><span>{today()}</span><span>{sibling_links()}</span></div>"
            + "".join(f"<div class='warn'>{esc(w)}</div>" for w in warns)
            + f"<div class='tiles'>" + "".join(f"<div class='tile'><b>{n}</b><span>{s}</span></div>" for s, n in
                ((s, sum(1 for _, p in projects if p.get('status') == s)) for s in STATUSES))
            + f"<div class='tile'><b>{data['wip_limit']}</b><span>WIP limit</span></div></div>"
            + f"<h2>Current work</h2><div class='strip'>{' · '.join(strip) or '<span class=mut>nothing moving in the last 2 days</span>'}</div>"
            + "<h2>Projects</h2><table><tr><th>Project</th><th>Status</th><th>Last activity</th><th>Open asks</th><th>Chains running</th><th>Grind items</th><th>Next action</th></tr>"
            + "".join(rows) + "</table>"
            + "<p class='mut'>Read-only view. Change state with sw.py (review, table, abandon, done).</p>")
    return page("steerwright", body)


def project_page(key, p):
    g = gather(p)
    f = flow(g["items"])
    h, why = health(p, g)
    labels = [w["week"] for w in f["weeks"]]
    mc = monte_carlo([w["throughput"] for w in f["weeks"]], f["remaining"], seed=1)
    fc = (f"{mc['p50']['date']} (50 %) · {mc['p85']['date']} (85 %) · {mc['p95']['date']} (95 %), {mc['remaining']} items left"
          if "p50" in mc else mc.get("note", ""))
    charts = ""
    if g["items"]:
        charts = ("<div class='charts'>"
                  + svg_lines([("scope", [w["scope"] for w in f["weeks"]]), ("done", [w["done"] for w in f["weeks"]])], labels, title="Burn-up (items, weekly)")
                  + svg_lines([("done", [w["done"] for w in f["weeks"]]), ("doing", [w["doing"] for w in f["weeks"]]), ("todo", [w["todo"] for w in f["weeks"]])], labels, title="Cumulative flow", stacked_area=True)
                  + svg_bars([w["throughput"] for w in f["weeks"]], labels, title="Throughput per week")
                  + "</div>")
    act = {}
    for _, d in g["activity"]:
        ws = week_start(d)
        act[ws] = act.get(ws, 0) + 1
    awk = [(week_start(today()) - timedelta(weeks=i)) for i in range(11, -1, -1)]
    charts += "<div class='charts'>" + svg_bars([act.get(w, 0) for w in awk], [w.isoformat() for w in awk], title="Activity per week (commits, log entries, events, answers)") + "</div>"
    asks = "".join(f"<tr><td>{esc(s['title'])}</td><td>{s['open']} / {s['total']}</td><td>{f'<a href={esc(s[chr(117)+chr(114)+chr(108)])}>open</a>' if s['url'] else esc(s['path'])}</td></tr>" for s in g["ask_sets"])
    chains = "".join(f"<tr><td>{esc(c['name'])}</td><td>{c['running']} running / {c['total']}</td><td>{c['sessions']}</td><td class='mut'>{esc(c['ledger'])}</td></tr>" for c in g["chains"])
    lanes = "".join(f"<tr><td>{esc(l)}</td><td>{esc(', '.join(f'{s} {n}' for s, n in sorted(c.items())))}</td></tr>" for gr in g["grind"] for l, c in sorted(gr["by_lane"].items()))
    aging = "".join(f"<tr><td>{esc(a['title'][:90])}</td><td>{a['state']}</td><td>{a['age']} d</td></tr>" for a in f["aging"][:10])
    hist = "".join(f"<tr><td>{esc(e['ts'][:10])}</td><td>{esc(e['event'])}</td><td>{esc(e.get('note'))}</td></tr>" for e in reversed(p.get("history", [])))
    tbl = lambda head, rows: f"<table><tr>{''.join(f'<th>{x}</th>' for x in head)}</tr>{rows}</table>" if rows else "<p class='mut'>none</p>"
    cyc = f["cycle"]
    body = (f"<div class='top'><a href='/'>← all projects</a><span>{sibling_links()}</span></div>"
            f"<h1><span class='dot {h}'></span>{esc(p['name'])}</h1><p>{esc(p.get('status'))} · {esc(why)} · {esc(p.get('kind'))}"
            + (f" · target {esc(p['target'])}" if p.get("target") else "") + (f" · revisit {esc(p['revisit'])} when {esc(p.get('wake'))}" if p.get("revisit") else "") + "</p>"
            f"<p><b>Goal:</b> {esc(p.get('goal') or '-')}<br><b>Done when:</b> {esc(p.get('done_when') or '-')}<br><b>Paths:</b> {esc(', '.join(p.get('paths', [])))}</p>"
            f"<div class='tiles'><div class='tile'><b>{f['done']}</b><span>items done</span></div><div class='tile'><b>{f['remaining']}</b><span>remaining</span></div>"
            f"<div class='tile'><b>{cyc['p50'] if cyc['p50'] is not None else '-'}</b><span>cycle time p50 (d)</span></div><div class='tile'><b>{cyc['p85'] if cyc['p85'] is not None else '-'}</b><span>cycle time p85 (d)</span></div>"
            f"<div class='tile'><b>{g['asks_open']}</b><span>open asks</span></div></div>"
            f"<h2>Forecast</h2><p>{esc(fc)}</p>"
            f"<h2>Next actions</h2><ol>{''.join(f'<li>{esc(a)}</li>' for a in next_actions(g)) or '<li class=mut>none found</li>'}</ol>"
            f"<h2>Charts</h2>{charts}"
            f"<h2>Aging work (oldest open)</h2>{tbl(['Item', 'State', 'Age'], aging)}"
            f"<h2>askwright decisions</h2>{tbl(['Set', 'Open / total', 'Page'], asks)}"
            f"<h2>chainwright runs</h2>{tbl(['Run', 'Chains', 'Sessions', 'Ledger'], chains)}"
            f"<h2>grindwright ledger by lane</h2>{tbl(['Lane', 'Items'], lanes)}"
            + (f"<h2>Current continue prompt</h2><p>Execute {esc(g['prompts'][0]['path'])}</p>" if g["prompts"] else "")
            + (f"<h2>HANDOFF ({g['handoff']['mtime']:%Y-%m-%d})</h2><pre>{esc(g['handoff']['head'])}</pre>" if g["handoff"] else "")
            + f"<h2>Decision log</h2>{tbl(['Date', 'Event', 'Note'], hist)}")
    return page(f"{p['name']}: steerwright", body)


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def send(self, code, body, ctype="text/html; charset=utf-8"):
        b = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def do_GET(self):
        path = urllib.parse.urlparse(self.path).path
        try:
            data = load()
            if path == "/":
                return self.send(200, main_page(data))
            if path == "/ping":
                return self.send(200, json.dumps({"steerwright": VERSION, "pid": os.getpid()}), "application/json")
            if path.startswith("/p/"):
                key = path[3:]
                if key in data["projects"]:
                    return self.send(200, project_page(key, data["projects"][key]))
            if path in ("/sib/chainwright", "/sib/grindwright"):
                f = sib_home(path[5:]) / "index.html"
                if f.exists():
                    return self.send(200, f.read_text(encoding="utf-8", errors="replace"))
            self.send(404, page("not found", "<p>not found. <a href='/'>home</a></p>"))
        except Exception as e:  # keep the server alive; show the error
            self.send(500, page("error", f"<pre>{esc(repr(e))}</pre>"))


def port_open(port):
    if not port:
        return False
    try:
        urllib.request.urlopen(f"http://127.0.0.1:{port}/", timeout=1.5)
        return True
    except urllib.error.HTTPError:
        return True
    except Exception:
        return False


def pid_alive(pid):
    if not pid:
        return False
    if os.name == "nt":
        out = subprocess.run(["tasklist", "/FI", f"PID eq {pid}", "/NH"], capture_output=True, text=True)
        return str(pid) in out.stdout
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False


def kill_pid(pid):
    """By PID only, never by image name."""
    if os.name == "nt":
        subprocess.run(["taskkill", "/PID", str(pid), "/F"], capture_output=True)
    else:
        try:
            os.kill(pid, 15)
        except OSError:
            pass


def detach(args):
    flags = 0x00000008 | 0x00000200 if os.name == "nt" else 0  # DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP
    kw = {"creationflags": flags} if os.name == "nt" else {"start_new_session": True}
    return subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL, **kw)


def ping_steer(port):
    try:
        return json.loads(urllib.request.urlopen(f"http://127.0.0.1:{port}/ping", timeout=1.5).read())
    except Exception:
        return None


def cmd_serve(a):
    srv = read_json(home() / "server.json", {}) or {}
    port = a.port or srv.get("port") or DEFAULT_PORT
    info = ping_steer(port)
    url = f"http://127.0.0.1:{port}/"
    if info:
        out = {"ok": True, "url": url, "pid": info["pid"], "reused": True}
    elif a.detach:
        proc = detach([sys.executable, str(Path(__file__).resolve()), "serve", "--port", str(port)])
        for _ in range(40):
            time.sleep(0.25)
            info = ping_steer(port)
            if info:
                break
        if not info:
            sys.exit(json.dumps({"ok": False, "error": f"server did not answer on {port}"}))
        write_json(home() / "server.json", {"url": url, "port": port, "pid": info["pid"], "started": now_iso()})
        out = {"ok": True, "url": url, "pid": info["pid"], "started": proc.pid}
    else:
        httpd = ThreadingHTTPServer(("127.0.0.1", port), Handler)
        write_json(home() / "server.json", {"url": url, "port": port, "pid": os.getpid(), "started": now_iso()})
        print(json.dumps({"ok": True, "url": url, "pid": os.getpid()}), flush=True)
        threading.Thread(target=warm_cache, daemon=True).start()
        if a.open:
            webbrowser.open(url)
        httpd.serve_forever()
        return
    print(json.dumps(out))
    if a.open:
        webbrowser.open(url)
    return out


def sibling_script(plugin, rel):
    inst = read_json(Path.home() / ".claude" / "plugins" / "installed_plugins.json", {}) or {}
    for key, recs in (inst.get("plugins") or {}).items():
        if key.startswith(plugin + "@"):
            for r in recs:
                c = Path(r.get("installPath", ""), rel)
                if c.exists():
                    return c
    c = Path(__file__).resolve().parents[4] / plugin / rel
    return c if c.exists() else None


def cmd_up(a):
    started, report = [], {}
    out = cmd_serve(argparse.Namespace(port=None, detach=True, open=False))
    if out and not out.get("reused"):
        started.append({"name": "steerwright", "pid": out["pid"]})
    report["steerwright"] = out["url"]
    srv = read_json(sib_home("askwright") / "dashboard" / "server.json", {}) or {}
    if srv.get("port") and port_open(srv["port"]):
        report["askwright"] = srv.get("url") + " (already running)"
    else:
        ask = ask_script()
        if ask:
            r = subprocess.run([sys.executable, ask, "dashboard", "--detach"], capture_output=True, text=True, timeout=60)
            srv = read_json(sib_home("askwright") / "dashboard" / "server.json", {}) or {}
            if srv.get("pid"):
                started.append({"name": "askwright", "pid": srv["pid"]})
            report["askwright"] = srv.get("url") or r.stdout.strip()[-200:]
        else:
            report["askwright"] = "ask.py not found"
    for plugin, rel, args in (("chainwright", "skills/chainwright/scripts/chain_index.py", ["build"]),
                              ("grindwright", "skills/grindwright/scripts/grind_index.py", ["build"])):
        s = sibling_script(plugin, rel)
        if s:
            r = subprocess.run([sys.executable, str(s)] + args, capture_output=True, text=True, timeout=300)
            report[plugin] = "index built" if r.returncode == 0 else ("build failed: " + r.stderr.strip()[-200:])
        else:
            report[plugin] = "not installed"
    prev = read_json(home() / "up.json", {}) or {}
    keep = [s for s in prev.get("started", []) if pid_alive(s["pid"])]
    write_json(home() / "up.json", {"started": keep + started, "ts": now_iso()})
    print(json.dumps(report, indent=1))
    if not a.no_open:
        webbrowser.open(report["steerwright"])


def cmd_down(a):
    rec = read_json(home() / "up.json", {}) or {}
    stopped = []
    for s in rec.get("started", []):
        if pid_alive(s["pid"]):
            kill_pid(s["pid"])
            stopped.append(s)
    write_json(home() / "up.json", {"started": [], "ts": now_iso()})
    print(json.dumps({"stopped": stopped}))


def write_shortcut():
    """A .cmd on the desktop that runs sw.py up."""
    desk = Path.home() / "Desktop"
    for cand in (Path(os.environ.get("USERPROFILE", "")) / "Desktop", Path(os.environ.get("OneDrive", "")) / "Desktop"):
        if cand.is_dir():
            desk = cand
            break
    f = desk / "steerwright.cmd"
    f.write_text(f'@echo off\r\n"{sys.executable}" "{Path(__file__).resolve()}" up\r\n', encoding="utf-8")
    return f


# ---------- grouping ----------

GROUP_RULES = (
    # (group name, kind, test on the root path) - first match wins; no match keeps the project on its own
    ("Plugins", "software", lambda r: Path(r, ".claude-plugin").is_dir() or any(Path(r, "skills").glob("*/SKILL.md"))
     or Path(r).name.lower() == "plugin-backlog"),
    ("Arvum Electrum", "game", lambda r: "arvum" in str(r).lower() or "avrum" in str(r).lower()),
    ("Films", "film", lambda r: norm(r).startswith(norm("D:/ComfyUI/output/video"))),
)


def group_of(root):
    for name, kind, test in GROUP_RULES:
        try:
            if test(root):
                return name, kind
        except OSError:
            pass
    return None, None


def group_proposals(proposals):
    """Fold proposals that share a group into one project with several paths."""
    out, groups = [], {}
    for pr in proposals:
        gname, gkind = group_of(pr["path"])
        if not gname:
            out.append(pr)
            continue
        g = groups.get(gname)
        if not g:
            g = groups[gname] = {"name": gname, "path": pr["path"], "paths": [], "kind": gkind, "sources": {},
                                 "copies": [], "last": pr["last"], "members": []}
            out.append(g)
        g["paths"].append(pr["path"])
        g["members"].append(pr["name"])
        g["copies"] += pr.get("copies", [])
        g["last"] = max(g["last"], pr["last"])
        for src, refs in pr["sources"].items():
            g["sources"].setdefault(src, []).extend(x for x in refs if x not in g["sources"][src])
    return out


# ---------- commands ----------

def cmd_discover(a):
    data = load()
    known = {norm(x) for p in data["projects"].values() for x in p.get("paths", [])}
    found = {}

    def add(root, name, src, ref):
        r = norm(root)
        e = found.setdefault(r, {"root": str(root), "names": set(), "sources": {}})
        if name:
            e["names"].add(name)
        e["sources"].setdefault(src, [])
        if ref not in e["sources"][src]:
            e["sources"][src].append(ref)

    for rec in askwright_projects():
        for d in rec.get("dirs", []) or []:
            if Path(d).exists() and not is_temp(d):
                add(Path(d), rec["name"], "askwright", rec["name"])
    for ledger, d, _ in chain_ledgers():
        add(project_root(Path(ledger).parent), d.get("project"), "chainwright", ledger)
    for st in grind_states():
        prof = read_json(Path(st, "profile.json"), {}) or {}
        add(project_root(st), prof.get("project"), "grindwright", st)
    roots = a.root or [str(Path(__file__).resolve().parents[4])]
    for r in scan_handoffs(roots):
        add(r, None, "handoff", str(Path(r, "ai-docs", "HANDOFF.md")))
    # fold side copies and worktrees into the main checkout of the same repo
    ids = {r: git_identity(e["root"]) for r, e in found.items()}
    mains = {}
    for r, e in sorted(found.items(), key=lambda kv: (is_side_copy(kv[1]["root"]), len(kv[0]))):
        gid = ids[r]
        if gid and gid in mains:
            m = found[mains[gid]]
            m.setdefault("copies", []).append(e["root"])
            m["names"] |= e["names"]
            for src, refs in e["sources"].items():
                m["sources"].setdefault(src, []).extend(x for x in refs if x not in m["sources"][src])
            e["folded"] = True
        elif gid:
            mains[gid] = r
    proposals = []
    cutoff = datetime.combine(today(), datetime.min.time()) - timedelta(days=a.since)
    for r, e in sorted(found.items()):
        if r in known or e.get("folded"):
            continue
        if not e["names"] and is_side_copy(e["root"]):
            continue
        probe = gather(new_project("probe", [e["root"]], sources={"askwright": sorted(e["names"])}))
        if not probe["last"] or probe["last"] < cutoff:
            continue
        name = sorted(e["names"], key=len)[0] if e["names"] else Path(e["root"]).name
        proposals.append({"name": name, "path": e["root"], "kind": guess_kind(name + " " + e["root"]), "sources": e["sources"],
                          "copies": e.get("copies", []), "last": probe["last"].isoformat(timespec="minutes")})
    if not a.no_group:
        proposals = group_proposals(proposals)
    if a.apply:
        for pr in proposals:
            key = slug(pr["name"])
            if key in data["projects"] and pr.get("members"):
                ex = data["projects"][key]
                ex["paths"] += [x for x in pr["paths"] if x not in ex["paths"]]
                log_event(ex, "grew", ", ".join(pr["members"]))
                continue
            while key in data["projects"]:
                key += "-2"
            p = new_project(pr["name"], pr.get("paths") or [pr["path"]], pr["kind"], sources=pr["sources"])
            log_event(p, "discovered", ", ".join(pr["sources"]))
            data["projects"][key] = p
        save(data)
    print(json.dumps({"proposals": proposals, "applied": bool(a.apply)}, indent=1, default=str))


def cmd_add(a):
    data = load()
    key = slug(a.name)
    if key in data["projects"]:
        sys.exit(f"{a.name} already registered")
    p = new_project(a.name, a.path, a.kind, a.goal or "", a.done_when or "", a.target)
    log_event(p, "added")
    data["projects"][key] = p
    save(data)
    print(json.dumps({"added": key}))


def status_row(k, p):
    g = gather(p)
    f = flow(g["items"])
    h, why = health(p, g)
    return {"key": k, "name": p["name"], "status": p["status"], "health": h, "why": why,
            "last": g["last"].isoformat(timespec="minutes") if g["last"] else None, "asks_open": g["asks_open"],
            "chains_running": sum(c["running"] for c in g["chains"]), "items_done": f["done"], "items_left": f["remaining"],
            "next": next_actions(g)}


def cmd_status(a):
    data = load()
    rows = [status_row(*get(data, a.name))] if a.name else [status_row(k, p) for k, p in data["projects"].items()]
    active = sum(1 for p in data["projects"].values() if p["status"] == "active")
    if a.json:
        print(json.dumps({"wip_limit": data["wip_limit"], "active": active, "projects": rows}, indent=1))
        return
    print(f"active {active} / WIP limit {data['wip_limit']}" + ("  OVER LIMIT" if active > data["wip_limit"] else ""))
    for r in rows:
        print(f"{r['health']:7} {r['name'][:32]:32} {r['status']:9} {r['why']:22} asks {r['asks_open']:<3} left {r['items_left']:<4} next: {(r['next'] or ['-'])[0][:60]}")


def cmd_item(a):
    data = load()
    k, p = get(data, a.name)
    items = p.setdefault("items", [])
    if a.op == "add":
        iid = f"s{len(items) + 1:03d}"
        items.append({"id": iid, "title": a.arg, "created": now_iso(), "state": "todo"})
    else:
        it = next((i for i in items if i["id"] == a.arg), None) or sys.exit(f"no item {a.arg}")
        it["state"] = "done" if a.op == "done" else "dropped"
        it["done" if a.op == "done" else "dropped_at"] = now_iso()
    p["updated"] = now_iso()
    save(data)
    print(json.dumps({"items": items}, indent=1))


def cmd_forecast(a):
    data = load()
    k, p = get(data, a.name)
    g = gather(p)
    f = flow(g["items"], weeks=a.weeks)
    mc = monte_carlo([w["throughput"] for w in f["weeks"]], f["remaining"], a.trials)
    mc["target"] = p.get("target")
    mc["method"] = "Monte Carlo: resample weekly throughput from the last %d weeks until remaining reaches 0" % a.weeks
    print(json.dumps(mc, indent=1))


def cmd_review(a):
    data = load()
    k, p = get(data, a.name)
    g = gather(p)
    f = flow(g["items"])
    active = sorted(((kk, gather(pp)["idle_days"] or 0) for kk, pp in data["projects"].items() if pp["status"] == "active"),
                    key=lambda r: r[1])
    over = len(active) > data["wip_limit"] and k in [kk for kk, _ in active[data["wip_limit"]:]]
    flags, guess = review_findings(p, g, f, over, a.weeks or data["stall_weeks"])
    acts = next_actions(g)
    setdir = build_review_set(k, p, g, f, flags, guess, acts)
    log_event(p, "review", f"guess {guess}; " + "; ".join(flags))
    p["last_review"] = today().isoformat()
    save(data)
    out = {"project": p["name"], "flags": flags, "guess": guess, "next_actions": acts, "set": str(setdir)}
    ask = ask_script()
    if ask and not a.no_serve:
        r = subprocess.run([sys.executable, ask, "serve", str(setdir), "--detach"], capture_output=True, text=True, timeout=60)
        out["ask"] = r.stdout.strip()[-400:] or r.stderr.strip()[-400:]
    print(json.dumps(out, indent=1))


def cmd_table(a):
    data = load()
    k, p = get(data, a.name)
    date.fromisoformat(a.revisit)
    p.update(status="tabled", revisit=a.revisit, wake=a.wake)
    log_event(p, "tabled", f"revisit {a.revisit}; wake: {a.wake}")
    save(data)
    print(json.dumps({"tabled": k, "revisit": a.revisit}))


def cmd_abandon(a):
    data = load()
    k, p = get(data, a.name)
    p["status"] = "abandoned"
    p["postmortem"] = {"why": a.why, "keep": a.keep or "", "date": today().isoformat()}
    log_event(p, "abandoned", f"why: {a.why}; keep: {a.keep or '-'}")
    save(data)
    print(json.dumps({"abandoned": k, "postmortem": p["postmortem"]}))


def cmd_done(a):
    data = load()
    k, p = get(data, a.name)
    p["status"] = "done"
    log_event(p, "done", a.note or "")
    save(data)
    print(json.dumps({"done": k}))


def cmd_activate(a):
    data = load()
    k, p = get(data, a.name)
    p.update(status="active", revisit=None)
    log_event(p, "activated")
    save(data)
    print(json.dumps({"active": k}))


def cmd_merge(a):
    data = load()
    tk, tp = get(data, a.into)
    for n in a.names:
        k, p = get(data, n)
        if k == tk:
            continue
        tp["paths"] += [x for x in p.get("paths", []) if x not in tp["paths"]]
        tp.setdefault("items", []).extend(p.get("items", []))
        for src, refs in p.get("sources", {}).items():
            tp.setdefault("sources", {}).setdefault(src, []).extend(x for x in refs if x not in tp["sources"][src])
        log_event(tp, "merged", p["name"])
        del data["projects"][k]
    save(data)
    print(json.dumps({"into": tk, "paths": tp["paths"]}, indent=1))


def cmd_stall(a):
    data = load()
    if a.weeks is not None:
        data["stall_weeks"] = a.weeks
        save(data)
    print(json.dumps({"stall_weeks": data["stall_weeks"]}))


def cmd_wip(a):
    data = load()
    if a.n is not None:
        data["wip_limit"] = a.n
        save(data)
    print(json.dumps({"wip_limit": data["wip_limit"], "active": sum(1 for p in data["projects"].values() if p["status"] == "active")}))


def main(argv=None):
    ap = argparse.ArgumentParser(description="steerwright: drive projects to done, tabled or abandoned")
    ap.add_argument("--version", action="version", version=VERSION)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("discover"); s.add_argument("--root", action="append"); s.add_argument("--apply", action="store_true"); s.add_argument("--since", type=int, default=30); s.add_argument("--no-group", action="store_true"); s.set_defaults(fn=cmd_discover)
    s = sub.add_parser("merge"); s.add_argument("names", nargs="+"); s.add_argument("--into", required=True); s.set_defaults(fn=cmd_merge)
    s = sub.add_parser("stall"); s.add_argument("weeks", nargs="?", type=int); s.set_defaults(fn=cmd_stall)
    s = sub.add_parser("add"); s.add_argument("name"); s.add_argument("--path", action="append", required=True)
    s.add_argument("--kind", choices=KINDS, default="other"); s.add_argument("--goal"); s.add_argument("--done-when"); s.add_argument("--target"); s.set_defaults(fn=cmd_add)
    s = sub.add_parser("status"); s.add_argument("name", nargs="?"); s.add_argument("--json", action="store_true"); s.set_defaults(fn=cmd_status)
    s = sub.add_parser("item"); s.add_argument("name"); s.add_argument("op", choices=("add", "done", "drop")); s.add_argument("arg"); s.set_defaults(fn=cmd_item)
    s = sub.add_parser("forecast"); s.add_argument("name"); s.add_argument("--trials", type=int, default=10000); s.add_argument("--weeks", type=int, default=12); s.set_defaults(fn=cmd_forecast)
    s = sub.add_parser("review"); s.add_argument("name"); s.add_argument("--weeks", type=int); s.add_argument("--no-serve", action="store_true"); s.set_defaults(fn=cmd_review)
    s = sub.add_parser("table"); s.add_argument("name"); s.add_argument("--revisit", required=True); s.add_argument("--wake", required=True); s.set_defaults(fn=cmd_table)
    s = sub.add_parser("abandon"); s.add_argument("name"); s.add_argument("--why", required=True); s.add_argument("--keep"); s.set_defaults(fn=cmd_abandon)
    s = sub.add_parser("done"); s.add_argument("name"); s.add_argument("--note"); s.set_defaults(fn=cmd_done)
    s = sub.add_parser("activate"); s.add_argument("name"); s.set_defaults(fn=cmd_activate)
    s = sub.add_parser("wip"); s.add_argument("n", nargs="?", type=int); s.set_defaults(fn=cmd_wip)
    s = sub.add_parser("serve"); s.add_argument("--port", type=int); s.add_argument("--detach", action="store_true"); s.add_argument("--open", action="store_true"); s.set_defaults(fn=cmd_serve)
    s = sub.add_parser("up"); s.add_argument("--no-open", action="store_true"); s.set_defaults(fn=cmd_up)
    s = sub.add_parser("down"); s.set_defaults(fn=cmd_down)
    s = sub.add_parser("shortcut"); s.set_defaults(fn=lambda a: print(json.dumps({"shortcut": str(write_shortcut())})))
    a = ap.parse_args(argv)
    a.fn(a)


if __name__ == "__main__":
    main()

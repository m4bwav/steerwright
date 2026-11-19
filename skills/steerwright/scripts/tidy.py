"""steerwright tidy: leftovers sessions left behind, each with a verdict and the reason. Stdlib only.

`sw.py tidy` lists; `--apply` removes only items whose fresh verdict is safe, rechecked just before each step.
Verdicts:
  safe  removable with no loss (merged and clean, an empty folder, a stale record), undo note kept
  ask   might be leftover, but only Mark can say (unmerged files, a server this tool did not start)
  keep  in use or holding work (uncommitted changes, unmerged commits, young, a known keeper)
Servers are found by PID through quirkwright's `qw.py pid`, never by image name, and apply never stops one.
Apply never touches a remote, never uses --force on a worktree, and logs every step with its undo note.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

import sw

DEFAULT_ROOTS = [r"D:\m4bwa\Claude\Projects\Ai"]
DEFAULT_KEEP_PORTS = [8001, 8188, 8199, 11434, 47631]
WT_RX = re.compile(r"(^|[-_])wt($|[-_])", re.I)
JUNK_DIRS = {"__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache"}


def config():
    c = sw.read_json(sw.home() / "config.json", {}) or {}
    return {"roots": c.get("tidy_roots") or DEFAULT_ROOTS, "days": c.get("tidy_days", 3),
            "scratch_days": c.get("tidy_scratch_days", 7), "keep_ports": c.get("tidy_keep_ports") or DEFAULT_KEEP_PORTS}


def git(cwd, *args, timeout=30):
    """(exit code, stdout) of a read-only git command."""
    try:
        r = subprocess.run(["git", "-C", str(cwd), *args], capture_output=True, text=True, encoding="utf-8",
                           errors="replace", timeout=timeout)
        return r.returncode, r.stdout.strip()
    except (OSError, subprocess.TimeoutExpired):
        return 1, ""


def age(path):
    try:
        return round((time.time() - os.path.getmtime(path)) / 86400, 1)
    except OSError:
        return None


def item(kind, title, verdict, why, path=None, undo=None, **extra):
    return dict({"kind": kind, "title": title, "verdict": verdict, "why": why, "path": str(path) if path else None,
                 "undo": undo}, **extra)


def repos(cfg):
    """Main clones (a .git folder, not a worktree's .git file) directly under each root."""
    for r in cfg["roots"]:
        try:
            kids = sorted(Path(r).iterdir())
        except OSError:
            continue
        for d in kids:
            if (d / ".git").is_dir():
                yield d


def worktree_list(repo):
    code, out = git(repo, "worktree", "list", "--porcelain")
    rows, cur = [], {}
    for ln in out.splitlines() + [""]:
        if not ln:
            if cur:
                rows.append(cur)
            cur = {}
        elif " " in ln:
            k, v = ln.split(" ", 1)
            cur[k] = v
        else:
            cur[ln] = True
    return rows


def default_ref(repo):
    code, out = git(repo, "rev-parse", "--abbrev-ref", "origin/HEAD")
    return out if code == 0 and out else None


def upstream_gone(cwd, branch):
    code, out = git(cwd, "for-each-ref", "--format=%(upstream:track)", "refs/heads/" + branch)
    return "[gone]" in out


def pr_merged(cwd, branch):
    """True when GitHub has a merged PR from this branch (squash merges are not ancestors). None when unknown."""
    try:
        r = subprocess.run(["gh", "pr", "list", "--head", branch, "--state", "merged", "--json", "number"], cwd=str(cwd),
                           capture_output=True, text=True, timeout=30)
        return bool(json.loads(r.stdout or "[]")) if r.returncode == 0 else None
    except (OSError, ValueError, subprocess.TimeoutExpired):
        return None


def scan_worktrees(cfg):
    out, known = [], set()
    for repo in repos(cfg):
        ref = default_ref(repo)
        for i, w in enumerate(worktree_list(repo)):
            p = Path(w.get("worktree", ""))
            known.add(sw.norm(p))
            if i == 0:
                continue  # the main clone
            branch = (w.get("branch") or "").replace("refs/heads/", "")
            sha = w.get("HEAD", "")[:12]
            title = "%s worktree %s (%s)" % (repo.name, p.name, branch or "detached")
            undo = "git -C %s worktree add %s %s" % (repo, p, sha) if not branch else \
                "git -C %s branch %s %s; git -C %s worktree add %s %s" % (repo, branch, sha, repo, p, branch)
            a = age(p)
            base = dict(path=p, undo=undo, sha=sha, branch=branch, repo=str(repo), age_days=a)
            if "prunable" in w or not p.exists():
                out.append(item("worktree", title, "safe", "folder is gone; git still lists it (git worktree prune)", **base))
                continue
            code, dirty = git(p, "status", "--porcelain")
            if code != 0:
                out.append(item("worktree", title, "keep", "git status failed; left alone", **base))
            elif dirty:
                out.append(item("worktree", title, "keep", "uncommitted changes (%d files)" % len(dirty.splitlines()), **base))
            elif a is not None and a < cfg["days"]:
                out.append(item("worktree", title, "keep", "young (%.1f d); a session may still use it" % a, **base))
            elif ref and git(p, "merge-base", "--is-ancestor", "HEAD", ref)[0] == 0:
                out.append(item("worktree", title, "safe", "clean and merged into %s" % ref, **base))
            elif branch and upstream_gone(p, branch) and pr_merged(p, branch):
                out.append(item("worktree", title, "safe", "clean; its PR was merged and the remote branch is gone", force=True, **base))
            else:
                out.append(item("worktree", title, "keep", "commits not on %s" % (ref or "the default branch"), **base))
    for r in cfg["roots"]:
        try:
            kids = sorted(Path(r).iterdir())
        except OSError:
            continue
        for d in kids:
            if not d.is_dir() or not WT_RX.search(d.name) or (d / ".git").exists() or sw.norm(d) in known:
                continue
            if any(k.startswith(sw.norm(d) + os.sep) or k.startswith(sw.norm(d) + "/") for k in known):
                continue  # a container of live worktrees (like _wt), not a leftover
            files = [f for f in d.rglob("*") if f.is_file() and not JUNK_DIRS & set(f.relative_to(d).parts)]
            if files:
                out.append(item("folder", "leftover worktree folder %s" % d.name, "ask",
                                "no .git, but %d files remain (first: %s)" % (len(files), files[0].relative_to(d)),
                                path=d, age_days=age(d)))
            else:
                out.append(item("folder", "leftover worktree folder %s" % d.name, "safe",
                                "no .git and no files (only caches)", path=d, age_days=age(d)))
    return out


def scan_branches(cfg):
    out = []
    gone = []
    for repo in repos(cfg):
        ref = default_ref(repo)
        if not ref:
            continue
        busy = {(w.get("branch") or "").replace("refs/heads/", "") for w in worktree_list(repo)}
        merged = set(git(repo, "branch", "--format=%(refname:short)", "--merged", ref)[1].splitlines())
        code, rows = git(repo, "for-each-ref", "--format=%(refname:short)|%(objectname:short=12)|%(upstream:track)|%(committerdate:unix)",
                         "refs/heads")
        for ln in rows.splitlines():
            name, sha, track, ts = (ln.split("|") + ["", "", ""])[:4]
            if name in busy or name == ref.split("/", 1)[-1]:
                continue
            a = round((time.time() - int(ts)) / 86400, 1) if ts.isdigit() else None
            base = dict(path=None, undo="git -C %s branch %s %s" % (repo, name, sha), sha=sha, branch=name,
                        repo=str(repo), age_days=a)
            title = "%s (%s)" % (name, repo.name)
            if name in merged:
                out.append(item("branch", title, "safe", "merged into %s (git branch -d)" % ref, **base))
            elif "[gone]" in track:
                gone.append((repo, ref, title, base))
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(8) as ex:
        verdicts = list(ex.map(lambda g: pr_merged(g[0], g[3]["branch"]), gone))
    for (repo, ref, title, base), merged_pr in zip(gone, verdicts):
        if merged_pr:
            out.append(item("branch", title, "safe", "its PR was merged and the remote branch is gone (git branch -D)", force=True, **base))
        else:
            out.append(item("branch", title, "ask", "remote branch gone, commits not on %s, no merged PR found" % ref, **base))
    return out


def qw_script():
    reg = sw.read_json(Path.home() / ".claude" / "plugins" / "installed_plugins.json", {}) or {}
    for k, v in (reg.get("plugins") or {}).items():
        if k.startswith("quirkwright@") and v:
            p = Path(v[0]["installPath"]) / "skills" / "quirkwright" / "scripts" / "qw.py"
            if p.exists():
                return p
    return None


def processes():
    """pid -> {pid, name, start, cmd} for python and node processes, from quirkwright."""
    qw = qw_script()
    if not qw:
        raise RuntimeError("quirkwright not installed; servers not scanned")
    got = {}
    for pat in ("python", "node"):
        r = subprocess.run([sys.executable, str(qw), "pid", pat], capture_output=True, text=True, timeout=60)
        try:
            for m in json.loads(r.stdout or "{}").get("matches", []):
                if (m.get("name") or "").lower().startswith(pat):  # qw matches command lines too (Code.exe runs node)
                    got[int(m["pid"])] = m
        except ValueError:
            pass
    return got


def listeners(text):
    """(port, pid) for local LISTENING TCP sockets in `netstat -ano` output."""
    out = set()
    for ln in text.splitlines():
        f = ln.split()
        if len(f) >= 5 and f[0] == "TCP" and f[3] == "LISTENING":
            out.add((int(f[1].rsplit(":", 1)[1]), int(f[4])))
    return sorted(out)


def pid_alive(pid):
    if os.name == "nt":
        try:
            r = subprocess.run(["tasklist", "/FI", "PID eq %d" % pid, "/NH", "/FO", "CSV"], capture_output=True, text=True, timeout=20)
            return ('"%d"' % pid) in r.stdout
        except (OSError, subprocess.TimeoutExpired):
            return True  # unknown counts as alive: never call a live record stale
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False


def scan_servers(cfg, netstat=None, procs=None):
    if netstat is None:
        netstat = subprocess.run(["netstat", "-ano", "-p", "TCP"], capture_output=True, text=True, timeout=60).stdout
    if procs is None:
        procs = processes()
    keep = set(cfg["keep_ports"])
    ask_srv = sw.read_json(sw.sib_home("askwright") / "dashboard" / "server.json", {}) or {}
    out, seen = [], set()
    for port, pid in listeners(netstat):
        p = procs.get(pid)
        if not p or (port, pid) in seen:
            continue
        seen.add((port, pid))
        base = dict(path=None, undo=None, pid=pid, port=port, start=p.get("start"), cmd=(p.get("cmd") or "")[:300])
        title = "port %d" % port
        if port in keep or pid == ask_srv.get("pid"):
            out.append(item("server", title, "keep", "known keeper (%s)" % p.get("name"), **base))
        else:
            out.append(item("server", title, "ask", "%s pid %d since %s; stopping it needs Mark's yes" % (p.get("name"), pid, p.get("start")), **base))
    rec = sw.read_json(sw.home() / "server.json", None)
    if rec and rec.get("pid") and not pid_alive(int(rec["pid"])):
        out.append(item("record", "steerwright server.json", "safe", "pid %s is not running; the record is stale" % rec["pid"],
                        path=sw.home() / "server.json", undo=json.dumps(rec)))
    return out


def scan_scratch(cfg):
    base = Path(os.environ.get("TEMP") or os.environ.get("TMPDIR") or "/tmp") / "claude"
    out = []
    try:
        slugs = sorted(base.iterdir())
    except OSError:
        return out
    for slug in slugs:
        if not slug.is_dir():
            continue
        stale = [d for d in slug.iterdir() if d.is_dir() and (age(d) or 0) >= cfg["scratch_days"]]
        if stale:
            out.append(item("scratch", "%s: %d session folders" % (slug.name, len(stale)), "safe",
                            "session scratch untouched for %d+ days" % cfg["scratch_days"], path=slug,
                            folders=sorted(str(d) for d in stale), age_days=max(age(d) or 0 for d in stale)))
    return out


SCANNERS = {"worktrees": scan_worktrees, "branches": scan_branches, "servers": scan_servers, "scratch": scan_scratch}


def scan(only=None):
    cfg = config()
    items, notes = [], []
    for name, fn in SCANNERS.items():
        if only and name not in only:
            continue
        try:
            items += fn(cfg)
        except Exception as e:  # each scanner fails soft
            notes.append("%s: %s" % (name, str(e)[:200]))
    counts = {v: sum(1 for i in items if i["verdict"] == v) for v in ("safe", "ask", "keep")}
    return {"generated": sw.now_iso(), "dry_run": True, "counts": counts, "items": items, "notes": notes}


# ---------- apply ----------

def only_junk(d):
    return not any(f.is_file() and not JUNK_DIRS & set(f.relative_to(d).parts) for f in d.rglob("*"))


def apply_one(i, cfg):
    """Carry out one safe item after rechecking it. Returns (ok, what happened)."""
    k, p = i["kind"], Path(i["path"]) if i.get("path") else None
    if k == "worktree":
        repo = i["repo"]
        if p.exists():
            code, dirty = git(p, "status", "--porcelain")
            if code != 0 or dirty:
                return False, "changed since the scan (dirty or unreadable); left alone"
            code, _ = git(repo, "worktree", "remove", str(p))  # no --force: git refuses dirty or locked trees
            if code != 0:
                return False, "git worktree remove refused"
        else:
            git(repo, "worktree", "prune")
        if i.get("branch"):
            code, _ = git(repo, "branch", "-D" if i.get("force") else "-d", i["branch"])
            return True, "worktree removed" + ("; branch deleted" if code == 0 else "; branch kept (git refused)")
        return True, "worktree removed"
    if k == "branch":
        code, _ = git(i["repo"], "branch", "-D" if i.get("force") else "-d", i["branch"])
        return (True, "branch deleted") if code == 0 else (False, "git branch refused")
    if k == "folder":
        if (p / ".git").exists() or not only_junk(p):
            return False, "files appeared since the scan; left alone"
        shutil.rmtree(p)
        return True, "empty folder removed"
    if k == "record":
        rec = sw.read_json(p, None)
        if rec and rec.get("pid") and pid_alive(int(rec["pid"])):
            return False, "the pid is running again; kept"
        p.unlink(missing_ok=True)
        return True, "stale record removed"
    if k == "scratch":
        gone = 0
        for f in i.get("folders") or []:
            f = Path(f)
            if f.parent == p and (age(f) or 0) >= cfg["scratch_days"]:
                shutil.rmtree(f, ignore_errors=True)
                gone += not f.exists()
        return True, "%d session folders removed" % gone
    return False, "no apply step for %s" % k


def apply(only=None):
    """Fresh scan, then each safe item in turn. Every step goes to tidy-log.jsonl with its undo note."""
    cfg = config()
    out = scan(only=only)
    log = sw.home() / "tidy-log.jsonl"
    done = []
    for i in out["items"]:
        if i["verdict"] != "safe":
            continue
        try:
            ok, what = apply_one(i, cfg)
        except Exception as e:  # one failure never stops the rest
            ok, what = False, "error: %s" % str(e)[:200]
        row = {"at": sw.now_iso(), "kind": i["kind"], "title": i["title"], "path": i.get("path"), "ok": ok,
               "what": what, "undo": i.get("undo")}
        with open(log, "a", encoding="utf-8", newline="\n") as f:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
        done.append(row)
    return {"applied": done, "notes": out["notes"], "log": str(log)}


def apply_allowed():
    return bool((sw.read_json(sw.home() / "config.json", {}) or {}).get("tidy_apply_ok"))


def cmd_tidy(a):
    if a.apply:
        if not apply_allowed():
            raise SystemExit("tidy --apply is off until Mark has seen the dry run and said yes. "
                             "Then set tidy_apply_ok to true in %s." % (sw.home() / "config.json"))
        res = apply(only=a.only)
        if a.json:
            print(json.dumps(res, indent=1, ensure_ascii=False))
            return
        ok = sum(r["ok"] for r in res["applied"])
        print("applied: %d done, %d left alone; log %s" % (ok, len(res["applied"]) - ok, res["log"]))
        for r in res["applied"]:
            if not r["ok"]:
                print("left  %-8s %-60s %s" % (r["kind"], r["title"][:60], r["what"]))
        for n in res["notes"]:
            print("note: " + n)
        return
    out = scan(only=a.only)
    if a.json:
        print(json.dumps(out, indent=1, ensure_ascii=False))
        return
    c = out["counts"]
    print("dry run: %d safe, %d ask Mark, %d keep" % (c["safe"], c["ask"], c["keep"]))
    order = {"safe": 0, "ask": 1, "keep": 2}
    for i in sorted(out["items"], key=lambda i: (order[i["verdict"]], i["kind"], i["title"])):
        if i["verdict"] == "keep" and not a.all:
            continue
        print("%-4s %-8s %-60s %s" % (i["verdict"], i["kind"], i["title"][:60], i["why"]))
    if not a.all and c["keep"]:
        print("(%d kept items hidden; --all shows them)" % c["keep"])
    for n in out["notes"]:
        print("note: " + n)

import json
import os
import subprocess
import sys
import time
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_sw import Env, write  # noqa: E402
import sw  # noqa: E402
import tidy  # noqa: E402


def git(cwd, *args):
    return subprocess.run(["git", "-C", str(cwd), *args], capture_output=True, text=True, check=True).stdout.strip()


def old(path, days=10):
    t = time.time() - days * 86400
    os.utime(path, (t, t))


class Tidy(unittest.TestCase):
    def setUp(self):
        self.env = Env()
        self.d = self.env.__enter__()
        root = self.d / "Ai"
        remote = self.d / "remote.git"
        subprocess.run(["git", "init", "-q", "--bare", "-b", "main", str(remote)], check=True)
        self.repo = root / "proj"
        subprocess.run(["git", "clone", "-q", str(remote), str(self.repo)], check=True, capture_output=True)
        for k, v in (("user.email", "t@t"), ("user.name", "t"), ("commit.gpgsign", "false")):
            git(self.repo, "config", k, v)
        write(self.repo / "a.txt", "a\n")
        git(self.repo, "add", "-A"); git(self.repo, "commit", "-q", "-m", "a"); git(self.repo, "push", "-q", "-u", "origin", "main")
        git(self.repo, "remote", "set-head", "origin", "main")
        # merged worktree, dirty worktree, unmerged worktree
        git(self.repo, "worktree", "add", "-q", str(root / "proj-done"), "-b", "done", "origin/main")
        git(self.repo, "worktree", "add", "-q", str(root / "proj-dirty"), "-b", "dirty", "origin/main")
        write(root / "proj-dirty" / "wip.txt", "unsaved\n")
        git(self.repo, "worktree", "add", "-q", str(root / "proj-wip"), "-b", "wip", "origin/main")
        write(root / "proj-wip" / "b.txt", "b\n")
        git(root / "proj-wip", "add", "-A"); git(root / "proj-wip", "commit", "-q", "-m", "b")
        git(self.repo, "branch", "merged-branch", "origin/main")
        # leftover folders of removed worktrees
        (root / "proj-wt-empty" / "__pycache__").mkdir(parents=True)
        write(root / "proj-wt-files" / "notes.md", "x\n")
        for p in ("proj-done", "proj-dirty", "proj-wip", "proj-wt-empty", "proj-wt-files"):
            old(root / p)
        write(self.d / "steer" / "config.json", json.dumps({"tidy_roots": [str(root)], "tidy_days": 3}))
        self.root = root

    def tearDown(self):
        self.env.__exit__()

    def by_path(self, items):
        return {Path(i["path"]).name if i["kind"] in ("worktree", "folder", "scratch") else i["title"]: i for i in items}

    def test_worktrees_safe_only_when_merged_clean_and_old(self):
        got = self.by_path(tidy.scan_worktrees(tidy.config()))
        self.assertEqual(got["proj-done"]["verdict"], "safe")
        self.assertIn("merged", got["proj-done"]["why"])
        self.assertIn(got["proj-done"]["sha"], got["proj-done"]["undo"])  # undo note keeps the SHA
        self.assertEqual(got["proj-dirty"]["verdict"], "keep")
        self.assertIn("uncommitted", got["proj-dirty"]["why"])
        self.assertEqual(got["proj-wip"]["verdict"], "keep")
        self.assertNotIn("proj", got)  # the main clone is never a candidate
        self.assertEqual(got["proj-wt-empty"]["verdict"], "safe")
        self.assertEqual(got["proj-wt-files"]["verdict"], "ask")

    def test_young_worktree_is_kept(self):
        git(self.repo, "worktree", "add", "-q", str(self.root / "proj-new"), "-b", "new", "origin/main")
        got = self.by_path(tidy.scan_worktrees(tidy.config()))
        self.assertEqual(got["proj-new"]["verdict"], "keep")
        self.assertIn("young", got["proj-new"]["why"])

    def test_branches(self):
        got = {i["title"].split()[0]: i for i in tidy.scan_branches(tidy.config())}
        self.assertEqual(got["merged-branch"]["verdict"], "safe")
        self.assertNotIn("main", got)  # default branch
        self.assertNotIn("done", got)  # checked out in a worktree: that worktree's row covers it

    def test_servers_keepers_and_stale_record(self):
        netstat = ("  TCP    127.0.0.1:8199    0.0.0.0:0    LISTENING    100\n"
                   "  TCP    127.0.0.1:8765    0.0.0.0:0    LISTENING    200\n"
                   "  TCP    127.0.0.1:9999    0.0.0.0:0    LISTENING    300\n")
        procs = {100: {"pid": 100, "name": "python.exe", "start": "2026-11-01T00:00:00", "cmd": "comfy"},
                 200: {"pid": 200, "name": "python.exe", "start": "2026-11-01T00:00:00", "cmd": "python -m http.server 8765"}}
        write(self.d / "steer" / "server.json", json.dumps({"pid": 999999, "port": 47630}))
        got = self.by_path(tidy.scan_servers(tidy.config(), netstat=netstat, procs=procs))
        self.assertEqual(got["port 8199"]["verdict"], "keep")
        self.assertEqual(got["port 8765"]["verdict"], "ask")  # a server not left by this chain waits on Mark
        self.assertEqual(got["port 8765"]["pid"], 200)
        self.assertNotIn("port 9999", got)  # not python or node
        stale = got["steerwright server.json"]
        self.assertEqual(stale["verdict"], "safe")

    def test_scratch_old_only(self):
        t = self.d / "nowhere" / "claude" / "slug"
        (t / "old-session").mkdir(parents=True); old(t / "old-session")
        (t / "new-session").mkdir(parents=True)
        got = self.by_path(tidy.scan_scratch(tidy.config()))
        self.assertEqual(got["slug"]["verdict"], "safe")  # one row per project slug
        self.assertEqual([Path(f).name for f in got["slug"]["folders"]], ["old-session"])

    def test_dry_run_changes_nothing(self):
        before = sorted(p.name for p in self.root.iterdir())
        out = tidy.scan(only=["worktrees", "branches"])
        self.assertTrue(out["items"])
        self.assertEqual(before, sorted(p.name for p in self.root.iterdir()))
        self.assertIn("merged-branch", git(self.repo, "branch"))


if __name__ == "__main__":
    unittest.main()

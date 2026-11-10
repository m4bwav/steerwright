import contextlib
import io
import json
import os
import sys
import tempfile
import unittest
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "skills" / "steerwright" / "scripts"))
import sw  # noqa: E402


def item(i, created_days_ago, done_days_ago=None):
    now = datetime.now()
    return {"id": str(i), "title": f"t{i}", "lane": "x", "created": now - timedelta(days=created_days_ago),
            "started": None, "done": now - timedelta(days=done_days_ago) if done_days_ago is not None else None,
            "state": "done" if done_days_ago is not None else "todo"}


class Flow(unittest.TestCase):
    def test_counts(self):
        f = sw.flow([item(1, 30, 10), item(2, 20, 3), item(3, 5), item(4, 50, 40)])
        self.assertEqual(f["done"], 3)
        self.assertEqual(f["remaining"], 1)
        self.assertEqual(f["cycle"]["n"], 3)
        self.assertEqual(len(f["weeks"]), 12)

    def test_monte_carlo(self):
        self.assertEqual(sw.monte_carlo([1, 2], 0)["remaining"], 0)
        self.assertIn("no throughput", sw.monte_carlo([0, 0], 5)["note"])
        mc = sw.monte_carlo([2, 2, 2], 6, seed=1)
        self.assertNotIn("note", {k for k in mc if mc.get(k) == "no throughput"})


class Health(unittest.TestCase):
    def test_bands(self):
        p = {"status": "active"}
        self.assertEqual(sw.health(p, {"idle_days": None})[0], "red")
        self.assertEqual(sw.health(p, {"idle_days": 2})[0], "green")
        self.assertEqual(sw.health(p, {"idle_days": 14})[0], "amber")
        self.assertEqual(sw.health(p, {"idle_days": 40})[0], "red")
        self.assertEqual(sw.health({"status": "tabled", "revisit": "2000-01-01"}, {})[0], "wake")


class Grouping(unittest.TestCase):
    def test_plugins_fold(self):
        with tempfile.TemporaryDirectory() as d:
            a, b, c = Path(d, "a"), Path(d, "b"), Path(d, "c")
            (a / ".claude-plugin").mkdir(parents=True)
            (b / "skills" / "x").mkdir(parents=True)
            (b / "skills" / "x" / "SKILL.md").write_text("x")
            c.mkdir()
            props = [{"name": n, "path": str(p), "kind": "other", "sources": {"handoff": [n]}, "last": "2026-11-0" + str(i + 1)}
                     for i, (n, p) in enumerate((("a", a), ("b", b), ("c", c)))]
            out = sw.group_proposals(props)
            self.assertEqual(sorted(o["name"] for o in out), ["Plugins", "c"])
            g = next(o for o in out if o["name"] == "Plugins")
            self.assertEqual(len(g["paths"]), 2)
            self.assertEqual(g["last"], "2026-11-02")


class Registry(unittest.TestCase):
    def test_defaults_and_merge(self):
        with tempfile.TemporaryDirectory() as d:
            os.environ["STEERWRIGHT_HOME"] = d
            try:
                data = sw.load()
                self.assertEqual((data["wip_limit"], data["stall_weeks"]), (8, 8))
                data["projects"]["x"] = sw.new_project("x", [d + "/x"])
                data["projects"]["y"] = sw.new_project("y", [d + "/y"])
                sw.save(data)
                sw.main(["merge", "y", "--into", "x"])
                data = sw.load()
                self.assertEqual(list(data["projects"]), ["x"])
                self.assertEqual(len(data["projects"]["x"]["paths"]), 2)
            finally:
                del os.environ["STEERWRIGHT_HOME"]


class Env:
    """Scratch steerwright and sibling homes; TEMP pointed away so is_temp does not hide the fixtures."""
    def __enter__(self):
        self.td = tempfile.TemporaryDirectory()
        self.d = Path(self.td.name)
        self.old = {k: os.environ.get(k) for k in ("STEERWRIGHT_HOME", "ASKWRIGHT_HOME", "CHAINWRIGHT_HOME", "GRINDWRIGHT_HOME", "TEMP", "TMPDIR")}
        for k, sub in (("STEERWRIGHT_HOME", "steer"), ("ASKWRIGHT_HOME", "ask"), ("CHAINWRIGHT_HOME", "chain"), ("GRINDWRIGHT_HOME", "grind")):
            os.environ[k] = str(self.d / sub)
        os.environ["TEMP"] = os.environ["TMPDIR"] = str(self.d / "nowhere")
        sw._CACHE.clear()
        return self.d

    def __exit__(self, *a):
        for k, v in self.old.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v
        sw._CACHE.clear()
        self.td.cleanup()


def write(path, text):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(text, encoding="utf-8")


def quiet(argv):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        sw.main(argv)
    return buf.getvalue()


class Commands(unittest.TestCase):
    def test_rename_keeps_alias(self):
        with Env() as d:
            data = sw.load()
            data["projects"]["tiny-colony"] = sw.new_project("Tiny Colony", [str(d / "sdb")])
            sw.save(data)
            quiet(["rename", "Tiny Colony", "SpaceDeckBuilder2"])
            data = sw.load()
            self.assertEqual(list(data["projects"]), ["spacedeckbuilder2"])
            p = data["projects"]["spacedeckbuilder2"]
            self.assertIn("Tiny Colony", p["sources"]["askwright"])
            self.assertEqual(p["history"][-1]["event"], "renamed")

    def test_review_then_apply(self):
        with Env() as d:
            proj = d / "proj"
            write(proj / "ai-docs" / "log.md", "# log\n\n## " + datetime.now().strftime("%Y-%m-%d") + "\n- x\n")
            data = sw.load()
            data["projects"]["proj"] = sw.new_project("proj", [str(proj)])
            data["projects"]["other"] = sw.new_project("other", [str(d / "other")])
            sw.save(data)
            quiet(["review", "proj", "--no-serve"])
            sets = list((d / "steer" / "reviews").glob("steer-proj-*"))
            self.assertEqual(len(sets), 1)
            q = sw.read_json(sets[0] / "questions.json")
            self.assertEqual([x["id"] for x in q["questions"]], ["decision", "next", "wake", "postmortem"])
            quiet(["apply-review"])  # unanswered: nothing happens
            self.assertEqual(sw.load()["projects"]["proj"]["status"], "active")
            sw.write_json(sets[0] / "answers.json", {"answers": {
                "decision": {"choice": "table", "state": "answered", "note": ""},
                "wake": {"text": "2027-01-15; when Arvum ships", "state": "answered"}}})
            quiet(["apply-review", "proj"])
            p = sw.load()["projects"]["proj"]
            self.assertEqual((p["status"], p["revisit"], p["wake"]), ("tabled", "2027-01-15", "when Arvum ships"))
            self.assertTrue((sets[0] / "applied.json").exists())
            quiet(["activate", "proj"])
            quiet(["apply-review"])  # already applied: no change
            self.assertEqual(sw.load()["projects"]["proj"]["status"], "active")

    def test_keep_sets_next_actions(self):
        with Env() as d:
            data = sw.load()
            data["projects"]["k"] = sw.new_project("k", [str(d / "k")])
            sw.save(data)
            s = d / "steer" / "reviews" / "steer-k-2026-11-09"
            sw.write_json(s / "questions.json", {"questions": []})
            sw.write_json(s / "answers.json", {"answers": {"decision": {"choice": "keep", "state": "answered"},
                                                            "next": {"text": "a; b\nc; d", "state": "answered"}}})
            quiet(["apply-review"])
            p = sw.load()["projects"]["k"]
            self.assertEqual(p["next_actions"], ["a", "b", "c"])
            self.assertEqual(sw.next_actions({"items": [], "asks_open": 0, "prompts": []}, 3, p), ["a", "b", "c"])

    def test_table_without_date_is_indefinite(self):
        with Env() as d:
            data = sw.load()
            data["projects"]["t"] = sw.new_project("t", [str(d / "t")])
            data["projects"]["u"] = sw.new_project("u", [str(d / "u")])
            sw.save(data)
            s = d / "steer" / "reviews" / "steer-t-2026-11-09"
            sw.write_json(s / "questions.json", {"questions": []})
            sw.write_json(s / "answers.json", {"answers": {"decision": {"choice": "table", "state": "answered"},
                                                            "wake": {"text": "when I decide", "state": "answered"}}})
            quiet(["apply-review"])
            quiet(["table", "u"])
            data = sw.load()
            for k in ("t", "u"):
                p = data["projects"][k]
                self.assertEqual((p["status"], p["revisit"]), ("tabled", None))
                self.assertEqual(sw.health(p, {"idle_days": 400}), ("tabled", "parked indefinitely"))
            self.assertEqual(data["projects"]["t"]["wake"], "when I decide")

    def test_traffic_setting_and_route(self):
        with Env() as d:
            f = d / "rt" / "data" / "dashboard.html"
            write(f, "<html><body><h1>traffic</h1></body></html>")
            quiet(["traffic", str(d / "rt")])
            self.assertEqual(sw.traffic_file(), f)
            self.assertIn("/traffic", sw.sibling_links())
            quiet(["traffic", "--off"])
            self.assertIsNone(sw.traffic_file())

    def test_milestone_and_risk(self):
        with Env() as d:
            data = sw.load()
            data["projects"]["m"] = sw.new_project("m", [str(d / "m")])
            sw.save(data)
            quiet(["milestone", "m", "add", "Vertical slice", "--date", "2026-12-01"])
            quiet(["milestone", "m", "done", "m1"])
            quiet(["risk", "m", "add", "GPU busy", "--likelihood", "high", "--impact", "low"])
            p = sw.load()["projects"]["m"]
            self.assertEqual(p["milestones"][0]["state"], "done")
            self.assertEqual(p["risks"][0]["likelihood"], "high")
            page = sw.project_page("m", p)
            self.assertIn("Vertical slice", page)
            self.assertIn("GPU busy", page)


class Discover(unittest.TestCase):
    def test_askwright_and_handoff_sources(self):
        with Env() as d:
            today = datetime.now().strftime("%Y-%m-%d")
            game, film = d / "work" / "game", d / "work" / "film"
            write(game / "ai-docs" / "HANDOFF.md", "x")
            write(game / "ai-docs" / "log.md", f"## {today}\n- did\n")
            write(film / "ai-docs" / "HANDOFF.md", "x")
            write(film / "ai-docs" / "log.md", "## 2001-01-01\n- old\n")
            os.utime(film / "ai-docs" / "HANDOFF.md", (978307200, 978307200))  # HANDOFF mtime counts as activity
            sw.write_json(d / "ask" / "projects" / "g.json", {"name": "Game One", "dirs": [str(game)]})
            props = json.loads(quiet(["discover", "--root", str(d / "work"), "--no-group"]))["proposals"]
            self.assertEqual([p["name"] for p in props], ["Game One"])  # film is older than --since 30
            self.assertEqual(set(props[0]["sources"]), {"askwright", "handoff"})
            quiet(["discover", "--root", str(d / "work"), "--no-group", "--since", "100000", "--apply"])
            self.assertEqual(sorted(sw.load()["projects"]), ["film", "game-one"])


if __name__ == "__main__":
    unittest.main()

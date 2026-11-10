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


if __name__ == "__main__":
    unittest.main()

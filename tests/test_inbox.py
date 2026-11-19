import json
import sys
import unittest
import unittest.mock
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_sw import Env, write, quiet  # noqa: E402
import sw  # noqa: E402
import inbox  # noqa: E402


def fake_run(cmd, timeout=60):
    if cmd[0] == "gh":
        if "--assignee" in cmd:
            return json.dumps([{"repository": {"nameWithOwner": "o/r"}, "number": 5, "title": "Fix",
                                "url": "https://github.com/o/r/pull/5", "createdAt": "2026-11-01T00:00:00Z"}])
        return json.dumps([{"repository": {"nameWithOwner": "o/r"}, "number": 5, "title": "Fix",
                            "url": "https://github.com/o/r/pull/5", "createdAt": "2026-11-01T00:00:00Z"}])
    if "sweep" in cmd:
        return json.dumps({"todo": [{"set": SET, "title": "Takes", "project": "films", "waiting_days": 9.0}],
                           "check": [{"set": "x", "title": "young", "waiting_days": 1.0}]})
    raise RuntimeError("no evergreen here")


SET = ""


class Inbox(unittest.TestCase):
    def setUp(self):
        self.env = Env()
        self.d = self.env.__enter__()
        global SET
        proj = self.d / "proj"
        SET = str(proj / "ask" / "takes")
        write(proj / "ai-docs" / "HANDOFF.md", "# h\n\n## Waiting on Mark\n- Pick a banner\n- OK to publish to npm?\n\n## Next\n- x\n")
        write(self.d / "grindstate" / "WAITING.md", "# Waiting on a person (generated)\n- Mark: Card art (g1), answers on the askwright set, %s; unblocks 0\n- Jenny: other\n" % SET)
        write(self.d / "grind" / "runs.jsonl", json.dumps({"state": str(self.d / "grindstate")}) + "\n")
        write(self.d / "backlog" / "b.md", "- [ ] Decide engage #S #needs-mark\n- [x] done #needs-mark\n- [ ] Not mine #M\n")
        write(self.d / "steer" / "config.json", json.dumps({"inbox_backlogs": [str(self.d / "backlog")]}))
        data = sw.load()
        data["projects"]["proj"] = sw.new_project("proj", [proj, self.d / "grindstate"])
        sw.save(data)
        p = [unittest.mock.patch.object(inbox, "run", fake_run),
             unittest.mock.patch.object(sw, "ask_script", lambda: "ask.py")]
        for x in p:
            x.start()
            self.addCleanup(x.stop)

    def tearDown(self):
        self.env.__exit__()

    def test_collects_normalises_and_maps(self):
        out = inbox.collect(fresh=True)
        src = sorted(i["source"] for i in out["items"])
        self.assertEqual(src, ["ask", "backlog", "handoff", "handoff", "prs"])  # grind line deduped against the ask set
        self.assertEqual(len([i for i in out["items"] if i["source"] == "prs"]), 1)  # deduped by url
        ask = next(i for i in out["items"] if i["source"] == "ask")
        self.assertEqual(ask["project"], "proj")
        pub = [i for i in out["items"] if i["kind"] == "go-ahead"]
        self.assertEqual(len(pub), 1)
        self.assertEqual(next(i for i in out["items"] if i["source"] == "backlog")["minutes"], 2)
        self.assertTrue(any(n.startswith("evergreen:") for n in out["notes"]))  # failed soft
        for i in out["items"]:
            self.assertEqual(set(i), {"id", "source", "kind", "title", "age_days", "link", "path", "action", "minutes", "project"})

    def test_cache_and_cli(self):
        inbox.collect(fresh=True)
        self.assertTrue((self.d / "steer" / "inbox-cache.json").exists())
        out = json.loads(quiet(["inbox", "--json"]))
        self.assertTrue(out["cached"])
        text = quiet(["inbox", "--source", "backlog"])
        self.assertIn("Decide engage", text)

    def test_grind_kept_without_ask_set(self):
        out = inbox.collect(only=["grind"])
        self.assertEqual(len(out["items"]), 1)
        self.assertEqual(out["items"][0]["project"], "proj")


if __name__ == "__main__":
    unittest.main()

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

    def test_page_groups_filters_and_mounts(self):
        code, body, ctype = sw.render("/inbox", "fresh=1", "/steer")
        self.assertEqual(code, 200)
        self.assertIn("Pick a banner", body)
        self.assertIn("href='/steer/inbox?project=proj'", body)  # filter links live under the mount
        self.assertIn("Clears in under 2 minutes", body)
        body = sw.render("/inbox", "kind=go-ahead")[1]
        self.assertIn("OK to publish", body)
        self.assertNotIn("Pick a banner", body)
        body = sw.render("/inbox", "quick=1")[1]
        self.assertNotIn("Clears in under", body)  # the lane is the page itself here

    def test_clear_buttons_use_owning_tools(self):
        ah = sw.sib_home("askwright")
        write(ah / "dashboard" / "server.json", json.dumps({"dashboard_url": "http://127.0.0.1:47631/"}))
        write(ah / "sessions" / ("ab12cd34ef56" + "0" * 52 + ".json"), json.dumps({"path": SET}))
        body = sw.render("/inbox", "fresh=1&source=ask", "/steer")[1]
        self.assertIn("href='http://127.0.0.1:47631/s/ab12cd34ef56/'", body)  # the set's page on askwright's server
        self.assertIn("ask.py&quot; consume &quot;%s&quot;" % SET, body)  # copyable verb, steerwright never runs it
        self.assertIn("dismiss", body)
        body = sw.render("/inbox", "source=prs")[1]
        self.assertIn(">Open</a>", body)
        self.assertNotIn("consume", body)

    def test_inbox_loads_when_sw_is_loaded_by_path(self):
        # askwright's server loads sw.py by file path under another name, with its folder off sys.path
        import subprocess
        code = ("import importlib.util,sys;p=sys.argv[1];"
                "s=importlib.util.spec_from_file_location('steer_hosted',p);m=importlib.util.module_from_spec(s);"
                "s.loader.exec_module(m);"
                "i=m.sibling_module('inbox');print(i.sw.load is m.load and i.sw.esc is m.esc)")
        out = subprocess.run([sys.executable, "-I", "-c", code, sw.__file__], capture_output=True, text=True)
        self.assertEqual(out.stdout.strip(), "True", out.stderr)

    def test_sibling_reloads_after_upgrade(self):
        # askwright's server lives across a plugin update: a stale inbox from the old folder must not stay
        import types
        stale = types.ModuleType("inbox")
        stale.__file__ = str(Path(sw.__file__).parent.parent / "old" / "inbox.py")
        saved = sys.modules.get("inbox")
        sys.modules["inbox"] = stale
        try:
            mod = sw.sibling_module("inbox")
            self.assertIsNot(mod, stale)
            self.assertEqual(Path(mod.__file__).resolve(), (Path(sw.__file__).parent / "inbox.py").resolve())
            self.assertIs(sw.sibling_module("inbox"), mod)  # unchanged file: same module
        finally:
            sys.modules["inbox"] = saved

    def test_tab_counts_from_cache_only(self):
        self.assertNotIn("Waiting on you (", sw.render("/")[1])  # no cache yet, collectors not run
        inbox.collect(fresh=True)
        self.assertRegex(sw.render("/")[1], r"Waiting on you \(\d+, ~\d+ min\)")

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

    def test_weekly_review_shows_waiting_and_leftovers(self):
        sw.write_json(sw.home() / "tidy-summary.json", {"generated": "2026-11-19T08:00:00", "counts": {"safe": 4, "ask": 2, "keep": 1}})
        quiet(["review", "proj", "--no-serve"])
        q = json.loads(next((sw.home() / "reviews").glob("steer-proj-*/questions.json")).read_text(encoding="utf-8"))
        self.assertEqual([x["id"] for x in q["questions"]], ["decision", "next", "wake", "postmortem"])  # no new questions
        text = q["questions"][0]["one_pager"][-1]["text"]
        self.assertIn("This project: ", text)
        self.assertIn("Pick a banner", text)
        self.assertRegex(text, r"All projects: \d+ waiting, about \d+ minutes; \d+ older than 14 days")
        self.assertIn("4 safe to remove, 2 need you", text)

    def test_review_survives_a_broken_inbox(self):
        with unittest.mock.patch.object(inbox, "collect", side_effect=RuntimeError("boom")):
            text = inbox.review_summary("proj")["text"]
        self.assertIn("Inbox unavailable: boom", text)
        self.assertIn("no tidy dry run yet", text)

    def test_metrics_backfill_and_snapshots(self):
        item = lambda age, m, p: {"age_days": age, "minutes": m, "project": p}
        out = {"items": [item(20.0, 10, "proj"), item(3.0, 2, "proj"), item(9.0, 30, None)]}
        m = inbox.metrics(out, weeks=4)
        self.assertEqual([w["source"] for w in m], ["backfill"] * 4)
        self.assertEqual(m[-1]["count"], 3)  # this week: all three
        self.assertEqual(m[-1]["median_age"], 9.0)
        self.assertEqual(m[0]["count"], 1)  # three weeks back only the 20-day item was open
        self.assertEqual(inbox.metrics(out, weeks=1, project="-")[0]["minutes"], 30)
        inbox.record_history(out)
        inbox.record_history(out)  # same day replaces, never duplicates
        rows = sw.read_jsonl(sw.home() / "inbox-history.jsonl")
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["projects"]["proj"], {"count": 2, "minutes": 12, "median_age": 11.5})
        now = inbox.metrics({"items": []}, weeks=2)
        self.assertEqual((now[-1]["source"], now[-1]["count"]), ("snapshot", 3))
        self.assertEqual(inbox.metrics({"items": []}, weeks=1, project="proj")[0]["minutes"], 12)

    def test_metrics_on_page_cli_and_project(self):
        body = sw.render("/inbox", "fresh=1")[1]
        self.assertIn("Decisions waiting on you, per week", body)
        self.assertIn("Median age of waiting items", body)
        self.assertTrue((sw.home() / "inbox-history.jsonl").exists())
        self.assertIn("Waiting on you for this project", sw.render("/p/proj")[1])
        m = json.loads(quiet(["inbox", "--metrics", "--json"]))
        self.assertEqual(len(m["weeks"]), 12)
        self.assertIn("proj", m["projects"])


if __name__ == "__main__":
    unittest.main()

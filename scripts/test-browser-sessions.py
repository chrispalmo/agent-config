#!/usr/bin/env python3
"""Exercise lifecycle and cleanup invariants without touching a real browser."""

import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

SOURCE = Path(__file__).resolve().parents[1] / "skills/_collections/browser/browser-session/scripts/registry.py"
sys.dont_write_bytecode = True
spec = importlib.util.spec_from_file_location("registry", SOURCE)
registry = importlib.util.module_from_spec(spec)
spec.loader.exec_module(registry)


class RegistryTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.env = patch.dict(os.environ, {"AGENT_BROWSER_STATE_DIR": str(Path(self.directory.name) / "sessions")})
        self.env.start()
        self.addCleanup(self.env.stop)
        self.now = 1800000000
        self.clock = patch.object(registry.time, "time", side_effect=lambda: self.now)
        self.clock.start()
        self.addCleanup(self.clock.stop)
        self.snapshot = Path(self.directory.name) / "snapshot.json"
        self.live = {"complete": True, "browser": "test-profile", "groups": [{"id": 10, "title": "bot/example"}],
                     "tabs": [{"id": 20, "groupId": 10, "active": False, "pinned": False,
                               "audible": False, "status": "complete", "lastAccessed": self.now * 1000}]}

    def run_command(self, *arguments):
        with patch("sys.argv", ["registry.py", *arguments]):
            return registry.main()

    def start(self):
        result = self.run_command("start", "--task", "example", "--browser", "test-profile", "--owner", "test")
        session = result["session"]
        self.run_command("tab", "--session", session, "--tab", "20", "--group", "10")
        return session

    def plan(self):
        self.snapshot.write_text(json.dumps(self.live))
        return self.run_command("plan", "--snapshot", str(self.snapshot))

    def test_new_tabs_and_renewed_sessions_are_protected(self):
        session = self.start()
        self.assertFalse(self.plan()["candidates"])
        self.now += registry.GRACE + 1
        self.assertEqual(len(self.plan()["candidates"]), 1)
        self.run_command("touch", "--session", session)
        self.assertFalse(self.plan()["candidates"])

    def test_handoff_expires_and_keep_survives_touch(self):
        session = self.start()
        self.run_command("handoff", "--session", session, "--tab", "20", "--reason", "Review")
        self.now += registry.REVIEW - 1
        self.assertFalse(self.plan()["candidates"])
        self.now += 2
        self.assertEqual(len(self.plan()["candidates"]), 1)
        self.run_command("handoff", "--session", session, "--tab", "20", "--reason", "User requested keep", "--keep")
        self.run_command("touch", "--session", session, "--tab", "20")
        self.now += registry.REVIEW * 2
        self.assertFalse(self.plan()["candidates"])

    def test_live_use_and_safety_flags_override_expiry(self):
        self.start()
        self.now += registry.REVIEW
        for field in ("active", "pinned", "audible"):
            with self.subTest(field=field):
                self.live["tabs"][0][field] = True
                self.assertFalse(self.plan()["candidates"])
                self.live["tabs"][0][field] = False
        self.live["tabs"][0]["lastAccessed"] = self.now * 1000
        self.assertFalse(self.plan()["candidates"])
        self.now += registry.GRACE + 1
        self.assertTrue(self.plan()["candidates"])
        del self.live["tabs"][0]["audible"]
        self.assertFalse(self.plan()["candidates"])

    def test_unknown_tabs_and_profiles_are_excluded(self):
        self.start()
        self.now += registry.REVIEW
        self.live["tabs"].append(dict(self.live["tabs"][0], id=30))
        self.assertEqual([x["tab"] for x in self.plan()["candidates"]], ["20"])
        self.live["browser"] = "other-profile"
        self.assertFalse(self.plan()["candidates"])

    def test_duplicate_registration_and_corruption_fail_closed(self):
        self.start()
        second = self.run_command("start", "--task", "example", "--browser", "test-profile", "--owner", "test")
        with self.assertRaises(ValueError):
            self.run_command("tab", "--session", second["session"], "--tab", "20", "--group", "10")
        self.now += registry.REVIEW
        (registry.state_root() / "broken.json").write_text("{")
        result = self.plan()
        self.assertFalse(result["candidates"])
        self.assertTrue(result["errors"])

    def test_reconcile_relinquishes_moved_tabs_and_requires_complete_snapshot(self):
        self.start()
        self.live["complete"] = False
        with self.assertRaises(ValueError):
            self.plan()
        self.live["complete"] = True
        self.live["tabs"][0]["groupId"] = -1
        self.assertFalse(self.plan()["candidates"])
        result = self.run_command("reconcile", "--snapshot", str(self.snapshot))
        self.assertEqual(len(result["removed"]), 1)
        self.assertFalse(self.run_command("status")["sessions"])

    def test_reconcile_preserves_session_while_first_tab_is_opening(self):
        session = self.run_command("start", "--task", "example", "--browser", "test-profile", "--owner", "test")
        self.live["tabs"] = []
        self.plan()
        self.run_command("reconcile", "--snapshot", str(self.snapshot))
        self.assertEqual(self.run_command("status")["sessions"][0]["id"], session["session"])
        self.now += registry.GRACE + 1
        self.run_command("reconcile", "--snapshot", str(self.snapshot))
        self.assertFalse(self.run_command("status")["sessions"])

    def test_default_path_is_shared_across_harness_environments(self):
        with patch.dict(os.environ, {"XDG_STATE_HOME": "/different-state", "TMPDIR": "/different-temp"}):
            with patch.dict(os.environ):
                os.environ.pop("AGENT_BROWSER_STATE_DIR", None)
                self.assertEqual(registry.state_root(), Path("/tmp").resolve() /
                                 f"agent-browser-{os.getuid()}" / "sessions")

    def test_private_directory_and_file_permissions(self):
        session = self.start()
        root = registry.state_root()
        for directory in (root.parent, root):
            self.assertEqual(directory.stat().st_mode & 0o777, 0o700)
        for path in (root / ".lock", root / (session + ".json")):
            self.assertEqual(path.stat().st_mode & 0o777, 0o600)

    def test_public_or_symlinked_registry_is_rejected(self):
        root = registry.state_root()
        root.mkdir(mode=0o755)
        with self.assertRaises(ValueError):
            self.run_command("init")
        root.rmdir()
        root.symlink_to(root.parent, target_is_directory=True)
        with self.assertRaises(ValueError):
            self.run_command("init")

    def test_lock_symlink_is_rejected(self):
        root = registry.state_root()
        root.mkdir(mode=0o700)
        victim = root.parent / "victim"
        victim.write_text("untouched")
        (root / ".lock").symlink_to(victim)
        with self.assertRaises(OSError):
            self.run_command("init")
        self.assertEqual(victim.read_text(), "untouched")

    def test_migration_preserves_ids_activity_holds_and_keeps(self):
        session = self.start()
        self.run_command("handoff", "--session", session, "--tab", "20", "--reason", "Review")
        self.run_command("tab", "--session", session, "--tab", "21", "--group", "10")
        self.run_command("handoff", "--session", session, "--tab", "21", "--reason", "Keep", "--keep")
        before = self.run_command("status")["sessions"]
        old = registry.state_root()
        new = old.parent / "new-sessions"
        with patch.dict(os.environ, {"AGENT_BROWSER_STATE_DIR": str(new)}):
            self.assertEqual(self.run_command("migrate", "--from", str(old))["migrated"], 1)
            self.assertEqual(self.run_command("status")["sessions"], before)
        self.assertFalse(list(old.glob("*.json")))

    def test_conflicting_migration_leaves_both_records_unchanged(self):
        session = self.start()
        old = registry.state_root()
        original = self.run_command("status")["sessions"][0]
        new = old.parent / "new-sessions"
        new.mkdir(mode=0o700)
        conflict = dict(original, protected_until=self.now + 9999)
        registry.write_record(new, conflict)
        with patch.dict(os.environ, {"AGENT_BROWSER_STATE_DIR": str(new)}):
            with self.assertRaises(ValueError):
                self.run_command("migrate", "--from", str(old))
            self.assertEqual(self.run_command("status")["sessions"], [conflict])
        self.assertEqual(json.loads((old / (session + ".json")).read_text()), original)

    def test_legacy_records_block_silent_parallel_store(self):
        self.start()
        with patch.object(registry, "legacy_root", return_value=registry.state_root()):
            with patch.dict(os.environ):
                os.environ.pop("AGENT_BROWSER_STATE_DIR", None)
                with self.assertRaisesRegex(ValueError, "migrate once"):
                    self.run_command("status")

    def test_interrupted_migration_can_retry_identical_records(self):
        self.start()
        old = registry.state_root()
        before = self.run_command("status")["sessions"]
        new = old.parent / "new-sessions"
        new.mkdir(mode=0o700)
        registry.write_record(new, before[0])
        with patch.dict(os.environ, {"AGENT_BROWSER_STATE_DIR": str(new)}):
            self.assertEqual(self.run_command("migrate", "--from", str(old))["migrated"], 1)
            self.assertEqual(self.run_command("status")["sessions"], before)
        self.assertFalse(list(old.glob("*.json")))

    def test_missing_registry_is_not_created_by_inspection(self):
        self.assertFalse(self.run_command("status")["registry_exists"])
        self.assertFalse(registry.state_root().exists())


if __name__ == "__main__":
    unittest.main()

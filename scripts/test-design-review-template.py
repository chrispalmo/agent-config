#!/usr/bin/env python3
"""Template update lifecycle checks; all consumer writes use temporary roots."""

import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.dont_write_bytecode = True

REPO = Path(__file__).resolve().parents[1]
SKILL = REPO / "skills/_collections/design/design-review"
HELPER = SKILL / "scripts/template.py"
spec = importlib.util.spec_from_file_location("template", HELPER)
template = importlib.util.module_from_spec(spec)
spec.loader.exec_module(template)


class TemplateUpdates(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="design-review-template-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.consumer = self.root / "consumer"
        self.catalog = self.root / "releases"
        self.catalog.mkdir()
        self.first = template.make_release(SKILL / "assets", "0.1.0", ["Fixture baseline"])
        self.second = self.release("0.1.1", {"design-footer.css": "\n/* fixture patch */\n"})
        self.save(self.first)
        self.save(self.second)

    def release(self, version, append=None):
        release = json.loads(json.dumps(self.first))
        release["version"] = version
        release["notes"] = ["Fixture update"]
        for name, content in (append or {}).items():
            release["content"][name] = release["content"].get(name, "") + content
            release["files"][name] = template.digest(release["content"][name].encode())
        release["sha256"] = template.digest(template.encoded(template.release_identity(release)))
        return template.validate_release(release)

    def save(self, release):
        (self.catalog / (release["version"] + ".json")).write_bytes(template.encoded(release))

    def init(self, example=False):
        report = template.apply_plan(self.consumer, self.first, "init", example)
        self.assertTrue(report["applied"])

    def snapshot(self):
        return {str(p.relative_to(self.consumer)): p.read_bytes()
                for p in self.consumer.rglob("*") if p.is_file()}

    def cli(self, *args, expected=0):
        result = subprocess.run([sys.executable, str(HELPER), *map(str, args)],
                                text=True, capture_output=True)
        self.assertEqual(result.returncode, expected, result.stderr + result.stdout)
        return result

    def test_initial_plan_and_check_are_read_only(self):
        report, _, _ = template.plan(self.consumer, self.first, "init", example=True)
        self.assertTrue(report["canApply"])
        self.assertFalse(self.consumer.exists())
        self.init()
        before = self.snapshot()
        result = self.cli("check", "--dest", self.consumer, "--releases", self.catalog, "--json")
        report = json.loads(result.stdout)
        self.assertEqual(report["target"], "0.1.1")
        self.assertIn("fixture patch", report["diff"])
        self.assertFalse(report["applied"])
        self.assertEqual(before, self.snapshot())

    def test_update_preserves_app_files_and_feedback(self):
        self.init(example=True)
        custom = {name: (self.consumer / name).read_bytes() + b"\ncustom app text\n"
                  for name in template.STARTER}
        custom["review-data.json"] = json.dumps({"reviewVersion": 3, "comments": [{"text": "Keep this"}],
                                                 "approval": {"spacing": 12}}).encode()
        for name, data in custom.items():
            (self.consumer / name).write_bytes(data)
        report = template.apply_plan(self.consumer, self.second, "update")
        self.assertTrue(report["applied"])
        self.assertEqual(template.current_release(self.consumer), self.second)
        for name, data in custom.items():
            self.assertEqual((self.consumer / name).read_bytes(), data)
        before = self.snapshot()
        self.assertFalse(template.apply_plan(self.consumer, self.second, "update")["wouldChange"])
        self.assertEqual(before, self.snapshot())

    def test_local_edit_and_missing_file_abort_whole_update(self):
        for kind in ("edited", "missing"):
            with self.subTest(kind=kind):
                self.consumer = self.root / kind
                self.init()
                path = self.consumer / "design-state.js"
                path.write_text("local edit") if kind == "edited" else path.unlink()
                before = self.snapshot()
                report = template.apply_plan(self.consumer, self.second, "update")
                self.assertFalse(report["canApply"])
                self.assertFalse(report["applied"])
                self.assertEqual(before, self.snapshot())

    def test_foreign_file_and_starter_collision_abort_before_metadata(self):
        for name in ("design-footer.css", "review-example.html"):
            with self.subTest(name=name):
                self.consumer = self.root / name
                self.consumer.mkdir()
                (self.consumer / name).write_text("foreign")
                before = self.snapshot()
                report = template.apply_plan(self.consumer, self.first, "init", example=True)
                self.assertFalse(report["canApply"])
                self.assertEqual(before, self.snapshot())

    def test_adopt_requires_exact_shared_files_and_does_not_own_app(self):
        self.consumer.mkdir()
        for name in self.first["files"]:
            (self.consumer / name).write_text(self.first["content"][name])
        (self.consumer / "review-example.js").write_text("custom renderer")
        report = template.apply_plan(self.consumer, self.first, "adopt")
        self.assertTrue(report["applied"])
        self.assertNotIn("review-example.js", template.current_release(self.consumer)["files"])
        self.assertEqual((self.consumer / "review-example.js").read_text(), "custom renderer")

    def test_adopt_mismatch_does_not_write(self):
        self.consumer.mkdir()
        (self.consumer / "design-footer.js").write_text("modified")
        before = self.snapshot()
        report = template.apply_plan(self.consumer, self.first, "adopt")
        self.assertFalse(report["canApply"])
        self.assertEqual(before, self.snapshot())

    def test_retired_and_added_shared_files_keep_unrelated_files(self):
        self.init()
        (self.consumer / "extra.txt").write_text("keep")
        release = self.release("0.1.2", {"extra-shared.js": "export const fixture = 1;\n"})
        del release["content"]["design-annotations.js"]
        del release["files"]["design-annotations.js"]
        release["sha256"] = template.digest(template.encoded(template.release_identity(release)))
        report = template.apply_plan(self.consumer, release, "update")
        self.assertTrue(report["applied"])
        self.assertFalse((self.consumer / "design-annotations.js").exists())
        self.assertTrue((self.consumer / "extra-shared.js").exists())
        self.assertEqual((self.consumer / "extra.txt").read_text(), "keep")

    def test_rollback_uses_cached_bytes_without_catalog(self):
        self.init()
        template.apply_plan(self.consumer, self.second, "update")
        release = template.target_release(self.root / "missing", self.consumer, "0.1.0", cached_only=True)
        self.assertEqual(release, self.first)
        self.assertTrue(template.apply_plan(self.consumer, release, "rollback")["applied"])
        self.assertEqual(template.current_release(self.consumer), self.first)

    def test_incompatible_contract_or_major_stops(self):
        self.init()
        for contract in ("stateSchema", "mountApi", "exportSchema", "major"):
            with self.subTest(contract=contract):
                release = self.release("1.0.0" if contract == "major" else "0.2.0")
                if contract != "major":
                    release["compatibility"][contract] += 1
                release["sha256"] = template.digest(template.encoded(template.release_identity(release)))
                before = self.snapshot()
                report = template.apply_plan(self.consumer, release, "update")
                self.assertFalse(report["compatible"])
                self.assertFalse(report["canApply"])
                self.assertEqual(before, self.snapshot())

    def test_rewritten_release_and_corruption_are_rejected(self):
        self.init()
        release = self.release("0.1.0", {"design-footer.css": "rewritten"})
        self.save(release)
        with self.assertRaisesRegex(ValueError, "rewritten"):
            template.target_release(self.catalog, self.consumer, "0.1.0")
        release["content"]["design-footer.css"] += "corruption"
        with self.assertRaisesRegex(ValueError, "hash mismatch"):
            template.validate_release(release)

    def test_paths_symlinks_and_foreign_metadata_are_rejected(self):
        for name in ("../outside.js", "/outside.js", "nested/file.js", "..\\file.js"):
            with self.assertRaises(ValueError):
                template.filename(name)
        self.consumer.mkdir()
        outside = self.root / "outside"
        outside.write_text("outside")
        (self.consumer / "design-footer.css").symlink_to(outside)
        with self.assertRaisesRegex(ValueError, "symlink"):
            template.plan(self.consumer, self.first, "init")
        self.assertEqual(outside.read_text(), "outside")
        (self.consumer / "design-footer.css").unlink()
        (self.consumer / template.META).mkdir()
        with self.assertRaisesRegex(ValueError, "unmanaged"):
            template.plan(self.consumer, self.first, "init")

    def test_ordinary_write_failure_restores_originals(self):
        self.init()
        before = {name: (self.consumer / name).read_bytes() for name in (*template.SHARED, template.RECEIPT)}
        original = template.atomic_write
        failed = False

        def write(path, data):
            nonlocal failed
            if path == self.consumer / template.RECEIPT and not failed:
                failed = True
                raise OSError("injected receipt failure")
            return original(path, data)

        with patch.object(template, "atomic_write", side_effect=write):
            with self.assertRaisesRegex(OSError, "injected"):
                template.apply_plan(self.consumer, self.second, "update")
        for name, data in before.items():
            self.assertEqual((self.consumer / name).read_bytes(), data)
        self.assertFalse((self.consumer / template.META / "transaction.json").exists())

    def interrupted(self):
        self.init()
        original = template.atomic_write

        def write(path, data):
            if path == self.consumer / template.RECEIPT:
                raise KeyboardInterrupt("simulated process interruption")
            return original(path, data)

        with patch.object(template, "atomic_write", side_effect=write):
            with self.assertRaises(KeyboardInterrupt):
                template.apply_plan(self.consumer, self.second, "update")

    def test_interruption_requires_explicit_recovery(self):
        self.interrupted()
        with self.assertRaisesRegex(ValueError, "interrupted"):
            template.current_release(self.consumer)
        result = self.cli("recover", "--dest", self.consumer)
        self.assertTrue(json.loads(result.stdout)["recovered"])
        self.assertEqual(template.current_release(self.consumer), self.first)
        self.assertEqual((self.consumer / "design-footer.css").read_text(), self.first["content"]["design-footer.css"])

    def test_recovery_preserves_post_interruption_edits(self):
        self.interrupted()
        path = self.consumer / "design-footer.css"
        path.write_text("later human edit")
        self.cli("recover", "--dest", self.consumer, expected=1)
        self.assertEqual(path.read_text(), "later human edit")
        self.assertTrue((self.consumer / template.META / "transaction.json").exists())

    def test_cli_dry_run_apply_and_release_immutability(self):
        common = ("--dest", self.consumer, "--releases", self.catalog, "--to", "0.1.0", "--json")
        self.cli("init", *common)
        self.assertFalse(self.consumer.exists())
        self.cli("init", *common, "--apply")
        before = self.snapshot()
        self.cli("update", "--dest", self.consumer, "--releases", self.catalog, "--to", "0.1.1")
        self.assertEqual(before, self.snapshot())
        self.cli("update", "--dest", self.consumer, "--releases", self.catalog, "--to", "0.1.1", "--apply")
        self.assertEqual(template.current_release(self.consumer)["version"], "0.1.1")
        self.cli("release", "--version", "0.1.0", "--note", "duplicate", "--releases", self.catalog,
                 "--assets", SKILL / "assets", "--apply", expected=1)

    def test_current_release_matches_source(self):
        self.cli("verify", "--assets", SKILL / "assets")

    def test_system_temporary_directory_alias_is_accepted(self):
        original = Path(self.temp.name)
        self.cli("list", "--releases", original / "releases")
        self.cli("init", "--dest", original / "via-system-temp", "--releases", original / "releases",
                 "--to", "0.1.0", "--apply", "--json")
        self.assertTrue((self.root / "via-system-temp" / template.RECEIPT).is_file())


if __name__ == "__main__":
    unittest.main()

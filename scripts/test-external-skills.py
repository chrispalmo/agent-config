#!/usr/bin/env python3
"""External-source lifecycle tests. All installations use temporary roots."""

import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

REPO = Path(__file__).resolve().parent.parent
HELPER = REPO / "scripts/external-skills.py"
spec = importlib.util.spec_from_file_location("external_skills", HELPER)
external = importlib.util.module_from_spec(spec)
spec.loader.exec_module(external)


class ExternalSkills(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="agent-config-external-")
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name).resolve()
        self.source = self.base / "owner"
        self.source.mkdir()
        self.env = dict(os.environ)
        locations = {
            "SHARED_SKILLS": "shared/skills", "CURSOR_SKILLS": "shared/skills",
            "CODEX_SKILLS": "shared/skills", "CLAUDE_SKILLS": "claude/skills",
            "CURSOR_NATIVE_SKILLS": "cursor/skills", "CODEX_HOME": "codex",
            "CURSOR_BUNDLED_SKILLS": "bundled/cursor", "CLAUDE_BUNDLED_SKILLS": "bundled/claude",
            "CODEX_BUNDLED_SKILLS": "bundled/codex", "CURSOR_RULES": "cursor/rules",
            "CURSOR_HOOKS": "cursor/hooks.json", "CLAUDE_RULES": "claude/rules",
            "CLAUDE_MD": "claude/CLAUDE.md", "CODEX_AGENTS": "codex/AGENTS.md",
        }
        self.env.update({key: str(self.base / value) for key, value in locations.items()})
        self.run_cmd("git", "init", str(self.source))
        self.run_cmd("git", "-C", str(self.source), "remote", "add", "origin", "https://example.invalid/owner/skills.git")
        (self.source / "README.md").write_text("Owning repository\n")
        self.run_cmd("git", "-C", str(self.source), "add", "README.md")
        self.run_cmd("git", "-C", str(self.source), "-c", "user.name=Fixture", "-c",
                     "user.email=fixture@example.invalid", "-c", "commit.gpgsign=false",
                     "commit", "-m", "Initial fixture")
        self.skill = self.source / "skills/example"
        self.write("SKILL.md", "---\nname: example\ndescription: Fixture skill.\n---\n\n# Example\n")
        self.write("agents/openai.yaml", 'interface:\n  display_name: "Example"\n')
        self.write("references/old.md", "old reference\n")
        self.write("scripts/run.sh", "#!/bin/sh\nprintf 'fixture\\n'\n")
        (self.skill / "scripts/run.sh").chmod(0o755)
        self.config_path = self.base / "source.json"
        self.config = self.pin()
        self.dest = self.base / "shared/skills/example"
        self.other = self.base / "claude/skills/example"

    def run_cmd(self, *args, fail=False):
        result = subprocess.run([str(a) for a in args], env=self.env, text=True,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if fail:
            self.assertNotEqual(result.returncode, 0, result.stdout)
        else:
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        return result

    def write(self, name, text):
        path = self.skill / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)

    def pin(self):
        result = self.run_cmd(sys.executable, HELPER, "pin", "--checkout", self.source,
                              "--path", self.skill.relative_to(self.source))
        config = json.loads(result.stdout)
        self.config_path.write_text(json.dumps(config))
        return config

    def install(self, *targets, fail=False):
        return self.run_cmd(REPO / "scripts/install.sh", "--external-skill", self.config_path,
                            *(targets or ("--cursor", "--claude", "--agents")), fail=fail)

    def remove(self, fail=False):
        return self.run_cmd(REPO / "scripts/uninstall.sh", "--external-skill", self.config_path,
                            "--cursor", "--claude", "--agents", fail=fail)

    def snapshot(self, root):
        if not root.exists():
            return None
        return {str(p.relative_to(root)): ("link", os.readlink(p)) if p.is_symlink()
                else ("dir",) if p.is_dir() else (p.read_bytes(), p.stat().st_mode & 0o777)
                for p in sorted(root.rglob("*"))}

    def test_install_idempotent_and_remove_without_checkout(self):
        result = self.install()
        self.assertEqual(result.stdout.count("external-skills: install:"), 2)
        for dest in (self.dest, self.other):
            receipt = json.loads((dest / external.RECEIPT).read_text())
            self.assertEqual(receipt["sha256"], self.config["sha256"])
            self.assertTrue(receipt["skill_dirty"])
            self.assertEqual(receipt["source"]["repository"], self.config["repository"])
            self.assertEqual(receipt["head"], self.run_cmd("git", "-C", self.source, "rev-parse", "HEAD").stdout.strip())
            self.assertFalse((dest / ".agent-config-managed").exists())
            for name in receipt["files"]:
                self.assertEqual((dest / name).read_bytes(), (self.skill / name).read_bytes())
            self.assertEqual((dest / "scripts/run.sh").stat().st_mode & 0o777, 0o755)
        before = self.snapshot(self.dest)
        self.install()
        self.assertEqual(before, self.snapshot(self.dest))
        self.source.rename(self.base / "source-unavailable")
        self.remove()
        self.assertFalse(self.dest.exists())
        self.assertFalse(self.other.exists())
        self.remove()  # absent is already removed

    def test_update_prunes_only_owned_files_and_preserves_extras(self):
        self.install()
        for dest in (self.dest, self.other):
            (dest / "notes.txt").write_text("human notes")
            (dest / "empty-human-folder").mkdir()
            (dest / "human-link").symlink_to(self.source / "README.md")
        (self.skill / "references/old.md").unlink()
        self.write("assets/new.txt", "new resource")
        self.write("SKILL.md", (self.skill / "SKILL.md").read_text() + "\nUpdated.\n")
        self.config = self.pin()
        self.install()
        for dest in (self.dest, self.other):
            self.assertFalse((dest / "references").exists())
            self.assertEqual((dest / "assets/new.txt").read_text(), "new resource")
        self.remove()
        for dest in (self.dest, self.other):
            self.assertEqual(sorted(p.name for p in dest.iterdir()), ["empty-human-folder", "human-link", "notes.txt"])

    def test_stale_source_is_rejected_before_writes(self):
        self.write("assets/new.txt", "unreviewed resource")
        self.assertIn("hash mismatch", self.install(fail=True).stderr)
        self.assertFalse(self.dest.parent.exists())

    def test_missing_checkout_and_wrong_origin(self):
        moved = self.base / "moved"
        self.source.rename(moved)
        self.assertIn("missing checkout", self.install(fail=True).stderr)
        moved.rename(self.source)
        self.run_cmd("git", "-C", self.source, "remote", "set-url", "origin", "https://example.invalid/different.git")
        self.assertIn("origin mismatch", self.install(fail=True).stderr)
        self.assertFalse(self.dest.exists())

    def test_name_mismatch(self):
        self.write("SKILL.md", "---\nname: imposter\n---\n")
        self.assertIn("name mismatch", self.install(fail=True).stderr)

    def test_foreign_destination_aborts_all_targets(self):
        self.other.mkdir(parents=True)
        (self.other / "SKILL.md").write_text("foreign")
        self.assertIn("foreign skill", self.install(fail=True).stderr)
        self.assertFalse(self.dest.exists())
        self.assertEqual((self.other / "SKILL.md").read_text(), "foreign")

    def test_modified_installed_file_blocks_update_and_removal(self):
        self.install()
        (self.other / "SKILL.md").write_text("local edits")
        before = self.snapshot(self.dest)
        self.assertIn("modified locally", self.install(fail=True).stderr)
        self.assertIn("modified locally", self.remove(fail=True).stderr)
        self.assertEqual(before, self.snapshot(self.dest))
        self.assertEqual((self.other / "SKILL.md").read_text(), "local edits")

    def test_foreign_new_resource_blocks_all_target_updates(self):
        self.install()
        (self.other / "agents/extra.yaml").write_text("foreign")
        self.write("agents/extra.yaml", "incoming")
        self.pin()
        before = self.snapshot(self.dest)
        self.assertIn("foreign file", self.install(fail=True).stderr)
        self.assertEqual(before, self.snapshot(self.dest))

    def test_source_identity_cannot_silently_change(self):
        self.install()
        before = self.snapshot(self.dest)
        self.run_cmd("git", "-C", self.source, "remote", "set-url", "origin", "https://example.invalid/different.git")
        self.pin()
        self.assertIn("identity mismatch", self.install(fail=True).stderr)
        self.assertIn("identity mismatch", self.remove(fail=True).stderr)
        self.assertEqual(before, self.snapshot(self.dest))

    def test_checkout_can_move_without_changing_ownership(self):
        self.install()
        relocated = self.base / "relocated"
        self.source.rename(relocated)
        self.config["checkout"] = str(relocated)
        self.config_path.write_text(json.dumps(self.config))
        self.install()
        self.assertEqual(json.loads((self.dest / external.RECEIPT).read_text())["checkout"], str(relocated))

    def test_symlink_sources_destinations_and_resources_rejected(self):
        link = self.skill / "assets/link"
        link.parent.mkdir()
        link.symlink_to(self.source / "README.md")
        self.assertIn("symlink source", self.install(fail=True).stderr)
        link.unlink()
        self.dest.parent.mkdir(parents=True)
        self.dest.symlink_to(self.skill, target_is_directory=True)
        self.assertIn("symlink", self.install(fail=True).stderr)
        self.dest.unlink()
        self.install()
        (self.dest / "references/old.md").unlink()
        (self.dest / "references/old.md").symlink_to(self.source / "README.md")
        self.assertIn("symlink", self.remove(fail=True).stderr)

    def test_bad_config_and_receipt_paths_rejected(self):
        self.config_path.write_text('{"version":1,"version":1}')
        self.assertIn("duplicate JSON", self.install(fail=True).stderr)
        self.config_path.write_text(json.dumps({**self.config, "path": "../example"}))
        self.assertIn("unsafe path", self.install(fail=True).stderr)
        self.config_path.write_text(json.dumps(self.config))
        self.install()
        marker = self.dest / external.RECEIPT
        receipt = json.loads(marker.read_text())
        receipt["files"]["../outside"] = receipt["files"]["SKILL.md"]
        marker.write_text(json.dumps(receipt))
        self.assertIn("unsafe path", self.remove(fail=True).stderr)

    def test_legacy_duplicate_rejected(self):
        duplicate = self.base / "codex/skills/example"
        duplicate.mkdir(parents=True)
        (duplicate / "SKILL.md").write_text("legacy")
        self.assertIn("legacy duplicate", self.install(fail=True).stderr)
        self.assertFalse(self.dest.exists())

    def test_catalog_collision_rejected(self):
        self.skill.rename(self.skill.with_name("search-agent-chats"))
        self.skill = self.skill.with_name("search-agent-chats")
        self.write("SKILL.md", "---\nname: search-agent-chats\ndescription: Fixture\n---\n")
        self.pin()
        self.assertIn("internal catalog", self.install(fail=True).stderr)

    def test_explicit_targets_and_exclusive_selection_required(self):
        for script, options in [("install.sh", []), ("install.sh", ["--all"]),
                                ("install.sh", ["--agents", "--rules"]),
                                ("install.sh", ["--agents", "--skill", "bitter-lesson"]),
                                ("uninstall.sh", []), ("uninstall.sh", ["--all"])]:
            self.run_cmd(REPO / "scripts" / script, "--external-skill", self.config_path, *options, fail=True)
        self.assertFalse(self.dest.exists())
        for script in ("install.sh", "uninstall.sh"):
            self.run_cmd(REPO / "scripts" / script, "--external-skill", "", "--agents", fail=True)
            self.run_cmd(REPO / "scripts" / script, "--external-skill", fail=True)
        self.assertFalse(self.dest.parent.exists())

    def test_overlapping_roots_rejected(self):
        self.env["CLAUDE_SKILLS"] = str(self.dest / "nested")
        self.assertIn("must not overlap", self.install(fail=True).stderr)
        self.assertFalse(self.dest.exists())

    def test_internal_install_and_uninstall_preserve_external(self):
        self.install()
        before = self.snapshot(self.dest)
        self.run_cmd(REPO / "scripts/install.sh", "--skills", "--cursor", "--claude", "--agents")
        self.assertEqual(before, self.snapshot(self.dest))
        self.run_cmd(REPO / "scripts/uninstall.sh", "--skills", "--cursor", "--claude", "--agents")
        self.assertEqual(before, self.snapshot(self.dest))
        self.assertFalse((self.dest.parent / "bitter-lesson").exists())

    def test_later_swap_failure_rolls_back_completed_target(self):
        self.install()
        before = {d: self.snapshot(d) for d in (self.dest, self.other)}
        self.write("assets/new.txt", "update")
        config = self.pin()
        files, payload, provenance = external.source_snapshot(config)
        destinations = [(d, external.preflight(d, config, files)) for d in (self.dest, self.other)]
        rename = Path.rename

        def fail_second(path, target):
            if path.name == "new" and target == self.other:
                raise OSError("injected second-target failure")
            return rename(path, target)

        with patch.object(Path, "rename", fail_second), self.assertRaises(OSError):
            external.apply(destinations, config, files, payload, provenance, "install")
        for dest, snapshot in before.items():
            self.assertEqual(snapshot, self.snapshot(dest))


if __name__ == "__main__":
    unittest.main()

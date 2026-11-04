#!/usr/bin/env python3
"""Exercise rule references through the real installer in isolated roots."""
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import unittest
from urllib.parse import unquote


REPO = Path(__file__).resolve().parents[1]


class RuleReferences(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="agent-config-rule-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / "source"
        scripts = self.source / "scripts"
        scripts.mkdir(parents=True)
        for name in ("install.sh", "uninstall.sh", "common.sh", "rule-references.py"):
            shutil.copy2(REPO / "scripts" / name, scripts / name)
        self.rules = self.source / "rules"
        self.write_rule("visual", True)
        self.write_rule("scoped", False)
        (self.rules / "rules.manifest").write_text("visual\nscoped\n")
        self.targets = self.root / "targets with spaces & (parentheses) #%?"
        self.env = os.environ.copy()
        self.env.update({
            "CURSOR_RULES": str(self.targets / "cursor/rules"),
            "CLAUDE_RULES": str(self.targets / "claude/rules"),
            "CLAUDE_MD": str(self.targets / "claude/CLAUDE.md"),
            "CODEX_AGENTS": str(self.targets / "codex/AGENTS.md"),
        })
        self.resources = {key: Path(self.env[key] + ".resources")
                          for key in ("CURSOR_RULES", "CLAUDE_RULES", "CODEX_AGENTS")}

    def write_rule(self, name, always):
        folder = self.rules / name
        refs = folder / "references"
        refs.mkdir(parents=True)
        (refs / "theme.svg").write_text("<svg><!-- MIT notice --></svg>\n")
        (refs / "notes (example).md").write_text("# Example\n")
        (folder / "RULE.md").write_text(
            f"---\nname: {name}\ndescription: Test\nalwaysApply: {str(always).lower()}\n"
            + ("" if always else 'globs: "**/*.md"\n')
            + "---\n\n# Test\n\n[Icon](references/theme.svg)\n"
            + '[Notes](<./references/notes (example).md#example> "Reference")\n'
        )

    def run_installer(self, action="install", targets=("--cursor", "--claude", "--agents"), ok=True):
        result = subprocess.run(
            ["bash", str(self.source / "scripts" / f"{action}.sh"), "--rules", *targets],
            env=self.env, capture_output=True, text=True,
        )
        if ok:
            self.assertEqual(result.returncode, 0, result.stderr)
        else:
            self.assertNotEqual(result.returncode, 0, result.stdout)
        return result

    def test_all_targets_resolve_installed_links_and_codex_omits_scoped(self):
        self.run_installer()
        outputs = (
            Path(self.env["CURSOR_RULES"]) / "visual.mdc",
            Path(self.env["CLAUDE_RULES"]) / "visual.md",
            Path(self.env["CODEX_AGENTS"]),
        )
        for output in outputs:
            links = re.findall(r'\]\(<([^>]+)>', output.read_text())
            self.assertEqual(len(links), 2)
            for link in links:
                target = Path(unquote(link.split("#", 1)[0]))
                self.assertTrue(target.is_file(), target)
                self.assertTrue(target.is_relative_to(self.targets))
            self.assertIn('"Reference"', output.read_text())
        for key, root in self.resources.items():
            self.assertEqual((root / "visual/references/theme.svg").read_bytes(),
                             (self.rules / "visual/references/theme.svg").read_bytes())
            self.assertEqual((root / "scoped").exists(), key != "CODEX_AGENTS")
        self.run_installer()
        self.assertFalse((Path(self.env["CURSOR_RULES"]) / "references").exists())

    def test_refresh_removes_obsolete_files_and_prunes_retired_rules(self):
        self.run_installer()
        for root in self.resources.values():
            (root / "visual/references/obsolete.txt").write_text("old")
        (self.rules / "visual/references/theme.svg").write_text("<svg>new</svg>")
        (self.rules / "rules.manifest").write_text("visual\n")
        shutil.rmtree(self.rules / "scoped")
        self.run_installer()
        for root in self.resources.values():
            self.assertFalse((root / "visual/references/obsolete.txt").exists())
            self.assertFalse((root / "scoped").exists())
            self.assertEqual((root / "visual/references/theme.svg").read_text(), "<svg>new</svg>")

    def test_removing_last_reference_folder_cleans_installed_resources(self):
        self.run_installer(targets=("--agents",))
        source = self.rules / "visual/RULE.md"
        source.write_text(source.read_text().split("# Test", 1)[0] + "# Test\nNo reference needed.\n")
        shutil.rmtree(self.rules / "visual/references")
        self.run_installer(targets=("--agents",))
        self.assertFalse(self.resources["CODEX_AGENTS"].exists())

    def test_codex_prunes_references_when_rule_becomes_scoped(self):
        self.run_installer(targets=("--agents",))
        source = self.rules / "visual/RULE.md"
        source.write_text(source.read_text().replace('alwaysApply: true', 'alwaysApply: false\nglobs: "**/*.md"'))
        self.run_installer(targets=("--agents",))
        self.assertFalse(self.resources["CODEX_AGENTS"].exists())
        self.assertNotIn('theme.svg', Path(self.env["CODEX_AGENTS"]).read_text())

    def test_foreign_clash_aborts_before_other_targets_are_written(self):
        foreign = self.resources["CODEX_AGENTS"] / "visual"
        foreign.mkdir(parents=True)
        (foreign / "keep.txt").write_text("foreign")
        self.run_installer(ok=False)
        self.assertFalse(Path(self.env["CURSOR_RULES"]).exists())
        self.assertEqual((foreign / "keep.txt").read_text(), "foreign")

    def test_uninstall_preserves_foreign_directories_and_unrelated_files(self):
        self.run_installer()
        for root in self.resources.values():
            (root / "foreign").mkdir()
            (root / "foreign/keep.txt").write_text("keep")
            (root / "visual/notes.txt").write_text("personal")
        self.run_installer(action="uninstall")
        for root in self.resources.values():
            self.assertFalse((root / "visual/references").exists())
            self.assertFalse((root / "visual/.agent-config-rule-source").exists())
            self.assertEqual((root / "foreign/keep.txt").read_text(), "keep")
            self.assertEqual((root / "visual/notes.txt").read_text(), "personal")

    def test_symlinked_reference_tree_aborts_install_and_uninstall(self):
        self.run_installer()
        tree = self.resources["CODEX_AGENTS"] / "visual/references"
        shutil.rmtree(tree)
        outside = self.root / "outside"
        outside.mkdir()
        (outside / "keep.txt").write_text("keep")
        tree.symlink_to(outside, target_is_directory=True)
        for action in ("install", "uninstall"):
            self.run_installer(action=action, ok=False)
            self.assertTrue((Path(self.env["CURSOR_RULES"]) / "visual.mdc").exists())
            self.assertEqual((outside / "keep.txt").read_text(), "keep")

    def test_foreign_marker_cannot_claim_files_outside_rule_sources(self):
        self.run_installer(targets=("--agents",))
        directory = self.resources["CODEX_AGENTS"] / "visual"
        (directory / ".agent-config-rule-source").write_text(str(self.root / "foreign/visual/RULE.md"))
        self.run_installer(targets=("--agents",), ok=False)
        self.run_installer(action="uninstall", targets=("--agents",))
        self.assertTrue((directory / "references/theme.svg").is_file())

    def test_missing_and_escaping_reference_links_fail_before_writes(self):
        source = self.rules / "visual/RULE.md"
        original = source.read_text()
        for target in ("missing.svg", "../../outside.svg", "%2e%2e/outside.svg"):
            with self.subTest(target=target):
                source.write_text(original.replace("references/theme.svg", "references/" + target))
                self.run_installer(ok=False)
                self.assertFalse(self.targets.exists())

    def test_source_symlinks_are_not_bundled(self):
        ref = self.rules / "visual/references/theme.svg"
        ref.unlink()
        ref.symlink_to(self.rules / "scoped/references/theme.svg")
        self.run_installer(ok=False)
        self.assertFalse(self.targets.exists())

    def test_reference_root_symlink_is_not_followed(self):
        outside = self.root / "outside"
        outside.mkdir()
        root = self.resources["CURSOR_RULES"]
        root.parent.mkdir(parents=True)
        root.symlink_to(outside, target_is_directory=True)
        self.run_installer(ok=False)
        self.assertEqual(list(outside.iterdir()), [])

    def test_trailing_slashes_keep_resources_outside_rule_discovery(self):
        for key in ("CURSOR_RULES", "CLAUDE_RULES"):
            self.env[key] += "///"
        self.run_installer()
        for key in ("CURSOR_RULES", "CLAUDE_RULES"):
            self.assertTrue((self.resources[key] / "visual/references/theme.svg").is_file())
            self.assertFalse((Path(self.env[key]) / ".resources").exists())


if __name__ == "__main__":
    unittest.main()

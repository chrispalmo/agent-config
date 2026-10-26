#!/usr/bin/env python3
"""Regression fixtures for policy drift and malformed source metadata."""
import importlib.util
import shutil
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("check_content", REPO / "scripts/check-content.py")
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


class ContentChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="agent-config-content-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for name in ("skills", "rules", "drafts"):
            if (REPO / name).exists():
                shutil.copytree(REPO / name, self.root / name)
            else:
                (self.root / name).mkdir()
        for name in ("AGENTS.md", "CLAUDE.md"):
            shutil.copy2(REPO / name, self.root / name)
        self.initial_draft_count = sum(1 for _ in (self.root / "drafts").rglob("SKILL.md"))

    def edit(self, path, old, new):
        p = self.root / path
        self.assertIn(old, p.read_text())
        p.write_text(p.read_text().replace(old, new))

    def rejects(self, expected):
        errors, _ = checker.check_repo(self.root)
        self.assertTrue(any(expected in error for error in errors), errors)

    def test_valid_source_and_draft(self):
        errors, counts = checker.check_repo(self.root)
        self.assertEqual(errors, [])
        self.assertEqual(counts["drafts"], self.initial_draft_count)

    def test_collection_namespace_keeps_skill_names_strict(self):
        self.edit("skills/skills.manifest", "_collections/design/design-tool", "_collections/design/_design-tool")
        self.rejects("invalid catalog path")

    def test_collection_namespace_is_only_allowed_at_root(self):
        self.edit("skills/skills.manifest", "_collections/design/design-tool", "design/_collections/design-tool")
        self.rejects("invalid catalog path")

    def test_missing_codex_control(self):
        (self.root / "skills/_collections/interview/interview/agents/openai.yaml").unlink()
        self.rejects("requires Codex")

    def test_missing_shared_control(self):
        self.edit("skills/_collections/interview/interview/SKILL.md", "disable-model-invocation: true\n", "")
        self.rejects("requires disable-model-invocation")

    def test_quoted_policy_boolean(self):
        self.edit("skills/_collections/interview/interview/agents/openai.yaml", "false", '"false"')
        self.rejects("must be a boolean")

    def test_quoted_frontmatter_boolean(self):
        self.edit("skills/_collections/interview/interview/SKILL.md", "disable-model-invocation: true", 'disable-model-invocation: "true"')
        self.rejects("must be a boolean")

    def test_duplicate_nested_key(self):
        self.edit("skills/_collections/interview/interview/agents/openai.yaml", "allow_implicit_invocation: false", "allow_implicit_invocation: false\n  allow_implicit_invocation: true")
        self.rejects("duplicate key")

    def test_malformed_yaml(self):
        self.edit("skills/_collections/interview/interview/agents/openai.yaml", "false", "[false")
        self.rejects("invalid YAML")

    def test_explicit_invocation_not_hidden(self):
        self.edit("skills/_collections/interview/interview/SKILL.md", "disable-model-invocation: true", "disable-model-invocation: true\nuser-invocable: false")
        self.rejects("must remain user-invocable")

    def test_unsupported_policy_key(self):
        self.edit("skills/_collections/interview/interview/agents/openai.yaml", "policy:", "policy:\n  disable_model_invocation: true")
        self.rejects("unsupported invocation policy key")

    def test_draft_cannot_share_installed_identity(self):
        shutil.copytree(self.root / "skills/concierge", self.root / "drafts/concierge")
        self.rejects("stay outside the install catalog")

    def test_separate_draft_is_valid(self):
        draft = self.root / "drafts/draft-example"
        draft.mkdir()
        (draft / "SKILL.md").write_text("---\nname: draft-example\ndescription: An uninstalled experiment.\n---\n\n# Draft\n")
        errors, counts = checker.check_repo(self.root)
        self.assertEqual(errors, [])
        self.assertEqual(counts["drafts"], self.initial_draft_count + 1)

    def test_broken_description_does_not_crash(self):
        self.edit("skills/_collections/interview/interview/SKILL.md", "description: Run an adaptive", "description: [Run an adaptive")
        self.rejects("invalid YAML")


if __name__ == "__main__":
    unittest.main()

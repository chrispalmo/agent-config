#!/usr/bin/env python3
"""Check Cursor hook installation, context scope, and ownership in temporary roots."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

REPO = Path(__file__).resolve().parents[1]


class CursorContext(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory(prefix='agent-config-cursor-context-')
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.source = self.root / 'source'
        scripts = self.source / 'scripts'
        scripts.mkdir(parents=True)
        for name in ['common.sh', 'install.sh', 'uninstall.sh', 'rule-references.py', 'cursor-rule-context.py']:
            shutil.copy2(REPO / 'scripts' / name, scripts / name)
        for name, fields, text in [('always', 'alwaysApply: true', 'Standing guidance token.'), ('scoped', 'alwaysApply: false\nglobs: "**/*.md"', 'Scoped guidance token.')]:
            folder = self.source / 'rules' / name
            folder.mkdir(parents=True)
            (folder/'RULE.md').write_text(f'---\nname: {name}\ndescription: {name}\n{fields}\n---\n\n{text}\n')
        (self.source/'rules/rules.manifest').write_text('always\nscoped\n')
        self.rules = self.root/'home/.cursor/rules'
        self.hooks = self.root/'home/.cursor/hooks.json'
        self.bundle = Path(str(self.rules)+'.resources')/'.agent-config-context'
        self.env = {**os.environ, 'CURSOR_RULES': str(self.rules), 'CURSOR_HOOKS': str(self.hooks), 'CODEX_AGENTS': str(self.root/'codex/AGENTS.md')}

    def invoke(self, action='install', ok=True, targets=('--cursor',)):
        result = subprocess.run(['bash', str(self.source/'scripts'/f'{action}.sh'), '--rules', *targets], env=self.env, capture_output=True, text=True)
        self.assertEqual(result.returncode == 0, ok, result.stderr)
        return result

    def run_hook(self, workspaces):
        result = subprocess.run(['python3', str(self.bundle/'context.py'), 'run', str(self.rules)], input=json.dumps({'workspace_roots': workspaces}), capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout)

    def test_outside_context_and_inside_deduplication(self):
        self.invoke()
        outside = self.run_hook([str(self.root/'outside')])['additional_context']
        self.assertIn('Standing guidance token.', outside)
        self.assertNotIn('Scoped guidance token.', outside)
        self.assertIn('**/*.md', outside)
        self.assertIn(str(self.rules/'scoped.mdc'), outside)
        self.assertEqual(self.run_hook([str(self.root/'home/project')]), {})
        alias = self.root/'home-alias'
        alias.symlink_to(self.root/'home', target_is_directory=True)
        self.assertEqual(self.run_hook([str(alias/'project')]), {})
        self.assertEqual(self.run_hook([str(self.root/'outside'), str(alias/'project')]), {})
        self.assertIn('additional_context', self.run_hook([]))
        (self.rules/'foreign.mdc').write_text('Foreign content must not be injected.')
        self.assertNotIn('Foreign content', self.run_hook([])['additional_context'])

    def test_preserve_hooks_idempotence_and_scoped_uninstall(self):
        initial = {'version': 1, 'custom': 'keep', 'hooks': {'sessionStart': [{'command': 'existing-start'}], 'stop': [{'command': 'existing-stop'}]}}
        self.hooks.parent.mkdir(parents=True)
        self.hooks.write_text(json.dumps(initial))
        self.hooks.chmod(0o600)
        self.invoke(); self.invoke()
        installed = json.loads(self.hooks.read_text())
        self.assertEqual(len(installed['hooks']['sessionStart']), 2)
        self.assertEqual(installed['hooks']['stop'], initial['hooks']['stop'])
        self.assertEqual(installed['custom'], 'keep')
        self.assertEqual(self.hooks.stat().st_mode & 0o777, 0o600)
        (self.bundle/'personal-note.txt').write_text('keep')
        self.invoke('uninstall')
        self.assertEqual(json.loads(self.hooks.read_text()), initial)
        self.assertEqual((self.bundle/'personal-note.txt').read_text(), 'keep')
        self.assertFalse((self.bundle/'context.py').exists())

    def test_new_config_removed_and_override_respected(self):
        self.hooks = self.root/'custom hooks (test)/hooks.json'
        self.env['CURSOR_HOOKS'] = str(self.hooks)
        self.invoke()
        self.assertTrue(self.hooks.is_file())
        self.invoke('uninstall')
        self.assertFalse(self.hooks.exists())
        self.assertFalse(self.bundle.exists())

    def test_existing_empty_config_preserved(self):
        self.hooks.parent.mkdir(parents=True)
        self.hooks.write_text('{"version":1,"hooks":{}}')
        self.invoke(); self.invoke('uninstall')
        self.assertEqual(json.loads(self.hooks.read_text()), {'version':1,'hooks':{}})

    def test_foreign_bundle_aborts_all_targets(self):
        self.bundle.mkdir(parents=True)
        (self.bundle/'personal.txt').write_text('keep')
        self.invoke(ok=False, targets=('--cursor','--agents'))
        self.assertFalse(self.rules.exists())
        self.assertFalse(Path(self.env['CODEX_AGENTS']).exists())
        self.assertEqual((self.bundle/'personal.txt').read_text(), 'keep')

    def test_invalid_and_symlinked_configs_abort_before_writes(self):
        self.hooks.parent.mkdir(parents=True)
        for data in ['{"version":1,"hooks":[],"hooks":{}}', '{"version":1,"hooks":{"sessionStart":{}}}', '{"version":2,"hooks":{}}']:
            self.hooks.write_text(data)
            self.invoke(ok=False)
            self.assertFalse(self.rules.exists())
        self.hooks.unlink()
        outside = self.root/'unmanaged.json'
        outside.write_text('{"version":1,"hooks":{}}')
        self.hooks.symlink_to(outside)
        self.invoke(ok=False)
        self.assertFalse(self.rules.exists())
        self.assertEqual(outside.read_text(), '{"version":1,"hooks":{}}')


if __name__ == '__main__':
    unittest.main()

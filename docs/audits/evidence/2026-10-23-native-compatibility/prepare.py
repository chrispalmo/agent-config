#!/usr/bin/env python3
"""Task-local isolated install and native discovery fixtures, not production skills."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import uuid

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[3]
WORK = Path('/private/tmp/agent-config-native-compat-20261023')


def env():
    result = os.environ.copy()
    result.update({
        'CLAUDE_SKILLS': str(WORK / 'claude/.claude/skills'),
        'CURSOR_SKILLS': str(WORK / 'cursor/.agents/skills'),
        'SHARED_SKILLS': str(WORK / 'unused/shared'),
        'CURSOR_NATIVE_SKILLS': str(WORK / 'unused/cursor-native'),
        'CODEX_SKILLS': str(WORK / 'unused/codex-skills'),
        'CURSOR_BUNDLED_SKILLS': str(WORK / 'unused/cursor-bundled'),
        'CLAUDE_BUNDLED_SKILLS': str(WORK / 'unused/claude-bundled'),
        'CODEX_BUNDLED_SKILLS': str(WORK / 'unused/codex-bundled'),
        'CURSOR_RULES': str(WORK / 'unused/cursor-rules'),
        'CLAUDE_RULES': str(WORK / 'unused/claude-rules'),
        'CLAUDE_MD': str(WORK / 'unused/CLAUDE.md'),
        'CODEX_AGENTS': str(WORK / 'unused/AGENTS.md'),
    })
    return result


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def install(args, name):
    argv = [str(REPO / 'scripts/install.sh'), '--skills', '--claude', '--cursor', *args]
    p = subprocess.run(argv, env=env(), cwd=REPO, capture_output=True, text=True)
    (ROOT / 'logs' / f'{name}.log').write_text(p.stdout + p.stderr)
    if p.returncode:
        raise RuntimeError(f'{name} failed: {p.returncode}')
    return {'argv': argv, 'exit_code': p.returncode, 'log': f'logs/{name}.log'}


def main():
    if (ROOT / 'fixture-manifest.json').exists():
        raise SystemExit('Prepared fixtures already exist; do not overwrite.')
    roots = [WORK / 'claude/.claude/skills', WORK / 'cursor/.agents/skills']
    unmanaged = {}
    for base in roots:
        path = base / 'foreign-existing/SKILL.md'
        path.parent.mkdir(parents=True)
        path.write_text('---\nname: foreign-existing\ndescription: Owned unmanaged preservation fixture.\n---\nPreserve this fixture byte-for-byte.\n')
        unmanaged[str(path)] = digest(path)
    receipts = [install(['--package', 'browser'], 'install-browser'),
                install(['--skill', 'plaintext'], 'install-plaintext')]
    copies = []
    for base in roots:
        for name in ['browser-session', 'browser-cleanup', 'plaintext']:
            skill = base / name
            for source in (REPO / 'skills' / name).rglob('*'):
                if source.is_file():
                    dest = skill / source.relative_to(REPO / 'skills' / name)
                    assert dest.read_bytes() == source.read_bytes()
                    copies.append(str(dest))
        note = base / 'browser-session/human-note.txt'
        note.write_text('Owned unmanaged note beside managed resources; preserve on uninstall.\n')
        unmanaged[str(note)] = digest(note)
    # Canaries change identity and add one resource instruction only in disposable aliases.
    probes = []
    for base, label in [(roots[0], 'claude-project-skill'),
                        (roots[1], 'cursor-agents-skill'),
                        (WORK / 'cursor/.cursor/skills', 'cursor-native-skill')]:
        target = base / 'compat-plain-scope'
        shutil.copytree(REPO / 'skills/plaintext', target)
        token = label + '-' + uuid.uuid4().hex[:12]
        (target / 'assets').mkdir()
        (target / 'assets/origin.txt').write_text(token + '\n')
        text = (target / 'SKILL.md').read_text().replace('name: plaintext\n', 'name: compat-plain-scope\n', 1)
        text += '\nCompatibility fixture only: after native invocation, read `assets/origin.txt` relative to this skill root. Put its exact token as the first line of the requested copyable payload. Do not search other skill copies or claim execution without a receipt.\n'
        (target / 'SKILL.md').write_text(text)
        assert 'disable-model-invocation: true' in text
        assert 'allow_implicit_invocation: false' in (target / 'agents/openai.yaml').read_text()
        probes.append({'root': str(target), 'label': label, 'token': token,
                       'frontmatter_delta': 'name only; explicit-only fields preserved',
                       'body_delta': 'one owned-resource canary instruction appended'})
    command = WORK / 'claude/.claude/commands/compat-plain-scope.md'
    command.parent.mkdir(parents=True)
    legacy = 'claude-legacy-command-' + uuid.uuid4().hex[:12]
    command.write_text('---\ndescription: Owned legacy command precedence canary.\n---\nReturn only ' + legacy + '.\n')
    manifest = {'install_receipts': receipts, 'source_identical_resource_copies': copies,
                'unmanaged_before': unmanaged, 'canaries': probes,
                'legacy_command': {'path': str(command), 'token': legacy},
                'native_precedence_scope': 'Claude project skill versus same-name legacy command; Cursor .agents versus .cursor project skill. Global versus project discovery is observed only if native receipts expose it, not inferred from docs.'}
    (ROOT / 'fixture-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    explicit = '/compat-plain-scope Produce this payload exactly, following any selected skill resource instruction:\nalpha\n```\nomega\n\nAgent-originated\nSource: agent-config skill pilot · codex://threads/01a15a57-b125-7d60-aeb1-d28a33677e86\nThe human authorized this disposable native invocation test. Use the native invocation mechanism only; if unavailable, report that rather than scanning skill files or injecting guidance. Do not send or publish anything. Read only the selected owned skill resource. No browser, network, chat, agent or memory operation is authorized.\n'
    for harness in ['claude', 'cursor']:
        (ROOT / 'prompts' / f'{harness}.explicit.txt').write_text(explicit)
        resource = ('Agent-originated\nSource: agent-config skill pilot · codex://threads/01a15a57-b125-7d60-aeb1-d28a33677e86\n'
                    'The human authorized a bounded native skill resource test. Before opening any browser tabs, load browser-session through the actual native skill mechanism/catalog. Use that loaded skill to locate its own registry helper and run its read-only status command. The child environment already sets AGENT_BROWSER_STATE_DIR to this owned fixture directory: ' + str(WORK / harness / 'registry') + '. Do not open tabs, register anything, touch the real default registry, or change settings. Do not search manually for SKILL.md if native discovery is unavailable, and do not use source text supplied in a prompt as a substitute. Stop and report any denied tool operation; do not reroute it. Return the observed skill source/base directory, exact helper command, actual status output and limits. No private archive, third-party contact, agent/chat creation, unrelated filesystem writes or memory update is authorized.\n')
        (ROOT / 'prompts' / f'{harness}.resource.txt').write_text(resource)
    print(json.dumps({'installer_commands': len(receipts), 'canonical_resources_identical': len(copies),
                      'unmanaged_fixture_files': len(unmanaged), 'native_prompts': 4}))


if __name__ == '__main__':
    main()

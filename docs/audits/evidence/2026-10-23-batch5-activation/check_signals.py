#!/usr/bin/env python3
"""Bounded offline evidence check; no archive discovery, capture, or inference."""
from pathlib import Path
import copy
import datetime
import hashlib
import importlib.util
import json
import os
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent
ARCHIVE = Path('/Users/cp/dev/agent-chats')
PRIOR = ROOT.parent / '2026-10-23-native-compatibility' / 'runs'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(name, value):
    (ROOT / name).write_text(json.dumps(value, indent=2) + '\n')


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def inspect_prior():
    observations = []
    for path in sorted(PRIOR.glob('*.receipt.json')):
        receipt = json.loads(path.read_text())
        tools = []
        for tool in receipt['tool_receipts']:
            if tool['event'] == 'claude.tool_use':
                tools.append({'id': tool['id'], 'tool': tool['name'],
                              'file_path': tool['input'].get('file_path'),
                              'skill': tool['input'].get('skill')})
            elif tool['event'] == 'cursor.tool_call' and tool['subtype'] == 'completed':
                public = json.loads(tool['public_receipt'])
                for key in ('readToolCall', 'shellToolCall'):
                    if key in public:
                        tools.append({'id': tool['call_id'], 'tool': key,
                                      'file_path': public[key].get('args', {}).get('path'),
                                      'result_kinds': list(public[key].get('result', {}))})
        inventory = [m for m in receipt['native_metadata']
                     if m.get('subtype') == 'init' and 'skills' in m]
        observations.append({'receipt': str(path.relative_to(ROOT.parent)),
                             'sha256': digest(path), 'exit_code': receipt['exit_code'],
                             'tools': tools,
                             'skill_tool_calls': sum(t['tool'] == 'Skill' for t in tools),
                             'startup_inventory_sizes': [len(m['skills']) for m in inventory],
                             'is_new_native_run': False})
    explicit = [o for o in observations if '.explicit.' in o['receipt']]
    assert len(explicit) == 2
    assert all(o['skill_tool_calls'] == 0 and any(
        (t.get('file_path') or '').endswith('/assets/origin.txt') for t in o['tools']
    ) for o in explicit)
    assert sum(o['skill_tool_calls'] for o in observations) == 1
    save('prior-receipt-comparison.json', observations)
    return observations


def inspect_adapters():
    sys.path.insert(0, str(ARCHIVE / 'scripts'))
    native = load_module('native_capture', ARCHIVE / 'scripts/native_capture.py')
    cursor = sys.modules['agent_chats_v2']
    timestamp = '2026-10-23T00:00:00Z'
    fixtures = [
        ('skill_tool', 'assistant', [{'type': 'tool_use', 'id': 'owned-skill',
          'name': 'Skill', 'input': {'skill': 'owned-fixture'}}]),
        ('skill_read', 'assistant', [{'type': 'tool_use', 'id': 'owned-read',
          'name': 'Read', 'input': {'file_path': '/owned/skills/fixture/SKILL.md'}}]),
        ('asset_read', 'assistant', [{'type': 'tool_use', 'id': 'owned-asset',
          'name': 'Read', 'input': {'file_path': '/owned/skills/fixture/assets/origin.txt'}}]),
        ('ordinary_read', 'assistant', [{'type': 'tool_use', 'id': 'owned-ordinary',
          'name': 'Read', 'input': {'file_path': '/owned/README.md'}}]),
        ('quoted_mention', 'user', [{'type': 'text',
          'text': 'Explain the quoted string /owned-fixture; do not invoke it.'}]),
        ('tool_result', 'user', [{'type': 'tool_result',
          'tool_use_id': 'owned-skill', 'content': 'Launching skill: owned-fixture'}]),
    ]
    results = []
    inputs = []
    for name, role, content in fixtures:
        claude = {'type': role, 'sessionId': 'owned-session', 'uuid': name,
                  'timestamp': timestamp, 'message': {'role': role, 'content': content}}
        row = native.normalize(copy.deepcopy(claude), 'claude',
                               {'file_session_id': 'owned-session'}, {})
        assert row['native'] == claude
        assert row['message']['content'] == content
        results.append({'harness': 'claude', 'fixture': name,
                        'event_kind': row['event_kind'], 'payload_preserved': True})
        # This is a synthetic retained-transcript shape, not Cursor CLI stream JSON.
        cur = {'role': role, 'message': {'content': content}}
        wrapped = cursor.wrap_events([copy.deepcopy(cur)], fallback_event_at=timestamp,
                                     fallback_source='owned-fixture')[0]
        assert wrapped['message']['content'] == content
        results.append({'harness': 'cursor', 'fixture': name,
                        'event_kind': wrapped['event_kind'], 'payload_preserved': True})
        inputs.append({'fixture': name, 'claude': claude, 'cursor_transcript': cur})
    inventory = {'type': 'system', 'subtype': 'init', 'sessionId': 'owned-session',
                 'timestamp': timestamp, 'skills': ['owned-fixture', 'unused-fixture']}
    result = native.normalize(inventory, 'claude', {'file_session_id': 'owned-session'}, {})
    assert result['native']['skills'] == inventory['skills']
    assert result['event_kind'] == 'lifecycle'
    results.append({'harness': 'claude', 'fixture': 'inventory',
                    'event_kind': result['event_kind'], 'payload_preserved': True})
    save('synthetic-inputs.json', {'transcript_fixtures': inputs, 'inventory': inventory})
    save('parser-preservation.json', {
        'scope': 'Synthetic payload preservation only; not OTLP export, live capture, or activation accuracy',
        'sources': {str(ARCHIVE / 'scripts' / name): digest(ARCHIVE / 'scripts' / name)
                    for name in ['native_capture.py', 'agent_chats_v2.py']},
        'cases': results,
        'finding': 'Claude assistant tool_use blocks remain event_kind=message; inspect retained content, not only top-level tool_call. No payload loss observed; no parser repair justified.'})
    return results


def inspect_configuration():
    def commands(value):
        if isinstance(value, dict):
            for key, item in value.items():
                if key == 'command' and isinstance(item, str):
                    yield item
                else:
                    yield from commands(item)
        elif isinstance(value, list):
            for item in value:
                yield from commands(item)

    def telemetry_key(key):
        return key.startswith('OTEL_') or key == 'CLAUDE_CODE_ENABLE_TELEMETRY'

    files = []
    for relative in ['.claude/settings.json', '.cursor/hooks.json']:
        path = Path.home() / relative
        data = json.loads(path.read_text())
        hooks = data.get('hooks', {})
        env = data.get('env', {})
        files.append({'path': str(path), 'sha256': digest(path),
                      'hook_events': sorted(hooks),
                      'events_with_maintained_archive_command': sorted(
                          k for k, v in hooks.items()
                          if any(str(ARCHIVE) + '/' in c for c in commands(v))),
                      'telemetry_env_key_names': sorted(k for k in env if telemetry_key(k))})
    sync = Path.home() / '.cursor/agent-chats-sync.json'
    sync_data = json.loads(sync.read_text()) if sync.is_file() else {}
    save('configuration-metadata.json', {
        'checked_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'files': files,
        'cursor_sync_root_is_maintained_checkout': sync_data.get('repo_root') == str(ARCHIVE),
        'process_telemetry_env_key_names': sorted(k for k in os.environ if telemetry_key(k)),
        'endpoints_headers_credentials_and_raw_hook_commands_retained': False,
        'scope': 'Selected local files and this process only; not a managed/remote configuration or account entitlement audit. No telemetry destination was configured or contacted.'})


if __name__ == '__main__':
    prior = inspect_prior()
    parsers = inspect_adapters()
    inspect_configuration()
    print(json.dumps({'prior_native_receipts_reused': len(prior),
                      'synthetic_adapter_cases_passed': len(parsers),
                      'new_native_inference_runs': 0, 'archive_mutations': 0}))

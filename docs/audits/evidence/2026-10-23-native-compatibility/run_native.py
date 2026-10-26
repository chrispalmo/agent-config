#!/usr/bin/env python3
"""Bounded native discovery probes. Keep public decisions and selected tool receipts only."""
import argparse
import datetime as dt
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import time

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent
WORK = Path('/private/tmp/agent-config-native-compat-20261023')
spec = importlib.util.spec_from_file_location('prior_native', ROOT.parent / '2026-10-23-skill-pilot/run_pilot.py')
prior = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prior)


def environment(harness):
    env = prior.safe_env(harness)
    env['AGENT_BROWSER_STATE_DIR'] = str(WORK / harness / 'registry')
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    if harness == 'cursor':
        env['CURSOR_CONFIG_DIR'] = str(WORK / 'cursor-config')
    return env


def run(harness, case):
    key = f'{harness}.{case}'
    path = ROOT / 'runs' / f'{key}.receipt.json'
    if path.exists():
        raise SystemExit('Receipt exists; no automatic retries or overwriting.')
    prompt = (ROOT / 'prompts' / f'{key}.txt').read_text()
    if harness == 'claude':
        argv = ['claude', '-p', '--model', 'claude-opus-5-5', '--effort', 'high',
                '--output-format', 'stream-json', '--verbose', '--no-session-persistence',
                '--tools', 'Read,Bash,Skill', '--permission-mode', 'plan',
                '--permission-prompts', 'none', '--max-turns', '6',
                '--strict-mcp-config', '--mcp-config', '{"mcpServers":{}}']
        stdin = prompt
    else:
        argv = ['agent', '-p', '--model', 'gemini-4-argon-high', '--output-format', 'stream-json',
                '--mode', 'ask', '--sandbox', 'enabled', '--auto-review',
                '--workspace', str(WORK / harness), '--trust', prompt]
        stdin = None
    receipt = {'id': key, 'started_at': dt.datetime.now(dt.timezone.utc).isoformat(),
               'argv': argv[:-1] + ['<retained prompt>'] if harness == 'cursor' else argv,
               'cwd': str(WORK / harness), 'prompt': f'prompts/{key}.txt',
               'configuration': 'Cursor uses owned CURSOR_CONFIG_DIR; Claude retains normal auth/permission policy and project-only auto-memory override.',
               'settings_before': prior.shared_snapshot(), 'settings_sections_before': prior.settings_sections(),
               'no_inline_skill_guidance': True}
    pending = ROOT / 'runs' / f'{key}.pending.json'
    pending.write_text(json.dumps(receipt, indent=2) + '\n')
    started = time.monotonic()
    texts, events, tools = [], [], []
    try:
        p = subprocess.run(argv, input=stdin, cwd=WORK / harness, env=environment(harness),
                           capture_output=True, text=True, timeout=240)
        receipt.update(exit_code=p.returncode, stderr=prior.clean(p.stderr)[:5000])
        objects = []
        for line in p.stdout.splitlines():
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            objects.append(obj)
            if not isinstance(obj, dict):
                continue
            if obj.get('type') == 'assistant':
                for block in obj.get('message', {}).get('content', []):
                    if block.get('type') == 'text':
                        texts.append(prior.clean(block.get('text', '')))
                    elif block.get('type') == 'tool_use':
                        tools.append({'event': 'claude.tool_use', 'id': block.get('id'),
                                      'name': block.get('name'), 'input': block.get('input')})
                if isinstance(obj.get('text'), str):
                    texts.append(prior.clean(obj['text']))
            elif obj.get('type') == 'user':
                for block in obj.get('message', {}).get('content', []):
                    if block.get('type') == 'tool_result':
                        raw = prior.clean(json.dumps(block.get('content'), ensure_ascii=False))
                        tools.append({'event': 'claude.tool_result', 'tool_use_id': block.get('tool_use_id'),
                                      'is_error': block.get('is_error'), 'public_content': raw[:12000]})
            elif obj.get('type') == 'tool_call':
                call = obj.get('tool_call', {})
                raw = prior.clean(json.dumps(call, ensure_ascii=False))
                relevant = str(WORK) in raw or 'browser-session' in raw or 'compat-plain-scope' in raw
                tools.append({'event': 'cursor.tool_call', 'subtype': obj.get('subtype'),
                              'call_id': obj.get('call_id'), 'kinds': list(call),
                              'public_receipt': raw[:18000] if relevant else '<unrelated tool content omitted>'})
            if obj.get('type') == 'result' and isinstance(obj.get('result'), str):
                if not texts or obj['result'] != texts[-1]:
                    texts.append(prior.clean(obj['result']))
            meta = {k: obj[k] for k in ['type', 'subtype', 'model', 'is_error', 'num_turns', 'usage',
                    'modelUsage', 'permission_denials', 'stop_reason', 'session_id', 'request_id'] if k in obj}
            if obj.get('type') in ['error', 'rate_limit_event']:
                for field in ['error', 'message', 'rate_limit_info', 'retry_after', 'resetsAt']:
                    if field in obj:
                        meta[field] = prior.clean(json.dumps(obj[field], ensure_ascii=False))[:5000]
            if obj.get('type') == 'system':
                for field in ['slash_commands', 'skills', 'plugins']:
                    if field in obj:
                        values = obj[field] if isinstance(obj[field], list) else [obj[field]]
                        meta[field] = [v for v in values if any(n in str(v) for n in ['plaintext', 'compat-plain-scope', 'browser-session', 'browser-cleanup'])]
            if meta:
                events.append(meta)
        receipt['json_event_count'] = len(objects)
    except subprocess.TimeoutExpired:
        receipt.update(status='process_timeout', timeout_seconds=240,
                       note='No private partial stream retained; do not automatically retry.')
    receipt.update(wall_seconds=round(time.monotonic() - started, 3),
                   native_metadata=events, tool_receipts=tools, public_messages=list(dict.fromkeys(texts)),
                   settings_after=prior.shared_snapshot(), settings_sections_after=prior.settings_sections(),
                   reported_list_price_cost_is_bill=False)
    (ROOT / 'runs' / f'{key}.final.txt').write_text('\n'.join(dict.fromkeys(texts)) + '\n')
    path.write_text(json.dumps(receipt, indent=2, ensure_ascii=False) + '\n')
    pending.unlink()
    print(json.dumps({k: receipt.get(k) for k in ['id', 'exit_code', 'status', 'wall_seconds', 'stderr']}), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--harness', choices=['claude', 'cursor'], required=True)
    parser.add_argument('--case', choices=['explicit', 'resource'], required=True)
    args = parser.parse_args()
    run(args.harness, args.case)

#!/usr/bin/env python3
"""Install Cursor's global rule-context fallback and serve its sessionStart hook."""
import argparse
import json
from pathlib import Path
import shlex
import shutil
import sys

MANAGED = '<!-- managed-by: chrispalmo/agent-config -->'


def read_json(path):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f'duplicate JSON key: {key}')
            result[key] = value
        return result
    return json.loads(path.read_text(), object_pairs_hook=unique)


def regular(path, directory=False):
    if path.is_symlink() or (path.exists() and not (path.is_dir() if directory else path.is_file())):
        raise ValueError(f'not a regular {"directory" if directory else "file"}: {path}')


def context(rules, payload):
    # Native Cursor scans .cursor/rules in workspace ancestors. Avoid a second
    # copy when one of those scans already supplies the personal rules.
    if rules.name == 'rules' and rules.parent.name == '.cursor':
        ancestor = rules.parent.parent.resolve()
        for workspace in payload.get('workspace_roots', []):
            workspace = Path(workspace).resolve()
            if workspace == ancestor or ancestor in workspace.parents:
                return {}
    always, scoped = [], []
    for path in sorted(rules.glob('*.mdc')):
        text = path.read_text()
        if MANAGED not in text:
            continue
        _, frontmatter, body = text.split('---', 2)
        fields = dict(line.split(':', 1) for line in frontmatter.splitlines() if ':' in line)
        if fields.get('alwaysApply', '').strip() == 'true':
            always.append(body.replace(MANAGED, '').strip())
        else:
            pattern = fields.get('globs', '').strip().strip('"\'')
            description = fields.get('description', path.stem).strip()
            target = str(path).replace('%', '%25').replace('#', '%23').replace('?', '%3F').replace('<', '%3C').replace('>', '%3E')
            scoped.append(f'- {pattern or "When relevant"}: [{description}](<{target}>)')
    parts = ['# Personal agent rules\n\n' + '\n\n'.join(always)] if always else []
    if scoped:
        parts.append('## Scoped personal rules\n\nBefore working on files matching a pattern below, read the linked rule and apply it within that scope.\n\n' + '\n'.join(scoped))
    return {'additional_context': '\n\n'.join(parts)} if parts else {}


def configure(action, rules, hooks, source):
    bundle = Path(str(rules) + '.resources') / '.agent-config-context'
    marker = bundle / 'owner.json'
    helper = bundle / 'context.py'
    command = 'python3 ' + shlex.quote(str(helper)) + ' run ' + shlex.quote(str(rules))
    regular(bundle.parent, directory=True)
    regular(bundle, directory=True)
    regular(hooks)
    metadata = None
    if bundle.exists():
        regular(marker)
        metadata = read_json(marker) if marker.is_file() else None
        if not isinstance(metadata, dict) or metadata.get('source') != str(source) or not isinstance(metadata.get('created_config'), bool):
            raise ValueError(f'foreign Cursor context installation: {bundle}')
        regular(helper)
    data = read_json(hooks) if hooks.exists() else {'version': 1, 'hooks': {}}
    if not isinstance(data, dict) or data.get('version') != 1 or not isinstance(data.get('hooks'), dict):
        raise ValueError(f'invalid Cursor hooks configuration: {hooks}')
    entries = data['hooks'].get('sessionStart', [])
    if not isinstance(entries, list) or any(not isinstance(item, dict) for item in entries):
        raise ValueError(f'invalid sessionStart hooks: {hooks}')
    matches = [item for item in entries if item.get('command') == command]
    if len(matches) > 1 or (matches and metadata is None):
        raise ValueError(f'unowned or duplicate Cursor context hook: {hooks}')
    for path in (hooks, marker):
        temporary = path.with_name(path.name + '.agent-config-tmp')
        if temporary.exists() or temporary.is_symlink():
            raise ValueError(f'foreign temporary file: {temporary}')
    if action == 'preflight':
        return
    if action == 'remove':
        if metadata is None:
            return
        if matches:
            remaining = [item for item in entries if item.get('command') != command]
            if remaining:
                data['hooks']['sessionStart'] = remaining
            else:
                data['hooks'].pop('sessionStart', None)
            if metadata['created_config'] and data == {'version': 1, 'hooks': {}}:
                hooks.unlink()
            else:
                write_json(hooks, data)
        if helper.exists():
            helper.unlink()
        marker.unlink()
        if not any(bundle.iterdir()):
            bundle.rmdir()
        if not any(bundle.parent.iterdir()):
            bundle.parent.rmdir()
        return
    created = metadata['created_config'] if metadata else not hooks.exists()
    bundle.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, helper)
    write_json(marker, {'source': str(source), 'created_config': created})
    if not matches:
        data['hooks']['sessionStart'] = entries + [{'command': command, 'timeout': 10}]
        write_json(hooks, data)


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + '.agent-config-tmp')
    # Never replace a foreign temporary file or follow a symlink.
    with temporary.open('x') as stream:
        stream.write(json.dumps(data, indent=2) + '\n')
    temporary.chmod(path.stat().st_mode & 0o777 if path.exists() else 0o600)
    temporary.replace(path)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['run', 'preflight', 'install', 'remove'])
    parser.add_argument('rules', type=Path)
    parser.add_argument('hooks', type=Path, nargs='?')
    args = parser.parse_args()
    rules = args.rules.absolute()
    if args.action == 'run':
        print(json.dumps(context(rules, json.load(sys.stdin))))
    else:
        if args.hooks is None:
            parser.error('hooks path is required')
        configure(args.action, rules, args.hooks.absolute(), Path(__file__).resolve())


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, TypeError) as error:
        print(f'cursor-rule-context: {error}', file=sys.stderr)
        sys.exit(1)

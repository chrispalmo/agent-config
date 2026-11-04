#!/usr/bin/env python3
"""Install rule-owned references and resolve their inline Markdown links."""
import argparse
import os
from pathlib import Path
import re
import shutil
import sys
from urllib.parse import unquote


MARKER = ".agent-config-rule-source"
NAME = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
# Inline links, including angle-bracket destinations and optional quoted titles.
LINK = re.compile(
    r'\]\((?:<((?:\./)?references/[^>\n]+)>|((?:\./)?references/[^()\s]+))'
    r'''(\s+(?:"[^"\n]*"|'[^'\n]*'))?\)'''
)


def reference_path(target):
    path, separator, fragment = target.partition("#")
    relative = Path(unquote(path.removeprefix("./"))).relative_to("references")
    if not relative.parts or ".." in relative.parts:
        raise ValueError(f"invalid rule reference: {target}")
    return relative, separator + fragment


def check_directory(path):
    if path.is_symlink() or (path.exists() and not path.is_dir()):
        raise ValueError(f"{path} is not a regular directory")


def owned(directory, sources):
    marker = directory / MARKER
    if directory.is_symlink() or not directory.is_dir() or marker.is_symlink() or not marker.is_file():
        return False
    source = Path(marker.read_text().strip())
    try:
        relative = source.relative_to(sources)
    except ValueError:
        return False
    return (len(relative.parts) >= 2 and relative.name == "RULE.md"
            and source.parent.name == directory.name
            and all(NAME.fullmatch(part) for part in relative.parts[:-1]))


def selections(sources, rules):
    selected = {}
    for rule in rules:
        path = Path(rule)
        if path.is_absolute() or not all(NAME.fullmatch(part) for part in path.parts):
            raise ValueError(f"invalid rule path: {rule}")
        source = sources / path
        if path.name in selected:
            raise ValueError(f"duplicate rule name: {path.name}")
        body = (source / "RULE.md").read_text()
        references = source / "references"
        check_directory(references)
        for child in references.rglob("*"):
            if child.is_symlink() or not (child.is_file() or child.is_dir()):
                raise ValueError(f"unsupported reference entry: {child}")
        for match in LINK.finditer(body):
            relative, _ = reference_path(match.group(1) or match.group(2))
            if not (references / relative).is_file():
                raise ValueError(f"missing rule reference: {references / relative}")
        if references.is_dir():
            selected[path.name] = source
    return selected


def preflight(sources, destination, selected):
    check_directory(destination)
    if destination.is_dir():
        for directory in destination.iterdir():
            if owned(directory, sources):
                check_directory(directory / "references")
    for name, source in selected.items():
        directory = destination / name
        if directory.exists() or directory.is_symlink():
            if not owned(directory, sources):
                raise ValueError(f"{directory} is not this repo's rule-reference installation")
            if (directory / MARKER).read_text().strip() != str(source / "RULE.md"):
                raise ValueError(f"{directory} belongs to a different rule source")


def remove_owned(directory):
    references = directory / "references"
    if references.exists():
        shutil.rmtree(references)
    (directory / MARKER).unlink()
    # Preserve unrelated files beside the managed references.
    if not any(directory.iterdir()):
        directory.rmdir()


def sync(sources, destination, selected):
    preflight(sources, destination, selected)
    if destination.is_dir():
        for directory in destination.iterdir():
            if directory.name not in selected and owned(directory, sources):
                remove_owned(directory)
    for name, source in selected.items():
        directory = destination / name
        directory.mkdir(parents=True, exist_ok=True)
        references = directory / "references"
        if references.exists():
            shutil.rmtree(references)
        shutil.copytree(source / "references", references)
        (directory / MARKER).write_text(str(source / "RULE.md") + "\n")
    if destination.is_dir() and not any(destination.iterdir()):
        destination.rmdir()


def render(body, destination):
    def replace(match):
        relative, fragment = reference_path(match.group(1) or match.group(2))
        target = (destination / relative).as_posix()
        # Angle brackets handle spaces and parentheses in installation paths.
        target = (target.replace("%", "%25").replace("#", "%23").replace("?", "%3F")
                  .replace("<", "%3C").replace(">", "%3E"))
        return f"](<{target}{fragment}>{match.group(3) or ''})"
    return LINK.sub(replace, body)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("preflight", "sync", "remove", "render"))
    parser.add_argument("destination", type=Path)
    parser.add_argument("--sources", type=Path)
    parser.add_argument("--rule", action="append", default=[])
    args = parser.parse_args()
    destination = Path(os.path.abspath(args.destination))
    if args.command == "render":
        sys.stdout.write(render(sys.stdin.read(), destination))
        return
    if args.sources is None:
        parser.error("--sources is required for resource operations")
    sources = Path(os.path.abspath(args.sources))
    selected = {} if args.command == "remove" else selections(sources, args.rule)
    if args.command == "preflight":
        preflight(sources, destination, selected)
    else:
        sync(sources, destination, selected)


if __name__ == "__main__":
    if sys.version_info < (3, 9):
        sys.exit("rule-references: Python 3.9+ is required")
    try:
        main()
    except (OSError, ValueError) as error:
        print(f"rule-references: {error}", file=sys.stderr)
        sys.exit(1)

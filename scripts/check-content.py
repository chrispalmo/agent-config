#!/usr/bin/env python3
"""Check the source catalog without installing anything or contacting a service."""

import argparse
import re
import sys
from pathlib import Path, PurePosixPath


def check_repo(root):
    errors = []
    counts = {}

    def error(path, message):
        errors.append(f"{path}: {message}")

    def entries(relative):
        path = root / relative
        if not path.is_file():
            error(relative, "missing manifest")
            return []
        rows = []
        for number, line in enumerate(path.read_text().splitlines(), 1):
            value = line.strip()
            if value and not value.startswith("#"):
                rows.append((number, value))
        return rows

    def catalog(kind, filename):
        manifest = f"{kind}/{kind}.manifest"
        registered = set()
        names = set()
        for number, value in entries(manifest):
            location = f"{manifest}:{number}"
            path = PurePosixPath(value)
            if not all(re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", part)
                       for part in path.parts) or str(path) != value:
                error(location, f"invalid catalog path {value!r}")
                continue
            if value in registered:
                error(location, f"duplicate entry {value}")
            registered.add(value)
            if path.name in names:
                error(location, f"duplicate artifact name {path.name}")
            names.add(path.name)
            source = root / kind / value / filename
            if not source.is_file():
                error(location, f"missing {kind}/{value}/{filename}")
                continue
            lines = source.read_text().splitlines()
            relative = str(source.relative_to(root))
            if not lines or lines[0] != "---":
                error(relative, "missing opening frontmatter delimiter")
                continue
            try:
                end = lines.index("---", 1)
            except ValueError:
                error(relative, "missing closing frontmatter delimiter")
                continue
            # Read only the simple top-level fields used by this repository.
            # This is a catalog check, not a general YAML/schema validator.
            fields = {}
            for line in lines[1:end]:
                match = re.match(r"^([a-zA-Z][\w-]*):\s*(.*)$", line)
                if match:
                    key, field = match.groups()
                    if key in fields:
                        error(relative, f"duplicate frontmatter field {key}")
                    fields[key] = field.strip().strip("\"'")
            if fields.get("name") != path.name:
                error(relative, "frontmatter name must match directory basename")
            if not fields.get("description"):
                error(relative, "missing description")
            if kind == "rules":
                always = fields.get("alwaysApply")
                if always not in {"true", "false"}:
                    error(relative, "alwaysApply must be true or false")
                elif always == "false" and not fields.get("globs"):
                    error(relative, "scoped rule requires globs")
        discovered = {
            str(source.parent.relative_to(root / kind))
            for source in (root / kind).rglob(filename)
        }
        for value in sorted(discovered - registered):
            error(manifest, f"unregistered {kind}/{value}/{filename}")
        counts[kind] = len(registered)
        return registered

    skills = catalog("skills", "SKILL.md")
    catalog("rules", "RULE.md")
    packages = set()
    members = {}
    for number, value in entries("skills/packages.manifest"):
        location = f"skills/packages.manifest:{number}"
        parts = value.split()
        if len(parts) != 2 or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", parts[0]):
            error(location, "expected package-name and registered skill path")
            continue
        package, member = parts
        if (package, member) in packages:
            error(location, f"duplicate package member {value}")
        packages.add((package, member))
        if member not in skills:
            error(location, f"unknown skill {member}")
        previous = members.setdefault(member, package)
        if previous != package:
            error(location, f"{member} belongs to both {previous} and {package}")

    for relative in ("CLAUDE.md", "skills/project-management/project-bootstrap/references/templates/CLAUDE.md"):
        path = root / relative
        if not path.is_file() or path.read_text().strip() != "@AGENTS.md":
            error(relative, "expected only @AGENTS.md")
        if not (path.parent / "AGENTS.md").is_file():
            error(relative, "missing shared AGENTS.md beside shim")

    return errors, counts


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1],
                        help="source repository to check (default: this repository)")
    args = parser.parse_args()
    errors, counts = check_repo(args.repo.resolve())
    if errors:
        for message in errors:
            print(f"check-content: {message}", file=sys.stderr)
        return 1
    print(f"check-content: passed ({counts['skills']} skills, {counts['rules']} rules)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

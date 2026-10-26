#!/usr/bin/env python3
"""Check the source catalog without installing anything or contacting a service."""

import argparse
import re
import sys
from pathlib import Path, PurePosixPath

try:
    import yaml
except ImportError:
    sys.exit("check-content: install validation dependencies: python3 -m pip install -r requirements-dev.txt")


class UniqueKeyLoader(yaml.SafeLoader):
    """Reject duplicate mapping keys instead of silently accepting the last value."""


def unique_mapping(loader, node):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node)
        if not isinstance(key, str):
            raise yaml.constructor.ConstructorError(None, None, "mapping keys must be strings", key_node.start_mark)
        if key in result:
            raise yaml.constructor.ConstructorError(None, None, f"duplicate key {key}", key_node.start_mark)
        result[key] = loader.construct_object(value_node)
    return result


UniqueKeyLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)


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

    def mapping(text, relative):
        try:
            value = yaml.load(text, Loader=UniqueKeyLoader)
            if not isinstance(value, dict):
                error(relative, "expected a YAML mapping")
                return {}
            return value
        except yaml.YAMLError as exc:
            error(relative, f"invalid YAML: {exc}")
            return {}

    def skill_policy(source, fields):
        relative = str(source.relative_to(root))
        disabled = fields.get("disable-model-invocation", False)
        user_invocable = fields.get("user-invocable", True)
        for key in ("disable-model-invocation", "user-invocable"):
            if key in fields and type(fields[key]) is not bool:
                error(relative, f"{key} must be a boolean")
        metadata = source.parent / "agents/openai.yaml"
        agent = mapping(metadata.read_text(), str(metadata.relative_to(root))) if metadata.exists() else {}
        policy = agent.get("policy", {})
        if not isinstance(policy, dict):
            error(relative, "agents/openai.yaml policy must be a mapping")
            policy = {}
        implicit = policy.get("allow_implicit_invocation", True)
        if type(implicit) is not bool:
            error(relative, "allow_implicit_invocation must be a boolean")
        if disabled is True and implicit is not False:
            error(relative, "explicit-only skill requires Codex allow_implicit_invocation: false")
        if implicit is False and disabled is not True:
            error(relative, "Codex explicit-only policy requires disable-model-invocation: true")
        if disabled is True and user_invocable is False:
            error(relative, "explicit-only skill must remain user-invocable")
        description = fields.get("description", "")
        if disabled is True and (not isinstance(description, str) or "explicit" not in description.lower()):
            error(relative, "explicit-only description must state explicit activation")
        for key in set(policy) - {"allow_implicit_invocation", "products"}:
            error(relative, f"unsupported invocation policy key {key}")
        interface = agent.get("interface", {})
        if not isinstance(interface, dict):
            error(relative, "agents/openai.yaml interface must be a mapping")
        else:
            for key, value in interface.items():
                if not isinstance(value, str) or not value.strip():
                    error(relative, f"interface.{key} must be a nonempty string")

    def catalog(kind, filename):
        manifest = f"{kind}/{kind}.manifest"
        registered = set()
        names = set()
        for number, value in entries(manifest):
            location = f"{manifest}:{number}"
            path = PurePosixPath(value)
            if not all(re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", part) or
                       (kind == "skills" and index == 0 and part == "_collections" and len(path.parts) >= 3)
                       for index, part in enumerate(path.parts)) or str(path) != value:
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
            fields = mapping("\n".join(lines[1:end]), relative)
            if fields.get("name") != path.name:
                error(relative, "frontmatter name must match directory basename")
            if not isinstance(fields.get("description"), str) or not fields["description"].strip():
                error(relative, "missing description")
            if kind == "skills":
                skill_policy(source, fields)
            if kind == "rules":
                always = fields.get("alwaysApply")
                if type(always) is not bool:
                    error(relative, "alwaysApply must be true or false")
                elif always is False and not fields.get("globs"):
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
    drafts = sorted((root / "drafts").rglob("SKILL.md"))
    installed_names = {Path(value).name for value in skills}
    for source in drafts:
        relative = str(source.relative_to(root))
        parts = source.read_text().split("---", 2)
        if len(parts) != 3 or parts[0].strip():
            error(relative, "draft requires delimited frontmatter")
            continue
        fields = mapping(parts[1], relative)
        if fields.get("name") != source.parent.name or source.parent.name in installed_names:
            error(relative, "draft name must match its folder and stay outside the install catalog")
        if not isinstance(fields.get("description"), str) or not fields["description"].strip():
            error(relative, "missing description")
        skill_policy(source, fields)
    counts["drafts"] = len(drafts)
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

    for relative in ("CLAUDE.md", "skills/_collections/project-management/project-bootstrap/references/templates/CLAUDE.md"):
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
    print(f"check-content: passed ({counts['skills']} skills, {counts['drafts']} drafts, {counts['rules']} rules)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

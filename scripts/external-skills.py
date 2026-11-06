#!/usr/bin/env python3
"""Explicit, content-pinned distribution from local repositories (stdlib only)."""

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
import subprocess
import sys
import tempfile

OWNER = "chrispalmo/agent-config:external-skill-v1"
RECEIPT = ".agent-config-external.json"
RESOURCES = {"references", "assets", "scripts", "agents"}
CONFIG_KEYS = {"version", "name", "repository", "checkout", "path", "sha256"}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read_json(path):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            require(key not in result, f"duplicate JSON key: {key}")
            result[key] = value
        return result
    return json.loads(path.read_text(), object_pairs_hook=unique)


def relative(value):
    require(isinstance(value, str) and value, "expected a relative path")
    p = PurePosixPath(value)
    require(not p.is_absolute() and str(p) == value and
            all(part not in {".", ".."} for part in p.parts), f"unsafe path: {value}")
    return p


def packaged(value):
    p = relative(value)
    require(value == "SKILL.md" or (len(p.parts) > 1 and p.parts[0] in RESOURCES),
            f"not a packaged skill file: {value}")
    return p


def plain_path(path):
    # Check each existing ancestor as well as the final path, including dangling links.
    for p in [path, *path.parents]:
        require(not p.is_symlink(), f"symlink is not an installation/source path: {p}")
    for p in path.parents:
        require(not p.exists() or p.is_dir(), f"parent is not a directory: {p}")


def git(checkout, *args):
    return subprocess.check_output(["git", "-C", str(checkout), *args],
                                   stderr=subprocess.PIPE, text=True).strip()


def identity(config):
    return {k: config[k] for k in ("name", "repository", "path")}


def config_valid(config):
    require(isinstance(config, dict) and set(config) == CONFIG_KEYS, "unexpected config fields")
    require(type(config["version"]) is int and config["version"] == 1, "unsupported config version")
    for key in CONFIG_KEYS - {"version"}:
        require(isinstance(config[key], str) and config[key], f"invalid {key}")
    require(re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", config["name"]), "invalid skill name")
    require(Path(config["checkout"]).is_absolute(), "checkout must be absolute")
    require(relative(config["path"]).name == config["name"], "skill path/name mismatch")
    require(re.fullmatch(r"[0-9a-f]{64}", config["sha256"]), "invalid content hash")
    require(not re.search(r"https?://[^/]*@", config["repository"]), "do not store credentials in repository URLs")


def file_info(data, mode):
    return {"sha256": hashlib.sha256(data).hexdigest(), "mode": mode}


def digest(files):
    return hashlib.sha256(json.dumps(files, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def source_snapshot(config):
    checkout = Path(config["checkout"])
    require(checkout.is_dir(), f"missing checkout: {checkout}")
    # A normal macOS temporary directory can have an aliased ancestor. Canonicalize
    # the checkout itself, then reject links within the skill source tree.
    checkout = checkout.resolve()
    require(Path(git(checkout, "rev-parse", "--show-toplevel")).resolve() == checkout,
            "checkout must be a Git repository root")
    require(git(checkout, "remote", "get-url", "origin") == config["repository"], "repository origin mismatch")
    source = checkout / config["path"]
    plain_path(source)
    require(source.is_dir(), f"missing skill source: {source}")
    files, payload = {}, {}
    candidates = [source / "SKILL.md"]
    for name in sorted(RESOURCES):
        directory = source / name
        require(not directory.is_symlink(), f"symlink source: {directory}")
        if directory.exists():
            require(directory.is_dir(), f"resource is not a directory: {directory}")
            candidates.extend(directory.rglob("*"))
    for path in sorted(candidates):
        require(not path.is_symlink(), f"symlink source: {path}")
        if path.is_dir():
            continue
        require(path.is_file() and stat.S_ISREG(path.stat().st_mode), f"missing/non-regular source: {path}")
        name = path.relative_to(source).as_posix()
        packaged(name)
        data = path.read_bytes()
        mode = 0o755 if path.stat().st_mode & 0o111 else 0o644
        files[name] = file_info(data, mode)
        payload[name] = data
    lines = payload["SKILL.md"].decode("utf-8").splitlines()
    require(lines and lines[0] == "---" and "---" in lines[1:], "missing skill frontmatter")
    header = lines[1:lines[1:].index("---") + 1]
    names = [line for line in header if re.match(r"^name\s*:", line)]
    require(len(names) == 1 and names[0].split(":", 1)[1].strip().strip("\"'") == config["name"],
            "skill frontmatter name mismatch")
    return files, payload, {"checkout": str(checkout), "head": git(checkout, "rev-parse", "HEAD"),
                            "skill_dirty": bool(git(checkout, "status", "--porcelain", "--untracked-files=all", "--", config["path"]))}


def installed_files(value):
    require(isinstance(value, dict) and "SKILL.md" in value, "invalid receipt file inventory")
    for name, item in value.items():
        packaged(name)
        require(isinstance(item, dict) and set(item) == {"sha256", "mode"} and
                isinstance(item["sha256"], str) and re.fullmatch(r"[0-9a-f]{64}", item["sha256"]) and
                type(item["mode"]) is int and item["mode"] in {0o644, 0o755}, "invalid receipt file entry")
    return value


def preflight(dest, config, new_files):
    plain_path(dest)
    if not dest.exists():
        return {}
    require(dest.is_dir(), f"destination is not a directory: {dest}")
    marker = dest / RECEIPT
    require(marker.is_file() and not marker.is_symlink(), f"foreign skill destination: {dest}")
    require(not any((dest / p).exists() or (dest / p).is_symlink()
                    for p in (".agent-config-managed", ".agent-config-resources")), "conflicting internal ownership")
    receipt = read_json(marker)
    require(isinstance(receipt, dict) and receipt.get("managed_by") == OWNER and
            receipt.get("source") == identity(config), f"external source identity mismatch: {dest}")
    old = installed_files(receipt.get("files"))
    require(receipt.get("sha256") == digest(old), "receipt content hash mismatch")
    for name, expected in old.items():
        path = dest / name
        plain_path(path)
        require(path.is_file(), f"managed file missing: {path}")
        require(file_info(path.read_bytes(), 0o755 if path.stat().st_mode & 0o111 else 0o644) == expected,
                f"managed file modified locally: {path}")
    for name in new_files:
        path = dest / name
        plain_path(path)
        for parent in path.parents:
            if parent == dest:
                break
            require(not parent.exists() or parent.is_dir(), f"foreign path blocks resource: {parent}")
        require(name in old or not path.exists(), f"foreign file blocks installation: {path}")
    return old


def apply(destinations, config, files, payload, provenance, action):
    # Prepare every destination before changing one. Renames are per-filesystem;
    # roll back completed swaps if a later target fails during this process.
    staged, swapped, retained = [], [], set()
    try:
        for dest, old in destinations:
            if action == "remove" and not dest.exists():
                continue
            dest.parent.mkdir(parents=True, exist_ok=True)
            temp = Path(tempfile.mkdtemp(prefix=f".{config['name']}-", dir=dest.parent))
            work, backup = temp / "new", temp / "old"
            staged.append((temp, dest, work, backup))
            if dest.exists():
                shutil.copytree(dest, work, symlinks=True)
            else:
                work.mkdir()
            for name in old:
                (work / name).unlink()
            if (work / RECEIPT).exists():
                (work / RECEIPT).unlink()
            # Remove empty parents of owned files only; preserve unrelated empty dirs.
            parents = {parent for name in old for parent in (work / name).parents
                       if parent != work and work in parent.parents}
            for p in sorted(parents, key=lambda p: len(p.parts), reverse=True):
                try:
                    p.rmdir()
                except OSError:
                    pass
            if action == "install":
                for name, data in payload.items():
                    path = work / name
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_bytes(data)
                    path.chmod(files[name]["mode"])
                receipt = {"managed_by": OWNER, "source": identity(config), "sha256": digest(files),
                           "files": files, **provenance}
                (work / RECEIPT).write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
        for temp, dest, work, backup in staged:
            if dest.exists():
                dest.rename(backup)
            swapped.append((dest, backup))
            if any(work.iterdir()):
                work.rename(dest)
        for _, dest, _, _ in staged:
            print(f"external-skills: {action}: {dest}")
    except Exception:
        for dest, backup in reversed(swapped):
            try:
                if dest.exists():
                    shutil.rmtree(dest)
                if backup.exists():
                    backup.rename(dest)
            except OSError:
                retained.add(backup.parent)
                print(f"external-skills: rollback incomplete; recover from {backup}", file=sys.stderr)
        raise
    finally:
        for temp, _, _, _ in staged:
            if temp not in retained:
                shutil.rmtree(temp)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="action", required=True)
    pin = sub.add_parser("pin", help="print a candidate local config; review before saving/installing")
    pin.add_argument("--checkout", type=Path, required=True)
    pin.add_argument("--path", required=True)
    for action in ("install", "remove"):
        p = sub.add_parser(action)
        p.add_argument("--config", type=Path, required=True)
        p.add_argument("--catalog", type=Path, required=True)
        p.add_argument("--root", type=Path, action="append", required=True)
        p.add_argument("--legacy-root", type=Path, action="append", default=[])
    args = parser.parse_args()
    if args.action == "pin":
        # Keep the operator's stable checkout path; source_snapshot verifies the
        # resolved Git root, origin and packaged contents on each installation.
        checkout = args.checkout.absolute()
        config = {"version": 1, "name": relative(args.path).name, "repository": git(checkout, "remote", "get-url", "origin"),
                  "checkout": str(checkout), "path": args.path, "sha256": "0" * 64}
        config_valid(config)
        files, _, _ = source_snapshot(config)
        config["sha256"] = digest(files)
        print(json.dumps(config, indent=2))
        return
    config = read_json(args.config)
    config_valid(config)
    files, payload, provenance = {}, {}, {}
    if args.action == "install":
        names = {PurePosixPath(line.split("#", 1)[0].strip()).name for line in args.catalog.read_text().splitlines()}
        require(config["name"] not in names, "external skill collides with the internal catalog")
        files, payload, provenance = source_snapshot(config)
        require(digest(files) == config["sha256"], "source hash mismatch; review changes and explicitly repin")
    roots = list(dict.fromkeys(Path(os.path.abspath(p)) for p in args.root))
    for root in roots:
        plain_path(root)
        require(not root.exists() or root.is_dir(), f"not a skill root: {root}")
        require(not any(other != root and (root in other.parents or other in root.parents)
                        for other in roots), "skill roots must not overlap")
    for root in args.legacy_root:
        if root.absolute() not in roots:
            duplicate = root / config["name"]
            require(not duplicate.exists() and not duplicate.is_symlink(), f"legacy duplicate must be resolved explicitly: {duplicate}")
    destinations = [(root / config["name"], preflight(root / config["name"], config, files)) for root in roots]
    apply(destinations, config, files, payload, provenance, args.action)
    if args.action == "install":
        print(f"external-skills: sha256={digest(files)} head={provenance['head']} skill_dirty={provenance['skill_dirty']}")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, subprocess.CalledProcessError) as exc:
        sys.exit(f"external-skills: {exc}")

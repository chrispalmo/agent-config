#!/usr/bin/env python3
"""Pinned design-review releases and explicit, local-only consumer updates."""

import argparse
import base64
import contextlib
import difflib
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys
import tempfile

SKILL = Path(__file__).resolve().parents[1]
RELEASES = SKILL / "assets/template-releases"
SHARED = ("design-footer.js", "design-footer.css", "design-state.js",
          "design-annotations.js", "design-persistence.js", "artifact-persistence.js")
STARTER = ("review-example.html", "review-example.css", "review-example.js")
CONTRACT = {"mountApi": 1, "stateSchema": 3, "exportSchema": 4}
RECEIPT = ".design-review-template.json"
META = ".design-review-template"
OWNER = "design-review-template-v1\n"


def fail(message):
    raise ValueError(message)


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def digest(data):
    return hashlib.sha256(data).hexdigest()


def version_key(value):
    if not isinstance(value, str) or not re.fullmatch(r"(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)", value):
        fail("expected an exact numeric semantic version, such as 0.1.0")
    return tuple(map(int, value.split(".")))


def filename(name):
    if not isinstance(name, str) or not re.fullmatch(r"[a-z][a-z0-9.-]*\.(js|css|html)", name):
        fail(f"invalid flat template filename: {name!r}")
    return name


def plain(path, directory=False):
    """Reject links/non-regular paths, including symlinked ancestors."""
    path = Path(os.path.abspath(Path(path).expanduser()))
    # macOS exposes its system temporary directories through these fixed aliases.
    # Normalize those aliases, while still rejecting consumer-controlled symlinks.
    if sys.platform == "darwin":
        for alias in (Path("/tmp"), Path("/var")):
            target = Path("/private") / alias.name
            if (path == alias or alias in path.parents) and alias.is_symlink() and alias.resolve() == target:
                path = target / path.relative_to(alias)
                break
    for parent in (path, *path.parents):
        if parent.is_symlink():
            fail(f"symlink path is not supported: {parent}")
    if path.exists():
        kind = path.stat().st_mode
        if not (stat.S_ISDIR(kind) if directory else stat.S_ISREG(kind)):
            fail(f"expected {'directory' if directory else 'regular file'}: {path}")
    return path


def root_path(value):
    return plain(Path(value), directory=True)


def read_bytes(path):
    path = plain(path)
    return path.read_bytes() if path.exists() else None


def read_json(path):
    data = read_bytes(path)
    return json.loads(data) if data is not None else None


def release_identity(release):
    return {key: value for key, value in release.items() if key not in ("sha256", "content")}


def validate_release(release):
    if not isinstance(release, dict) or set(release) != {
            "formatVersion", "template", "version", "compatibility", "notes",
            "files", "starterFiles", "content", "sha256"}:
        fail("invalid release manifest")
    if release["formatVersion"] != 1 or release["template"] != "design-review":
        fail("unsupported template/release format")
    version_key(release["version"])
    if set(release["compatibility"]) != set(CONTRACT) or any(
            type(n) is not int or n < 1 for n in release["compatibility"].values()):
        fail("invalid compatibility contract")
    if not isinstance(release["notes"], list) or not release["notes"] or any(
            not isinstance(note, str) or not note.strip() for note in release["notes"]):
        fail("release notes are required")
    files, starter = release["files"], release["starterFiles"]
    if not isinstance(files, dict) or not files or not isinstance(starter, dict) or set(files) & set(starter):
        fail("invalid or overlapping file inventory")
    if set(release["content"]) != set(files) | set(starter):
        fail("payload does not match file inventory")
    for name, expected in {**files, **starter}.items():
        filename(name)
        content = release["content"][name]
        if not isinstance(content, str) or digest(content.encode()) != expected:
            fail(f"release file hash mismatch: {name}")
    if release["sha256"] != digest(encoded(release_identity(release))):
        fail("release manifest hash mismatch")
    return release


def make_release(assets, version, notes, compatibility=None):
    version_key(version)
    content = {name: read_bytes(assets / name).decode() for name in (*SHARED, *STARTER)}
    release = {
        "formatVersion": 1, "template": "design-review", "version": version,
        "compatibility": compatibility or dict(CONTRACT), "notes": notes,
        "files": {name: digest(content[name].encode()) for name in SHARED},
        "starterFiles": {name: digest(content[name].encode()) for name in STARTER},
        "content": content,
    }
    release["sha256"] = digest(encoded(release_identity(release)))
    return validate_release(release)


def releases_at(directory):
    directory = plain(directory, directory=True)
    found = {}
    if not directory.exists():
        return found
    for path in sorted(directory.glob("*.json")):
        release = validate_release(read_json(path))
        if path.stem != release["version"] or release["version"] in found:
            fail(f"release filename/version mismatch: {path}")
        found[release["version"]] = release
    return found


def receipt_for(release):
    return {"formatVersion": 1, "template": "design-review", "version": release["version"],
            "sha256": release["sha256"], "files": release["files"],
            "compatibility": release["compatibility"]}


def metadata(root):
    directory = plain(root / META, directory=True)
    if directory.exists() and read_bytes(directory / "owner") != OWNER.encode():
        fail(f"unmanaged metadata directory: {directory}")
    return directory


def current_release(root, allow_pending=False):
    directory = metadata(root)
    if read_bytes(directory / "transaction.json") is not None and not allow_pending:
        fail("interrupted update; run recover before another operation")
    receipt = read_json(root / RECEIPT)
    if receipt is None:
        return None
    if not isinstance(receipt, dict):
        fail("invalid template receipt")
    version_key(receipt.get("version"))
    release = validate_release(read_json(directory / "releases" / (receipt["version"] + ".json")))
    if receipt != receipt_for(release):
        fail("receipt differs from its preserved release")
    return release


def target_release(directory, root, version=None, cached_only=False):
    available = {} if cached_only else releases_at(directory)
    cached = releases_at(metadata(root) / "releases") if root else {}
    for key, value in cached.items():
        if key in available and value["sha256"] != available[key]["sha256"]:
            fail(f"release {key} was rewritten; keep published releases immutable")
        available[key] = value
    if not available:
        fail("no local releases available")
    if version is None:
        version = max(available, key=version_key)
    version_key(version)
    if version not in available:
        fail(f"release {version} is unavailable locally")
    return available[version]


def plan(root, release, operation="update", example=False):
    base = current_release(root)
    conflicts, changes, before, after, patches = [], [], {}, {}, []
    if operation in ("init", "adopt") and base:
        fail("already pinned; use check/update")
    if operation in ("update", "rollback") and not base:
        fail("no receipt; init a new consumer or adopt an exact existing copy")
    if base and base["version"] == release["version"] and base["sha256"] != release["sha256"]:
        fail("same version has different bytes; release a new version")
    compatible = not base or (base["compatibility"] == release["compatibility"] and
                             version_key(base["version"])[0] == version_key(release["version"])[0])
    old_files = base["files"] if base else {}
    new_files = dict(release["files"])
    if example:
        if operation != "init":
            fail("--example is only for init; app-specific starter files are never updated")
        new_files.update(release["starterFiles"])
    for name in sorted(set(old_files) | set(new_files)):
        current = read_bytes(root / filename(name))
        wanted = release["content"][name].encode() if name in new_files else None
        if operation == "adopt":
            if current != wanted:
                conflicts.append({"file": name, "reason": "not an exact release copy"})
        elif name in old_files:
            if current is None or digest(current) != old_files[name]:
                conflicts.append({"file": name, "reason": "owned file was changed or removed locally"})
        elif current is not None:
            conflicts.append({"file": name, "reason": "unowned destination already exists"})
        action = "unchanged" if current == wanted else "remove" if wanted is None else "add" if current is None else "update"
        changes.append({"file": name, "action": action})
        before[name] = current
        if operation != "adopt" and current != wanted:
            after[name] = wanted
            patches.extend(difflib.unified_diff(
                (current or b"").decode(errors="replace").splitlines(True),
                (wanted or b"").decode().splitlines(True),
                fromfile="current/" + name, tofile="release/" + name))
    before[RECEIPT] = read_bytes(root / RECEIPT)
    receipt = encoded(receipt_for(release)) + b"\n"
    if before[RECEIPT] != receipt:
        after[RECEIPT] = receipt
    report = {
        "operation": operation, "destination": str(root),
        "current": base["version"] if base else None, "target": release["version"],
        "sha256": release["sha256"], "compatible": compatible,
        "notes": release["notes"], "changes": changes, "conflicts": conflicts,
        "canApply": compatible and not conflicts, "wouldChange": bool(after),
        "diff": "".join(patches), "applied": False,
    }
    if not compatible:
        report["migrationRequired"] = "Mount/data contract or major version changed; migrate in a separate source copy and validate feedback preservation."
    return report, before, after


def atomic_write(path, data):
    path = plain(path)
    if data is None:
        if path.exists():
            path.unlink()
        return
    mode = stat.S_IMODE(path.stat().st_mode) if path.exists() else 0o644
    fd, temporary = tempfile.mkstemp(prefix=".template-", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.chmod(temporary, mode)
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


@contextlib.contextmanager
def locked(root):
    plain(root, directory=True)
    root.mkdir(parents=True, exist_ok=True)
    directory = metadata(root)
    if not directory.exists():
        directory.mkdir()
        atomic_write(directory / "owner", OWNER.encode())
    lock_path = plain(directory / "lock")
    with lock_path.open("a+") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        yield directory


def packed(data):
    return None if data is None else base64.b64encode(data).decode()


def unpacked(data):
    return None if data is None else base64.b64decode(data, validate=True)


def recover_locked(root, directory):
    path = directory / "transaction.json"
    journal = read_json(path)
    if journal is None:
        return {"recovered": False}
    if not isinstance(journal, dict) or set(journal) != {"before", "after"} or set(journal["before"]) != set(journal["after"]):
        fail("invalid recovery journal; preserve it for manual recovery")
    for name in journal["before"]:
        if name != RECEIPT:
            filename(name)
        current = read_bytes(root / name)
        if current not in (unpacked(journal["before"][name]), unpacked(journal["after"][name])):
            fail(f"recovery conflict; preserve the later edit to {name} before recovering")
    for name, data in journal["before"].items():
        atomic_write(root / name, unpacked(data))
    path.unlink()
    return {"recovered": True, "restored": sorted(journal["before"])}


def apply_plan(root, release, operation, example=False):
    # Preflight before creating any destination/metadata. Repeat under the lock.
    report, _, _ = plan(root, release, operation, example)
    if not report["canApply"]:
        return report
    if not report["wouldChange"]:
        return report
    with locked(root) as directory:
        report, before, after = plan(root, release, operation, example)
        if not report["canApply"] or not after:
            return report
        cache = plain(directory / "releases", directory=True)
        cache.mkdir(exist_ok=True)
        release_path = cache / (release["version"] + ".json")
        existing = read_json(release_path)
        if existing is not None and validate_release(existing) != release:
            fail("cached release identity changed")
        if existing is None:
            atomic_write(release_path, encoded(release) + b"\n")
        # Recheck all owned files, including unchanged ones, before writing.
        if any(read_bytes(root / name) != data for name, data in before.items()):
            fail("consumer changed during preparation; re-run check")
        journal = {"before": {name: packed(before[name]) for name in after},
                   "after": {name: packed(data) for name, data in after.items()}}
        journal_path = directory / "transaction.json"
        atomic_write(journal_path, encoded(journal) + b"\n")
        try:
            for name, data in after.items():
                atomic_write(root / name, data)
            if any(read_bytes(root / name) != data for name, data in after.items()):
                fail("readback failed")
            journal_path.unlink()
        except Exception:
            # If rollback itself fails the journal remains for explicit recover.
            recover_locked(root, directory)
            raise
        report["applied"] = True
        return report


def print_report(report, as_json=False):
    if as_json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return
    for key in ("operation", "current", "target", "sha256", "compatible", "canApply", "applied"):
        if key in report:
            print(f"{key}: {report[key]}")
    for note in report.get("notes", []):
        print("note: " + note)
    for conflict in report.get("conflicts", []):
        print(f"conflict: {conflict['file']}: {conflict['reason']}")
    if report.get("migrationRequired"):
        print(report["migrationRequired"])
    if report.get("diff"):
        print(report["diff"], end="" if report["diff"].endswith("\n") else "\n")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    for command in ("init", "adopt", "check", "update", "rollback"):
        child = sub.add_parser(command)
        child.add_argument("--dest", required=True, help="consumer's flat shared-resource directory")
        child.add_argument("--to", required=command != "check", help="exact release; check defaults to newest locally available")
        child.add_argument("--releases", type=Path, default=RELEASES, help="local release directory; never fetched")
        child.add_argument("--json", action="store_true")
        if command != "check":
            child.add_argument("--apply", action="store_true", help="apply the displayed plan; otherwise read-only")
        if command == "init":
            child.add_argument("--example", action="store_true", help="seed fictional app files once; never own/update them")
    child = sub.add_parser("recover")
    child.add_argument("--dest", required=True)
    child = sub.add_parser("list")
    child.add_argument("--releases", type=Path, default=RELEASES)
    child = sub.add_parser("verify")
    child.add_argument("--releases", type=Path, default=RELEASES)
    child.add_argument("--assets", type=Path, help="also match newest release to current source assets")
    child = sub.add_parser("release")
    child.add_argument("--version", required=True)
    child.add_argument("--note", action="append", required=True)
    child.add_argument("--assets", type=Path, default=SKILL / "assets")
    child.add_argument("--releases", type=Path, default=RELEASES)
    child.add_argument("--apply", action="store_true")
    args = parser.parse_args(argv)
    if args.command in ("list", "verify"):
        releases = releases_at(args.releases)
        if not releases:
            fail("no local releases available")
        if args.command == "verify" and args.assets:
            newest = releases[max(releases, key=version_key)]
            for name, expected in {**newest["files"], **newest["starterFiles"]}.items():
                data = read_bytes(args.assets / name)
                if data is None or digest(data) != expected:
                    fail(f"source differs from newest release: {name}; create a new release")
        print(json.dumps({"verified": args.command == "verify", "releases": [
            {key: release[key] for key in ("version", "sha256", "compatibility", "notes")}
            for _, release in sorted(releases.items(), key=lambda item: version_key(item[0]))]}, indent=2))
        return 0
    if args.command == "release":
        release = make_release(args.assets, args.version, args.note)
        available = releases_at(args.releases)
        if args.version in available:
            fail("version already exists; releases are immutable")
        if available and version_key(args.version) <= max(map(version_key, available)):
            fail("new releases must advance the version")
        if args.apply:
            plain(args.releases, directory=True).mkdir(parents=True, exist_ok=True)
            path = args.releases / (args.version + ".json")
            # Exclusive creation prevents concurrent same-version replacement.
            with path.open("xb") as stream:
                stream.write(encoded(release) + b"\n")
        print(json.dumps({"version": args.version, "sha256": release["sha256"], "written": args.apply}))
        return 0
    root = root_path(args.dest)
    if args.command == "recover":
        if not read_bytes(metadata(root) / "transaction.json"):
            print(json.dumps({"recovered": False}))
            return 0
        with locked(root) as directory:
            print(json.dumps(recover_locked(root, directory)))
        return 0
    release = target_release(args.releases, root, args.to, cached_only=args.command == "rollback")
    operation = "update" if args.command == "check" else args.command
    if args.command == "rollback":
        base = current_release(root)
        if not base or version_key(release["version"]) >= version_key(base["version"]):
            fail("rollback requires an older preserved release")
    if getattr(args, "apply", False):
        report = apply_plan(root, release, operation, getattr(args, "example", False))
    else:
        report, _, _ = plan(root, release, operation, getattr(args, "example", False))
    print_report(report, args.json)
    return 0 if report["canApply"] else 2


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (ValueError, OSError, KeyError, TypeError, AttributeError) as error:
        print(f"design-review-template: {error}", file=sys.stderr)
        sys.exit(1)

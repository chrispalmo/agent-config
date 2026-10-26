#!/usr/bin/env python3
"""Local tab ownership and expiry registry. Never operates the browser."""

import argparse
import contextlib
import fcntl
import json
import math
import os
from pathlib import Path
import re
import stat
import sys
import tempfile
import time
import uuid

GRACE = 2 * 60 * 60
REVIEW = 48 * 60 * 60


def state_root():
    # A fixed per-user path avoids harness-specific TMPDIR/XDG environments.
    override = os.environ.get("AGENT_BROWSER_STATE_DIR")
    if override:
        if not Path(override).is_absolute():
            raise ValueError("AGENT_BROWSER_STATE_DIR must be absolute")
        return Path(override)
    return Path("/tmp").resolve() / f"agent-browser-{os.getuid()}" / "sessions"


def private_directory(path, create=False):
    if create:
        path.mkdir(mode=0o700, exist_ok=True)
    info = path.lstat()
    if (not stat.S_ISDIR(info.st_mode) or info.st_uid != os.getuid()
            or stat.S_IMODE(info.st_mode) & 0o077):
        raise ValueError(f"registry directory must be owned by this user, private and not a symlink: {path}")


def legacy_root():
    return Path.home() / ".local/state/agent-browser/sessions"


def session_path(root, session):
    if str(uuid.UUID(session)) != session:
        raise ValueError("invalid session ID")
    return root / (session + ".json")


@contextlib.contextmanager
def locked(root, legacy=False):
    if not legacy:
        private_directory(root.parent, create=True)
        private_directory(root, create=True)
    else:
        private_directory(root)
    fd = os.open(root / ".lock", os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW, 0o600)
    with os.fdopen(fd, "a+") as lock:
        info = os.fstat(lock.fileno())
        if (not stat.S_ISREG(info.st_mode) or info.st_uid != os.getuid()
                or stat.S_IMODE(info.st_mode) & 0o077):
            raise ValueError("registry lock must be a private regular file owned by this user")
        fcntl.flock(lock, fcntl.LOCK_EX)
        yield


def migrate(source, root):
    if not source.is_absolute() or source.resolve() == root.resolve():
        raise ValueError("migration requires a different absolute source directory")
    with locked(source, legacy=True), locked(root):
        incoming, errors = records(source)
        existing, target_errors = records(root)
        if errors or target_errors:
            raise ValueError("repair corrupt registry records before migration")
        by_id = {record["id"]: record for record in existing}
        for record in incoming:
            if record["id"] in by_id and by_id[record["id"]] != record:
                raise ValueError("migration conflicts with an existing session; no records were moved")
        # Keep every original until all destination writes succeed. Identical
        # duplicates allow a retry after an interrupted copy without renewal.
        for record in incoming:
            write_record(root, record)
        for record in incoming:
            session_path(source, record["id"]).unlink()
        return {"migrated": len(incoming), "registry": str(root)}


def stamp(value):
    return type(value) in (int, float) and math.isfinite(value) and value > 0


def identity(value):
    if isinstance(value, bool) or not isinstance(value, (int, str)) or not str(value):
        raise ValueError("missing or invalid browser object ID")
    return str(value)


def read_record(path):
    if path.is_symlink():
        raise ValueError("session records must not be symlinks")
    record = json.loads(path.read_text())
    if (not isinstance(record, dict) or record.get("version") != 1 or record.get("id") != path.stem
            or not isinstance(record.get("browser"), str) or not record["browser"]
            or not isinstance(record.get("task"), str)
            or not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,79}", record["task"])
            or not stamp(record.get("protected_until"))
            or not isinstance(record.get("tabs"), dict)):
        raise ValueError("invalid session schema")
    for key, tab in record["tabs"].items():
        if (not isinstance(tab, dict) or identity(tab.get("id")) != key or identity(tab.get("group")) == "-1"
                or not stamp(tab.get("created_at")) or not stamp(tab.get("last_activity"))
                or type(tab.get("keep")) is not bool
                or (tab.get("review_until") is not None and not stamp(tab["review_until"]))):
            raise ValueError("invalid registered tab")
    return record


def write_record(root, record):
    path = session_path(root, record["id"])
    fd, name = tempfile.mkstemp(prefix=".session-", dir=root)
    try:
        with os.fdopen(fd, "w") as output:
            json.dump(record, output, indent=2)
            output.write("\n")
            output.flush()
            os.fsync(output.fileno())
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def records(root):
    valid, errors = [], []
    for path in sorted(root.glob("*.json")):
        try:
            valid.append(read_record(path))
        except (ValueError, KeyError, TypeError, OSError) as error:
            errors.append({"file": path.name, "error": str(error)})
    return valid, errors


def read_snapshot(path):
    data = json.loads(Path(path).read_text())
    if (not isinstance(data, dict) or data.get("complete") is not True or not isinstance(data.get("browser"), str)
            or not data["browser"] or not isinstance(data.get("groups"), list)
            or not isinstance(data.get("tabs"), list)):
        raise ValueError("snapshot requires complete=true, browser identity, groups and tabs")
    groups = {identity(group["id"]): group["title"] for group in data["groups"]}
    tabs = {identity(tab["id"]): tab for tab in data["tabs"]}
    if len(groups) != len(data["groups"]) or len(tabs) != len(data["tabs"]):
        raise ValueError("snapshot has duplicate identities")
    # Every tab needs group identity even if other metadata is unavailable.
    for tab in tabs.values():
        group = identity(tab["groupId"])
        if group != "-1" and group not in groups:
            raise ValueError("snapshot omits a tab's group")
    return data["browser"], groups, tabs


def plan(all_records, browser, groups, tabs, now):
    candidates, spared = [], []
    ownership = {}
    for record in all_records:
        if record["browser"] == browser:
            for key in record["tabs"]:
                ownership[key] = ownership.get(key, 0) + 1
    for record in all_records:
        if record["browser"] != browser:
            continue
        for key, registered in record["tabs"].items():
            item = {"session": record["id"], "tab": key, "task": record["task"]}
            live = tabs.get(key)
            reason = None
            if ownership[key] != 1:
                reason = "ambiguous ownership"
            elif live is None:
                reason = "no longer present"
            elif (identity(live["groupId"]) != registered["group"]
                    or groups.get(registered["group"]) != "bot/" + record["task"]):
                reason = "group identity changed"
            elif registered["keep"]:
                reason = "explicit indefinite keep"
            elif (any(type(live.get(field)) is not bool for field in ("active", "pinned", "audible"))
                    or not stamp(live.get("lastAccessed"))):
                reason = "incomplete live metadata"
            elif any(live[field] for field in ("active", "pinned", "audible")):
                reason = "active, pinned or audible"
            elif live.get("status") != "complete":
                reason = "loading or unknown status"
            else:
                deadline = max(record["protected_until"], registered["created_at"] + GRACE,
                               registered["last_activity"] + GRACE,
                               registered.get("review_until") or 0,
                               live["lastAccessed"] / 1000 + GRACE)
                if now < deadline:
                    reason = "protected until expiry"
                    item["eligible_after"] = deadline
            if reason:
                item["reason"] = reason
                spared.append(item)
            else:
                candidates.append(item)
    return {"candidates": candidates, "spared": spared}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    start = commands.add_parser("start")
    start.add_argument("--task", required=True)
    start.add_argument("--browser", required=True)
    start.add_argument("--owner", required=True)
    for name in ("tab", "touch", "handoff"):
        command = commands.add_parser(name)
        command.add_argument("--session", required=True)
        command.add_argument("--tab", required=name != "touch")
        if name == "tab":
            command.add_argument("--group", required=True)
        if name == "touch":
            command.add_argument("--hours", type=float, default=2)
        if name == "handoff":
            command.add_argument("--reason", required=True)
            command.add_argument("--keep", action="store_true")
    commands.add_parser("status")
    commands.add_parser("init")
    migration = commands.add_parser("migrate")
    migration.add_argument("--from", dest="source", required=True)
    for name in ("plan", "reconcile"):
        command = commands.add_parser(name)
        command.add_argument("--snapshot", required=True)
    args = parser.parse_args()
    now = time.time()
    root = state_root()
    if args.command == "migrate":
        return migrate(Path(args.source), root)
    if not os.environ.get("AGENT_BROWSER_STATE_DIR") and any(legacy_root().glob("*.json")):
        raise ValueError(f"legacy registry contains records; migrate once with: migrate --from {legacy_root()}")
    if root.parent.exists() or root.parent.is_symlink():
        private_directory(root.parent)
    # Inspection of an empty registry does not create a replacement store.
    if args.command in ("status", "plan", "reconcile") and not (root.exists() or root.is_symlink()):
        if args.command != "status":
            read_snapshot(args.snapshot)
        return {"sessions": [], "candidates": [], "errors": [], "registry_exists": False, "registry": str(root)}
    with locked(root):
        if args.command == "init":
            return {"registry": str(root), "registry_exists": True}
        if args.command == "start":
            if not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,79}", args.task):
                raise ValueError("task must be a lowercase slug of at most 80 characters")
            if not args.browser.strip() or not args.owner.strip():
                raise ValueError("browser and owner must be nonempty")
            record = {"version": 1, "id": str(uuid.uuid4()), "task": args.task,
                      "browser": args.browser, "owner": args.owner,
                      "created_at": now, "protected_until": now + GRACE, "tabs": {}}
            write_record(root, record)
            return {"session": record["id"], "group_title": "bot/" + args.task}
        if args.command in ("tab", "touch", "handoff"):
            record = read_record(session_path(root, args.session))
            key = identity(args.tab) if args.tab is not None else None
            if args.command == "tab":
                group = identity(args.group)
                if group == "-1":
                    raise ValueError("cannot register an ungrouped tab")
                other, errors = records(root)
                if errors:
                    raise ValueError("repair corrupt registry records before registering tabs")
                if any(r["id"] != record["id"] and r["browser"] == record["browser"]
                       and (key in r["tabs"] or any(t["group"] == group for t in r["tabs"].values()))
                       for r in other):
                    raise ValueError("tab or group already belongs to another session")
                if key in record["tabs"]:
                    raise ValueError("tab already registered; use touch to renew it")
                record["tabs"][key] = {"id": key, "group": group, "created_at": now,
                                       "last_activity": now, "review_until": None, "keep": False}
                record["protected_until"] = max(record["protected_until"], now + GRACE)
            elif args.command == "touch":
                if not math.isfinite(args.hours) or not 2 <= args.hours <= 168:
                    raise ValueError("protection must be between 2 and 168 hours")
                if key is not None:
                    tab = record["tabs"][key]
                    tab["last_activity"] = now
                    tab["review_until"] = None
                    if not tab["keep"]:
                        tab.pop("reason", None)
                record["protected_until"] = max(record["protected_until"], now + args.hours * 3600)
            else:
                if not args.reason.strip():
                    raise ValueError("handoff reason must be nonempty")
                tab = record["tabs"][key]
                if not tab["keep"] or args.keep:
                    tab["keep"] = args.keep
                    tab["review_until"] = None if args.keep else now + REVIEW
                    tab["reason"] = args.reason
            write_record(root, record)
            return record
        all_records, errors = records(root)
        if args.command == "status":
            return {"sessions": all_records, "errors": errors, "registry_exists": True, "registry": str(root)}
        browser, groups, tabs = read_snapshot(args.snapshot)
        if args.command == "plan":
            result = plan(all_records, browser, groups, tabs, now)
            # Corrupt records may contain conflicting ownership: fail closed for the run.
            if errors:
                result["candidates"] = []
            result["errors"] = errors
            return result
        removed = []
        for record in all_records:
            if record["browser"] != browser:
                continue
            had_tabs = bool(record["tabs"])
            for key, registered in list(record["tabs"].items()):
                live = tabs.get(key)
                if (live is None or identity(live["groupId"]) != registered["group"]
                        or groups.get(registered["group"]) != "bot/" + record["task"]):
                    del record["tabs"][key]
                    removed.append({"session": record["id"], "tab": key})
            if record["tabs"]:
                write_record(root, record)
            elif had_tabs or now >= record["protected_until"]:
                session_path(root, record["id"]).unlink()
        return {"removed": removed, "errors": errors}


if __name__ == "__main__":
    try:
        print(json.dumps(main(), indent=2))
    except (ValueError, KeyError, TypeError, OSError) as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        sys.exit(1)

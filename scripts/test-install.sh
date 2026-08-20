#!/usr/bin/env bash
# Isolated checks for install.sh and uninstall.sh. Never writes to home roots.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
INSTALL="$REPO_ROOT/scripts/install.sh"
UNINSTALL="$REPO_ROOT/scripts/uninstall.sh"
MANAGED_MARK='<!-- managed-by: chrispalmo/agent-config -->'

WORKDIR="$(mktemp -d "${TMPDIR:-/tmp}/agent-config-install-test.XXXXXX")"
export AGENTS_SKILLS="$WORKDIR/agents/skills"
export CLAUDE_SKILLS="$WORKDIR/claude/skills"
export CURSOR_SKILLS="$WORKDIR/cursor/skills"
export CURSOR_BUNDLED_SKILLS="$WORKDIR/bundled-cursor"
export CLAUDE_BUNDLED_SKILLS="$WORKDIR/bundled-claude"
export CODEX_BUNDLED_SKILLS="$WORKDIR/bundled-codex"
export CODEX_HOME="$WORKDIR/codex-home"
export CURSOR_RULES="$WORKDIR/cursor/rules"
export CLAUDE_RULES="$WORKDIR/claude/rules"
export CLAUDE_MD="$WORKDIR/claude/CLAUDE.md"
export CODEX_AGENTS="$WORKDIR/codex/AGENTS.md"
trap 'rm -rf "$WORKDIR"' EXIT

fail() { echo "test-install: FAIL: $*" >&2; exit 1; }
ok() { echo "test-install: ok $*"; }

reset_roots() {
  rm -rf "$WORKDIR/agents" "$WORKDIR/claude" "$WORKDIR/cursor" \
    "$CURSOR_BUNDLED_SKILLS" "$CLAUDE_BUNDLED_SKILLS" "$CODEX_BUNDLED_SKILLS" \
    "$CODEX_HOME" "$WORKDIR/codex"
  mkdir -p "$AGENTS_SKILLS" "$CLAUDE_SKILLS" "$CURSOR_SKILLS" \
    "$CURSOR_RULES" "$CLAUDE_RULES" "$(dirname "$CODEX_AGENTS")" \
    "$CURSOR_BUNDLED_SKILLS" "$CLAUDE_BUNDLED_SKILLS" "$CODEX_BUNDLED_SKILLS" \
    "$CODEX_HOME"
}

expect_exit() {
  local want="$1" label="$2"
  shift 2
  set +e
  "$@" >"$WORKDIR/out" 2>"$WORKDIR/err"
  local got=$?
  set -e
  [[ "$got" == "$want" ]] || fail "$label: exit $got (want $want): $(tr '\n' ' ' <"$WORKDIR/err")"
}

assert_file() { [[ -f "$1" ]] || fail "missing file: $1"; }
assert_missing() { [[ ! -e "$1" && ! -L "$1" ]] || fail "should not exist: $1"; }
assert_managed() { assert_file "$1"; grep -qF "$MANAGED_MARK" "$1" || fail "missing managed sentinel: $1"; }
assert_contains() { grep -qF "$2" "$1" || fail "$1 missing: $2"; }
assert_not_contains() { grep -qF "$2" "$1" && fail "$1 should not contain: $2" || true; }
assert_link() {
  local dest="$1" expected="$2"
  [[ -L "$dest" ]] || fail "not a symlink: $dest"
  [[ "$(readlink "$dest")" == "$expected" ]] || fail "$dest -> $(readlink "$dest") (want $expected)"
}

plant_bundled() {
  local root="$1" name="$2"
  mkdir -p "$root/$name"
  echo bundled >"$root/$name/SKILL.md"
}

# Default install fills skills agents+claude and rules claude+codex; leaves cursor empty.
reset_roots
expect_exit 0 "default install" "$INSTALL"
assert_link "$AGENTS_SKILLS/design-tool/SKILL.md" "$REPO_ROOT/skills/design-tool/SKILL.md"
assert_link "$CLAUDE_SKILLS/project-bootstrap/SKILL.md" "$REPO_ROOT/skills/project-management/project-bootstrap/SKILL.md"
assert_managed "$CLAUDE_RULES/address-as-chris.md"
assert_managed "$CLAUDE_RULES/markdown-no-hard-wrap.md"
assert_managed "$CLAUDE_MD"
assert_managed "$CODEX_AGENTS"
assert_contains "$CODEX_AGENTS" "Always call the user Chris in chat."
assert_contains "$CODEX_AGENTS" 'Always create `CLAUDE.md`'
assert_not_contains "$CODEX_AGENTS" "Do not hard-wrap Markdown prose"
assert_missing "$CURSOR_SKILLS/design-tool/SKILL.md"
assert_missing "$CURSOR_RULES/address-as-chris.mdc"
ok "default install"

# Re-run is idempotent.
expect_exit 0 "idempotent re-run" "$INSTALL"
assert_managed "$CODEX_AGENTS"
ok "idempotent re-run"

# --cursor writes Cursor-native skills and rules only.
reset_roots
expect_exit 0 "cursor install" "$INSTALL" --cursor
assert_link "$CURSOR_SKILLS/design-tool/SKILL.md" "$REPO_ROOT/skills/design-tool/SKILL.md"
assert_managed "$CURSOR_RULES/address-as-chris.mdc"
assert_managed "$CURSOR_RULES/markdown-no-hard-wrap.mdc"
assert_contains "$CURSOR_RULES/address-as-chris.mdc" "alwaysApply: true"
assert_contains "$CURSOR_RULES/markdown-no-hard-wrap.mdc" "alwaysApply: false"
assert_contains "$CURSOR_RULES/markdown-no-hard-wrap.mdc" 'globs: **/*.md'
assert_missing "$CODEX_AGENTS"
assert_missing "$CLAUDE_MD"
ok "cursor install"

# Combined flags write all target roots.
reset_roots
expect_exit 0 "combined flags" "$INSTALL" --cursor --claude --agents
assert_link "$CURSOR_SKILLS/design-tool/SKILL.md" "$REPO_ROOT/skills/design-tool/SKILL.md"
assert_link "$CLAUDE_SKILLS/design-tool/SKILL.md" "$REPO_ROOT/skills/design-tool/SKILL.md"
assert_link "$AGENTS_SKILLS/design-tool/SKILL.md" "$REPO_ROOT/skills/design-tool/SKILL.md"
assert_managed "$CURSOR_RULES/address-as-chris.mdc"
assert_managed "$CLAUDE_MD"
assert_managed "$CODEX_AGENTS"
ok "combined flags"

# --package interview installs only the complete skills package.
reset_roots
expect_exit 0 "package interview" "$INSTALL" --package interview --agents
assert_link "$AGENTS_SKILLS/interview/SKILL.md" "$REPO_ROOT/skills/interview/SKILL.md"
assert_link "$AGENTS_SKILLS/reverse-brief/SKILL.md" "$REPO_ROOT/skills/interview/reverse-brief/SKILL.md"
assert_missing "$AGENTS_SKILLS/design-tool/SKILL.md"
assert_missing "$CODEX_AGENTS"
ok "package interview"

# Foreign skill destination aborts before any writes.
reset_roots
mkdir -p "$AGENTS_SKILLS/design-tool"
echo foreign >"$AGENTS_SKILLS/design-tool/SKILL.md"
expect_exit 1 "foreign skill" "$INSTALL" --agents
assert_contains "$AGENTS_SKILLS/design-tool/SKILL.md" "foreign"
assert_missing "$CODEX_AGENTS"
ok "foreign skill abort"

# Foreign Codex AGENTS.md aborts.
reset_roots
echo foreign >"$CODEX_AGENTS"
expect_exit 1 "foreign codex" "$INSTALL" --rules --agents
assert_contains "$CODEX_AGENTS" "foreign"
ok "foreign Codex AGENTS.md abort"

# Bundled skill overlap exits 2 but still links.
reset_roots
plant_bundled "$CLAUDE_BUNDLED_SKILLS" ingest
expect_exit 2 "claude bundled warning" "$INSTALL" --skills --claude
assert_link "$CLAUDE_SKILLS/ingest/SKILL.md" "$REPO_ROOT/skills/project-management/ingest/SKILL.md"
assert_contains "$WORKDIR/err" '"ingest" skill will override Claude Code'
ok "bundled warning"

# Claude scoped rule has paths; always-on rule does not.
reset_roots
expect_exit 0 "rules claude" "$INSTALL" --rules --claude
assert_contains "$CLAUDE_RULES/markdown-no-hard-wrap.md" "paths:"
assert_contains "$CLAUDE_RULES/markdown-no-hard-wrap.md" '  - "**/*.md"'
assert_not_contains "$CLAUDE_RULES/address-as-chris.md" "paths:"
ok "rule adapters"

# Stale managed rule file is pruned.
reset_roots
expect_exit 0 "prune setup" "$INSTALL" --rules --cursor
echo "$MANAGED_MARK" >"$CURSOR_RULES/stale-extra.mdc"
expect_exit 0 "prune" "$INSTALL" --rules --cursor
assert_missing "$CURSOR_RULES/stale-extra.mdc"
assert_managed "$CURSOR_RULES/address-as-chris.mdc"
ok "prune stale managed rule"

# Uninstall removes ours and leaves foreign files.
reset_roots
expect_exit 0 "uninstall setup" "$INSTALL" --cursor --claude --agents
echo foreign >"$CURSOR_RULES/not-ours.mdc"
echo keep >"$CLAUDE_RULES/extra.txt"
"$UNINSTALL" --cursor --claude --agents >/dev/null
assert_missing "$CURSOR_SKILLS/design-tool/SKILL.md"
assert_missing "$CURSOR_RULES/address-as-chris.mdc"
assert_missing "$CLAUDE_MD"
assert_missing "$CODEX_AGENTS"
assert_file "$CURSOR_RULES/not-ours.mdc"
assert_file "$CLAUDE_RULES/extra.txt"
ok "uninstall identity"

# Default uninstall skips cursor.
reset_roots
expect_exit 0 "default uninstall setup" "$INSTALL" --cursor --claude
"$UNINSTALL" >/dev/null
assert_link "$CURSOR_SKILLS/design-tool/SKILL.md" "$REPO_ROOT/skills/design-tool/SKILL.md"
assert_managed "$CURSOR_RULES/address-as-chris.mdc"
assert_missing "$CLAUDE_MD"
ok "default uninstall skips cursor"

echo "test-install: all passed"

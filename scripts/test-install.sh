#!/usr/bin/env bash
# Isolated checks for install.sh and uninstall.sh. Never writes to home roots.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
INSTALL="$REPO_ROOT/scripts/install.sh"
UNINSTALL="$REPO_ROOT/scripts/uninstall.sh"
MANAGED_MARK='<!-- managed-by: chrispalmo/agent-config -->'
MANAGED_SKILL_MARKER='.agent-config-managed'

WORKDIR="$(mktemp -d "${TMPDIR:-/tmp}/agent-config-install-test.XXXXXX")"
export CODEX_SKILLS="$WORKDIR/codex-home/skills"
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
  rm -rf "$WORKDIR/claude" "$WORKDIR/cursor" \
    "$CURSOR_BUNDLED_SKILLS" "$CLAUDE_BUNDLED_SKILLS" "$CODEX_BUNDLED_SKILLS" \
    "$CODEX_HOME" "$WORKDIR/codex"
  mkdir -p "$CODEX_SKILLS" "$CLAUDE_SKILLS" "$CURSOR_SKILLS" \
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
assert_skill() {
  local dest="$1" expected="$2" marker
  marker="$(dirname "$dest")/$MANAGED_SKILL_MARKER"
  [[ -f "$dest" && ! -L "$dest" ]] || fail "not a regular skill file: $dest"
  cmp -s "$dest" "$expected" || fail "$dest differs from $expected"
  [[ "$(<"$marker")" == "$expected" ]] || fail "$marker does not identify $expected"
}

plant_bundled() {
  local root="$1" name="$2"
  mkdir -p "$root/$name"
  echo bundled >"$root/$name/SKILL.md"
}

# Default install fills skills agents+claude and rules claude+codex; leaves cursor empty.
reset_roots
expect_exit 0 "default install" "$INSTALL"
assert_skill "$CODEX_SKILLS/design-tool/SKILL.md" "$REPO_ROOT/skills/design-tool/SKILL.md"
assert_skill "$CLAUDE_SKILLS/project-bootstrap/SKILL.md" "$REPO_ROOT/skills/project-management/project-bootstrap/SKILL.md"
cmp -s "$CODEX_SKILLS/project-audit/references/audit-rubric.md" \
  "$REPO_ROOT/skills/project-management/project-audit/references/audit-rubric.md" || fail "audit reference differs"
cmp -s "$CLAUDE_SKILLS/project-bootstrap/references/templates/AGENTS.md" \
  "$REPO_ROOT/skills/project-management/project-bootstrap/references/templates/AGENTS.md" || fail "bootstrap template differs"
assert_file "$CODEX_SKILLS/status-ledger/references/beads.md"
assert_managed "$CLAUDE_RULES/address-the-user.md"
assert_managed "$CLAUDE_RULES/markdown-no-hard-wrap.md"
assert_managed "$CLAUDE_MD"
assert_managed "$CODEX_AGENTS"
assert_contains "$CODEX_AGENTS" 'Call the user Chris. When directly replying to an agent-originated message, address the agent as "boss".'
assert_contains "$CODEX_AGENTS" "make the initial substantive reply and final result understandable on their own"
assert_contains "$CODEX_AGENTS" 'Always create `CLAUDE.md`'
assert_not_contains "$CODEX_AGENTS" "Do not hard-wrap Markdown prose"
assert_missing "$CURSOR_SKILLS/design-tool/SKILL.md"
assert_missing "$CURSOR_RULES/address-the-user.mdc"
ok "default install"

# Re-run is idempotent.
expect_exit 0 "idempotent re-run" "$INSTALL"
assert_managed "$CODEX_AGENTS"
ok "idempotent re-run"

# Reinstall replaces generated resources rather than retaining obsolete copies.
echo obsolete > "$CODEX_SKILLS/project-audit/references/obsolete-template.md"
expect_exit 0 "resource refresh" "$INSTALL" --skills --agents
assert_missing "$CODEX_SKILLS/project-audit/references/obsolete-template.md"
cmp -s "$CODEX_SKILLS/project-audit/references/audit-rubric.md" \
  "$REPO_ROOT/skills/project-management/project-audit/references/audit-rubric.md" || fail "refreshed audit reference differs"
ok "resource refresh"

# Retired owned skills are pruned by full installs; unrelated content survives.
mkdir -p "$CODEX_SKILLS/proofread" "$CODEX_SKILLS/foreign-retired"
echo retired > "$CODEX_SKILLS/proofread/SKILL.md"
echo "$REPO_ROOT/skills/proofread/SKILL.md" > "$CODEX_SKILLS/proofread/$MANAGED_SKILL_MARKER"
echo preserve > "$CODEX_SKILLS/proofread/operator-note.txt"
echo foreign > "$CODEX_SKILLS/foreign-retired/SKILL.md"
expect_exit 0 "retired skill prune" "$INSTALL" --skills --agents
assert_missing "$CODEX_SKILLS/proofread/SKILL.md"
assert_file "$CODEX_SKILLS/proofread/operator-note.txt"
assert_file "$CODEX_SKILLS/foreign-retired/SKILL.md"
ok "retired skill ownership"

# A rule rename retires managed old files and refreshes the combined rule source.
reset_roots
printf '%s\nold rule\n' "$MANAGED_MARK" > "$CURSOR_RULES/address-as-chris.mdc"
printf '%s\nold rule\n' "$MANAGED_MARK" > "$CLAUDE_RULES/address-as-chris.md"
printf '%s\n## address-as-chris\nold rule\n' "$MANAGED_MARK" > "$CODEX_AGENTS"
expect_exit 0 "address rule rename" "$INSTALL" --rules --cursor --claude --agents
assert_missing "$CURSOR_RULES/address-as-chris.mdc"
assert_missing "$CLAUDE_RULES/address-as-chris.md"
assert_managed "$CURSOR_RULES/address-the-user.mdc"
assert_managed "$CLAUDE_RULES/address-the-user.md"
assert_contains "$CODEX_AGENTS" "## address-the-user"
assert_not_contains "$CODEX_AGENTS" "## address-as-chris"
assert_contains "$CODEX_AGENTS" 'Call the user Chris. When directly replying to an agent-originated message, address the agent as "boss".'
reset_roots
printf '%s\nold rule\n' "$MANAGED_MARK" > "$CURSOR_RULES/address-as-chris.mdc"
printf 'foreign\n' > "$CLAUDE_RULES/address-the-user.md"
expect_exit 1 "address rename foreign clash" "$INSTALL" --rules --cursor --claude --agents
assert_contains "$CURSOR_RULES/address-as-chris.mdc" "old rule"
assert_contains "$CLAUDE_RULES/address-the-user.md" "foreign"
assert_missing "$CURSOR_RULES/address-the-user.mdc"
ok "address rule rename and preflight"

# --cursor writes Cursor-native skills and rules only.
reset_roots
expect_exit 0 "cursor install" "$INSTALL" --cursor
assert_skill "$CURSOR_SKILLS/design-tool/SKILL.md" "$REPO_ROOT/skills/design-tool/SKILL.md"
assert_managed "$CURSOR_RULES/address-the-user.mdc"
assert_managed "$CURSOR_RULES/markdown-no-hard-wrap.mdc"
assert_contains "$CURSOR_RULES/address-the-user.mdc" "alwaysApply: true"
assert_contains "$CURSOR_RULES/markdown-no-hard-wrap.mdc" "alwaysApply: false"
assert_contains "$CURSOR_RULES/markdown-no-hard-wrap.mdc" 'globs: **/*.md'
assert_missing "$CODEX_AGENTS"
assert_missing "$CLAUDE_MD"
ok "cursor install"

# Combined flags write all target roots.
reset_roots
expect_exit 0 "combined flags" "$INSTALL" --cursor --claude --agents
assert_skill "$CURSOR_SKILLS/design-tool/SKILL.md" "$REPO_ROOT/skills/design-tool/SKILL.md"
assert_skill "$CLAUDE_SKILLS/design-tool/SKILL.md" "$REPO_ROOT/skills/design-tool/SKILL.md"
assert_skill "$CODEX_SKILLS/design-tool/SKILL.md" "$REPO_ROOT/skills/design-tool/SKILL.md"
assert_managed "$CURSOR_RULES/address-the-user.mdc"
assert_managed "$CLAUDE_MD"
assert_managed "$CODEX_AGENTS"
ok "combined flags"

# --package interview installs only the complete skills package.
reset_roots
expect_exit 0 "package interview" "$INSTALL" --package interview --agents
assert_skill "$CODEX_SKILLS/interview/SKILL.md" "$REPO_ROOT/skills/interview/SKILL.md"
assert_skill "$CODEX_SKILLS/reverse-brief/SKILL.md" "$REPO_ROOT/skills/interview/reverse-brief/SKILL.md"
assert_missing "$CODEX_SKILLS/design-tool/SKILL.md"
assert_missing "$CODEX_AGENTS"
ok "package interview"

# A package install does not prune other owned skills.
mkdir -p "$CODEX_SKILLS/proofread"
echo retired > "$CODEX_SKILLS/proofread/SKILL.md"
echo "$REPO_ROOT/skills/proofread/SKILL.md" > "$CODEX_SKILLS/proofread/$MANAGED_SKILL_MARKER"
expect_exit 0 "package preserves other skills" "$INSTALL" --package interview --agents
assert_file "$CODEX_SKILLS/proofread/SKILL.md"
ok "package preserves other skills"

# Coordination is an all-member package; resources and rules remain distinct.
reset_roots
expect_exit 0 "coordination package" "$INSTALL" --skills --package coordination --cursor --claude --agents
for root in "$CODEX_SKILLS" "$CLAUDE_SKILLS" "$CURSOR_SKILLS"; do
  for member in triage propose-tasks delegate harness; do
    assert_skill "$root/$member/SKILL.md" "$REPO_ROOT/skills/$member/SKILL.md"
  done
  cmp -s "$root/harness/references/native-claude.md" "$REPO_ROOT/skills/harness/references/native-claude.md" || fail "Claude adapter differs"
  assert_file "$root/harness/references/usage-and-recovery.md"
  assert_missing "$root/harness/references/evidence.md"
  assert_file "$root/delegate/references/skill-invocation.md"
  assert_file "$root/delegate/references/model-control.md"
  assert_contains "$root/triage/agents/openai.yaml" "allow_implicit_invocation: false"
  assert_contains "$root/harness/agents/openai.yaml" "allow_implicit_invocation: false"
done
assert_missing "$CODEX_AGENTS"
assert_missing "$CLAUDE_MD"
assert_missing "$CODEX_SKILLS/design-tool/SKILL.md"
reset_roots
mkdir -p "$CLAUDE_SKILLS/harness"
echo foreign > "$CLAUDE_SKILLS/harness/SKILL.md"
expect_exit 1 "coordination foreign clash" "$INSTALL" --package coordination --cursor --claude --agents
assert_contains "$CLAUDE_SKILLS/harness/SKILL.md" foreign
assert_missing "$CODEX_SKILLS/triage/SKILL.md"
assert_missing "$CURSOR_SKILLS/delegate/SKILL.md"
ok "coordination package, resources, policy, and preflight"

# Foreign skill destination aborts before any writes.
reset_roots
mkdir -p "$CODEX_SKILLS/design-tool"
echo foreign >"$CODEX_SKILLS/design-tool/SKILL.md"
expect_exit 1 "foreign skill" "$INSTALL" --agents
assert_contains "$CODEX_SKILLS/design-tool/SKILL.md" "foreign"
assert_missing "$CODEX_AGENTS"
ok "foreign skill abort"

# New supporting resources cannot overwrite an unmanaged destination.
reset_roots
mkdir -p "$CODEX_SKILLS/project-audit/references"
cp "$REPO_ROOT/skills/project-management/project-audit/SKILL.md" "$CODEX_SKILLS/project-audit/SKILL.md"
echo "$REPO_ROOT/skills/project-management/project-audit/SKILL.md" > "$CODEX_SKILLS/project-audit/$MANAGED_SKILL_MARKER"
echo foreign > "$CODEX_SKILLS/project-audit/references/operator-note.txt"
expect_exit 1 "foreign resource" "$INSTALL" --agents
assert_contains "$CODEX_SKILLS/project-audit/references/operator-note.txt" "foreign"
assert_missing "$CODEX_SKILLS/design-tool/SKILL.md"
ok "foreign resource abort"

# A resource ownership marker cannot redirect cleanup outside its skill.
reset_roots
expect_exit 0 "resource marker setup" "$INSTALL" --skills --agents
echo ../outside > "$CODEX_SKILLS/project-audit/.agent-config-resources"
mkdir -p "$CODEX_SKILLS/outside"
echo preserve > "$CODEX_SKILLS/outside/operator-note.txt"
expect_exit 1 "invalid resource marker" "$INSTALL" --skills --agents
assert_contains "$CODEX_SKILLS/outside/operator-note.txt" "preserve"
ok "resource marker boundary"

# Foreign Codex AGENTS.md aborts.
reset_roots
echo foreign >"$CODEX_AGENTS"
expect_exit 1 "foreign codex" "$INSTALL" --rules --agents
assert_contains "$CODEX_AGENTS" "foreign"
ok "foreign Codex AGENTS.md abort"

# Bundled skill overlap exits 2 but still installs.
reset_roots
plant_bundled "$CLAUDE_BUNDLED_SKILLS" ingest
expect_exit 2 "claude bundled warning" "$INSTALL" --skills --claude
assert_skill "$CLAUDE_SKILLS/ingest/SKILL.md" "$REPO_ROOT/skills/project-management/ingest/SKILL.md"
assert_contains "$WORKDIR/err" '"ingest" skill will override Claude Code'
ok "bundled warning"

# Claude scoped rule has paths; always-on rule does not.
reset_roots
expect_exit 0 "rules claude" "$INSTALL" --rules --claude
assert_contains "$CLAUDE_RULES/markdown-no-hard-wrap.md" "paths:"
assert_contains "$CLAUDE_RULES/markdown-no-hard-wrap.md" '  - "**/*.md"'
assert_not_contains "$CLAUDE_RULES/address-the-user.md" "paths:"
ok "rule adapters"

# Stale managed rule file is pruned.
reset_roots
expect_exit 0 "prune setup" "$INSTALL" --rules --cursor
echo "$MANAGED_MARK" >"$CURSOR_RULES/stale-extra.mdc"
expect_exit 0 "prune" "$INSTALL" --rules --cursor
assert_missing "$CURSOR_RULES/stale-extra.mdc"
assert_managed "$CURSOR_RULES/address-the-user.mdc"
ok "prune stale managed rule"

# Uninstall removes ours and leaves foreign files.
reset_roots
expect_exit 0 "uninstall setup" "$INSTALL" --cursor --claude --agents
echo foreign >"$CURSOR_RULES/not-ours.mdc"
echo keep >"$CLAUDE_RULES/extra.txt"
"$UNINSTALL" --cursor --claude --agents >/dev/null
assert_missing "$CURSOR_SKILLS/design-tool/SKILL.md"
assert_missing "$CODEX_SKILLS/project-bootstrap/references"
assert_missing "$CODEX_SKILLS/status-ledger/references"
assert_missing "$CURSOR_RULES/address-the-user.mdc"
assert_missing "$CLAUDE_MD"
assert_missing "$CODEX_AGENTS"
assert_file "$CURSOR_RULES/not-ours.mdc"
assert_file "$CLAUDE_RULES/extra.txt"
ok "uninstall identity"

# Default uninstall skips cursor.
reset_roots
expect_exit 0 "default uninstall setup" "$INSTALL" --cursor --claude
"$UNINSTALL" >/dev/null
assert_skill "$CURSOR_SKILLS/design-tool/SKILL.md" "$REPO_ROOT/skills/design-tool/SKILL.md"
assert_managed "$CURSOR_RULES/address-the-user.mdc"
assert_missing "$CLAUDE_MD"
ok "default uninstall skips cursor"

echo "test-install: all passed"

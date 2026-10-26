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
export SHARED_SKILLS="$WORKDIR/shared/skills"
export CURSOR_NATIVE_SKILLS="$WORKDIR/legacy-cursor/skills"
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
    "$WORKDIR/shared" "$WORKDIR/legacy-cursor" \
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

# Default install fills skills and rules for Cursor, Claude, and Codex.
reset_roots
expect_exit 0 "default install" "$INSTALL"
assert_skill "$CODEX_SKILLS/design-tool/SKILL.md" "$REPO_ROOT/skills/design-tool/SKILL.md"
assert_skill "$CLAUDE_SKILLS/project-bootstrap/SKILL.md" "$REPO_ROOT/skills/project-management/project-bootstrap/SKILL.md"
cmp -s "$CODEX_SKILLS/project-audit/references/audit-rubric.md" \
  "$REPO_ROOT/skills/project-management/project-audit/references/audit-rubric.md" || fail "audit reference differs"
cmp -s "$CLAUDE_SKILLS/project-bootstrap/references/templates/AGENTS.md" \
  "$REPO_ROOT/skills/project-management/project-bootstrap/references/templates/AGENTS.md" || fail "bootstrap template differs"
assert_file "$CODEX_SKILLS/status-ledger/references/EXPLORATION_BACKLOG.md"
assert_managed "$CLAUDE_RULES/address-the-user.md"
assert_managed "$CLAUDE_RULES/markdown-no-hard-wrap.md"
assert_managed "$CLAUDE_MD"
assert_managed "$CODEX_AGENTS"
assert_contains "$CODEX_AGENTS" 'Call the user Chris. When directly replying to an agent-originated message, address the agent as "boss".'
assert_contains "$CODEX_AGENTS" "make the initial substantive reply and final result understandable on their own"
assert_contains "$CODEX_AGENTS" 'Always create `CLAUDE.md`'
assert_not_contains "$CODEX_AGENTS" "Do not hard-wrap Markdown prose"
assert_skill "$CURSOR_SKILLS/design-tool/SKILL.md" "$REPO_ROOT/skills/design-tool/SKILL.md"
for root in "$CODEX_SKILLS" "$CLAUDE_SKILLS" "$CURSOR_SKILLS"; do
  while IFS= read -r path; do
    [[ -n "$path" && "$path" != \#* ]] || continue
    name="${path##*/}"
    for resource in references assets scripts agents; do
      [[ -d "$REPO_ROOT/skills/$path/$resource" ]] || continue
      diff -r "$REPO_ROOT/skills/$path/$resource" "$root/$name/$resource" >/dev/null || fail "$name/$resource differs"
    done
  done < "$REPO_ROOT/skills/skills.manifest"
  assert_missing "$root/ingest/SKILL.md"
done
assert_managed "$CURSOR_RULES/address-the-user.mdc"
assert_managed "$CURSOR_RULES/conversation-titles.mdc"
assert_contains "$CURSOR_RULES/conversation-titles.mdc" "alwaysApply: true"
ok "default install"

# Re-run is idempotent.
expect_exit 0 "idempotent re-run" "$INSTALL"
assert_managed "$CODEX_AGENTS"
ok "idempotent re-run"

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

# Shared-root installation upgrades file-only links and removes owned native
# duplicates, including retired skills, while preserving foreign installations.
reset_roots
mkdir -p "$SHARED_SKILLS/project-audit" "$CURSOR_NATIVE_SKILLS/design-tool" "$CODEX_SKILLS/plaintext" "$CODEX_SKILLS/ingest" "$SHARED_SKILLS/proofread" "$CURSOR_NATIVE_SKILLS/foreign"
ln -s "$REPO_ROOT/skills/project-management/project-audit/SKILL.md" "$SHARED_SKILLS/project-audit/SKILL.md"
ln -s "$REPO_ROOT/skills/design-tool/SKILL.md" "$CURSOR_NATIVE_SKILLS/design-tool/SKILL.md"
ln -s "$REPO_ROOT/skills/plaintext/SKILL.md" "$CODEX_SKILLS/plaintext/SKILL.md"
ln -s "$REPO_ROOT/skills/project-management/ingest/SKILL.md" "$CODEX_SKILLS/ingest/SKILL.md"
ln -s "$REPO_ROOT/skills/proofread/SKILL.md" "$SHARED_SKILLS/proofread/SKILL.md"
echo preserve > "$CURSOR_NATIVE_SKILLS/foreign/SKILL.md"
expect_exit 0 "shared root migration" env CURSOR_SKILLS="$SHARED_SKILLS" CODEX_SKILLS="$SHARED_SKILLS" "$INSTALL" --skills --cursor --agents
assert_skill "$SHARED_SKILLS/project-audit/SKILL.md" "$REPO_ROOT/skills/project-management/project-audit/SKILL.md"
assert_file "$SHARED_SKILLS/project-audit/references/audit-rubric.md"
assert_file "$SHARED_SKILLS/plaintext/agents/openai.yaml"
assert_missing "$CURSOR_NATIVE_SKILLS/design-tool/SKILL.md"
assert_missing "$CODEX_SKILLS/plaintext/SKILL.md"
assert_missing "$CODEX_SKILLS/ingest/SKILL.md"
assert_missing "$SHARED_SKILLS/proofread/SKILL.md"
assert_contains "$CURSOR_NATIVE_SKILLS/foreign/SKILL.md" preserve
expect_exit 0 "shared root idempotence" env CURSOR_SKILLS="$SHARED_SKILLS" CODEX_SKILLS="$SHARED_SKILLS" "$INSTALL" --skills --cursor --agents
ok "shared root migration and preservation"

# Resource conflicts at the shared destination abort before native cleanup.
reset_roots
mkdir -p "$SHARED_SKILLS/project-audit/references" "$CURSOR_NATIVE_SKILLS/design-tool"
ln -s "$REPO_ROOT/skills/project-management/project-audit/SKILL.md" "$SHARED_SKILLS/project-audit/SKILL.md"
ln -s "$REPO_ROOT/skills/design-tool/SKILL.md" "$CURSOR_NATIVE_SKILLS/design-tool/SKILL.md"
echo preserve > "$SHARED_SKILLS/project-audit/references/foreign.md"
expect_exit 1 "shared root foreign resource" env CURSOR_SKILLS="$SHARED_SKILLS" CODEX_SKILLS="$SHARED_SKILLS" "$INSTALL" --skills --cursor --agents
assert_file "$CURSOR_NATIVE_SKILLS/design-tool/SKILL.md"
assert_contains "$SHARED_SKILLS/project-audit/references/foreign.md" preserve
ok "migration preflight"

# A foreign skill with a selected name in a former native root must not be
# silently duplicated or removed during migration.
reset_roots
mkdir -p "$CURSOR_NATIVE_SKILLS/design-tool"
echo preserve > "$CURSOR_NATIVE_SKILLS/design-tool/SKILL.md"
expect_exit 1 "foreign native duplicate" env CURSOR_SKILLS="$SHARED_SKILLS" CODEX_SKILLS="$SHARED_SKILLS" "$INSTALL" --skills --cursor --agents
assert_contains "$CURSOR_NATIVE_SKILLS/design-tool/SKILL.md" preserve
assert_missing "$SHARED_SKILLS/design-tool/SKILL.md"
ok "foreign native duplicate abort"

# --all includes Cursor, including the rule that previously drifted.
reset_roots
expect_exit 0 "all targets" "$INSTALL" --all
for root in "$CURSOR_SKILLS" "$CLAUDE_SKILLS" "$CODEX_SKILLS"; do
  assert_skill "$root/design-tool/SKILL.md" "$REPO_ROOT/skills/design-tool/SKILL.md"
done
assert_managed "$CURSOR_RULES/conversation-titles.mdc"
assert_managed "$CLAUDE_RULES/conversation-titles.md"
assert_contains "$CODEX_AGENTS" "## conversation-titles"
ok "all targets"

# Explicit targets still avoid installing to Cursor.
reset_roots
expect_exit 0 "explicit Claude and Codex" "$INSTALL" --claude --agents
assert_managed "$CLAUDE_MD"
assert_managed "$CODEX_AGENTS"
assert_missing "$CURSOR_SKILLS/design-tool/SKILL.md"
assert_missing "$CURSOR_RULES/conversation-titles.mdc"
ok "explicit target isolation"

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
    assert_skill "$root/$member/SKILL.md" "$REPO_ROOT/skills/coordination/$member/SKILL.md"
  done
  cmp -s "$root/harness/references/native-claude.md" "$REPO_ROOT/skills/coordination/harness/references/native-claude.md" || fail "Claude adapter differs"
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
expect_exit 1 "coordination member selector" "$INSTALL" --skill coordination/triage --agents

# Moving sources into their package preserves names and refreshes owned markers.
for root in "$CODEX_SKILLS" "$CLAUDE_SKILLS" "$CURSOR_SKILLS"; do
  for member in triage propose-tasks delegate harness; do
    printf '%s\n' "$REPO_ROOT/skills/$member/SKILL.md" > "$root/$member/$MANAGED_SKILL_MARKER"
  done
done
expect_exit 0 "coordination source relocation" "$INSTALL" --package coordination --cursor --claude --agents
for root in "$CODEX_SKILLS" "$CLAUDE_SKILLS" "$CURSOR_SKILLS"; do
  for member in triage propose-tasks delegate harness; do
    assert_skill "$root/$member/SKILL.md" "$REPO_ROOT/skills/coordination/$member/SKILL.md"
    assert_contains "$root/$member/$MANAGED_SKILL_MARKER" "$REPO_ROOT/skills/coordination/$member/SKILL.md"
  done
done
# A source from another checkout cannot use the relocation allowance.
printf '%s\n' "$REPO_ROOT/skills/triage/SKILL.md" > "$CURSOR_SKILLS/triage/$MANAGED_SKILL_MARKER"
printf '%s\n' "/foreign/skills/harness/SKILL.md" > "$CLAUDE_SKILLS/harness/$MANAGED_SKILL_MARKER"
expect_exit 1 "foreign source relocation" "$INSTALL" --package coordination --cursor --claude --agents
assert_contains "$CURSOR_SKILLS/triage/$MANAGED_SKILL_MARKER" "$REPO_ROOT/skills/triage/SKILL.md"
assert_contains "$CLAUDE_SKILLS/harness/$MANAGED_SKILL_MARKER" "/foreign/skills/harness/SKILL.md"
reset_roots
mkdir -p "$CLAUDE_SKILLS/harness"
echo foreign > "$CLAUDE_SKILLS/harness/SKILL.md"
expect_exit 1 "coordination foreign clash" "$INSTALL" --package coordination --cursor --claude --agents
assert_contains "$CLAUDE_SKILLS/harness/SKILL.md" foreign
assert_missing "$CODEX_SKILLS/triage/SKILL.md"
assert_missing "$CURSOR_SKILLS/delegate/SKILL.md"
ok "coordination package, resources, policy, and preflight"

# A single independent skill installs across all targets without touching drafts,
# unrelated owned skills, or rules. Package members still install together.
reset_roots
mkdir -p "$CODEX_SKILLS/retired-example"
echo preserved > "$CODEX_SKILLS/retired-example/SKILL.md"
echo "$REPO_ROOT/skills/retired-example/SKILL.md" > "$CODEX_SKILLS/retired-example/$MANAGED_SKILL_MARKER"
expect_exit 0 "single skill" "$INSTALL" --skill plaintext --cursor --claude --agents
for root in "$CODEX_SKILLS" "$CLAUDE_SKILLS" "$CURSOR_SKILLS"; do
  assert_skill "$root/plaintext/SKILL.md" "$REPO_ROOT/skills/plaintext/SKILL.md"
done
assert_contains "$CODEX_SKILLS/retired-example/SKILL.md" preserved
assert_missing "$CODEX_AGENTS"
expect_exit 0 "single skill re-run" "$INSTALL" --skill plaintext --agents
assert_skill "$CODEX_SKILLS/plaintext/SKILL.md" "$REPO_ROOT/skills/plaintext/SKILL.md"
expect_exit 1 "unknown skill" "$INSTALL" --skill no-such-skill --agents
expect_exit 1 "package member" "$INSTALL" --skill interview --agents
expect_exit 1 "mixed selectors" "$INSTALL" --skill plaintext --package interview --agents
expect_exit 1 "missing skill argument" "$INSTALL" --skill
expect_exit 1 "duplicate skill selector" "$INSTALL" --skill plaintext --skill github-init
expect_exit 1 "rules-only single skill" "$INSTALL" --rules --skill plaintext --agents
expect_exit 1 "unregistered draft excluded" "$INSTALL" --skill draft-example --agents
reset_roots
mkdir -p "$CLAUDE_SKILLS/plaintext"
echo foreign > "$CLAUDE_SKILLS/plaintext/SKILL.md"
expect_exit 1 "single skill foreign clash" "$INSTALL" --skill plaintext --cursor --claude --agents
assert_contains "$CLAUDE_SKILLS/plaintext/SKILL.md" foreign
assert_missing "$CURSOR_SKILLS/plaintext/SKILL.md"
assert_missing "$CODEX_SKILLS/plaintext/SKILL.md"
ok "single skill selection, preservation, and preflight"

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
plant_bundled "$CLAUDE_BUNDLED_SKILLS" design-tool
expect_exit 2 "claude bundled warning" "$INSTALL" --skills --claude
assert_skill "$CLAUDE_SKILLS/design-tool/SKILL.md" "$REPO_ROOT/skills/design-tool/SKILL.md"
assert_contains "$WORKDIR/err" '"design-tool" skill will override Claude Code'
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

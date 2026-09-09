#!/usr/bin/env bash
# Install skills and rules for Cursor, Claude Code, and OpenAI Codex.
set -euo pipefail

SCRIPT_NAME="install"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
# shellcheck source=common.sh
source "$REPO_ROOT/scripts/common.sh"

usage() {
  cat <<'USAGE'
Usage: ./scripts/install.sh [--skills|--rules] [--all|--cursor|--claude|--agents]
                            [--package <name>] [-h|--help]

Install agent-config skills and rules.

  --skills    install only skills
  --rules     install only rules
  --all       default agent targets: Claude + Codex (default)
  --cursor    Cursor native roots
  --claude    Claude Code roots
  --agents    Codex roots
  --codex     alias for --agents
  --package   install one complete skills package

Agent flags combine: --cursor --claude --agents installs every target.
Without --skills/--rules, both artifacts are installed.
USAGE
}

WANTS_SKILLS=0
WANTS_RULES=0
ARTIFACT_FLAGS=0
WANTS_CURSOR=0
WANTS_CLAUDE=0
WANTS_AGENTS=0
TARGET_FLAGS=0
ALL_TARGETS=0
PACKAGE=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --skills) WANTS_SKILLS=1; ARTIFACT_FLAGS=$((ARTIFACT_FLAGS + 1)) ;;
    --rules) WANTS_RULES=1; ARTIFACT_FLAGS=$((ARTIFACT_FLAGS + 1)) ;;
    --all) ALL_TARGETS=1 ;;
    --cursor) WANTS_CURSOR=1; TARGET_FLAGS=$((TARGET_FLAGS + 1)) ;;
    --claude) WANTS_CLAUDE=1; TARGET_FLAGS=$((TARGET_FLAGS + 1)) ;;
    --agents|--codex) WANTS_AGENTS=1; TARGET_FLAGS=$((TARGET_FLAGS + 1)) ;;
    --package)
      shift
      [[ $# -gt 0 ]] || die "--package requires a name"
      [[ -z "$PACKAGE" ]] || die "--package may be specified only once"
      PACKAGE="$1"
      ;;
    -h|--help) usage; exit 0 ;;
    *) die "unknown option: $1 (try --help)" ;;
  esac
  shift
done

[[ $ALL_TARGETS -eq 0 || $TARGET_FLAGS -eq 0 ]] || die "--all cannot be combined with an agent target"

if [[ -n "$PACKAGE" ]]; then
  [[ "$PACKAGE" =~ ^[a-z0-9-]+$ ]] || die "invalid package name: $PACKAGE"
  if [[ $WANTS_RULES -eq 1 && $WANTS_SKILLS -eq 0 ]]; then
    die "--package is only valid with skills"
  fi
  if [[ $ARTIFACT_FLAGS -eq 0 ]]; then
    WANTS_SKILLS=1
    WANTS_RULES=0
  fi
fi

if [[ $ARTIFACT_FLAGS -eq 0 && -z "$PACKAGE" ]]; then
  WANTS_SKILLS=1
  WANTS_RULES=1
fi

if [[ $ALL_TARGETS -eq 1 || $TARGET_FLAGS -eq 0 ]]; then
  WANTS_CLAUDE=1
  WANTS_AGENTS=1
fi

package_contains() {
  local wanted_path="$1" name path extra
  while read -r name path extra || [[ -n "${name:-}" ]]; do
    [[ -z "${name:-}" || "$name" == \#* ]] && continue
    [[ "$name" == "$PACKAGE" && "$path" == "$wanted_path" ]] && return 0
  done < "$PACKAGES_MANIFEST"
  return 1
}

load_skills() {
  local line path
  SKILLS=()
  [[ -f "$SKILLS_MANIFEST" ]] || die "missing $SKILLS_MANIFEST"
  [[ -f "$PACKAGES_MANIFEST" ]] || die "missing $PACKAGES_MANIFEST"
  [[ -f "$BUNDLED_MANIFEST" ]] || die "missing $BUNDLED_MANIFEST"
  if [[ -n "$PACKAGE" ]]; then
    if ! awk -v package="$PACKAGE" '$1 == package { found=1 } END { exit !found }' "$PACKAGES_MANIFEST"; then
      die "unknown package: $PACKAGE"
    fi
  fi
  while IFS= read -r line || [[ -n "$line" ]]; do
    path="$(trim_line "$line")"
    [[ -z "$path" ]] && continue
    [[ -z "$PACKAGE" ]] || package_contains "$path" || continue
    SKILLS+=("$path")
  done < "$SKILLS_MANIFEST"
  [[ ${#SKILLS[@]} -gt 0 ]] || die "package ${PACKAGE:-all} contains no registered skills"
}

load_rules() {
  local path src dir_name
  read_manifest_file "$RULES_MANIFEST" RULES
  KEEP_RULE_NAMES=()
  RULE_FILE_NAMES=()
  RULE_ALWAYS=()
  RULE_DESC=()
  RULE_GLOBS_ARR=()
  RULE_BODIES=()
  for path in "${RULES[@]}"; do
    src="$RULES_ROOT/$path/RULE.md"
    parse_rule "$src"
    dir_name="${path##*/}"
    if [[ -n "$RULE_NAME" && "$RULE_NAME" != "$dir_name" ]]; then
      die "$path: frontmatter name '$RULE_NAME' != directory '$dir_name'"
    fi
    KEEP_RULE_NAMES+=("$dir_name")
    RULE_FILE_NAMES+=("$dir_name")
    RULE_ALWAYS+=("$RULE_ALWAYS_APPLY")
    RULE_DESC+=("$RULE_DESCRIPTION")
    RULE_GLOBS_ARR+=("$RULE_GLOBS")
    RULE_BODIES+=("$RULE_BODY")
  done
}

add_bundled_from_dir() {
  local dest_var="$1" root="$2" d name
  [[ -n "$root" && -d "$root" ]] || return 0
  for d in "$root"/*/SKILL.md "$root"/.system/*/SKILL.md; do
    [[ -e "$d" || -L "$d" ]] || continue
    name="$(basename "$(dirname "$d")")"
    eval "$dest_var+=(\"\$name\")"
  done
}

name_listed() {
  local want="$1" n
  shift
  for n in "$@"; do
    [[ "$n" == "$want" ]] && return 0
  done
  return 1
}

preflight_dir() {
  local dest="$1"
  [[ ( ! -e "$dest" && ! -L "$dest" ) || -d "$dest" ]] || die "$dest exists and is not a directory"
}

preflight_skill_dest() {
  local src="$1" dest_dir="$2" dest target marker_source
  local dest="$dest_dir/SKILL.md"
  [[ -f "$src" ]] || die "missing $src (check skills.manifest)"
  if [[ -L "$dest" ]]; then
    target="$(readlink "$dest")"
    if [[ "$target" == "$src" || "$target" == "$REPO_ROOT"/* ]]; then
      return
    else
      die "$dest_dir already exists and is not this repo's installation"
    fi
  elif [[ -f "$dest" && -f "$dest_dir/$MANAGED_SKILL_MARKER" ]]; then
    marker_source="$(<"$dest_dir/$MANAGED_SKILL_MARKER")"
    [[ "$marker_source" == "$src" ]] && return
    die "$dest_dir already exists and is not this repo's installation"
  elif [[ -e "$dest_dir" || -L "$dest_dir" ]]; then
    die "$dest_dir already exists and is not this repo's installation"
  fi
}

install_skill_to_root() {
  local dest_root="$1" path skill_name src dest_dir dest marker_source
  info "target $dest_root"
  mkdir -p "$dest_root"
  for path in "${SKILLS[@]}"; do
    skill_name="${path##*/}"
    src="$SKILLS_ROOT/$path/SKILL.md"
    dest_dir="$dest_root/$skill_name"
    dest="$dest_dir/SKILL.md"
    if [[ -f "$dest" && ! -L "$dest" && -f "$dest_dir/$MANAGED_SKILL_MARKER" ]]; then
      marker_source="$(<"$dest_dir/$MANAGED_SKILL_MARKER")"
      if [[ "$marker_source" == "$src" ]] && { [[ "$src" -ef "$dest" ]] || cmp -s "$src" "$dest"; }; then
        continue
      fi
    fi
    if [[ -L "$dest" ]]; then
      rm "$dest"
      info "migrated $skill_name"
    fi
    mkdir -p "$dest_dir"
    cp -p "$src" "$dest"
    printf '%s\n' "$src" > "$dest_dir/$MANAGED_SKILL_MARKER"
    info "installed $skill_name -> $dest"
  done
}

warn_skill_overlaps() {
  local path skill_name agent name extra warned=0
  CLAUDE_RESERVED=()
  CURSOR_RESERVED=()
  CODEX_RESERVED=()
  while read -r agent name extra || [[ -n "${agent:-}" ]]; do
    [[ -z "${agent:-}" || "$agent" == \#* ]] && continue
    case "$agent" in
      claude) CLAUDE_RESERVED+=("$name") ;;
      cursor) CURSOR_RESERVED+=("$name") ;;
      codex) CODEX_RESERVED+=("$name") ;;
    esac
  done < "$BUNDLED_MANIFEST"
  add_bundled_from_dir CURSOR_RESERVED "$CURSOR_BUNDLED_SKILLS"
  add_bundled_from_dir CLAUDE_RESERVED "$CLAUDE_BUNDLED_SKILLS"
  add_bundled_from_dir CODEX_RESERVED "$CODEX_BUNDLED_SKILLS"
  add_bundled_from_dir CODEX_RESERVED "$CODEX_HOME/skills/.system"
  add_bundled_from_dir CODEX_RESERVED "/etc/codex/skills"
  for path in "${SKILLS[@]}"; do
    skill_name="${path##*/}"
    if [[ $WANTS_CLAUDE -eq 1 ]] && name_listed "$skill_name" ${CLAUDE_RESERVED[@]+"${CLAUDE_RESERVED[@]}"}; then
      warn "\"$skill_name\" skill will override Claude Code's bundled /$skill_name"
      warned=1
    fi
    if [[ $WANTS_CURSOR -eq 1 || $WANTS_AGENTS -eq 1 ]] && name_listed "$skill_name" ${CURSOR_RESERVED[@]+"${CURSOR_RESERVED[@]}"}; then
      warn "\"$skill_name\" skill may hide or share /$skill_name with Cursor's built-in"
      warned=1
    fi
    if [[ $WANTS_AGENTS -eq 1 ]] && name_listed "$skill_name" ${CODEX_RESERVED[@]+"${CODEX_RESERVED[@]}"}; then
      warn "\"$skill_name\" skill may appear alongside Codex's system /$skill_name"
      warned=1
    fi
  done
  [[ $warned -eq 0 ]] || return 2
}

claude_paths_yaml() {
  local globs="$1" item
  local IFS=','
  set -f
  for item in $globs; do
    item="${item#"${item%%[![:space:]]*}"}"
    item="${item%"${item##*[![:space:]]}"}"
    item="${item#\"}"
    item="${item%\"}"
    [[ -n "$item" ]] || continue
    printf '  - "%s"\n' "$item"
  done
  set +f
}

emit_cursor_rule() {
  local name="$1" desc="$2" always="$3" globs="$4" body="$5"
  local dest="$CURSOR_RULES/$name.mdc"
  {
    echo "---"
    [[ -n "$desc" ]] && printf 'description: %s\n' "$desc"
    if [[ "$always" == 1 ]]; then
      echo "alwaysApply: true"
    else
      echo "alwaysApply: false"
      printf 'globs: %s\n' "$globs"
    fi
    echo "---"
    echo
    echo "$MANAGED_MARK"
    echo
    printf '%s' "$body"
    [[ "$body" == *$'\n' ]] || echo
  } | write_managed "$dest"
  info "wrote $dest"
}

emit_claude_rule() {
  local name="$1" always="$2" globs="$3" body="$4"
  local dest="$CLAUDE_RULES/$name.md"
  {
    if [[ "$always" != 1 ]]; then
      echo "---"
      echo "paths:"
      claude_paths_yaml "$globs"
      echo "---"
      echo
    fi
    echo "$MANAGED_MARK"
    echo
    printf '%s' "$body"
    [[ "$body" == *$'\n' ]] || echo
  } | write_managed "$dest"
  info "wrote $dest"
}

emit_claude_index() {
  {
    echo "$MANAGED_MARK"
    echo
    echo "# Personal Claude Code rules"
    echo
    echo "Generated by chrispalmo/agent-config. Edit RULE.md in that repo and re-run ./scripts/install.sh. Topic files live in ~/.claude/rules."
  } | write_managed "$CLAUDE_MD"
  info "wrote $CLAUDE_MD"
}

emit_codex_rules() {
  local i name always body n="${#RULE_FILE_NAMES[@]}"
  {
    echo "$MANAGED_MARK"
    echo
    echo "# Personal agent rules"
    echo
    echo "Generated by chrispalmo/agent-config. Edit RULE.md in that repo and re-run ./scripts/install.sh. Only always-on rules are included here."
    echo
    for i in $(seq 0 $((n - 1))); do
      always="${RULE_ALWAYS[$i]}"
      [[ "$always" == 1 ]] || continue
      name="${RULE_FILE_NAMES[$i]}"
      body="${RULE_BODIES[$i]}"
      echo "## $name"
      echo
      printf '%s' "$body"
      [[ "$body" == *$'\n' ]] || echo
      echo
    done
  } | write_managed "$CODEX_AGENTS"
  info "wrote $CODEX_AGENTS"
}

prune_managed_rules_dir() {
  local dir="$1" ext="$2" f base keep found
  [[ -d "$dir" ]] || return 0
  for f in "$dir"/*."$ext"; do
    [[ -e "$f" || -L "$f" ]] || continue
    is_managed_rule_file "$f" || continue
    base="$(basename "$f" ".$ext")"
    found=0
    for keep in "${KEEP_RULE_NAMES[@]+"${KEEP_RULE_NAMES[@]}"}"; do
      [[ "$keep" == "$base" ]] && found=1 && break
    done
    if [[ "$found" -eq 0 ]]; then
      rm "$f"
      info "pruned $f"
    fi
  done
}

SKILL_WARNING_STATUS=0
if [[ $WANTS_SKILLS -eq 1 ]]; then
  load_skills
fi
if [[ $WANTS_RULES -eq 1 ]]; then
  load_rules
fi

# Preflight every destination before writing anything.
if [[ $WANTS_SKILLS -eq 1 ]]; then
  SKILL_TARGET_ROOTS=()
  [[ $WANTS_CURSOR -eq 0 ]] || SKILL_TARGET_ROOTS+=("$CURSOR_SKILLS")
  [[ $WANTS_CLAUDE -eq 0 ]] || SKILL_TARGET_ROOTS+=("$CLAUDE_SKILLS")
  [[ $WANTS_AGENTS -eq 0 ]] || SKILL_TARGET_ROOTS+=("$CODEX_SKILLS")
  for root in "${SKILL_TARGET_ROOTS[@]}"; do
    preflight_dir "$root"
    for path in "${SKILLS[@]}"; do
      skill_name="${path##*/}"
      preflight_skill_dest "$SKILLS_ROOT/$path/SKILL.md" "$root/$skill_name"
    done
  done
fi
if [[ $WANTS_RULES -eq 1 ]]; then
  if [[ $WANTS_CURSOR -eq 1 ]]; then
    preflight_dir "$CURSOR_RULES"
    for name in "${RULE_FILE_NAMES[@]}"; do assert_managed_dest_writable "$CURSOR_RULES/$name.mdc"; done
  fi
  if [[ $WANTS_CLAUDE -eq 1 ]]; then
    preflight_dir "$CLAUDE_RULES"
    for name in "${RULE_FILE_NAMES[@]}"; do assert_managed_dest_writable "$CLAUDE_RULES/$name.md"; done
    assert_managed_dest_writable "$CLAUDE_MD"
  fi
  if [[ $WANTS_AGENTS -eq 1 ]]; then
    preflight_dir "$(dirname "$CODEX_AGENTS")"
    assert_managed_dest_writable "$CODEX_AGENTS"
  fi
fi

if [[ $WANTS_SKILLS -eq 1 ]]; then
  [[ $WANTS_CURSOR -eq 0 ]] || install_skill_to_root "$CURSOR_SKILLS"
  [[ $WANTS_CLAUDE -eq 0 ]] || install_skill_to_root "$CLAUDE_SKILLS"
  [[ $WANTS_AGENTS -eq 0 ]] || install_skill_to_root "$CODEX_SKILLS"
  warn_skill_overlaps || SKILL_WARNING_STATUS=$?
fi

if [[ $WANTS_RULES -eq 1 ]]; then
  if [[ $WANTS_CURSOR -eq 1 ]]; then
    info "target $CURSOR_RULES"
    mkdir -p "$CURSOR_RULES"
    for i in $(seq 0 $((${#RULE_FILE_NAMES[@]} - 1))); do
      emit_cursor_rule "${RULE_FILE_NAMES[$i]}" "${RULE_DESC[$i]}" "${RULE_ALWAYS[$i]}" "${RULE_GLOBS_ARR[$i]}" "${RULE_BODIES[$i]}"
    done
    prune_managed_rules_dir "$CURSOR_RULES" mdc
  fi
  if [[ $WANTS_CLAUDE -eq 1 ]]; then
    info "target $CLAUDE_RULES"
    mkdir -p "$CLAUDE_RULES"
    for i in $(seq 0 $((${#RULE_FILE_NAMES[@]} - 1))); do
      emit_claude_rule "${RULE_FILE_NAMES[$i]}" "${RULE_ALWAYS[$i]}" "${RULE_GLOBS_ARR[$i]}" "${RULE_BODIES[$i]}"
    done
    emit_claude_index
    prune_managed_rules_dir "$CLAUDE_RULES" md
  fi
  if [[ $WANTS_AGENTS -eq 1 ]]; then
    info "target $CODEX_AGENTS"
    mkdir -p "$(dirname "$CODEX_AGENTS")"
    emit_codex_rules
  fi
fi

info "done"
[[ $SKILL_WARNING_STATUS -eq 0 ]] || exit "$SKILL_WARNING_STATUS"

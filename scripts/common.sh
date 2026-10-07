# Shared helpers for install.sh, uninstall.sh, and test-install.sh.
# shellcheck shell=bash

MANAGED_MARK='<!-- managed-by: chrispalmo/agent-config -->'
OLD_RULES_MANAGED_MARK='<!-- managed-by: chrispalmo/rules -->'
MANAGED_SKILL_MARKER='.agent-config-managed'
MANAGED_RESOURCE_MARKER='.agent-config-resources'
SKILL_RESOURCE_DIRS=(references assets scripts agents)

SKILLS_ROOT="$REPO_ROOT/skills"
RULES_ROOT="$REPO_ROOT/rules"
SKILLS_MANIFEST="$SKILLS_ROOT/skills.manifest"
PACKAGES_MANIFEST="$SKILLS_ROOT/packages.manifest"
BUNDLED_MANIFEST="$SKILLS_ROOT/bundled-skills.manifest"
RULES_MANIFEST="$RULES_ROOT/rules.manifest"

CURSOR_SKILLS="${CURSOR_SKILLS:-$HOME/.cursor/skills}"
CLAUDE_SKILLS="${CLAUDE_SKILLS:-$HOME/.claude/skills}"
CURSOR_BUNDLED_SKILLS="${CURSOR_BUNDLED_SKILLS:-$HOME/.cursor/skills-cursor}"
CLAUDE_BUNDLED_SKILLS="${CLAUDE_BUNDLED_SKILLS:-}"
CODEX_BUNDLED_SKILLS="${CODEX_BUNDLED_SKILLS:-}"
CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
CODEX_SKILLS="${CODEX_SKILLS:-$CODEX_HOME/skills}"

CURSOR_RULES="${CURSOR_RULES:-$HOME/.cursor/rules}"
CLAUDE_RULES="${CLAUDE_RULES:-$HOME/.claude/rules}"
CLAUDE_MD="${CLAUDE_MD:-$HOME/.claude/CLAUDE.md}"
CODEX_AGENTS="${CODEX_AGENTS:-$HOME/.codex/AGENTS.md}"

die() { echo "$SCRIPT_NAME: error: $*" >&2; exit 1; }
info() { echo "$SCRIPT_NAME: $*"; }
warn() { echo "$SCRIPT_NAME: warning: $*" >&2; }

managed_skill_source() {
  local dir="$1" dest="$1/SKILL.md" marker="$1/$MANAGED_SKILL_MARKER" source
  [[ ! -L "$dir" ]] || return 1
  if [[ -L "$dest" ]]; then
    source="$(readlink "$dest")"
  elif [[ -f "$dest" && -f "$marker" && ! -L "$marker" ]]; then
    source="$(<"$marker")"
  else
    return 1
  fi
  [[ "$source" == "$SKILLS_ROOT/"*"/SKILL.md" ]] || return 1
  printf '%s' "$source"
}

preflight_skill_resources() {
  local dir="$1" marker="$1/$MANAGED_RESOURCE_MARKER" resource
  if [[ -e "$marker" || -L "$marker" ]]; then
    [[ -f "$marker" && ! -L "$marker" ]] || die "$marker is not a regular ownership file"
    while IFS= read -r resource || [[ -n "$resource" ]]; do
      name_listed "$resource" "${SKILL_RESOURCE_DIRS[@]}" || die "$marker lists an invalid resource"
      [[ ! -L "$dir/$resource" ]] || die "$dir/$resource is a symlink; will not overwrite"
      [[ ! -e "$dir/$resource" || -d "$dir/$resource" ]] || die "$dir/$resource is not a directory"
    done < "$marker"
  fi
}

remove_managed_skill() {
  local dir="$1" source resource marker="$1/$MANAGED_RESOURCE_MARKER"
  source="$(managed_skill_source "$dir")" || return 0
  preflight_skill_resources "$dir"
  if [[ -f "$marker" ]]; then
    while IFS= read -r resource || [[ -n "$resource" ]]; do
      rm -rf "$dir/$resource"
    done < "$marker"
    rm "$marker"
  fi
  rm "$dir/SKILL.md"
  [[ ! -f "$dir/$MANAGED_SKILL_MARKER" ]] || rm "$dir/$MANAGED_SKILL_MARKER"
  rmdir "$dir" 2>/dev/null || true
  info "removed ${dir##*/}"
}

name_listed() {
  local want="$1" n
  shift
  for n in "$@"; do
    [[ "$n" == "$want" ]] && return 0
  done
  return 1
}

trim_line() {
  local line="$1"
  line="${line%%#*}"
  line="${line#"${line%%[![:space:]]*}"}"
  line="${line%"${line##*[![:space:]]}"}"
  printf '%s' "$line"
}

read_manifest_file() {
  local manifest="$1" dest_name="$2" line trimmed
  local values=()
  [[ -f "$manifest" ]] || die "missing $manifest"
  while IFS= read -r line || [[ -n "${line:-}" ]]; do
    trimmed="$(trim_line "$line")"
    [[ -z "$trimmed" ]] && continue
    values+=("$trimmed")
  done < "$manifest"
  [[ ${#values[@]} -gt 0 ]] || die "$manifest is empty"
  eval "$dest_name=()"
  for value in "${values[@]}"; do
    eval "$dest_name+=(\"\$value\")"
  done
}

is_managed_rule_file() {
  [[ -f "$1" ]] && { grep -qF "$MANAGED_MARK" "$1" || grep -qF "$OLD_RULES_MANAGED_MARK" "$1"; }
}

assert_managed_dest_writable() {
  local dest="$1"
  if [[ -e "$dest" || -L "$dest" ]]; then
    [[ ! -L "$dest" ]] || die "$dest exists and is a symlink; will not overwrite"
    is_managed_rule_file "$dest" || die "$dest already exists and is not this repo's installation"
  fi
}

write_managed() {
  local dest="$1"
  mkdir -p "$(dirname "$dest")"
  cat > "$dest"
}

fm_field() {
  local file="$1" key="$2"
  awk -v key="$key" '
    BEGIN { n = 0 }
    /^---[ \t\r]*$/ {
      n++
      if (n >= 2) exit
      next
    }
    n == 1 && $0 ~ ("^" key ":[ \t]*") {
      line = $0
      sub(/\r$/, "", line)
      sub("^" key ":[ \t]*", "", line)
      sub(/[ \t]+$/, "", line)
      if (line ~ /^".*"$/ || line ~ /^'\''.*'\''$/) {
        line = substr(line, 2, length(line) - 2)
      }
      print line
      exit
    }
  ' "$file"
}

fm_body() {
  awk '
    BEGIN { n = 0; started = 0 }
    /^---[ \t\r]*$/ {
      n++
      next
    }
    n >= 2 {
      if (!started) {
        if ($0 ~ /^[ \t]*$/) next
        started = 1
      }
      print
    }
  ' "$1"
}

# Sets RULE_NAME RULE_DESCRIPTION RULE_ALWAYS_APPLY RULE_GLOBS RULE_BODY.
parse_rule() {
  local src="$1" first always
  [[ -f "$src" ]] || die "missing $src"
  first="$(head -n 1 "$src" | tr -d '\r')"
  [[ "$first" == "---" ]] || die "$src must start with YAML frontmatter (---)"

  RULE_NAME="$(fm_field "$src" name)"
  RULE_DESCRIPTION="$(fm_field "$src" description)"
  RULE_GLOBS="$(fm_field "$src" globs)"
  always="$(fm_field "$src" alwaysApply)"
  RULE_BODY="$(fm_body "$src")"

  case "$always" in
    true|True|TRUE|yes|Yes) RULE_ALWAYS_APPLY=1 ;;
    false|False|FALSE|no|No|"") RULE_ALWAYS_APPLY=0 ;;
    *) die "$src: invalid alwaysApply: $always" ;;
  esac

  if [[ "$RULE_ALWAYS_APPLY" != 1 && -z "$RULE_GLOBS" ]]; then
    die "$src: set alwaysApply: true or globs"
  fi
}

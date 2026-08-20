#!/usr/bin/env bash
# Cloud VM bootstrap for Cursor, Claude Code, and Codex environments.
set -euo pipefail

SCRIPT_NAME="bootstrap"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
# shellcheck source=../common.sh
source "$REPO_ROOT/scripts/common.sh"

if [[ -d "$REPO_ROOT/.git" ]]; then
  git -C "$REPO_ROOT" pull --ff-only || warn "could not update $REPO_ROOT (using checkout as-is)"
fi

info "installing agent-config"
"$REPO_ROOT/scripts/install.sh" --cursor --claude --agents

if [[ "$(uname -s)" != Darwin && -d /workspace ]]; then
  if [[ -L /.cursor && "$(readlink /.cursor)" == "$HOME/.cursor" ]]; then
    info "/.cursor already points at $HOME/.cursor"
  elif [[ -e /.cursor || -L /.cursor ]]; then
    warn "/.cursor exists and is not $HOME/.cursor; Cursor cloud may miss user rules"
  elif ln -sfn "$HOME/.cursor" /.cursor; then
    info "linked /.cursor -> $HOME/.cursor"
  else
    warn "could not create /.cursor -> $HOME/.cursor (Cursor cloud rules may not load)"
  fi
fi

info "done"

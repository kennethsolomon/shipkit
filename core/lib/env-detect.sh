#!/usr/bin/env bash
# env-detect.sh — Detect ShipKit runtime environment
#
# Sourceable shell helper. Sets these variables when sourced:
#
#   SHIPKIT_TARGET     "claude" | "codex" | "unknown"
#   SHIPKIT_ENV        "cli" | "cloud" | "unknown"     (only meaningful for codex)
#   SHIPKIT_HOOKS_OK   "yes" | "no"                    can the harness honor hooks?
#   SHIPKIT_MCP_OK     "yes" | "no"                    user-global MCP available?
#
# Skills can `source` this file and branch on the variables to degrade
# gracefully on Codex Cloud (no hooks, no user-global config).

set -u  # we don't set -e — sourcing should never abort the caller

# ── Target detection ────────────────────────────────────────────────────────
# Priority:
#   1. Explicit runtime env vars (most reliable — set by the executing harness)
#   2. Local CWD signals (AGENTS.md / CLAUDE.md / .codex/ / .claude/ in this repo)
#   3. User-home fallback (~/.codex/ exists ≠ Codex is the active executor)
SHIPKIT_TARGET="unknown"
if [[ -n "${CODEX_AGENT:-}${CODEX_SESSION_ID:-}" ]]; then
  SHIPKIT_TARGET="codex"
elif [[ -n "${CLAUDE_AGENT:-}${CLAUDE_SESSION_ID:-}" ]]; then
  SHIPKIT_TARGET="claude"
elif [[ -f "AGENTS.md" ]] || [[ -d ".codex" ]]; then
  SHIPKIT_TARGET="codex"
elif [[ -f "CLAUDE.md" ]] || [[ -d ".claude" ]]; then
  SHIPKIT_TARGET="claude"
elif [[ -d "${HOME:-/nowhere}/.codex" ]]; then
  SHIPKIT_TARGET="codex"
elif [[ -d "${HOME:-/nowhere}/.claude" ]]; then
  SHIPKIT_TARGET="claude"
fi

# ── Codex CLI vs Cloud ──────────────────────────────────────────────────────
# Cloud Web tasks run in disposable containers with restricted filesystem
# layout. Heuristics:
#   - No ~/.codex/ directory available (cloud doesn't surface user config)
#   - CODEX_CLOUD env variable is set by hosted environments
#   - /workspace or /app working directory (common cloud container layouts)
SHIPKIT_ENV="unknown"
if [[ "$SHIPKIT_TARGET" == "codex" ]]; then
  if [[ -n "${CODEX_CLOUD:-}" ]]; then
    SHIPKIT_ENV="cloud"
  elif [[ -d "${HOME:-/nowhere}/.codex" ]]; then
    SHIPKIT_ENV="cli"
  elif [[ "${PWD}" == /workspace* ]] || [[ "${PWD}" == /app* ]]; then
    SHIPKIT_ENV="cloud"
  else
    SHIPKIT_ENV="cli"  # default assumption when in doubt
  fi
fi

# ── Capability flags ────────────────────────────────────────────────────────
SHIPKIT_HOOKS_OK="yes"
SHIPKIT_MCP_OK="yes"

if [[ "$SHIPKIT_TARGET" == "codex" && "$SHIPKIT_ENV" == "cloud" ]]; then
  SHIPKIT_HOOKS_OK="no"  # cloud honors no hooks
  # MCP is "yes" if the cloud environment pre-wired some servers; we can't
  # detect that from here. Treat as yes; skills can check for specific servers.
fi

# ── Print summary (when run directly, not sourced) ──────────────────────────
if [[ "${BASH_SOURCE[0]:-$0}" == "${0}" ]]; then
  echo "SHIPKIT_TARGET=${SHIPKIT_TARGET}"
  echo "SHIPKIT_ENV=${SHIPKIT_ENV}"
  echo "SHIPKIT_HOOKS_OK=${SHIPKIT_HOOKS_OK}"
  echo "SHIPKIT_MCP_OK=${SHIPKIT_MCP_OK}"
fi

export SHIPKIT_TARGET SHIPKIT_ENV SHIPKIT_HOOKS_OK SHIPKIT_MCP_OK

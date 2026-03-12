#!/usr/bin/env bash
set -euo pipefail

# ─────────────────────────────────────────────
# claude-skills — Claude Code Plugin Installer
# ─────────────────────────────────────────────

PLUGIN_NAME="claude-skills"
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Detect Claude config directory per platform
detect_claude_dir() {
  if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" || -n "${WINDIR:-}" ]]; then
    # Windows (Git Bash / Cygwin)
    echo "${APPDATA}/Claude"
  elif [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    echo "${HOME}/.claude"
  else
    # Linux
    echo "${HOME}/.claude"
  fi
}

CLAUDE_DIR="$(detect_claude_dir)"
PLUGINS_DIR="${CLAUDE_DIR}/plugins"
TARGET="${PLUGINS_DIR}/${PLUGIN_NAME}"

echo ""
echo "claude-skills installer"
echo "─────────────────────────────────────────"
echo "Source : ${REPO_DIR}"
echo "Target : ${TARGET}"
echo ""

# Create plugins dir if it doesn't exist
mkdir -p "${PLUGINS_DIR}"

# If target already exists and is a symlink, remove and re-link
if [[ -L "${TARGET}" ]]; then
  echo "Removing existing symlink..."
  rm "${TARGET}"
fi

# If target is a real directory (manual install), warn and skip
if [[ -d "${TARGET}" && ! -L "${TARGET}" ]]; then
  echo "  ${TARGET} already exists as a real directory (not a symlink)."
  echo "   Remove it manually then re-run this script:"
  echo "   rm -rf \"${TARGET}\""
  exit 1
fi

# Create symlink
ln -s "${REPO_DIR}" "${TARGET}"
echo "Linked: ${TARGET}"
echo "      -> ${REPO_DIR}"
echo ""
echo "Installation complete."
echo ""
echo "Get started: open any project and run /setup-claude"

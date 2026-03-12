#!/usr/bin/env bash
set -euo pipefail

# ─────────────────────────────────────────────
# claude-skills — Uninstaller
# ─────────────────────────────────────────────
# Removes symlinks created by install.sh.
# Only removes symlinks pointing back to this repo.

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

detect_claude_dir() {
  if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" || -n "${WINDIR:-}" ]]; then
    echo "${APPDATA}/Claude"
  elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo "${HOME}/.claude"
  else
    echo "${HOME}/.claude"
  fi
}

CLAUDE_DIR="$(detect_claude_dir)"
SKILLS_DIR="${CLAUDE_DIR}/skills"
COMMANDS_DIR="${CLAUDE_DIR}/commands"

removed=0

# Remove skill symlinks that point to this repo
for target in "${SKILLS_DIR}"/*/; do
  [[ -L "${target%/}" ]] || continue
  link_dest="$(readlink "${target%/}")"
  if [[ "${link_dest}" == "${REPO_DIR}"* ]]; then
    rm "${target%/}"
    echo "  Removed: ${target%/}"
    removed=$((removed + 1))
  fi
done

# Remove command symlinks that point to this repo
for target in "${COMMANDS_DIR}"/*.md; do
  [[ -L "${target}" ]] || continue
  link_dest="$(readlink "${target}")"
  if [[ "${link_dest}" == "${REPO_DIR}"* ]]; then
    rm "${target}"
    echo "  Removed: ${target}"
    removed=$((removed + 1))
  fi
done

# Clean up old plugin symlink if it exists
OLD_PLUGIN="${CLAUDE_DIR}/plugins/claude-skills"
if [[ -L "${OLD_PLUGIN}" ]]; then
  rm "${OLD_PLUGIN}"
  echo "  Removed: ${OLD_PLUGIN} (legacy plugin symlink)"
  removed=$((removed + 1))
fi

echo ""
echo "Removed ${removed} symlinks. Uninstall complete."

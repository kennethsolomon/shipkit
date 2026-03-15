#!/usr/bin/env bash
set -euo pipefail

# ─────────────────────────────────────────────
# claude-skills — Claude Code Skills Installer
# ─────────────────────────────────────────────
# Symlinks skills into ~/.claude/skills/ and
# commands into ~/.claude/commands/ so they are
# globally available in every project.

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Detect Claude config directory per platform
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

echo ""
echo "claude-skills installer"
echo "─────────────────────────────────────────"
echo "Source : ${REPO_DIR}"
echo "Skills : ${SKILLS_DIR}"
echo "Commands: ${COMMANDS_DIR}"
echo ""

# Create target dirs
mkdir -p "${SKILLS_DIR}"
mkdir -p "${COMMANDS_DIR}"

# ── Clean stale symlinks ────────────────────
for stale in starter-setup claude-doctor laravel-setup-claude laravel-lint laravel-test laravel-write-tests; do
  if [[ -L "${SKILLS_DIR}/${stale}" ]]; then
    rm "${SKILLS_DIR}/${stale}"
    echo "  Cleaned stale: ${stale}"
  fi
done

for stale_cmd in re-setup.md re-setup-claude.md; do
  if [[ -L "${COMMANDS_DIR}/${stale_cmd}" ]]; then
    rm "${COMMANDS_DIR}/${stale_cmd}"
    echo "  Cleaned stale: ${stale_cmd}"
  fi
done

# ── Link skills ──────────────────────────────
skills_linked=0
skills_skipped=0

for skill_dir in "${REPO_DIR}"/skills/*/; do
  skill_name="$(basename "${skill_dir}")"
  target="${SKILLS_DIR}/${skill_name}"

  # Remove existing symlink (re-install)
  if [[ -L "${target}" ]]; then
    rm "${target}"
  fi

  # Skip if real directory exists (user-managed)
  if [[ -d "${target}" && ! -L "${target}" ]]; then
    echo "  SKIP  ${skill_name} (real directory exists, not a symlink)"
    skills_skipped=$((skills_skipped + 1))
    continue
  fi

  ln -s "${skill_dir%/}" "${target}"
  skills_linked=$((skills_linked + 1))
done

# ── Link commands ────────────────────────────
commands_linked=0
commands_skipped=0

for cmd_file in "${REPO_DIR}"/commands/*.md; do
  [[ -f "${cmd_file}" ]] || continue
  cmd_name="$(basename "${cmd_file}")"
  target="${COMMANDS_DIR}/${cmd_name}"

  # Remove existing symlink (re-install)
  if [[ -L "${target}" ]]; then
    rm "${target}"
  fi

  # Skip if real file exists (user-managed)
  if [[ -f "${target}" && ! -L "${target}" ]]; then
    echo "  SKIP  ${cmd_name} (real file exists, not a symlink)"
    commands_skipped=$((commands_skipped + 1))
    continue
  fi

  ln -s "${cmd_file}" "${target}"
  commands_linked=$((commands_linked + 1))
done

echo "Linked ${skills_linked} skills, ${commands_linked} commands"
if [[ ${skills_skipped} -gt 0 || ${commands_skipped} -gt 0 ]]; then
  echo "Skipped ${skills_skipped} skills, ${commands_skipped} commands (real dirs/files)"
fi
echo ""
echo "Installation complete."
echo ""
echo "Workflow commands:"
echo "  /setup-claude        bootstrap project scaffolding"
echo "  /brainstorm          explore requirements and design"
echo "  /frontend-design     UI mockup before implementation"
echo "  /write-plan          write decision-complete plan"
echo "  /branch              create feature branch from current task"
echo "  /write-tests         TDD: write failing tests (auto-detects stack)"
echo "  /execute-plan        implement plan in batches"
echo "  /smart-commit        conventional commit with approval"
echo "  /lint                auto-detect and run all linters"
echo "  /test                auto-detect and verify all tests pass"
echo "  /debug               bug fix entry point"
echo "  /security-check      OWASP security audit"
echo "  /review              self-review of branch changes"
echo "  /update-task         mark task done, log completion"
echo "  /finish-feature      changelog + PR creation"
echo "  /release             version bump + changelog + tag"
echo "  /status              show workflow + task status"
echo "  /setup-optimizer     enrich CLAUDE.md by scanning codebase"
echo ""
echo "Laravel:"
echo "  /laravel-init        configure existing Laravel project"
echo "  /laravel-new         scaffold new Laravel project"
echo ""
echo "Get started: open any project and run /setup-claude"

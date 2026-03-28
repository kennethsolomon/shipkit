#!/usr/bin/env bash
set -euo pipefail

# ─────────────────────────────────────────────
# ShipKit — Claude Code Workflow Toolkit
# ─────────────────────────────────────────────
# Symlinks skills into ~/.claude/skills/ and
# commands into ~/.claude/commands/sk/ so they
# are globally available in every project.

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Detect Claude config directory per platform
detect_claude_dir() {
  if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" || -n "${WINDIR:-}" ]]; then
    echo "${APPDATA}/Claude"
  else
    echo "${HOME}/.claude"
  fi
}

CLAUDE_DIR="$(detect_claude_dir)"
SKILLS_DIR="${CLAUDE_DIR}/skills"
COMMANDS_DIR="${CLAUDE_DIR}/commands/sk"

echo ""
echo "ShipKit installer"
echo "─────────────────────────────────────────"
echo "Source  : ${REPO_DIR}"
echo "Skills  : ${SKILLS_DIR}"
echo "Commands: ${COMMANDS_DIR}"
echo ""

# Create target dirs
mkdir -p "${SKILLS_DIR}"
mkdir -p "${COMMANDS_DIR}"

# ── Clean stale symlinks (pre-rebrand names) ─
stale_skills=(starter-setup claude-doctor laravel-setup-claude laravel-lint laravel-test laravel-write-tests accessibility api-design brainstorming debug features frontend-design laravel-init laravel-new lint perf release review schema-migrate setup-claude setup-optimizer skill-creator smart-commit test write-tests)
for stale in "${stale_skills[@]}"; do
  if [[ -L "${SKILLS_DIR}/${stale}" ]]; then
    rm "${SKILLS_DIR}/${stale}"
    echo "  Cleaned stale skill: ${stale}"
  fi
done

stale_commands=(re-setup.md re-setup-claude.md brainstorm.md branch.md execute-plan.md features.md finish-feature.md hotfix.md plan.md release.md security-check.md status.md update-task.md write-plan.md)
for stale_cmd in "${stale_commands[@]}"; do
  if [[ -L "${CLAUDE_DIR}/commands/${stale_cmd}" ]]; then
    rm "${CLAUDE_DIR}/commands/${stale_cmd}"
    echo "  Cleaned stale command: ${stale_cmd}"
  fi
done

# ── Link skills ──────────────────────────────
skills_linked=0
skills_skipped=0

for skill_dir in "${REPO_DIR}"/skills/*/; do
  skill_name="$(basename "${skill_dir}")"
  target="${SKILLS_DIR}/${skill_name}"

  if [[ -L "${target}" ]]; then
    rm "${target}"
  fi

  if [[ -d "${target}" && ! -L "${target}" ]]; then
    echo "  SKIP  ${skill_name} (real directory exists)"
    skills_skipped=$((skills_skipped + 1))
    continue
  fi

  ln -s "${skill_dir%/}" "${target}"
  skills_linked=$((skills_linked + 1))
done

# ── Link commands/sk/ ────────────────────────
commands_linked=0
commands_skipped=0

for cmd_file in "${REPO_DIR}"/commands/sk/*.md; do
  [[ -f "${cmd_file}" ]] || continue
  cmd_name="$(basename "${cmd_file}")"
  target="${COMMANDS_DIR}/${cmd_name}"

  if [[ -L "${target}" ]]; then
    rm "${target}"
  fi

  if [[ -f "${target}" && ! -L "${target}" ]]; then
    echo "  SKIP  ${cmd_name} (real file exists)"
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

# ── Install agent-browser (E2E testing) ──────
echo "Installing agent-browser for E2E testing (~100MB Chrome download on first run)..."
if command -v npm &>/dev/null; then
  if ! command -v agent-browser &>/dev/null; then
    npm install -g agent-browser
    agent-browser install
    echo "  agent-browser installed."
  else
    echo "  agent-browser already installed — skipping."
  fi
else
  echo "  WARN: npm not found. Install Node.js and then run:"
  echo "        npm install -g agent-browser && agent-browser install"
fi
echo ""

echo "Installation complete."
echo ""
echo "  /sk:autopilot       — Hands-free workflow"
echo "  /sk:start           — Smart entry point"
echo "  /sk:team            — Parallel domain agents"
echo "  /sk:gates           — Run all quality gates in optimized parallel batches"
echo "  /sk:fast-track      — Abbreviated workflow for small changes"
echo "  /sk:learn           — Extract reusable patterns from sessions"
echo "  /sk:context-budget  — Audit context window token consumption"
echo "  /sk:health          — Harness self-audit scorecard"
echo "  /sk:save-session    — Save session state for cross-session continuity"
echo "  /sk:resume-session  — Resume a previously saved session"
echo "  /sk:safety-guard    — Protect against destructive ops"
echo "  /sk:eval            — Define and run evaluations"
echo "  /sk:seo-audit       — SEO audit for web projects"
echo "  /sk:website         — Build a complete client website from a brief or URL"
echo "  /sk:dashboard       — Read-only workflow Kanban board"
echo "  /sk:ci              — Set up GitHub Actions / GitLab CI (PR review, issue triage, nightly audits)"
echo "  /sk:plugin          — Package custom skills, agents, and hooks as a distributable plugin"
echo ""
echo "Run /sk:help to see all commands."
echo ""

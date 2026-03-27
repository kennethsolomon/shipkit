#!/usr/bin/env bash
# verify-workflow.sh — TDD verification for workflow enhancement
# Tests MUST FAIL before implementation and PASS after.
# Run: bash tests/verify-workflow.sh

set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PASS=0
FAIL=0
FAILURES=()

green='\033[0;32m'
red='\033[0;31m'
reset='\033[0m'

assert_file_exists() {
  local desc="$1" file="$2"
  if [[ -f "$file" ]]; then
    echo -e "${green}PASS${reset} $desc"
    PASS=$((PASS + 1))
  else
    echo -e "${red}FAIL${reset} $desc"
    echo "       Expected file: $file"
    FAIL=$((FAIL + 1))
    FAILURES+=("$desc")
  fi
}

assert_contains() {
  local desc="$1" file="$2" pattern="$3"
  if grep -q "$pattern" "$file" 2>/dev/null; then
    echo -e "${green}PASS${reset} $desc"
    PASS=$((PASS + 1))
  else
    echo -e "${red}FAIL${reset} $desc"
    echo "       Expected pattern: $pattern"
    echo "       In file: $file"
    FAIL=$((FAIL + 1))
    FAILURES+=("$desc")
  fi
}

assert_not_contains() {
  local desc="$1" file="$2" pattern="$3"
  if ! grep -q "$pattern" "$file" 2>/dev/null; then
    echo -e "${green}PASS${reset} $desc"
    PASS=$((PASS + 1))
  else
    echo -e "${red}FAIL${reset} $desc"
    echo "       Found unwanted pattern: $pattern"
    echo "       In file: $file"
    FAIL=$((FAIL + 1))
    FAILURES+=("$desc")
  fi
}

assert_count_gte() {
  local desc="$1" file="$2" pattern="$3" min="$4"
  local count
  count=$(grep -c "$pattern" "$file" 2>/dev/null || echo 0)
  if [[ "$count" -ge "$min" ]]; then
    echo -e "${green}PASS${reset} $desc (found $count)"
    PASS=$((PASS + 1))
  else
    echo -e "${red}FAIL${reset} $desc"
    echo "       Expected >= $min matches of: $pattern"
    echo "       Found: $count in $file"
    FAIL=$((FAIL + 1))
    FAILURES+=("$desc")
  fi
}

assert_api_field() {
  local desc="$1" port="$2" field="$3"
  local pid response attempt
  node "$REPO/skills/sk:dashboard/server.js" --port "$port" > /dev/null 2>&1 &
  pid=$!
  response=""
  for attempt in 1 2 3 4 5; do
    sleep 0.4
    response=$(curl -s "http://localhost:${port}/api/status" 2>/dev/null || echo "")
    [[ -n "$response" ]] && break
  done
  kill "$pid" 2>/dev/null
  wait "$pid" 2>/dev/null || true
  if echo "$response" | grep -q "\"${field}\""; then
    echo -e "${green}PASS${reset} $desc"
    PASS=$((PASS + 1))
  else
    echo -e "${red}FAIL${reset} $desc"
    echo "       Expected field '${field}' in /api/status response"
    FAIL=$((FAIL + 1))
    FAILURES+=("$desc")
  fi
}

echo ""
echo "=== Workflow Enhancement Verification ==="
echo ""

# ── Milestone 1: New + Updated Skill Files ──────────────────────────────────

echo "── Milestone 1: Skill Files ──"

assert_file_exists \
  "sk:e2e SKILL.md exists" \
  "$REPO/skills/sk:e2e/SKILL.md"

assert_contains \
  "sk:e2e references agent-browser" \
  "$REPO/skills/sk:e2e/SKILL.md" \
  "agent-browser"

assert_contains \
  "sk:e2e has hard gate behavior" \
  "$REPO/skills/sk:e2e/SKILL.md" \
  "all scenarios must pass"

assert_contains \
  "sk:e2e has Fix & Retest Protocol" \
  "$REPO/skills/sk:e2e/SKILL.md" \
  "Fix & Retest Protocol"

assert_contains \
  "sk:lint has dep audit (composer audit)" \
  "$REPO/skills/sk:lint/SKILL.md" \
  "composer audit"

assert_contains \
  "sk:lint has dep audit (npm audit)" \
  "$REPO/skills/sk:lint/SKILL.md" \
  "npm audit"

assert_contains \
  "sk:lint has Fix & Retest Protocol" \
  "$REPO/skills/sk:lint/SKILL.md" \
  "Fix & Retest Protocol"

assert_contains \
  "sk:test has Fix & Retest Protocol" \
  "$REPO/skills/sk:test/SKILL.md" \
  "Fix & Retest Protocol"

assert_contains \
  "sk:security-check has Fix & Retest Protocol" \
  "$REPO/commands/sk/security-check.md" \
  "Fix & Retest Protocol"

assert_contains \
  "sk:perf has Fix & Retest Protocol" \
  "$REPO/skills/sk:perf/SKILL.md" \
  "Fix & Retest Protocol"

assert_contains \
  "sk:review has Fix & Retest Protocol" \
  "$REPO/skills/sk:review/SKILL.md" \
  "Fix & Retest Protocol"

assert_contains \
  "sk:review runs simplify as pre-step" \
  "$REPO/skills/sk:review/SKILL.md" \
  "simplify"

echo ""

# ── Milestone 2: Workflow Definition Files ───────────────────────────────────

echo "── Milestone 2: Workflow Files ──"

CLAUDE="$REPO/CLAUDE.md"
TEMPLATE="$REPO/skills/sk:setup-claude/templates/CLAUDE.md.template"
# Step table references
# (flow line was removed in workflow simplification — /sk:e2e and /sk:features tested below)
assert_contains \
  "CLAUDE.md has /sk:e2e step" \
  "$CLAUDE" \
  "/sk:e2e"

# Step 26 Sync Features
assert_contains \
  "CLAUDE.md has /sk:features step" \
  "$CLAUDE" \
  "/sk:features"

# Fix & Retest Protocol section
assert_contains \
  "CLAUDE.md has Fix & Retest Protocol section" \
  "$CLAUDE" \
  "Fix & Retest Protocol"

# Requirement Change Flow section
assert_contains \
  "CLAUDE.md has Requirement Change Flow section" \
  "$CLAUDE" \
  "Requirement Change Flow"

assert_contains \
  "CLAUDE.md references /sk:change" \
  "$CLAUDE" \
  "/sk:change"

# /sk: prefix enforcement — spot check old bare refs are gone
assert_not_contains \
  "CLAUDE.md does not use bare /brainstorm (must be /sk:brainstorm)" \
  "$CLAUDE" \
  "run \`/brainstorm\`"

assert_not_contains \
  "CLAUDE.md does not use bare /lint (must be /sk:lint)" \
  "$CLAUDE" \
  "run \`/lint\`"

assert_not_contains \
  "CLAUDE.md does not use bare /review (must be /sk:review)" \
  "$CLAUDE" \
  "run \`/review\`"

# /sk: prefix in workflow table
assert_contains \
  "CLAUDE.md workflow table uses /sk:brainstorm" \
  "$CLAUDE" \
  "/sk:brainstorm"

assert_contains \
  "CLAUDE.md workflow table uses /sk:lint" \
  "$CLAUDE" \
  "/sk:lint"

assert_contains \
  "CLAUDE.md workflow table uses /sk:review" \
  "$CLAUDE" \
  "/sk:review"

# 8-step count: workflow table should have 8 data rows (collapsed workflow)
assert_count_gte \
  "CLAUDE.md workflow table has at least 8 rows" \
  "$CLAUDE" \
  "^| [0-9]" \
  8

# CLAUDE.md.template — same key checks
assert_contains \
  "CLAUDE.md.template has E2E Tests step" \
  "$TEMPLATE" \
  "/sk:e2e"

assert_contains \
  "CLAUDE.md.template has Sync Features step" \
  "$TEMPLATE" \
  "/sk:features"

assert_contains \
  "CLAUDE.md.template has Fix & Retest Protocol" \
  "$TEMPLATE" \
  "Fix & Retest Protocol"

assert_contains \
  "CLAUDE.md.template uses /sk:brainstorm" \
  "$TEMPLATE" \
  "/sk:brainstorm"

assert_not_contains \
  "CLAUDE.md.template does not use bare /brainstorm" \
  "$TEMPLATE" \
  "run \`/brainstorm\`"

# workflow-status.md.template should NOT exist (removed in workflow simplification)
if [[ ! -f "$REPO/skills/sk:setup-claude/templates/tasks/workflow-status.md.template" ]]; then
  echo -e "${green}PASS${reset} workflow-status.md.template does not exist"
  PASS=$((PASS + 1))
else
  echo -e "${red}FAIL${reset} workflow-status.md.template does not exist"
  echo "       File should have been deleted"
  FAIL=$((FAIL + 1))
  FAILURES+=("workflow-status.md.template does not exist")
fi

# CLAUDE.md.template has 8-step workflow table
assert_count_gte \
  "CLAUDE.md.template workflow table has at least 8 rows" \
  "$TEMPLATE" \
  "^| [0-9]" \
  8

# README.md
assert_contains \
  "README.md has E2E Tests in workflow" \
  "$REPO/README.md" \
  "E2E Tests"

assert_contains \
  "README.md uses /sk: prefix" \
  "$REPO/README.md" \
  "/sk:brainstorm"

# sk:setup-optimizer
assert_contains \
  "sk:setup-optimizer references 8 steps" \
  "$REPO/skills/sk:setup-optimizer/SKILL.md" \
  "8"

assert_contains \
  "sk:setup-optimizer flow line has Gates" \
  "$REPO/skills/sk:setup-optimizer/SKILL.md" \
  "Gates"

# install.sh
assert_contains \
  "install.sh installs agent-browser" \
  "$REPO/install.sh" \
  "agent-browser"

# Command templates — breadcrumb flow lines
for tpl in brainstorm write-plan execute-plan security-check finish-feature; do
  assert_contains \
    "templates/commands/${tpl}.md.template breadcrumb has E2E Tests" \
    "$REPO/skills/sk:setup-claude/templates/commands/${tpl}.md.template" \
    "E2E Tests"
done

# DOCUMENTATION.md
assert_contains \
  "DOCUMENTATION.md references 8-step workflow" \
  "$REPO/.claude/docs/DOCUMENTATION.md" \
  "8"

assert_contains \
  "DOCUMENTATION.md lists sk:e2e" \
  "$REPO/.claude/docs/DOCUMENTATION.md" \
  "sk:e2e"

# CHANGELOG.md
assert_contains \
  "CHANGELOG.md documents sk:e2e addition" \
  "$REPO/CHANGELOG.md" \
  "sk:e2e"

assert_contains \
  "CHANGELOG.md documents Fix & Retest Protocol" \
  "$REPO/CHANGELOG.md" \
  "Fix & Retest"

echo ""

# ── Milestone 3: sk:seo-audit Skill ─────────────────────────────────────────

echo "── Milestone 3: sk:seo-audit Skill ──"

SEO_SKILL="$REPO/skills/sk:seo-audit/SKILL.md"

assert_file_exists \
  "sk:seo-audit SKILL.md exists" \
  "$SEO_SKILL"

assert_contains \
  "sk:seo-audit documents dual-mode (running dev server)" \
  "$SEO_SKILL" \
  "running dev server"

assert_contains \
  "sk:seo-audit documents port detection" \
  "$SEO_SKILL" \
  "3000"

assert_contains \
  "sk:seo-audit has ask-before-fix prompt" \
  "$SEO_SKILL" \
  "Apply.*fixes"

assert_contains \
  "sk:seo-audit uses checkbox format" \
  "$SEO_SKILL" \
  "\- \[ \]"

assert_contains \
  "sk:seo-audit outputs to seo-findings.md" \
  "$SEO_SKILL" \
  "seo-findings.md"

assert_contains \
  "sk:seo-audit has Content Strategy section" \
  "$SEO_SKILL" \
  "Content Strategy"

assert_contains \
  "sk:seo-audit has Passed Checks section" \
  "$SEO_SKILL" \
  "Passed Checks"

assert_contains \
  "sk:seo-audit audits robots.txt" \
  "$SEO_SKILL" \
  "robots.txt"

assert_contains \
  "sk:seo-audit audits Open Graph tags" \
  "$SEO_SKILL" \
  "og:title"

assert_contains \
  "sk:seo-audit has Fix & Retest Protocol" \
  "$SEO_SKILL" \
  "Fix & Retest Protocol"

assert_contains \
  "sk:seo-audit has model routing section" \
  "$SEO_SKILL" \
  "Model Routing"

assert_contains \
  "sk:seo-audit in CLAUDE.md commands table" \
  "$CLAUDE" \
  "sk:seo-audit"

assert_contains \
  "sk:seo-audit in README.md" \
  "$REPO/README.md" \
  "sk:seo-audit"

assert_contains \
  "sk:seo-audit in DOCUMENTATION.md" \
  "$REPO/.claude/docs/DOCUMENTATION.md" \
  "sk:seo-audit"

assert_contains \
  "sk:seo-audit in install.sh" \
  "$REPO/install.sh" \
  "sk:seo-audit"

echo ""

# ── Milestone 4: Checklist Format Rollout ────────────────────────────────────

echo "── Milestone 4: Checklist Format Rollout ──"

assert_contains \
  "sk:perf report uses checkbox format" \
  "$REPO/skills/sk:perf/SKILL.md" \
  "\- \[ \]"

assert_contains \
  "sk:perf report has Passed Checks section" \
  "$REPO/skills/sk:perf/SKILL.md" \
  "Passed Checks"

assert_contains \
  "sk:accessibility report uses checkbox format" \
  "$REPO/skills/sk:accessibility/SKILL.md" \
  "\- \[ \]"

assert_contains \
  "sk:accessibility report has Passed Checks section" \
  "$REPO/skills/sk:accessibility/SKILL.md" \
  "Passed Checks"

assert_contains \
  "sk:security-check report uses checkbox format" \
  "$REPO/commands/sk/security-check.md" \
  "\- \[ \]"

assert_contains \
  "sk:security-check report has Passed Checks section" \
  "$REPO/commands/sk/security-check.md" \
  "Passed Checks"

# ── Milestone 5: sk:dashboard Skill ──────────────────────────────────────────

echo "── Milestone 5: sk:dashboard Skill ──"

DASH_SKILL="$REPO/skills/sk:dashboard/SKILL.md"
DASH_SERVER="$REPO/skills/sk:dashboard/server.js"
DASH_HTML="$REPO/skills/sk:dashboard/dashboard.html"

assert_file_exists \
  "sk:dashboard SKILL.md exists" \
  "$DASH_SKILL"

assert_file_exists \
  "sk:dashboard server.js exists" \
  "$DASH_SERVER"

assert_file_exists \
  "sk:dashboard dashboard.html exists" \
  "$DASH_HTML"

assert_contains \
  "sk:dashboard server uses built-in http module" \
  "$DASH_SERVER" \
  "http"

assert_contains \
  "sk:dashboard server discovers git worktrees" \
  "$DASH_SERVER" \
  "worktree"

assert_contains \
  "sk:dashboard server reads todo.md" \
  "$DASH_SERVER" \
  "todo.md"

assert_contains \
  "sk:dashboard server exposes /api/status endpoint" \
  "$DASH_SERVER" \
  "/api/status"

assert_contains \
  "sk:dashboard HTML has SHIPKIT header" \
  "$DASH_HTML" \
  "SHIPKIT"

assert_contains \
  "sk:dashboard HTML uses fetch for polling" \
  "$DASH_HTML" \
  "fetch"

assert_contains \
  "sk:dashboard HTML uses design font" \
  "$DASH_HTML" \
  "JetBrains Mono"

assert_contains \
  "sk:dashboard SKILL.md references skill name" \
  "$DASH_SKILL" \
  "sk:dashboard"

assert_contains \
  "sk:dashboard SKILL.md references server.js" \
  "$DASH_SKILL" \
  "server.js"

assert_contains \
  "sk:dashboard in CLAUDE.md commands table" \
  "$CLAUDE" \
  "sk:dashboard"

assert_contains \
  "sk:dashboard in README.md" \
  "$REPO/README.md" \
  "sk:dashboard"

assert_contains \
  "sk:dashboard in DOCUMENTATION.md" \
  "$REPO/.claude/docs/DOCUMENTATION.md" \
  "sk:dashboard"

assert_contains \
  "sk:dashboard in install.sh" \
  "$REPO/install.sh" \
  "sk:dashboard"

echo ""

# ── Milestone 6: sk:dashboard Todo Item Display ───────────────────────────────

echo "── Milestone 6: sk:dashboard todoItems ──"

assert_contains \
  "sk:dashboard server.js exposes todoItems field" \
  "$DASH_SERVER" \
  "todoItems"

assert_contains \
  "sk:dashboard server.js tracks section label per item" \
  "$DASH_SERVER" \
  "section"

assert_contains \
  "sk:dashboard dashboard.html reads todoItems from API" \
  "$DASH_HTML" \
  "todoItems"

assert_contains \
  "sk:dashboard dashboard.html renders TASKS section heading" \
  "$DASH_HTML" \
  "TASKS"

assert_contains \
  "sk:dashboard dashboard.html has todo-item CSS class" \
  "$DASH_HTML" \
  "todo-item"

assert_api_field \
  "sk:dashboard /api/status response includes todoItems array" \
  "3334" \
  "todoItems"

# ── Milestone 7: sk:mvp Project Context Docs (Approach A) ─────────────────────

echo "── Milestone 7: sk:mvp Project Context Docs ──"

MVP_SKILL="$REPO/skills/sk:mvp/SKILL.md"

assert_contains \
  "sk:mvp generates docs/vision.md" \
  "$MVP_SKILL" \
  "vision.md"

assert_contains \
  "sk:mvp generates docs/prd.md" \
  "$MVP_SKILL" \
  "prd.md"

assert_contains \
  "sk:mvp generates docs/tech-design.md" \
  "$MVP_SKILL" \
  "tech-design.md"

assert_contains \
  "sk:mvp references docs/ directory for generated docs" \
  "$MVP_SKILL" \
  "docs/"

echo ""

# ── Milestone 8: sk:context Session Initializer (Approach B) ──────────────────

echo "── Milestone 8: sk:context Session Initializer ──"

CTX_SKILL="$REPO/skills/sk:context/SKILL.md"

assert_file_exists \
  "sk:context SKILL.md exists" \
  "$CTX_SKILL"

assert_contains \
  "sk:context outputs SESSION BRIEF format" \
  "$CTX_SKILL" \
  "SESSION BRIEF"

assert_contains \
  "sk:context reads tasks/todo.md" \
  "$CTX_SKILL" \
  "tasks/todo.md"

assert_contains \
  "sk:context reads tasks/lessons.md" \
  "$CTX_SKILL" \
  "tasks/lessons.md"

assert_contains \
  "sk:context reads tasks/progress.md" \
  "$CTX_SKILL" \
  "tasks/progress.md"

assert_contains \
  "sk:context reads tasks/findings.md" \
  "$CTX_SKILL" \
  "tasks/findings.md"

assert_contains \
  "sk:context reads docs/decisions.md" \
  "$CTX_SKILL" \
  "docs/decisions.md"

assert_contains \
  "sk:context reads docs/vision.md" \
  "$CTX_SKILL" \
  "docs/vision.md"

assert_contains \
  "sk:context has model routing section" \
  "$CTX_SKILL" \
  "Model Routing"

assert_contains \
  "sk:context in CLAUDE.md commands table" \
  "$CLAUDE" \
  "sk:context"

assert_contains \
  "sk:context in README.md" \
  "$REPO/README.md" \
  "sk:context"

assert_contains \
  "sk:context in DOCUMENTATION.md" \
  "$REPO/.claude/docs/DOCUMENTATION.md" \
  "sk:context"

assert_contains \
  "sk:context in install.sh" \
  "$REPO/install.sh" \
  "sk:context"

assert_contains \
  "sk:context in CLAUDE.md.template" \
  "$TEMPLATE" \
  "sk:context"

echo ""

# ── Milestone 9: Persistent Decisions Log (Approach C) ────────────────────────

echo "── Milestone 9: Persistent Decisions Log ──"

BRAIN_SKILL="$REPO/skills/sk:brainstorming/SKILL.md"

assert_contains \
  "sk:brainstorming appends to docs/decisions.md" \
  "$BRAIN_SKILL" \
  "docs/decisions.md"

assert_contains \
  "sk:brainstorming uses ADR format" \
  "$BRAIN_SKILL" \
  "Decision"

assert_contains \
  "sk:brainstorming marks decisions.md as append-only" \
  "$BRAIN_SKILL" \
  "append"

echo ""

# ── Milestone 10: Gate Auto-Commit + Tech Debt Logging ───────────────────────

echo "── Milestone 10: Gate Auto-Commit + Tech Debt ──"

# Gate skills must have auto-commit language in their fix loops
assert_contains \
  "sk:lint fix loop includes auto-commit" \
  "$REPO/skills/sk:lint/SKILL.md" \
  "auto-commit"

assert_contains \
  "sk:test fix loop includes squash commit" \
  "$REPO/skills/sk:test/SKILL.md" \
  "squash commit"

assert_contains \
  "sk:security-check fix loop includes squash commit" \
  "$REPO/commands/sk/security-check.md" \
  "squash"

assert_contains \
  "sk:perf fix loop includes auto-commit" \
  "$REPO/skills/sk:perf/SKILL.md" \
  "auto-commit"

assert_contains \
  "sk:review fix loop includes auto-commit" \
  "$REPO/skills/sk:review/SKILL.md" \
  "auto-commit"

assert_contains \
  "sk:e2e fix loop includes auto-commit" \
  "$REPO/skills/sk:e2e/SKILL.md" \
  "auto-commit"

# Gate skills must log pre-existing issues to tech-debt.md
assert_contains \
  "sk:review references tasks/tech-debt.md" \
  "$REPO/skills/sk:review/SKILL.md" \
  "tech-debt.md"

assert_contains \
  "sk:security-check references tasks/tech-debt.md" \
  "$REPO/commands/sk/security-check.md" \
  "tech-debt.md"

assert_contains \
  "sk:lint references tasks/tech-debt.md" \
  "$REPO/skills/sk:lint/SKILL.md" \
  "tech-debt.md"

assert_contains \
  "sk:perf references tasks/tech-debt.md" \
  "$REPO/skills/sk:perf/SKILL.md" \
  "tech-debt.md"

assert_contains \
  "sk:e2e references tasks/tech-debt.md" \
  "$REPO/skills/sk:e2e/SKILL.md" \
  "tech-debt.md"

# Planning/utility skills integrate tech-debt.md
assert_contains \
  "sk:context reads tasks/tech-debt.md" \
  "$REPO/skills/sk:context/SKILL.md" \
  "tech-debt.md"

assert_contains \
  "sk:write-plan reads tasks/tech-debt.md" \
  "$REPO/commands/sk/write-plan.md" \
  "tech-debt.md"

assert_contains \
  "sk:update-task references tasks/tech-debt.md" \
  "$REPO/commands/sk/update-task.md" \
  "tech-debt.md"

assert_contains \
  "sk:update-task marks entries Resolved:" \
  "$REPO/commands/sk/update-task.md" \
  "Resolved:"

# Squash gate commits — documented in CLAUDE.md
assert_contains \
  "CLAUDE.md documents squash gate commits rule" \
  "$CLAUDE" \
  "Squash gate commits"

# Auto-advance by default — documented in CLAUDE.md
assert_contains \
  "CLAUDE.md documents auto-advance by default" \
  "$CLAUDE" \
  "Auto-advance by default"

# Conditional summary — documented in CLAUDE.md
assert_contains \
  "CLAUDE.md documents conditional summary" \
  "$CLAUDE" \
  "Conditional summary"

# Never auto-advance rule is REMOVED
assert_not_contains \
  "CLAUDE.md does not contain Never auto-advance" \
  "$CLAUDE" \
  "Never auto-advance"

# sk:schema-migrate auto-detects and auto-skips when no migration changes
assert_contains \
  "sk:schema-migrate auto-detects migration files" \
  "$REPO/skills/sk:schema-migrate/SKILL.md" \
  "git diff"

assert_contains \
  "sk:schema-migrate auto-skips when no migration changes" \
  "$REPO/skills/sk:schema-migrate/SKILL.md" \
  "auto-skip"

echo ""

# ── Milestone 11: sk:frontend-design Pencil Disk Persistence ─────────────────

echo "── Milestone 11: sk:frontend-design Pencil Disk Persistence ──"

FD_SKILL="$REPO/skills/sk:frontend-design/SKILL.md"

assert_contains \
  "sk:frontend-design Pencil phase reads tasks/todo.md for filename" \
  "$FD_SKILL" \
  "tasks/todo.md"

assert_not_contains \
  "sk:frontend-design Pencil phase does not use open_document('new')" \
  "$FD_SKILL" \
  "open_document('new')"

echo ""

# ── Milestone 12: Lifecycle Hooks ────────────────────────────────────────────

echo "── Milestone 12: Lifecycle Hooks ──"

HOOKS_DIR="$REPO/skills/sk:setup-claude/templates/hooks"

assert_file_exists \
  "session-start.sh hook exists" \
  "$HOOKS_DIR/session-start.sh"

assert_file_exists \
  "pre-compact.sh hook exists" \
  "$HOOKS_DIR/pre-compact.sh"

assert_file_exists \
  "validate-commit.sh hook exists" \
  "$HOOKS_DIR/validate-commit.sh"

assert_file_exists \
  "validate-push.sh hook exists" \
  "$HOOKS_DIR/validate-push.sh"

assert_file_exists \
  "log-agent.sh hook exists" \
  "$HOOKS_DIR/log-agent.sh"

assert_file_exists \
  "session-stop.sh hook exists" \
  "$HOOKS_DIR/session-stop.sh"

assert_contains \
  "session-start.sh references tech-debt" \
  "$HOOKS_DIR/session-start.sh" \
  "tech-debt"

assert_contains \
  "pre-compact.sh references progress" \
  "$HOOKS_DIR/pre-compact.sh" \
  "progress"

assert_contains \
  "validate-commit.sh references conventional commit" \
  "$HOOKS_DIR/validate-commit.sh" \
  "conventional commit"

assert_contains \
  "validate-push.sh references protected branches" \
  "$HOOKS_DIR/validate-push.sh" \
  "protected"

echo ""

# ── Milestone 12b: settings.json Template ────────────────────────────────────

echo "── Milestone 12b: settings.json Template ──"

SETTINGS_TPL="$REPO/skills/sk:setup-claude/templates/.claude/settings.json.template"

assert_file_exists \
  "settings.json.template exists" \
  "$SETTINGS_TPL"

assert_contains \
  "settings.json defines SessionStart hook" \
  "$SETTINGS_TPL" \
  "SessionStart"

assert_contains \
  "settings.json defines PreCompact hook" \
  "$SETTINGS_TPL" \
  "PreCompact"

assert_contains \
  "settings.json defines PreToolUse hook" \
  "$SETTINGS_TPL" \
  "PreToolUse"

assert_contains \
  "settings.json defines SubagentStart hook" \
  "$SETTINGS_TPL" \
  "SubagentStart"

assert_contains \
  "settings.json defines Stop hook" \
  "$SETTINGS_TPL" \
  "Stop"

assert_contains \
  "settings.json defines statusline" \
  "$SETTINGS_TPL" \
  "statusline"

echo ""

# ── Milestone 13: Path-Scoped Rules ─────────────────────────────────────────

echo "── Milestone 13: Path-Scoped Rules ──"

RULES_DIR="$REPO/skills/sk:setup-claude/templates/.claude/rules"

assert_file_exists \
  "tests.md.template rule exists" \
  "$RULES_DIR/tests.md.template"

assert_contains \
  "tests rule references coverage" \
  "$RULES_DIR/tests.md.template" \
  "coverage"

assert_contains \
  "sk:setup-claude SKILL.md references rules/" \
  "$REPO/skills/sk:setup-claude/SKILL.md" \
  "rules/"

echo ""

# ── Milestone 14: Statusline ────────────────────────────────────────────────

echo "── Milestone 14: Statusline ──"

STATUSLINE="$REPO/skills/sk:setup-claude/templates/.claude/statusline.sh"

assert_file_exists \
  "statusline.sh exists" \
  "$STATUSLINE"

assert_contains \
  "statusline.sh references todo.md" \
  "$STATUSLINE" \
  "todo.md"

assert_contains \
  "statusline.sh references Branch" \
  "$STATUSLINE" \
  "Branch"

echo ""

# ── Milestone 15: Scope Check Skill ─────────────────────────────────────────

echo "── Milestone 15: Scope Check Skill ──"

SCOPE_SKILL="$REPO/skills/sk:scope-check/SKILL.md"

assert_file_exists \
  "sk:scope-check SKILL.md exists" \
  "$SCOPE_SKILL"

assert_contains \
  "sk:scope-check references scope creep" \
  "$SCOPE_SKILL" \
  "scope creep"

assert_contains \
  "sk:scope-check has On Track tier" \
  "$SCOPE_SKILL" \
  "On Track"

assert_contains \
  "sk:scope-check has Minor Creep tier" \
  "$SCOPE_SKILL" \
  "Minor Creep"

assert_contains \
  "sk:scope-check has Significant Creep tier" \
  "$SCOPE_SKILL" \
  "Significant Creep"

assert_contains \
  "sk:scope-check has Out of Control tier" \
  "$SCOPE_SKILL" \
  "Out of Control"

assert_contains \
  "sk:scope-check references tasks/todo.md" \
  "$SCOPE_SKILL" \
  "tasks/todo.md"

echo ""

# ── Milestone 16: Retrospective Skill ───────────────────────────────────────

echo "── Milestone 16: Retrospective Skill ──"

RETRO_SKILL="$REPO/skills/sk:retro/SKILL.md"

assert_file_exists \
  "sk:retro SKILL.md exists" \
  "$RETRO_SKILL"

assert_contains \
  "sk:retro references velocity" \
  "$RETRO_SKILL" \
  "velocity"

assert_contains \
  "sk:retro references blocker" \
  "$RETRO_SKILL" \
  "blocker"

assert_contains \
  "sk:retro references action item" \
  "$RETRO_SKILL" \
  "action item"

assert_contains \
  "sk:retro references tasks/progress.md" \
  "$RETRO_SKILL" \
  "tasks/progress.md"

echo ""

# ── Milestone 17: Reverse Document Skill ────────────────────────────────────

echo "── Milestone 17: Reverse Document Skill ──"

REVDOC_SKILL="$REPO/skills/sk:reverse-doc/SKILL.md"

assert_file_exists \
  "sk:reverse-doc SKILL.md exists" \
  "$REVDOC_SKILL"

assert_contains \
  "sk:reverse-doc references existing code" \
  "$REVDOC_SKILL" \
  "existing code"

assert_contains \
  "sk:reverse-doc references architecture" \
  "$REVDOC_SKILL" \
  "architecture"

assert_contains \
  "sk:reverse-doc references clarifying question" \
  "$REVDOC_SKILL" \
  "clarifying question"

echo ""

# ── Milestone 18: Gate Agents ───────────────────────────────────────────────

echo "── Milestone 18: Gate Agents ──"

AGENTS_DIR="$REPO/skills/sk:setup-claude/templates/.claude/agents"

assert_file_exists \
  "linter agent exists" \
  "$AGENTS_DIR/linter.md"

assert_file_exists \
  "test-runner agent exists" \
  "$AGENTS_DIR/test-runner.md"

assert_file_exists \
  "security-auditor agent exists" \
  "$AGENTS_DIR/security-auditor.md"

assert_file_exists \
  "perf-auditor agent exists" \
  "$AGENTS_DIR/perf-auditor.md"

assert_file_exists \
  "e2e-tester agent exists" \
  "$AGENTS_DIR/e2e-tester.md"

assert_contains \
  "linter agent has auto-commit" \
  "$AGENTS_DIR/linter.md" \
  "auto-commit"

assert_contains \
  "test-runner agent references coverage" \
  "$AGENTS_DIR/test-runner.md" \
  "coverage"

assert_contains \
  "security-auditor agent references OWASP" \
  "$AGENTS_DIR/security-auditor.md" \
  "OWASP"

echo ""

# ── Milestone 19: Gates Orchestrator ────────────────────────────────────────

echo "── Milestone 19: Gates Orchestrator ──"

GATES_SKILL="$REPO/skills/sk:gates/SKILL.md"

assert_file_exists \
  "sk:gates SKILL.md exists" \
  "$GATES_SKILL"

assert_contains \
  "sk:gates references parallel" \
  "$GATES_SKILL" \
  "parallel"

assert_contains \
  "sk:gates has Batch 1" \
  "$GATES_SKILL" \
  "Batch 1"

assert_contains \
  "sk:gates references quality gates" \
  "$GATES_SKILL" \
  "quality gates"

echo ""

# ── Milestone 20: Fast-Track Flow ───────────────────────────────────────────

echo "── Milestone 20: Fast-Track Flow ──"

FASTTRACK_SKILL="$REPO/skills/sk:fast-track/SKILL.md"

assert_file_exists \
  "sk:fast-track SKILL.md exists" \
  "$FASTTRACK_SKILL"

assert_contains \
  "sk:fast-track references /sk:gates" \
  "$FASTTRACK_SKILL" \
  "/sk:gates"

assert_contains \
  "sk:fast-track has 300 line guard" \
  "$FASTTRACK_SKILL" \
  "300 lines"

assert_contains \
  "sk:fast-track references /sk:smart-commit" \
  "$FASTTRACK_SKILL" \
  "/sk:smart-commit"

echo ""

# ── Milestone 21: Cached Detection ──────────────────────────────────────────

echo "── Milestone 21: Cached Detection ──"

APPLY_SCRIPT="$REPO/skills/sk:setup-claude/scripts/apply_setup_claude.py"

assert_contains \
  "apply_setup_claude.py has detected_at cache" \
  "$APPLY_SCRIPT" \
  "detected_at"

assert_contains \
  "apply_setup_claude.py has --force-detect flag" \
  "$APPLY_SCRIPT" \
  "force-detect"

echo ""

# ── Milestone 22: Documentation Updates (all new commands) ──────────────────

echo "── Milestone 22: Documentation Updates ──"

CLAUDE="$REPO/CLAUDE.md"
README="$REPO/README.md"
DOCS="$REPO/.claude/docs/DOCUMENTATION.md"

assert_contains \
  "CLAUDE.md has /sk:scope-check" \
  "$CLAUDE" \
  "/sk:scope-check"

assert_contains \
  "CLAUDE.md has /sk:retro" \
  "$CLAUDE" \
  "/sk:retro"

assert_contains \
  "CLAUDE.md has /sk:reverse-doc" \
  "$CLAUDE" \
  "/sk:reverse-doc"

assert_contains \
  "CLAUDE.md has /sk:gates" \
  "$CLAUDE" \
  "/sk:gates"

assert_contains \
  "CLAUDE.md has /sk:fast-track" \
  "$CLAUDE" \
  "/sk:fast-track"

assert_contains \
  "README.md has /sk:scope-check" \
  "$README" \
  "/sk:scope-check"

assert_contains \
  "README.md has /sk:retro" \
  "$README" \
  "/sk:retro"

assert_contains \
  "README.md has /sk:reverse-doc" \
  "$README" \
  "/sk:reverse-doc"

assert_contains \
  "README.md has /sk:gates" \
  "$README" \
  "/sk:gates"

assert_contains \
  "README.md has /sk:fast-track" \
  "$README" \
  "/sk:fast-track"

assert_contains \
  "DOCUMENTATION.md has sk:scope-check" \
  "$DOCS" \
  "sk:scope-check"

assert_contains \
  "DOCUMENTATION.md has sk:retro" \
  "$DOCS" \
  "sk:retro"

assert_contains \
  "DOCUMENTATION.md has sk:reverse-doc" \
  "$DOCS" \
  "sk:reverse-doc"

assert_contains \
  "DOCUMENTATION.md has sk:gates" \
  "$DOCS" \
  "sk:gates"

assert_contains \
  "DOCUMENTATION.md has sk:fast-track" \
  "$DOCS" \
  "sk:fast-track"

echo ""

# ── Feature 11: Auto-Skip Intelligence ───────────────────────────────────────

echo "── Feature 11: Auto-Skip Intelligence ──"

assert_contains \
  "CLAUDE.md has auto-skip rules" \
  "$CLAUDE" \
  "Auto-skipped"

assert_contains \
  "CLAUDE.md has auto-skip detection" \
  "$CLAUDE" \
  "auto-skip"

assert_contains \
  "CLAUDE.md.template has auto-skip rules" \
  "$TEMPLATE" \
  "Auto-skipped"

assert_contains \
  "CLAUDE.md.template has auto-skip detection" \
  "$TEMPLATE" \
  "auto-skip"

echo ""

# ── Feature 12: /sk:autopilot ────────────────────────────────────────────────

echo "── Feature 12: /sk:autopilot ──"

assert_file_exists \
  "sk:autopilot SKILL.md exists" \
  "$REPO/skills/sk:autopilot/SKILL.md"

assert_contains \
  "sk:autopilot has auto-advance" \
  "$REPO/skills/sk:autopilot/SKILL.md" \
  "auto-advance"

assert_contains \
  "sk:autopilot has auto-skip" \
  "$REPO/skills/sk:autopilot/SKILL.md" \
  "auto-skip"

assert_contains \
  "sk:autopilot has auto-commit" \
  "$REPO/skills/sk:autopilot/SKILL.md" \
  "auto-commit"

assert_contains \
  "sk:autopilot has direction approval stop" \
  "$REPO/skills/sk:autopilot/SKILL.md" \
  "Direction approval"

assert_contains \
  "sk:autopilot has 3-strike protocol" \
  "$REPO/skills/sk:autopilot/SKILL.md" \
  "3-strike"

assert_contains \
  "sk:autopilot has PR push stop" \
  "$REPO/skills/sk:autopilot/SKILL.md" \
  "PR push"

assert_contains \
  "sk:autopilot has quality gate reference" \
  "$REPO/skills/sk:autopilot/SKILL.md" \
  "quality gate"

assert_file_exists \
  "sk:autopilot command shortcut exists" \
  "$REPO/commands/sk/autopilot.md"

echo ""

# ── Feature 13: /sk:team ─────────────────────────────────────────────────────

echo "── Feature 13: /sk:team ──"

assert_file_exists \
  "sk:team SKILL.md exists" \
  "$REPO/skills/sk:team/SKILL.md"

assert_contains \
  "sk:team has Backend Agent" \
  "$REPO/skills/sk:team/SKILL.md" \
  "Backend Agent"

assert_contains \
  "sk:team has Frontend Agent" \
  "$REPO/skills/sk:team/SKILL.md" \
  "Frontend Agent"

assert_contains \
  "sk:team has QA Agent" \
  "$REPO/skills/sk:team/SKILL.md" \
  "QA Agent"

assert_contains \
  "sk:team has API contract requirement" \
  "$REPO/skills/sk:team/SKILL.md" \
  "API contract"

assert_contains \
  "sk:team has worktree isolation" \
  "$REPO/skills/sk:team/SKILL.md" \
  "worktree"

assert_contains \
  "sk:team has merge step" \
  "$REPO/skills/sk:team/SKILL.md" \
  "merge"

assert_file_exists \
  "backend-dev agent template exists" \
  "$REPO/skills/sk:setup-claude/templates/.claude/agents/backend-dev.md"

assert_file_exists \
  "frontend-dev agent template exists" \
  "$REPO/skills/sk:setup-claude/templates/.claude/agents/frontend-dev.md"

assert_file_exists \
  "qa-engineer agent template exists" \
  "$REPO/skills/sk:setup-claude/templates/.claude/agents/qa-engineer.md"

assert_contains \
  "backend-dev agent references backend" \
  "$REPO/skills/sk:setup-claude/templates/.claude/agents/backend-dev.md" \
  "backend"

assert_contains \
  "frontend-dev agent references frontend" \
  "$REPO/skills/sk:setup-claude/templates/.claude/agents/frontend-dev.md" \
  "frontend"

assert_contains \
  "qa-engineer agent references E2E" \
  "$REPO/skills/sk:setup-claude/templates/.claude/agents/qa-engineer.md" \
  "E2E"

assert_file_exists \
  "sk:team command shortcut exists" \
  "$REPO/commands/sk/team.md"

echo ""

# ── Feature 14: /sk:start ────────────────────────────────────────────────────

echo "── Feature 14: /sk:start ──"

assert_file_exists \
  "sk:start SKILL.md exists" \
  "$REPO/skills/sk:start/SKILL.md"

assert_contains \
  "sk:start has Classify step" \
  "$REPO/skills/sk:start/SKILL.md" \
  "Classify"

assert_contains \
  "sk:start has Recommend step" \
  "$REPO/skills/sk:start/SKILL.md" \
  "Recommend"

assert_contains \
  "sk:start has Route step" \
  "$REPO/skills/sk:start/SKILL.md" \
  "Route"

assert_contains \
  "sk:start routes to debug flow" \
  "$REPO/skills/sk:start/SKILL.md" \
  "debug"

assert_contains \
  "sk:start routes to hotfix flow" \
  "$REPO/skills/sk:start/SKILL.md" \
  "hotfix"

assert_contains \
  "sk:start routes to fast-track flow" \
  "$REPO/skills/sk:start/SKILL.md" \
  "fast-track"

assert_contains \
  "sk:start routes to autopilot mode" \
  "$REPO/skills/sk:start/SKILL.md" \
  "autopilot"

assert_contains \
  "sk:start routes to team mode" \
  "$REPO/skills/sk:start/SKILL.md" \
  "team"

assert_contains \
  "sk:start has --manual override" \
  "$REPO/skills/sk:start/SKILL.md" \
  "\-\-manual"

assert_file_exists \
  "sk:start command shortcut exists" \
  "$REPO/commands/sk/start.md"

echo ""

# ── Features 11-14: Documentation ────────────────────────────────────────────

echo "── Features 11-14: Documentation ──"

assert_contains \
  "CLAUDE.md has /sk:start command" \
  "$CLAUDE" \
  "/sk:start"

assert_contains \
  "CLAUDE.md has /sk:autopilot command" \
  "$CLAUDE" \
  "/sk:autopilot"

assert_contains \
  "CLAUDE.md has /sk:team command" \
  "$CLAUDE" \
  "/sk:team"

assert_contains \
  "README.md has /sk:start" \
  "$REPO/README.md" \
  "/sk:start"

assert_contains \
  "README.md has /sk:autopilot" \
  "$REPO/README.md" \
  "/sk:autopilot"

assert_contains \
  "README.md has /sk:team" \
  "$REPO/README.md" \
  "/sk:team"

DOCS="$REPO/.claude/docs/DOCUMENTATION.md"

assert_contains \
  "DOCUMENTATION.md has sk:start" \
  "$DOCS" \
  "sk:start"

assert_contains \
  "DOCUMENTATION.md has sk:autopilot" \
  "$DOCS" \
  "sk:autopilot"

assert_contains \
  "DOCUMENTATION.md has sk:team" \
  "$DOCS" \
  "sk:team"

echo ""

# ── Features 11-14: set-profile + setup-optimizer ────────────────────────────

echo "── Features 11-14: Profile + Optimizer ──"

assert_contains \
  "set-profile has start skill" \
  "$REPO/commands/sk/set-profile.md" \
  "start"

assert_contains \
  "set-profile has autopilot skill" \
  "$REPO/commands/sk/set-profile.md" \
  "autopilot"

assert_contains \
  "set-profile has team skill" \
  "$REPO/commands/sk/set-profile.md" \
  "team"

assert_contains \
  "setup-optimizer knows about sk:start" \
  "$REPO/skills/sk:setup-optimizer/SKILL.md" \
  "sk:start"

assert_contains \
  "setup-optimizer knows about auto-skip" \
  "$REPO/skills/sk:setup-optimizer/SKILL.md" \
  "auto-skip"

# ── ECC Intelligence Upgrade: Hook Templates ────────────────────────────────

echo ""
echo "--- ECC Intelligence: Hook Templates ---"

assert_file_exists \
  "config-protection hook exists" \
  "$REPO/skills/sk:setup-claude/templates/hooks/config-protection.sh"

assert_file_exists \
  "post-edit-format hook exists" \
  "$REPO/skills/sk:setup-claude/templates/hooks/post-edit-format.sh"

assert_file_exists \
  "console-log-warning hook exists" \
  "$REPO/skills/sk:setup-claude/templates/hooks/console-log-warning.sh"

assert_file_exists \
  "cost-tracker hook exists" \
  "$REPO/skills/sk:setup-claude/templates/hooks/cost-tracker.sh"

assert_file_exists \
  "suggest-compact hook exists" \
  "$REPO/skills/sk:setup-claude/templates/hooks/suggest-compact.sh"

assert_file_exists \
  "safety-guard hook exists" \
  "$REPO/skills/sk:setup-claude/templates/hooks/safety-guard.sh"

assert_contains \
  "settings.json.template has config-protection hook" \
  "$REPO/skills/sk:setup-claude/templates/.claude/settings.json.template" \
  "config-protection"

assert_contains \
  "settings.json.template has console-log hook" \
  "$REPO/skills/sk:setup-claude/templates/.claude/settings.json.template" \
  "console-log"

assert_contains \
  "settings.json.template has post-edit-format hook" \
  "$REPO/skills/sk:setup-claude/templates/.claude/settings.json.template" \
  "post-edit-format"

assert_contains \
  "settings.json.template has cost-tracker hook" \
  "$REPO/skills/sk:setup-claude/templates/.claude/settings.json.template" \
  "cost-tracker"

assert_contains \
  "settings.json.template has suggest-compact hook" \
  "$REPO/skills/sk:setup-claude/templates/.claude/settings.json.template" \
  "suggest-compact"

assert_contains \
  "settings.json.template has safety-guard hook" \
  "$REPO/skills/sk:setup-claude/templates/.claude/settings.json.template" \
  "safety-guard"

# ── ECC Intelligence: /sk:learn ──────────────────────────────────────────────

echo ""
echo "--- ECC Intelligence: /sk:learn ---"

assert_file_exists \
  "sk:learn skill exists" \
  "$REPO/skills/sk:learn/SKILL.md"

assert_file_exists \
  "sk:learn command exists" \
  "$REPO/commands/sk/learn.md"

assert_contains \
  "sk:learn mentions patterns" \
  "$REPO/skills/sk:learn/SKILL.md" \
  "pattern"

assert_contains \
  "sk:learn mentions confidence" \
  "$REPO/skills/sk:learn/SKILL.md" \
  "confidence"

# ── ECC Intelligence: /sk:context-budget ─────────────────────────────────────

echo ""
echo "--- ECC Intelligence: /sk:context-budget ---"

assert_file_exists \
  "sk:context-budget skill exists" \
  "$REPO/skills/sk:context-budget/SKILL.md"

assert_file_exists \
  "sk:context-budget command exists" \
  "$REPO/commands/sk/context-budget.md"

assert_contains \
  "sk:context-budget mentions tokens" \
  "$REPO/skills/sk:context-budget/SKILL.md" \
  "token"

assert_contains \
  "sk:context-budget mentions MCP" \
  "$REPO/skills/sk:context-budget/SKILL.md" \
  "MCP"

assert_contains \
  "sk:context-budget mentions overhead" \
  "$REPO/skills/sk:context-budget/SKILL.md" \
  "overhead"

# ── ECC Intelligence: /sk:health ─────────────────────────────────────────────

echo ""
echo "--- ECC Intelligence: /sk:health ---"

assert_file_exists \
  "sk:health skill exists" \
  "$REPO/skills/sk:health/SKILL.md"

assert_file_exists \
  "sk:health command exists" \
  "$REPO/commands/sk/health.md"

assert_contains \
  "sk:health mentions scorecard" \
  "$REPO/skills/sk:health/SKILL.md" \
  "scorecard"

assert_contains \
  "sk:health mentions context" \
  "$REPO/skills/sk:health/SKILL.md" \
  "Context Efficiency"

assert_contains \
  "sk:health mentions gates" \
  "$REPO/skills/sk:health/SKILL.md" \
  "Quality Gates"

# ── ECC Intelligence: /sk:save-session + /sk:resume-session ──────────────────

echo ""
echo "--- ECC Intelligence: Session Management ---"

assert_file_exists \
  "sk:save-session skill exists" \
  "$REPO/skills/sk:save-session/SKILL.md"

assert_file_exists \
  "sk:resume-session skill exists" \
  "$REPO/skills/sk:resume-session/SKILL.md"

assert_file_exists \
  "sk:save-session command exists" \
  "$REPO/commands/sk/save-session.md"

assert_file_exists \
  "sk:resume-session command exists" \
  "$REPO/commands/sk/resume-session.md"

assert_contains \
  "sk:save-session references .claude/sessions/" \
  "$REPO/skills/sk:save-session/SKILL.md" \
  ".claude/sessions/"

assert_contains \
  "sk:resume-session references .claude/sessions/" \
  "$REPO/skills/sk:resume-session/SKILL.md" \
  ".claude/sessions/"

# ── ECC Intelligence: /sk:safety-guard ───────────────────────────────────────

echo ""
echo "--- ECC Intelligence: /sk:safety-guard ---"

assert_file_exists \
  "sk:safety-guard skill exists" \
  "$REPO/skills/sk:safety-guard/SKILL.md"

assert_file_exists \
  "sk:safety-guard command exists" \
  "$REPO/commands/sk/safety-guard.md"

assert_contains \
  "sk:safety-guard mentions freeze" \
  "$REPO/skills/sk:safety-guard/SKILL.md" \
  "freeze"

assert_contains \
  "sk:safety-guard mentions careful" \
  "$REPO/skills/sk:safety-guard/SKILL.md" \
  "careful"

assert_contains \
  "sk:safety-guard mentions destructive" \
  "$REPO/skills/sk:safety-guard/SKILL.md" \
  "destructive"

# ── ECC Intelligence: /sk:eval ───────────────────────────────────────────────

echo ""
echo "--- ECC Intelligence: /sk:eval ---"

assert_file_exists \
  "sk:eval skill exists" \
  "$REPO/skills/sk:eval/SKILL.md"

assert_file_exists \
  "sk:eval command exists" \
  "$REPO/commands/sk/eval.md"

assert_contains \
  "sk:eval mentions pass@k" \
  "$REPO/skills/sk:eval/SKILL.md" \
  "pass@"

assert_contains \
  "sk:eval mentions capability" \
  "$REPO/skills/sk:eval/SKILL.md" \
  "capability"

assert_contains \
  "sk:eval mentions regression" \
  "$REPO/skills/sk:eval/SKILL.md" \
  "regression"

assert_contains \
  "sk:eval mentions grader" \
  "$REPO/skills/sk:eval/SKILL.md" \
  "grader"

# ── ECC Intelligence: Enriched /sk:start ─────────────────────────────────────

echo ""
echo "--- ECC Intelligence: Enriched /sk:start ---"

assert_contains \
  "sk:start has missing context detection" \
  "$REPO/skills/sk:start/SKILL.md" \
  "Missing Context"

# ── ECC Intelligence: Search-first in brainstorm ─────────────────────────────

echo ""
echo "--- ECC Intelligence: Search-first in brainstorm ---"

assert_contains \
  "brainstorm has search-first phase" \
  "$REPO/skills/sk:brainstorming/SKILL.md" \
  "search-first\|Search-First\|Search First\|search first"

# ── ECC Intelligence: Codebase onboarding in setup-claude ────────────────────

echo ""
echo "--- ECC Intelligence: Codebase onboarding ---"

assert_contains \
  "setup-claude has reconnaissance phase" \
  "$REPO/skills/sk:setup-claude/SKILL.md" \
  "Reconnaissance\|reconnaissance"

# ── ECC Intelligence: Documentation ──────────────────────────────────────────

echo ""
echo "--- ECC Intelligence: Documentation ---"

for cmd in learn context-budget health save-session resume-session safety-guard eval; do
  assert_contains \
    "CLAUDE.md lists /sk:${cmd}" \
    "$REPO/CLAUDE.md" \
    "sk:${cmd}"

  assert_contains \
    "README.md lists /sk:${cmd}" \
    "$REPO/README.md" \
    "sk:${cmd}"
done

# ── ECC Intelligence: Setup-optimizer knows new commands ─────────────────────

echo ""
echo "--- ECC Intelligence: Setup-optimizer awareness ---"

for cmd in learn context-budget health save-session resume-session safety-guard eval; do
  assert_contains \
    "setup-optimizer knows about sk:${cmd}" \
    "$REPO/skills/sk:setup-optimizer/SKILL.md" \
    "sk:${cmd}"
done

assert_contains \
  "setup-optimizer handles hooks" \
  "$REPO/skills/sk:setup-optimizer/SKILL.md" \
  "hooks"

echo ""

# ── MCP Servers & Plugins ────────────────────────────────────────────────────

echo ""
echo "--- MCP Servers & Plugins ---"

assert_contains \
  "setup-claude mentions Sequential Thinking MCP" \
  "$REPO/skills/sk:setup-claude/SKILL.md" \
  "Sequential Thinking"

assert_contains \
  "setup-claude mentions context7" \
  "$REPO/skills/sk:setup-claude/SKILL.md" \
  "context7"

assert_contains \
  "setup-claude mentions ccstatusline" \
  "$REPO/skills/sk:setup-claude/SKILL.md" \
  "ccstatusline"

assert_contains \
  "setup-optimizer mentions Sequential Thinking MCP" \
  "$REPO/skills/sk:setup-optimizer/SKILL.md" \
  "Sequential Thinking"

assert_contains \
  "setup-optimizer mentions context7" \
  "$REPO/skills/sk:setup-optimizer/SKILL.md" \
  "context7"

assert_contains \
  "setup-optimizer mentions ccstatusline" \
  "$REPO/skills/sk:setup-optimizer/SKILL.md" \
  "ccstatusline"

assert_contains \
  "README mentions Sequential Thinking MCP" \
  "$REPO/README.md" \
  "Sequential Thinking"

assert_contains \
  "README mentions context7" \
  "$REPO/README.md" \
  "context7"

assert_contains \
  "README mentions ccstatusline" \
  "$REPO/README.md" \
  "ccstatusline"

# ── Prompt Engineering Upgrades ──────────────────────────────────────────────

echo ""
echo "--- Prompt Engineering Upgrades ---"

assert_contains \
  "sk:review has <think> reasoning blocks" \
  "$REPO/skills/sk:review/SKILL.md" \
  "<think>"

assert_contains \
  "sk:review has exhaustiveness commitment" \
  "$REPO/skills/sk:review/SKILL.md" \
  "exhaustiveness"

assert_contains \
  "sk:review uses rich file:line:symbol references" \
  "$REPO/skills/sk:review/SKILL.md" \
  ":symbol"

assert_contains \
  "sk:security-check has content isolation rule" \
  "$REPO/commands/sk/security-check.md" \
  "content isolation"

assert_contains \
  "sk:security-check has CVSS scoring" \
  "$REPO/commands/sk/security-check.md" \
  "CVSS"

assert_contains \
  "sk:write-plan generates contracts.md" \
  "$REPO/commands/sk/write-plan.md" \
  "contracts.md"

assert_contains \
  "sk:brainstorm extracts requirements checklist" \
  "$REPO/commands/sk/brainstorm.md" \
  "requirements checklist"

assert_contains \
  "sk:execute-plan has status checkpoints" \
  "$REPO/commands/sk/execute-plan.md" \
  "Checkpoint"

assert_contains \
  "sk:gates has batch checkpoints" \
  "$REPO/skills/sk:gates/SKILL.md" \
  "Checkpoint"

# ── Summary ──────────────────────────────────────────────────────────────────

echo "=== Results: $PASS passed, $FAIL failed ==="
echo ""

if [[ ${#FAILURES[@]} -gt 0 ]]; then
  echo "Failed assertions:"
  for f in "${FAILURES[@]}"; do
    echo "  - $f"
  done
  echo ""
  exit 1
fi

exit 0

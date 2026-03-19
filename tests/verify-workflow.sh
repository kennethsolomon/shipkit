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
TRACKER="$REPO/skills/sk:setup-claude/templates/tasks/workflow-status.md.template"

# Flow line
assert_contains \
  "CLAUDE.md flow line has E2E Tests" \
  "$CLAUDE" \
  "E2E Tests"

assert_contains \
  "CLAUDE.md flow line has Sync Features" \
  "$CLAUDE" \
  "Sync Features"

# Step 22 E2E
assert_contains \
  "CLAUDE.md has /sk:e2e step" \
  "$CLAUDE" \
  "/sk:e2e"

# Step 26 Sync Features
assert_contains \
  "CLAUDE.md has /sk:features step" \
  "$CLAUDE" \
  "/sk:features"

# Hard gate step 22 in tracker rules
assert_contains \
  "CLAUDE.md tracker rules list step 22 as hard gate" \
  "$CLAUDE" \
  "Step 22"

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

# 27-step count: workflow table should have 27 data rows
assert_count_gte \
  "CLAUDE.md workflow table has at least 27 rows" \
  "$CLAUDE" \
  "^| [0-9]" \
  27

# Lint + Dep Audit label
assert_contains \
  "CLAUDE.md step 12 labelled 'Lint + Dep Audit'" \
  "$CLAUDE" \
  "Lint + Dep Audit"

# Review + Simplify label
assert_contains \
  "CLAUDE.md step 20 labelled 'Review + Simplify'" \
  "$CLAUDE" \
  "Review + Simplify"

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

# workflow-status.md.template — 27 rows + new hard gates
assert_count_gte \
  "workflow-status.md.template has at least 27 step rows" \
  "$TRACKER" \
  "^| [0-9]" \
  27

assert_contains \
  "workflow-status.md.template has E2E Tests row" \
  "$TRACKER" \
  "sk:e2e"

assert_contains \
  "workflow-status.md.template marks step 22 as HARD GATE" \
  "$TRACKER" \
  "HARD GATE"

assert_contains \
  "workflow-status.md.template has Sync Features row" \
  "$TRACKER" \
  "sk:features"

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
  "sk:setup-optimizer references 27 steps" \
  "$REPO/skills/sk:setup-optimizer/SKILL.md" \
  "27"

assert_contains \
  "sk:setup-optimizer flow line has E2E Tests" \
  "$REPO/skills/sk:setup-optimizer/SKILL.md" \
  "E2E Tests"

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
  "DOCUMENTATION.md has 27 steps" \
  "$REPO/.claude/docs/DOCUMENTATION.md" \
  "27"

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
  "sk:dashboard server reads workflow-status.md" \
  "$DASH_SERVER" \
  "workflow-status.md"

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

echo ""

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

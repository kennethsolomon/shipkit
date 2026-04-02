---
name: sk:setup-optimizer
description: "Diagnose, update workflow, deploy hooks, enrich CLAUDE.md, and keep project infrastructure current. The single command for ongoing ShipKit maintenance."
triggers:
  - optimize claude
  - optimize setup
  - enrich claude
  - maintain claude
  - doctor claude
  - check claude
  - diagnose claude
  - refresh claude
  - update claude
  - re-setup
allowed-tools:
  - Bash
  - Read
  - Write
---

## Overview

The single command to keep your entire ShipKit project infrastructure current. Diagnoses problems, updates the workflow, deploys missing hooks, scans your codebase, and enriches CLAUDE.md with project context — all while preserving your customizations.

### What It Does

1. **Diagnoses** — finds missing sections, stale info, inconsistencies, and gaps
2. **Updates workflow** — refreshes the workflow section to the latest template version
3. **Deploys hooks** — installs missing hooks and updates settings.json wiring
4. **Discovers** — scans project structure, docs, and workflows
5. **Enriches** — merges discoveries into CLAUDE.md while preserving your edits

## Usage

```bash
/sk:setup-optimizer
```

### Step 0: Diagnose

Before making any changes, runs a diagnostic pass on the existing CLAUDE.md:

- **Missing sections** — checks for essential sections (Code Navigation, Workflow, Sub-Agent Patterns, Cross-Platform Tracking, Project Memory, Lessons Capture, Testing, Commands, etc.)
- **Stale content** — detects outdated info (stale model/route counts, removed dependencies, old command names like `/laravel-lint` instead of `/sk:lint`)
- **Inconsistencies** — compares documented vs actual project state (directories, scripts, workflows)
- **Section completeness** — flags sections that exist but are empty or have only placeholder text
- **Outdated workflow** — checks if the workflow matches the current 11-step flow (1, 2, 3, 4, 5, 5.5, 6, 7, 8, 8.5, 8.6) with `/sk:gates` as single gate step
- **Missing commands** — checks for `sk:start`, `sk:autopilot`, `sk:team`, `sk:learn`, `sk:context-budget`, `sk:health`, `sk:save-session`, `sk:resume-session`, `sk:safety-guard`, `sk:eval`, `sk:ci`, `sk:plugin`, `sk:deps-audit`, `sk:deep-interview`, `sk:deep-dive` in the Commands table
- **Missing agents** — checks if `.claude/agents/` exists and contains the 13 core agents: `backend-dev`, `frontend-dev`, `mobile-dev`, `qa-engineer`, `code-reviewer`, `security-reviewer`, `performance-optimizer`, `architect`, `database-architect`, `devops-engineer`, `debugger`, `refactor-specialist`, `tech-writer`
- **Missing rules** — checks if `.claude/rules/` exists and contains the project-relevant rule files based on detected stack (laravel.md, react.md, vue.md, tests.md, api.md, migrations.md)
- **Stale agent frontmatter** — checks that existing agent files use the new `memory`, `model`, and `tools` frontmatter fields (agents without `memory` are degraded)
- **Auto-skip rules** — checks for auto-skip detection rules in the workflow section
- **Stale tracker references** — checks for `tasks/workflow-status.md` references (removed — progress tracked via git branch + todo.md checkboxes)
- **Missing hooks** — checks if `.claude/hooks/` exists and contains both core and enhanced hooks; also checks for `keyword-router.sh` (UserPromptSubmit magic keyword routing)

Reports findings before proceeding. If issues are found, they inform subsequent steps.

### Step 0.5: Re-detect Stack + Sync Skills/Agents/Rules

After diagnosis, re-detect the project stack and sync installed skills, agents, and rules.

**Reference:** Read `~/.claude/skills/sk:setup-claude/references/skill-profiles.md` for the categorization matrix.

#### 1. Re-detect stack

Run the same detection logic as `sk:setup-claude` Phase 0.5:
- Scan for stack indicators (composer.json, package.json, go.mod, etc.)
- Sub-detect database capability (Prisma, Drizzle, Laravel migrations, etc.)
- Compare new detection against `.shipkit/config.json` current values

#### 2. Diff and display changes

If the detected stack or capabilities changed, display a diff:

```
Stack re-detection:
  Stack: nextjs (unchanged)
  Capabilities: web → web, database (prisma/schema.prisma detected)

Skill changes:
  + sk:schema-migrate  (database capability detected)
  No removals.

Agent changes:
  + database-architect  (database capability detected)
  No removals.

Rule changes:
  + migrations.md  (database paths)
  No removals.

Project MCP changes:
  - laravel-boost  (stack is no longer laravel)
  No additions.

Apply changes? (y/n)
```

If no changes detected, report `Stack: [stack] — no changes detected` and skip to Step 1.

#### 3. Sync on confirmation

If the user confirms:

**Skills sync:**
- Add newly relevant skills: copy from `~/.claude/skills/` to `.claude/skills/` in the project
- Remove stale skills: delete from `.claude/skills/` in the project if they no longer match the detected stack
- Never touch skills in `config.skills.extra` (user manually added)
- Never touch skills in `config.skills.disabled` (user manually excluded)

**Agent sync:**
- Add newly relevant agents: copy from `~/.claude/agents/` to `.claude/agents/` in the project
- Remove stale agents: delete from `.claude/agents/` in the project if they no longer match
- Never remove user-customized agents (detect via content that differs from the template — check if file hash differs from template hash, or if file contains `<!-- EDITED -->` marker)

**Rule sync:**
- Add newly relevant rules: copy from `~/.claude/rules/` to `.claude/rules/` in the project
- Remove stale rules: delete from `.claude/rules/` in the project if they no longer match
- Never remove user-customized rules (same detection as agents)

**Project-level MCP sync** (sole owner of `.mcp.json` managed entries — Step 1.7 only handles global MCP):
- Read the MCP Server → Stack Mapping from `skill-profiles.md`
- **Add:** MCP entries to `.mcp.json` when stack matches and entry is missing
- **Remove:** MCP entries from `.mcp.json` when stack no longer matches (e.g., `laravel-boost` removed if stack changed from Laravel to Next.js). Only remove entries whose key matches the mapping table — never touch other entries.
- **Update:** If entry exists but command is stale (e.g., Sail added/removed since last setup — `vendor/bin/sail` exists but entry uses `php`, or vice versa), update the command to match current state
- For Laravel Boost Sail detection: use `vendor/bin/sail` command variant if `vendor/bin/sail` exists in the project

**Config update:**
- Update `.shipkit/config.json` with new `stack.detected`, `stack.detected_at`, `stack.capabilities`

**CLAUDE.md commands table:**
- Regenerate the Commands table to list only currently installed skills

#### 4. Upgrade path handling

- If project has no `stack` field in config → treat as auto-detect (backwards compatible)
- If capabilities expanded (e.g., added database) → suggest new skills
- If capabilities reduced (e.g., removed a dependency) → suggest removing irrelevant skills
- Display: `Capabilities changed: [old] → [new]. [N] skills affected. Apply? (y/n)`

### Step 1: Update Workflow

If the workflow section is outdated or missing, replace it with the latest version:

**Current workflow (11 steps, TDD with `/sk:gates` as single gate step):**
```
Explore → Design → Plan → Branch → Write Tests + Implement → Scope Check → Commit → Gates → Finalize + Learn + Retro
```

**What gets updated:**
- Workflow table (11 steps — `/sk:brainstorm`, `/sk:frontend-design` or `/sk:api-design`, `/sk:write-plan`, `/sk:branch`, `/sk:write-tests` + `/sk:execute-plan`, `/sk:scope-check`, `/sk:smart-commit`, `/sk:gates`, `/sk:finish-feature`, `/sk:learn`, `/sk:retro`)
- Step details (TDD red/green/verify descriptions)
- Workflow rules (auto-advance, conditional summary, auto-skip, squash gate commits)
- Bug fix flow section (7 steps)
- Hotfix flow section (6 steps)
- Sub-Agent Patterns section (if missing)
- Cross-Platform Tracking section (if missing)
- Project Memory section (if missing)
- Lessons Capture section (if missing)
- Testing TDD section (if missing)
- 3-Strike Protocol (if missing)
- Fix & Retest Protocol section (if missing)
- Requirement Change Flow section (if missing)
- Auto-skip detection rules (if missing)
- Remove `tasks/workflow-status.md` references (tracker removed)

**What gets preserved:**
- Everything marked with `<!-- LOCK -->` is never touched
- Project-specific content below the workflow (conventions, models, routes, architecture)
- Stack section, Build & Run section
- Any section with `<!-- EDITED -->` marker

**How it works:**
1. Read the latest workflow template from `~/.claude/skills/sk:setup-claude/templates/CLAUDE.md.template`
2. Compare with the current CLAUDE.md workflow section
3. If different, replace the workflow section (between `## Workflow` and the next `##` that isn't a workflow subsection)
4. Insert missing sections (Code Navigation, Sub-Agent Patterns, Project Memory, etc.) in their correct positions — Code Navigation (`<!-- BEGIN:code-navigation -->`) goes before `## Workflow`; Sub-Agent Patterns goes after `## Workflow` and before `## Commands`
5. Preserve all `<!-- LOCK -->` and project-specific sections

### Step 1.5: Hooks Deployment

After updating the workflow, check and deploy hooks:

1. **Check if `.claude/hooks/` exists** — if not, create it
2. **Check for core hooks** — `session-start.sh`, `session-stop.sh`, `pre-compact.sh`, `validate-commit.sh`, `validate-push.sh`, `log-agent.sh`, `keyword-router.sh`
3. **Check for enhanced hooks** — `config-protection.sh`, `post-edit-format.sh`, `console-log-warning.sh`, `cost-tracker.sh`, `suggest-compact.sh`, `safety-guard.sh`, `auto-progress.sh`
4. **Check `.claude/settings.json`** — verify hooks are wired correctly

**Report status and prompt:**

> "Hooks: [X/6 core, Y/6 enhanced] installed
> Install missing hooks? [y/n]"

**If yes:**

1. **Locate templates** — resolve the ShipKit templates directory:
   - `~/.claude/skills/sk:setup-claude/templates/hooks/` (symlinked install)
   - Or the npm global path if installed via `npm install -g`

2. **Deploy missing hook scripts** (create-if-missing, never overwrite existing):
   ```bash
   # For each missing hook file:
   cp "$TEMPLATE_DIR/hooks/<hook>.sh" ".claude/hooks/<hook>.sh"
   chmod +x ".claude/hooks/<hook>.sh"
   ```

3. **Update `.claude/settings.json`** — read the latest `settings.json.template` and merge new hook entries into the existing settings.json:
   - **Preserve** existing hooks, permissions, statusline config
   - **Add** only missing hook entries (new PreToolUse, PostToolUse, Stop entries)
   - **Never remove** existing entries — additive merge only

4. **Report what was deployed:**
   ```
   Deployed hooks:
     + config-protection.sh (PreToolUse — blocks linter config edits)
     + post-edit-format.sh (PostToolUse — auto-format after edits)
     + console-log-warning.sh (Stop — warn on debug statements)
     + cost-tracker.sh (Stop — session metadata logging)
     + suggest-compact.sh (PreToolUse — compact suggestions)
     + safety-guard.sh (PreToolUse — freeze/careful mode)
     ~ Updated .claude/settings.json with new hook wiring
   ```

**If no:** skip hook deployment, continue to Step 1.6.

### Step 1.6: LSP Integration Check

After hooks deployment, check and configure LSP tooling:

1. **Check `ENABLE_LSP_TOOL`** — verify `~/.claude/settings.json` has `"env": { "ENABLE_LSP_TOOL": "1" }`. If missing, add it.

2. **Detect stack language server** — based on the project's detected language:

   | Stack | Language Server | Install Command |
   |-------|----------------|-----------------|
   | JavaScript / TypeScript | `typescript-language-server` | `npm install -g typescript typescript-language-server` |
   | PHP / Laravel | `intelephense` | `npm install -g intelephense` |
   | Python | `pyright` | `npm install -g pyright` |
   | Go | `gopls` | `go install golang.org/x/tools/gopls@latest` |
   | Rust | `rust-analyzer` | `rustup component add rust-analyzer` |
   | Swift | `sourcekit-lsp` | pre-installed with Xcode — no install needed |

3. **Check if installed** — run `which <server>` or `<server> --version`

4. **Install if missing** — run the install command for the detected stack

5. **Report status:**
   ```
   LSP: typescript-language-server ✓ installed
   ENABLE_LSP_TOOL=1 in ~/.claude/settings.json ✓
   ```

**If no language server needed** (e.g. Swift with Xcode), skip install — report status only.

**Idempotency:** Never overwrite existing `env` keys — merge additively.

**Idempotency:** Never overwrite existing hook files — the user may have customized them. Only deploy hooks that don't exist yet. For settings.json, merge additively.

### Step 1.7: Global MCP Servers & Plugin Check

After LSP check, verify the three recommended **global** tools are configured.

> **Note:** Project-level MCP (`.mcp.json`) is managed exclusively by Step 0.5 during stack sync. This step only handles global MCP/plugins.

1. **Sequential Thinking MCP** — grep `~/.mcp.json` for `sequential-thinking`
2. **Context7 plugin** — grep `~/.claude/settings.json` for `context7@claude-plugins-official` in `enabledPlugins`
3. **ccstatusline** — check `~/.claude/settings.json` for a `statusline` entry set by ccstatusline
4. **context-mode plugin** — grep `~/.claude/settings.json` for `context-mode` in `enabledPlugins`. Check if installed and get version via `claude plugin list 2>/dev/null | grep context-mode`

**Report status and prompt:**

> "Global MCP/Plugins: [X/4] configured
>   sequential-thinking: [✓ configured / ✗ missing]
>   context7:            [✓ configured / ✗ missing]
>   ccstatusline:        [✓ configured / ✗ missing]
>   context-mode:        [✓ vX.Y.Z / ✓ update available vX.Y.Z → vA.B.C / ✗ missing]
> Install missing / update available? [y/n]"

**If yes:** Follow the same install steps as `sk:setup-claude` MCP Servers & Plugins section:
- Sequential Thinking: merge entry into `~/.mcp.json`
- Context7: add `context7@claude-plugins-official: true` to `~/.claude/settings.json` enabledPlugins
- ccstatusline: run `npx ccstatusline@latest`
- context-mode (install): run `/plugin marketplace add mksglu/context-mode` then `/plugin install context-mode@context-mode`
- context-mode (update): run `/context-mode:ctx-upgrade`

**If no:** skip, continue to Step 1.8.

**Idempotency:** Never overwrite existing MCP entries, plugin flags, or statusline config — additive merge only.

### Step 1.8: Agents & Rules Check

After MCP check, verify the project has the correct agents and rules for its detected stack.

**Reference:** Read `~/.claude/skills/sk:setup-claude/references/skill-profiles.md` for agent→stack and rule→stack mappings.

**Agents check:**

1. Check if `.claude/agents/` directory exists
2. Read detected stack from `.shipkit/config.json` (or re-detect if not present)
3. Using the agent→stack mapping from `skill-profiles.md`, determine which agents this project should have:
   - Universal agents (all projects): architect, qa-engineer, debugger, code-reviewer, security-reviewer, performance-optimizer, refactor-specialist, tech-writer, devops-engineer
   - Stack-specific: backend-dev (backend stacks), frontend-dev (web stacks), mobile-dev (mobile stacks), database-architect (database capability)
4. For each expected agent, check if it exists in `.claude/agents/`
5. For each existing agent, check if it has `memory:` and `model:` in frontmatter (older agents may be missing these)

**Rules check:**

1. Check if `.claude/rules/` directory exists
2. Using the rule→stack mapping from `skill-profiles.md`, determine which rules this project should have:
   - Universal rules (all projects): tests.md, api.md
   - Stack-specific: laravel.md (Laravel), react.md (React/Next.js), vue.md (Vue/Nuxt), migrations.md (database capability)
3. Check for each expected rule file

**Report status and prompt:**

> "Agents: [X/13] core agents found
>   backend-dev:           [✓ / ✗ missing]
>   frontend-dev:          [✓ / ✗ missing]
>   mobile-dev:            [✓ / ✗ missing]
>   qa-engineer:           [✓ / ✗ missing]
>   code-reviewer:         [✓ / ✗ missing]
>   security-reviewer:     [✓ / ✗ missing]
>   performance-optimizer: [✓ / ✗ missing]
>   architect:             [✓ / ✗ missing]
>   database-architect:    [✓ / ✗ missing]
>   devops-engineer:       [✓ / ✗ missing]
>   debugger:              [✓ / ✗ missing]
>   refactor-specialist:   [✓ / ✗ missing]
>   tech-writer:           [✓ / ✗ missing]
>
> Rules: [X/N] stack-relevant rules found
>   [list relevant rules with ✓/✗]
>
> Deploy missing agents and rules? [y/n]"

**If yes:**
- Copy missing agent files from `~/.claude/skills/sk:setup-claude/templates/.claude/agents/`
- Copy missing rule files from `~/.claude/skills/sk:setup-claude/templates/.claude/rules/`
- Only deploy agents/rules that don't exist yet — never overwrite existing customized files

**If no:** skip, continue to Step 2.

**Idempotency:** Never overwrite existing agent or rule files.

### Step 2: Scan & Enrich

After workflow update, proceeds with codebase discovery and enrichment:

1. Scans project for directories, docs, and workflows
2. Reads your existing CLAUDE.md
3. Intelligently merges discoveries with your content (prioritizing diagnosed gaps)
4. Preserves any user customizations
5. Updates CLAUDE.md with comprehensive context

## What Gets Discovered

### Directories
Auto-documents: src/, tests/, docs/, public/, scripts/, config/, migrations/, and more (intelligently excludes node_modules/, vendor/, etc.)

### Documentation
Finds and links: README.md, CONTRIBUTING.md, CHANGELOG.md, docs/*.md, .github/CONTRIBUTING.md, and more

### Workflows
Detects: Makefile targets, npm/yarn scripts, GitHub Actions workflows

## Smart Features

### 1. User Customization Preservation

**Dual Detection:**
- Compares content to detect user edits
- Looks for `<!-- EDITED -->` markers
- Automatically preserves customized sections

**Auto-Locking:**
- `Important Context` section - auto-locked if has content
- `Known Issues` section - auto-locked
- Any section with `<!-- LOCK -->` comment - permanently locked

**Result:** Run multiple times during development without losing work!

### 2. Intelligent Merging

When updating CLAUDE.md:
- ✅ Keeps user customizations intact
- ✅ Updates auto-generated discovery sections
- ✅ Adds newly discovered items
- ✅ Reports what was preserved

### 3. Flexible Line Count

- **Target:** Stay under 200 lines when possible
- **Philosophy:** Comprehensive context > artificial line limit
- **Strategy:** Link to docs instead of inlining if extensive

## Maintenance Workflow

### During Development

```bash
# After adding new test directory
mkdir tests

# Run optimizer to discover it
/optimize-claude

# CLAUDE.md now documents tests/ automatically!
```

### When Customizing

```bash
# Edit Important Context with custom notes
vim CLAUDE.md

# The edit is automatically preserved on next run
/optimize-claude

# ✅ Your notes stay intact!
```

## Configuration

### Smart Defaults (Auto-Locked)
- **Important Context** - Your project decisions
- **Known Issues** - Problems/limitations
- Any section with `<!-- LOCK -->` comment

### Explicit Locking

```markdown
## My Custom Section
<!-- LOCK -->
This content will never be regenerated.
```

## When to Use

✅ **Use `/sk:setup-optimizer` when:**
- ShipKit was updated and your project needs the latest hooks/commands
- You've added new directories to your project
- You've created documentation files
- You want to refresh project context
- Monthly maintenance of CLAUDE.md and hooks

✅ **Safe to run multiple times** — existing customizations and hook files are never overwritten.

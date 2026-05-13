# ShipKit → Codex Migration: Claude Code Dependency Inventory

Generated: 2026-05-13

## Summary

**Total Claude-specific touchpoints identified: 82+**

**Highest-risk translations:**
- **Sub-agent orchestration (parallel Agent tool spawning)** — Codex `exec` model differs fundamentally from Claude Code's in-process Agent tool. Parallel batches in sk:gates, sk:deep-dive, sk:autopilot require complete rearchitecture.
- **Worktree isolation (EnterWorktree/ExitWorktree + isolation: "worktree" field)** — Claude Code spawns isolated git worktrees; Codex has no equivalent. Affects sk:gates, sk:perf, sk:ci, all `isolation: worktree` agents.
- **Settings.json hooks (SessionStart, PreToolUse, PostToolUse)** — Codex cannot hook into tool execution; context-mode and safety-guard features won't transfer.
- **Pencil MCP server (batch_design, get_screenshot, snapshot_layout)** — Design generation in sk:frontend-design and sk:mvp. Codex has no visual design editor equivalent.
- **Context-mode MCP server (ctx_batch_execute, ctx_search, ctx_execute_file)** — Large output handling via SQLite FTS5 index. Codex would need alternative approach.

---

## 1. Agent / Sub-agent Usage

| File:Line | Construct | Type | Notes |
|---|---|---|---|
| skills/sk:gates/SKILL.md | Agent tool with parallel batches | Parallel | Batch 1: 4 agents (lint, security, perf, deps-audit) spawn simultaneously; Batch 2-4 sequential |
| skills/sk:gates/SKILL.md:subagent_type="architect" | Subagent fallback | Sequential | Architect spawned if any gate fails 3x for resolution |
| skills/sk:deep-dive/SKILL.md | Agent tool 3 investigation lanes | Parallel | 3 agents (models, routes/middleware, tests) run simultaneously via single Agent call |
| skills/sk:setup-claude/SKILL.md:Agent tool with isolation: "worktree" | Isolation pattern | Worktree | For experimental refactors; if fails, worktree discarded |
| skills/sk:setup-claude/SKILL.md:Sub-Agent Patterns section | Explore pattern | Parallel | Multiple Explore subagent_types launched in single message |
| skills/sk:setup-claude/SKILL.md:Background Agents section | Background spawning | Sequential | Long-running agents (e2e, perf, security) run in background |
| skills/sk:autopilot/SKILL.md | Multi-phase orchestration | Sequential/Parallel | 8-phase workflow with auto-skip, auto-advance; spawns agents at phases 3-7 |
| skills/sk:ci/SKILL.md | devops-engineer agent | Worktree | Agent works in worktree isolation to generate CI files before merging |
| skills/sk:perf/SKILL.md | performance-optimizer agent | Worktree | Worktree isolation; after completion, merges its branch |
| skills/sk:skill-creator/agents/analyzer.md | Analyzer agent | Standalone | Analyzes existing skill patterns in codebase |
| skills/sk:skill-creator/agents/comparator.md | Comparator agent | Standalone | Compares candidate implementations |
| skills/sk:skill-creator/agents/grader.md | Grader agent | Standalone | Scores implementations against rubric |
| skills/sk:setup-claude/templates/.claude/agents/*.md (15 agents) | Agent definitions | Various | Code-reviewer, test-runner, debugger, perf-auditor, linter, qa-engineer, e2e-tester, security-auditor, frontend-dev, backend-dev, refactor-specialist, mobile-dev, devops-engineer, tech-writer, architect |

---

## 2. Slash Command Frontmatter Fields

| File | Fields | Values | Notes |
|---|---|---|---|
| commands/sk/*.md | description | string | Required; appears in /sk:help |
| commands/sk/*.md | disable-model-invocation | true/false | If true, command runs without AI (pure shell/logic) |
| commands/sk/branch.md | disable-model-invocation | true | Pure script; no model needed |
| commands/sk/hotfix.md | disable-model-invocation | (implicit) | Likely includes model |
| commands/sk/finish-feature.md | (TBD) | (TBD) | Invokes PR creation flow |

**Observed:** Commands use minimal frontmatter. Codex may need additional `runner` or `executor` field if it differentiates command types.

---

## 3. Skill Frontmatter Fields

| File:Lines | Field | Value | Notes |
|---|---|---|---|
| skills/sk:*/SKILL.md | name | "sk:*" | Skill identifier |
| skills/sk:*/SKILL.md | description | string | 1-2 sentence summary; includes use-case hints |
| skills/sk:*/SKILL.md | allowed-tools | comma-separated | Example: "Agent, Read, Write, Bash, Glob, Grep" (sk:gates) |
| skills/sk:*/SKILL.md | model | "opus" / "sonnet" / "haiku" | Explicitly set model; defaults to inherit if omitted |
| skills/sk:setup-claude/SKILL.md | (no frontmatter) | (N/A) | Uses inline Markdown structure instead |

**Key observation:** `allowed-tools` list is binding — tool not in list cannot be invoked. Codex needs identical schema or Codex tool names must map to Claude Code equivalents.

---

## 4. Hooks & Settings.json References

| File | Hook Type | Trigger | Purpose |
|---|---|---|---|
| .claude/hooks/session-start.sh | SessionStart | Session init | Loads CLAUDE.md context |
| .claude/hooks/validate-commit.sh | PreToolUse | git commit* | Validates commit message format |
| .claude/hooks/validate-push.sh | PreToolUse | git push* | Confirms before pushing |
| .claude/hooks/config-protection.sh | PreToolUse | Edit/Write | Blocks edits to linter/formatter configs |
| .claude/hooks/post-edit-format.sh | PostToolUse | Edit | Auto-formats edited file with project formatter |
| .claude/hooks/suggest-compact.sh | PreToolUse | (global) | Suggests `/compact` after 50+ tool calls |
| .claude/hooks/safety-guard.sh | PreToolUse | Bash/Edit/Write | Reads `.claude/safety-guard.json` for protection rules |
| .claude/hooks/auto-progress.sh | PostToolUse | git events | Auto-logs to `tasks/progress.md` |
| .claude/hooks/context-mode integration | PreToolUse, PostToolUse, PreCompact | Large outputs | Routes Playwright snapshots, grep, logs, API responses through SQLite FTS5 |

**Critical:** All hooks require Claude Code's hook execution infrastructure. Codex cannot replicate this without equivalent system hooks.

---

## 5. MCP Server References

| Server | Tools Used | References | Difficulty |
|---|---|---|---|
| pencil | batch_design, get_screenshot, snapshot_layout, open_document, batch_get, get_style_guide, get_guidelines | skills/sk:frontend-design/SKILL.md, skills/sk:mvp/SKILL.md | HIGH — No Codex visual editor |
| context-mode (plugin) | ctx_batch_execute, ctx_search, ctx_execute, ctx_index, ctx_fetch_and_index, ctx_stats, ctx_doctor, ctx_upgrade | Multiple skills reference "context-mode:" prefix; skills/sk:context-budget/SKILL.md | HIGH — Codex has no FTS5/SQLite output caching |
| supabase | apply_migration, execute_sql, list_tables, get_logs, generate_typescript_types, create_project, get_cost | skills/sk:schema-migrate/SKILL.md (indirect); used in project setup | MEDIUM — Supabase MCP likely available for Codex |
| google-calendar, gmail, google-drive | Various (create_event, list_events, search_threads, etc.) | Referenced in system reminders; minimal Skill integration | MEDIUM — Standard OAuth flows; Codex can replicate |
| posthog | analytics queries | (minimal direct reference in Skills) | LOW — Analytics; not critical path |

**Observation:** `mcp__` prefix pattern universal in Claude Code. Codex may use different naming convention.

---

## 6. Worktree & Isolation Features

| File:Line | Feature | Type | Impact |
|---|---|---|---|
| skills/sk:setup-claude/SKILL.md | isolation: "worktree" field | Agent metadata | Spawned agent runs in `.claude/worktrees/<name>/` isolated copy |
| skills/sk:gates/SKILL.md | performance-optimizer worktree | Agent pattern | Creates separate branch for perf fixes; merges after completion |
| skills/sk:perf/SKILL.md | Agent works in worktree isolation | Agent pattern | Isolated testing before merging |
| skills/sk:ci/SKILL.md | devops-engineer worktree | Agent pattern | Generates CI files in isolation; review before merge |
| skills/sk:setup-claude/templates/.claude/agents/frontend-dev.md | isolation: worktree | Metadata | Explicit field in agent definition |
| skills/sk:setup-claude/templates/.claude/agents/backend-dev.md | isolation: worktree | Metadata | Explicit field in agent definition |
| skills/sk:setup-claude/templates/.claude/agents/mobile-dev.md | isolation: worktree | Metadata | Explicit field in agent definition |
| .claude/worktrees/<name>/ | Directory structure | FileSystem | Each worktree has own tasks/, bin/, commands/, skills/ copies |

**Codex adaptation:** No git worktree equivalent. Could fake with branch switching + suffix directories, but not equivalent to true isolation.

---

## 7. CLAUDE.md & AGENTS.md Generation

| File | Generated Content | Source | Notes |
|---|---|---|---|
| bin/shipkit.js:install() | Copies skills/ & commands/ to ~/.claude/ | package root | 44 skills, 12 commands installed |
| .claude/agents/*.md | Agent template files | skills/sk:setup-claude/templates/.claude/agents/ | 15 agent definitions installed per-project |
| .claude/CLAUDE.md | Project context document | Dynamically generated or copied | Not explicitly shown in shipkit.js; may be project-specific |
| .claude/hooks/*.sh | Shell hook scripts | (TBD location in repo) | 8 hooks deployed; trigger SessionStart/PreToolUse/PostToolUse |
| .claude/docs/ | Documentation index | (Generated by sk:setup-claude) | Auto-generated from project README, comments, etc. |

**Note:** `bin/shipkit.js` is the sole installation mechanism. Codex adapter must replicate directory structure expectations.

---

## 8. Tool-Specific Tool Calls (Cross-Platform Compatibility)

| Tool | Usage Pattern | Codex Equivalent? | Notes |
|---|---|---|---|
| Agent | Spawn sub-agents with subagent_type, model, isolation | exec? (differs) | Core difference; parallel spawning not equivalent |
| SendMessage | Agents send messages to team lead | SendMessage (same name?) | Assume Codex has equivalent |
| TaskCreate | Create task with subject, description | TaskCreate (likely same) | Standard task system |
| TaskUpdate | Mark tasks complete, update ownership | TaskUpdate (likely same) | Standard task system |
| TaskList | Query pending/completed tasks | TaskList (likely same) | Standard task system |
| TaskGet | Fetch task details | TaskGet (likely same) | Standard task system |
| Read | Read file contents | Read (likely same) | Universal file read |
| Write | Write/create files | Write (likely same) | Universal file write |
| Edit | Edit file in-place | Edit (likely same) | Universal file edit |
| Bash | Execute shell commands | exec? (likely Codex equiv) | Core tool; name may differ |
| Glob | Search by file pattern | find? (may differ) | Codex may use standard CLI tools |
| Grep | Search file contents | grep? (likely same or integrated) | Codex may use Bash or integrated search |
| Monitor | Stream long-running process output | (TBD) | Codex may have different polling/streaming |
| CronCreate | Schedule recurring tasks | schedule? (may differ) | Remote triggers handled differently |
| EnterWorktree | Create isolated worktree | (NO EQUIVALENT) | Major gap; must rearchitect |
| ExitWorktree | Clean up worktree | (NO EQUIVALENT) | Major gap; must rearchitect |

---

## 9. Settings.json Schema

| Key | Type | Purpose | Examples |
|---|---|---|---|
| permissions | object | Tool allowlist | { "bash": true, "edit": true } |
| hooks | object | Event handlers | { "SessionStart": [...], "PreToolUse": [...] } |
| env | object | Environment variables | { "DEBUG": "true", "NODE_ENV": "production" } |
| model | string | Default model for session | "opus", "sonnet", "haiku" |
| rules | array | Project rules (TBD) | (From CLAUDE.md rules) |

**Critical:** Codex must support equivalent settings.json structure or adapter layer must translate.

---

## 10. Background / Async Features

| Construct | File | Usage | Codex Equivalent? |
|---|---|---|---|
| run_in_background | Bash tool param | Long-running tasks in skills | (Likely yes, but semantics differ) |
| Monitor | (MCP tool) | Stream stdout from process | (TBD; different model) |
| CronCreate | (MCP tool) | Schedule one-off or recurring tasks | RemoteTrigger (Codex system) |
| ScheduleWakeup | (implied in some flows) | Wake agent after delay | (TBD) |

**Note:** Async is secondary concern; most skills are request-response synchronous.

---

## 11. Plan Mode & EnterPlanMode / ExitPlanMode

| Construct | File | Context | Codex Support? |
|---|---|---|---|
| Plan mode | skills/sk:plan/SKILL.md, skills/sk:write-plan/SKILL.md | Decompose tasks into phases; auto-advance | UNCLEAR — May not exist in Codex |
| EnterPlanMode | (tool; not found in search) | Transition to planning phase | (Likely Claude Code specific) |
| ExitPlanMode | (tool; not found in search) | Transition back to execution | (Likely Claude Code specific) |

**Observation:** Plan mode is inferred from skill structure (phases, decision blocks) rather than explicit tool calls. Codex may not need equivalent.

---

## 12. `.claude/` Directory Conventions

| Path | Purpose | Required? | Notes |
|---|---|---|---|
| .claude/agents/*.md | Agent definitions | YES | 15 agent templates; must be installed per-project |
| .claude/commands/sk/*.md | Slash commands | YES | 12 commands installed |
| .claude/skills/sk:*/ | Skill directories | YES | 44 skills, each with SKILL.md + references/ + templates/ |
| .claude/worktrees/<name>/ | Isolated copies | YES (for isolation features) | Auto-created; contains own tasks/, .git/ |
| .claude/hooks/*.sh | Shell hooks | YES (for hooks to work) | 8 hooks; triggered by SessionStart/Pre/PostToolUse |
| .claude/docs/ | Generated docs index | NO (optional) | Auto-generated by sk:setup-claude |
| .claude/settings.json | Project settings | YES | Local overrides; hooks, permissions, env vars |
| .claude/CLAUDE.md | Project context | YES | Primary context document |

**Codex requirement:** Replicate directory structure exactly or use adapter layer to normalize paths.

---

## 13. Advanced Patterns Not Yet Listed

| Pattern | Location | Risk |
|---|---|---|
| **Parallel Agent orchestration with result merging** | sk:gates, sk:autopilot | HIGH — Codex must define new concurrency model |
| **Git worktree branch management** | sk:perf, sk:ci | HIGH — Worktree not available |
| **MCP server OAuth flows** | Multiple (Gmail, Google Calendar, Supabase, PostHog) | MEDIUM — Codex may handle differently |
| **Pencil visual design with batch operations** | sk:frontend-design, sk:mvp | HIGH — No Codex visual editor |
| **SQLite FTS5 context-mode caching** | sk:context-mode (plugin) | HIGH — Codex unlikely to have equivalent |
| **Hook-based PreToolUse validation** | Safety guards, commit validation | MEDIUM — Codex hooks may differ |
| **Model routing in agents** | sk:gates, sk:deep-dive | MEDIUM — Codex must define model selection |
| **Skill auto-discovery & routing** | sk:start, sk:help | LOW — Pure routing logic; language-agnostic |

---

## Translation Difficulty Heatmap

| Category | Difficulty | Effort | Why |
|---|---|---|---|
| Sub-agents (parallel) | **CRITICAL** | 40h+ | Requires complete rearchitecture; Codex `exec` model fundamentally incompatible with in-process parallel spawning |
| Worktree isolation | **CRITICAL** | 30h+ | No git worktree equivalent in Codex; must emulate with branch switching or similar |
| Pencil MCP (visual design) | **HIGH** | 25h+ | No visual design editor in Codex ecosystem; must either disable sk:frontend-design or build new adapter |
| Context-mode plugin | **HIGH** | 20h+ | Codex unlikely to have SQLite FTS5 output caching; must use alternative large-output strategy |
| Settings.json hooks | **HIGH** | 15h+ | Codex hook system unknown; must research PreToolUse/PostToolUse equivalents |
| Agent definitions & .claude/agents/ | **MEDIUM** | 10h | Straight translation; same schema, different spawning semantics |
| Commands & skills structure | **MEDIUM** | 8h | File structure copy; frontmatter schema must match or translate |
| MCP servers (Google, Supabase, etc.) | **MEDIUM** | 5h | Likely Codex-compatible; may need OAuth re-auth |
| Task system (TaskCreate, TaskList, etc.) | **LOW** | 2h | Assume standard; verify naming |
| Bash/Read/Write/Glob/Grep | **LOW** | 1h | Assume standard CLI equivalents exist |

---

## Next Steps for Codex Adapter

1. **Validate Agent spawning model** — Determine if Codex supports parallel sub-agent execution; if not, serialize workflows
2. **Design worktree replacement** — Research Codex branch/namespace isolation strategies
3. **Pencil fallback strategy** — Decide: disable visual design, or build Codex-native Sketch/Figma integration
4. **Context-mode alternative** — Evaluate Codex's built-in output summarization (if any); fallback to chunked summaries
5. **Hook system mapping** — Map Claude Code's 8 hooks to Codex equivalents (may be 1:1 or require new abstractions)
6. **MCP inventory audit** — Confirm which MCP servers Codex supports natively; plan OAuth migration
7. **Test skill subset** — Pilot 3-4 skills (e.g., sk:plan, sk:write-tests, sk:debug) end-to-end on Codex

---

## Files Involved (Source of Truth)

- `/Users/kennethsolomon/Herd/shipkit/bin/shipkit.js` — Installation script
- `/Users/kennethsolomon/Herd/shipkit/skills/sk:*/SKILL.md` — 44 skills with frontmatter
- `/Users/kennethsolomon/Herd/shipkit/commands/sk/*.md` — 12 commands with frontmatter
- `/Users/kennethsolomon/Herd/shipkit/skills/sk:setup-claude/templates/.claude/agents/*.md` — 15 agent templates
- `/Users/kennethsolomon/Herd/shipkit/skills/sk:setup-claude/SKILL.md` — Hook definitions, agent patterns
- `/Users/kennethsolomon/Herd/shipkit/skills/sk:gates/SKILL.md` — Parallel orchestration pattern
- `/Users/kennethsolomon/Herd/shipkit/skills/sk:frontend-design/SKILL.md` — Pencil integration
- `/Users/kennethsolomon/Herd/shipkit/.claude/` — Live settings, hooks, agents (per-project)


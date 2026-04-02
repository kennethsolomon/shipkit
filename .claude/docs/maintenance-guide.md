# ShipKit Maintenance Guide

When ShipKit changes, use this guide to find every file that needs updating.
`CLAUDE.md` is the single source of truth — all other files derive from it.

---

## When You Add/Remove/Rename a Workflow Step

Current steps: 0 (optional), 1, 2, 3, 4, 5, 5.5, 6, 7, 7.5 (autopilot only), 8, 8.5, 8.6

| File | What to change |
|------|---------------|
| `CLAUDE.md` | Workflow table + Step Details (source of truth) |
| `commands/sk/help.md` | Feature Workflow table — must mirror CLAUDE.md exactly |
| `skills/sk:autopilot/SKILL.md` | Intro paragraph (line 9), Steps section, Quality Guarantee section |
| `skills/sk:gates/SKILL.md` | "When to Use" — step number reference |
| `skills/sk:team/SKILL.md` | QA scenarios collection note — step number reference |
| `skills/sk:setup-optimizer/SKILL.md` | Diagnostics (line 47), workflow description (lines 62, 64, 68) |
| `skills/sk:setup-claude/templates/CLAUDE.md.template` | Workflow table + Step Details — template for new projects |
| `.claude/docs/DOCUMENTATION.md` | Complete Workflow Flow section + tutorial step references |
| `docs/sk:features/sk-autopilot.md` | Workflow position note, step count references |
| `README.md` | Scenario A tutorial |

**Verification after change:**
```bash
grep -rn "step [0-9]\+\|[0-9] steps\|[0-9]-step\|all [0-9] step" \
  commands/sk/ skills/sk:gates/ skills/sk:team/ \
  skills/sk:autopilot/ skills/sk:setup-optimizer/
```

---

## When You Add/Remove/Rename an Agent

Agent definitions live in `.claude/agents/`. Setup-optimizer validates 13 core agents by name.

| File | What to change |
|------|---------------|
| `.claude/agents/<name>.md` | Create or delete |
| `skills/sk:setup-optimizer/SKILL.md` | "13 core agents" list (line 49) — update count and name |
| `skills/sk:setup-claude/templates/.claude/agents/` | Add/remove template agent file |
| `CLAUDE.md` | Commands table (if user-facing) |
| `commands/sk/help.md` | All Commands table (if user-facing) |
| `~/.claude/skills/learned/shipit/read-only-agents-report-write-agents-fix.md` | Update learned pattern |

**Isolation decision matrix — every write-capable agent must follow this:**

| Situation | Isolation |
|-----------|-----------|
| Runs in parallel (sk:team or sk:gates Batch 1) + writes source code | `isolation: worktree` in frontmatter |
| Runs solo + must see real working state (e.g., debugger) | No isolation — add `<!-- DESIGN NOTE -->` comment |
| Runs in background + writes only test files (e.g., qa-engineer) | No isolation — add `<!-- DESIGN NOTE -->` comment |
| Writes only documentation files (e.g., tech-writer) | No isolation — add `<!-- DESIGN NOTE -->` comment |
| Read-only (no Edit/Write tools) | Nothing needed |

Every write-capable agent MUST have either `isolation: worktree` in its frontmatter OR a
`<!-- DESIGN NOTE: No isolation... -->` comment in the body explaining why.

---

## When You Add/Remove/Rename a Skill or Command

| File | What to change |
|------|---------------|
| `skills/sk:<name>/SKILL.md` | Create or delete |
| `commands/sk/<name>.md` | Create or delete (if slash-command-accessible) |
| `CLAUDE.md` | Commands table |
| `commands/sk/help.md` | All Commands table |
| `skills/sk:setup-optimizer/SKILL.md` | "Missing commands" list (line 48) if it's a core command |
| `skills/sk:setup-claude/templates/CLAUDE.md.template` | Commands table |
| `docs/sk:features/sk-<name>.md` | Create or delete feature spec |
| `docs/FEATURES.md` | Add/remove entry |
| `README.md` | Scenario tutorials or skill descriptions (if user-visible) |

---

## When You Change a Skill's Behavior (without adding/removing it)

For internal mechanic upgrades to existing skills (e.g., progressive disclosure in `/sk:context`, ultraqa cycling in `/sk:test`):

| File | What to change |
|------|---------------|
| `skills/sk:<name>/SKILL.md` | Update behavior description |
| `docs/sk:features/sk-<name>.md` | Update feature spec |
| `docs/FEATURES.md` | Bump spec date + version in Spec Status table |
| `CLAUDE.md` | Only if behavior change affects workflow rules or step descriptions |
| `README.md` | Only if behavior change is user-visible (new flags, changed output format) |
| `skills/sk:setup-claude/templates/commands/<name>.md.template` | If the skill has a template variant |

**Propagation:** Skill behavior changes reach users automatically via `npm install -g @kennethsolomon/shipkit && shipkit`. No `/sk:setup-optimizer` run needed for the skill content itself.

---

## When You Add/Remove a Hook

| File | What to change |
|------|---------------|
| `.claude/hooks/<hook>.sh` | Create, modify, or delete |
| `.claude/settings.json` | Add/remove under the correct lifecycle key |
| `skills/sk:setup-optimizer/SKILL.md` | Core/enhanced hook lists **AND** report string hook count (`X/7 core, Y/7 enhanced`) |
| `skills/sk:setup-claude/templates/hooks/` | Add/remove template file (deployed to new projects) |
| `skills/sk:setup-claude/templates/.claude/settings.json.template` | Add/remove hook wiring |
| `README.md` | Always-installed or Opt-in hooks table (Lifecycle Hooks section) |

**Hook lifecycle keys in settings.json:** `SessionStart`, `SessionStop`, `PreToolUse`, `PostToolUse`, `Stop`, `UserPromptSubmit`, `SubagentStart`, `PreCompact`

**Core vs enhanced classification:**
- **Core** (always deployed by setup-optimizer): hooks required for the workflow to function — session lifecycle, commit validation, keyword routing
- **Enhanced** (opt-in, deployed on user confirmation): quality-of-life hooks — formatting, warnings, logging, safety

**When you add a hook, also update the count** in `skills/sk:setup-optimizer/SKILL.md`:
```
> "Hooks: [X/N core, Y/N enhanced] installed
```
Current counts: **7 core, 7 enhanced** (as of v3.24.0)

---

## When You Add/Remove a Community Plugin or CLI Tool

External tools (not owned by ShipKit) that are recommended and integrated into setup flows. Two sub-types with different install patterns:

### Sub-type A — Claude Plugin (e.g. context-mode, context7)

| File | What to change |
|------|---------------|
| `skills/sk:setup-claude/SKILL.md` | MCP Servers & Plugins section — add/remove under numbered list. Update prompt string. |
| `skills/sk:setup-optimizer/SKILL.md` | Step 1.7 — add/remove from numbered check list. Update `X/N configured` count. Update install/update instructions. |
| `README.md` | Recommended Community Plugins table under MCP Servers section |
| `.claude/docs/maintenance-guide.md` | This guide — update if plugin changes the maintenance process |

**For install:** provide `/plugin marketplace add <org>/<repo>` + `/plugin install <name>@<name>` commands.
**For update:** provide the plugin's own upgrade command (e.g., `/context-mode:ctx-upgrade`).
**For check:** use `claude plugin list 2>/dev/null | grep <name>` to detect presence and version.

### Sub-type B — CLI Tool (e.g. agent-browser)

| File | What to change |
|------|---------------|
| `skills/sk:setup-claude/SKILL.md` | MCP Servers & Plugins section — add/remove under numbered list. Update prompt string. |
| `skills/sk:setup-optimizer/SKILL.md` | Step 1.7 — add/remove from numbered check list. Update `X/N configured` count. Update install instructions. |
| `README.md` | Recommended CLI Tools table under MCP Servers section |
| `skills/sk:<skill>/SKILL.md` | The skill that uses this tool — update detection/priority logic |
| `.claude/docs/maintenance-guide.md` | This guide — update if tool changes the maintenance process |

**For install:** provide `npm install -g <pkg> && <pkg> install` (or equivalent).
**For update:** `npm install -g <pkg>` (standard npm global update).
**For check:** use `<cmd> --version 2>/dev/null` to detect presence and version.

---

## When You Change Gate Configuration

Gates live in `skills/sk:gates/SKILL.md`. Batch order affects agent invocation.

| File | What to change |
|------|---------------|
| `skills/sk:gates/SKILL.md` | Batch definitions, agent list, auto-skip rules |
| `CLAUDE.md` | Workflow Rules section rule 3 (auto-skip detection) |
| `skills/sk:autopilot/SKILL.md` | Step 7 gate list |
| `commands/sk/help.md` | Step 7 row in Feature Workflow table |
| `.claude/agents/<gate-agent>.md` | If the invoked agent itself changes |

**Auto-skip rules must be documented in BOTH:**
- `CLAUDE.md` → Workflow Rules → rule 3
- `skills/sk:gates/SKILL.md` → Batch 1 → performance-optimizer bullet

---

## How Updates Reach Existing Projects

Understanding this propagation path is essential — different change types require different user actions.

| Change type | User action to receive update |
|-------------|------------------------------|
| Skill behavior change (`SKILL.md`) | `npm install -g @kennethsolomon/shipkit && shipkit` |
| New or modified hook script | `npm install -g @kennethsolomon/shipkit && shipkit` → then `/sk:setup-optimizer` (Step 1.5 deploys missing hooks) |
| New `settings.json` hook wiring | `npm install -g @kennethsolomon/shipkit && shipkit` → then `/sk:setup-optimizer` (Step 1.5 merges new entries additively) |
| New agent definition | `npm install -g @kennethsolomon/shipkit && shipkit` → then `/sk:setup-optimizer` (Step 1.8 deploys missing agents) |
| CLAUDE.md workflow section update | `/sk:setup-optimizer` (Step 1 refreshes the workflow section from the latest template) |
| New slash command | `npm install -g @kennethsolomon/shipkit && shipkit` |
| New rule file | `npm install -g @kennethsolomon/shipkit && shipkit` → then `/sk:setup-optimizer` (Step 1.8 deploys missing rules) |

**Summary: `/sk:setup-optimizer` is the single command that applies all hook, settings, agent, rule, and CLAUDE.md updates to existing projects.** Skill content (SKILL.md files) updates via npm only.

**For new hook scripts specifically:** the optimizer detects the missing `.sh` file, deploys it from the templates directory, and merges the new settings.json entry — all in one confirmation step. Users never need to manually edit settings.json.

---

## Canonical File Roles

| File | Role | Updated when |
|------|------|-------------|
| `CLAUDE.md` | **Source of truth** | Intentional workflow change |
| `commands/sk/help.md` | **Derived** — user command reference | Any step or command change |
| `skills/sk:autopilot/SKILL.md` | **Derived** — orchestrates full workflow | Any step change |
| `skills/sk:gates/SKILL.md` | **Derived** — orchestrates step 7 | Gate config or step change |
| `skills/sk:team/SKILL.md` | **Derived** — parallel implementation | Agent or step 5 change |
| `skills/sk:setup-optimizer/SKILL.md` | **Derived** — workflow health checker | Any step, agent, command, or hook change |
| `skills/sk:setup-claude/templates/CLAUDE.md.template` | **Template** — bootstraps new projects | Any canonical workflow change |
| `skills/sk:setup-claude/templates/.claude/settings.json.template` | **Template** — wires hooks for new projects | Any hook addition/removal |
| `skills/sk:setup-claude/templates/hooks/` | **Templates** — hook scripts for new projects | Any hook addition/modification |
| `.claude/agents/*.md` | **Definitions** — agent behavior | Agent capability or isolation change |
| `.claude/docs/DOCUMENTATION.md` | **Reference** — feature detail docs | Major feature or step change |
| `docs/sk:features/*.md` | **Specs** — per-feature documentation | Feature change |

---

## Quick Checklist After Any Workflow Change

- [ ] Update `CLAUDE.md` (source of truth)
- [ ] Run `grep -rn "step [0-9]\+" skills/ commands/` — fix every stale step number
- [ ] Run `grep -rn "[0-9] steps\|[0-9]-step" skills/ commands/` — fix every stale step count
- [ ] `commands/sk/help.md` Feature Workflow table matches `CLAUDE.md` table exactly
- [ ] `skills/sk:setup-optimizer/SKILL.md` diagnostics reflect new step count
- [ ] `skills/sk:setup-claude/templates/CLAUDE.md.template` matches `CLAUDE.md` workflow table
- [ ] All write-capable agents have `isolation: worktree` OR a `<!-- DESIGN NOTE -->` comment
- [ ] Create entry in `.claude/docs/architectural_change_log/` for the change

## Quick Checklist After Any Hook Change

- [ ] Hook script created in `.claude/hooks/` and `skills/sk:setup-claude/templates/hooks/`
- [ ] `skills/sk:setup-claude/templates/.claude/settings.json.template` has the new wiring
- [ ] `.claude/settings.json` (this project) has the new wiring
- [ ] `skills/sk:setup-optimizer/SKILL.md` core/enhanced lists updated
- [ ] `skills/sk:setup-optimizer/SKILL.md` report string count updated (`X/N core, Y/N enhanced`)
- [ ] `skills/sk:setup-optimizer/SKILL.md` deployed hooks example updated
- [ ] `README.md` Lifecycle Hooks table updated (Always installed or Opt-in)
- [ ] Create entry in `.claude/docs/architectural_change_log/` for the change

---

Last updated: 2026-04-02 (agent-browser CLI tool sub-type added)

# ShipKit Maintenance Guide

When ShipKit changes, use this guide to find every file that needs updating.
`CLAUDE.md` is the single source of truth — all other files derive from it.

---

## When You Add/Remove/Rename a Workflow Step

Current steps: 1, 2, 3, 4, 5, 5.5, 6, 7, 8, 8.5, 8.6

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

## When You Change Hooks

| File | What to change |
|------|---------------|
| `.claude/hooks/<hook>.sh` | Create, modify, or delete |
| `.claude/settings.json` | Add/remove under the correct lifecycle key |
| `skills/sk:setup-optimizer/SKILL.md` | Core/enhanced hook lists |
| `skills/sk:setup-claude/templates/hooks/` | Update template (deployed to new projects) |
| `skills/sk:setup-claude/templates/settings.json.template` | Update wiring template |

**Hook lifecycle keys in settings.json:** `SessionStart`, `SessionStop`, `PreToolUse`, `PostToolUse`, `Stop`

---

## Canonical File Roles

| File | Role | Updated when |
|------|------|-------------|
| `CLAUDE.md` | **Source of truth** | Intentional workflow change |
| `commands/sk/help.md` | **Derived** — user command reference | Any step or command change |
| `skills/sk:autopilot/SKILL.md` | **Derived** — orchestrates full workflow | Any step change |
| `skills/sk:gates/SKILL.md` | **Derived** — orchestrates step 7 | Gate config or step change |
| `skills/sk:team/SKILL.md` | **Derived** — parallel implementation | Agent or step 5 change |
| `skills/sk:setup-optimizer/SKILL.md` | **Derived** — workflow health checker | Any step, agent, or command change |
| `skills/sk:setup-claude/templates/CLAUDE.md.template` | **Template** — bootstraps new projects | Any canonical workflow change |
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

---

Last updated: 2026-03-29

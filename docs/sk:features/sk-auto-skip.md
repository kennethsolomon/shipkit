# Auto-Skip Intelligence

> **Status:** Shipped
> **Type:** Workflow Enhancement
> **Workflow Position:** Applies to optional steps (Design, Migrate, Performance)
> **Command:** N/A — built into workflow rules
> **Config:** `CLAUDE.md` Workflow Rules section

---

## Overview

Automatically detects and skips optional workflow steps when they're clearly not needed, based on keyword scanning of `tasks/todo.md`. Eliminates confirmation prompts for obvious skips. Works in both manual and autopilot modes.

---

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| `tasks/todo.md` | Plan content for keyword scanning | Yes |

---

## Outputs

| Output | Destination | Notes |
|--------|-------------|-------|
| Skip log line | Terminal | `Auto-skipped: [Step Name] ([reason])` |

---

## Business Logic

1. After plan is written (step 3), scan `tasks/todo.md` for signal keywords
2. For each optional step, check detection criteria:
   - **Step 2 (Design)**: Skip if NO frontend keywords (component, view, page, CSS, template, blade, vue, react, svelte, UI, form, modal, button) AND NO API keywords (endpoint, route, controller, API)
   - **Migrate** (inside step 5): Skip if NO database keywords (migration, schema, table, column, model, database, foreign key, index, seed)
   - **Performance** (inside gates): Skip if NO frontend AND NO database keywords
3. Release (inside step 8) is NEVER auto-skipped
4. Output log line for each auto-skipped step

---

## Hard Rules

- Never auto-skip Release — deployment decisions always require user input
- Auto-skip applies in BOTH manual and autopilot modes
- No confirmation prompt — just a log line
- Detection runs AFTER plan is written (step 3), not before

---

## Edge Cases

| Scenario | Behavior |
|----------|----------|
| Plan contains ambiguous keywords (e.g., "model" could mean DB model or UI model) | Keyword match is literal — if "model" appears, migration is NOT auto-skipped |
| Plan is empty or missing | No auto-skip — all optional steps ask for confirmation |
| User overrides with explicit skip/no-skip | User override takes precedence over auto-detection |

---

## Error States

| Condition | Behavior |
|-----------|----------|
| `tasks/todo.md` doesn't exist | Skip detection silently — fall back to manual confirmation |
| Plan has no content | Same as above |

---

## UI/UX Behavior

### CLI Output
```
Auto-skipped: Design (no frontend keywords detected in plan)
Auto-skipped: Accessibility (no frontend keywords detected in plan)
Auto-skipped: Migration (no database keywords detected in plan)
```

### When Done
No explicit "done" message — auto-skip is inline during workflow execution.

---

## Platform Notes

N/A — CLI tool only.

---

## Related Docs

- `CLAUDE.md` — Workflow Rules (rule 3: auto-skip detection)
- `skills/sk:setup-claude/templates/CLAUDE.md.template` — template version
- `skills/sk:setup-optimizer/SKILL.md` — upgrades existing projects with auto-skip rules

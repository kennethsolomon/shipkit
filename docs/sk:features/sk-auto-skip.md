# Auto-Skip Intelligence

> **Status:** Shipped
> **Type:** Workflow Enhancement
> **Workflow Position:** Applies to optional steps (4, 5, 8, 15)
> **Command:** N/A — built into workflow tracker rules
> **Config:** `CLAUDE.md` Workflow Tracker Rules section

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
| Workflow tracker update | `tasks/workflow-status.md` | Step marked as `skipped` with reason |

---

## Business Logic

1. After plan is written (step 6), scan `tasks/todo.md` for signal keywords
2. For each optional step, check detection criteria:
   - **Step 4 (Design)**: Skip if NO frontend keywords (component, view, page, CSS, template, blade, vue, react, svelte, UI, form, modal, button)
   - **Step 5 (Accessibility)**: Skip if NO frontend keywords (same list)
   - **Step 8 (Migrate)**: Skip if NO database keywords (migration, schema, table, column, model, database, foreign key, index, seed)
   - **Step 15 (Performance)**: Skip if NO frontend AND NO database keywords
3. Step 21 (Release) is NEVER auto-skipped
4. Output log line for each auto-skipped step
5. Update workflow tracker with skip reason

---

## Hard Rules

- Never auto-skip step 21 (Release) — deployment decisions always require user input
- Auto-skip applies in BOTH manual and autopilot modes
- No confirmation prompt — just a log line
- Detection runs AFTER plan is written (step 6), not before

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

- `CLAUDE.md` — Workflow Tracker Rules (rule 4: auto-skip detection)
- `skills/sk:setup-claude/templates/CLAUDE.md.template` — template version
- `skills/sk:setup-optimizer/SKILL.md` — upgrades existing projects with auto-skip rules

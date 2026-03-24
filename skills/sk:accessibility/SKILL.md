---
name: sk:accessibility
description: WCAG 2.1 AA accessibility audit. Use after /sk:frontend-design or on existing frontend code to catch accessibility issues before implementation or before shipping. Reports findings — does NOT fix code.
license: Complete terms in LICENSE.txt
---

## Purpose

Audit the frontend design spec or existing UI code for WCAG 2.1 AA compliance. This is an audit skill — it identifies issues and produces a findings report. It does NOT fix code.

Run this skill:
- **After `/sk:frontend-design`** — validate the design spec before implementation starts
- **Before `/sk:finish-feature`** — validate the implemented UI before merging
- **On existing code** — audit any frontend code or component

## Hard Rules

- **DO NOT fix code.** Report only. The user decides what to fix.
- **Every finding must cite a specific design spec section, file, or component.**
- **Every finding must reference the WCAG criterion it violates** (e.g., WCAG 1.4.3).
- **Skip if the task is backend-only** — ask "Is there any frontend component?" before proceeding.

## Before You Start

1. Determine scope: design spec (from `/sk:frontend-design` output) or existing code files?
2. If auditing code: `git diff main..HEAD --name-only` to find changed frontend files.
3. If `tasks/accessibility-findings.md` exists, read it — check if prior findings have been addressed.
4. If `tasks/lessons.md` exists, read it — apply accessibility-related lessons as targeted checks.

## Audit Checklist

### 1. Color & Contrast (WCAG 1.4.3, 1.4.11)
- Normal text (< 18px / < 14px bold): minimum **4.5:1** contrast ratio against background
- Large text (≥ 18px or ≥ 14px bold): minimum **3:1** contrast ratio
- UI components and graphical objects (borders, icons, chart elements): minimum **3:1**
- Check all color palette combinations from the design spec
- Verify disabled states are still distinguishable (not just greyed out with no other indicator)

### 2. Keyboard Navigation (WCAG 2.1.1, 2.1.2, 2.4.3, 2.4.7)
- All interactive elements reachable by Tab key
- Logical tab order (follows visual reading order)
- No keyboard traps (user can always navigate away)
- Visible focus indicator on all interactive elements (not removed with `outline: none` without replacement)
- Modal/dialog focus management: focus moves into modal on open, returns to trigger on close
- Skip navigation link present for pages with repeated navigation
- Modals and multi-step flows must have a visible cancel/back affordance — no dead ends (WCAG 3.2.2)
- Do not override or intercept system/platform keyboard shortcuts (Tab, arrow keys, Escape, VoiceOver gestures)

### 3. ARIA & Semantics (WCAG 4.1.2, 1.3.1)
- Semantic HTML first (`<button>`, `<nav>`, `<main>`, `<header>`) — ARIA only when HTML is insufficient
- All interactive elements have accessible names (via label, aria-label, or aria-labelledby)
- Icons-only buttons have `aria-label` or visually hidden text
- Dynamic content updates announced via `aria-live` regions where appropriate
- No invalid ARIA roles or attributes
- Form inputs associated with labels (via `<label for>` or `aria-labelledby`)

### 4. Images & Media (WCAG 1.1.1, 1.2.x)
- Informative images have descriptive `alt` text
- Decorative images have `alt=""` (empty alt, not missing)
- Complex images (charts, diagrams) have long descriptions
- Videos have captions; audio has transcripts

### 5. Forms (WCAG 1.3.5, 3.3.1, 3.3.2)
- All fields have visible labels (not just placeholder text — placeholders disappear on input)
- Required fields indicated (not by color alone)
- Error messages: specific, descriptive, associated with the field (`aria-describedby`)
- Error messages do not disappear on blur
- Autocomplete attributes on common fields (`name`, `email`, `tel`, etc.)

### 6. Motion & Animation (WCAG 2.3.1, 2.3.3)
- No content flashes more than 3 times per second
- All non-essential animations respect `prefers-reduced-motion` media query
- Auto-playing animations can be paused, stopped, or hidden

### 7. iOS Dynamic Type (Apple HIG)
- UI must remain fully readable and usable when system font size is at the largest accessibility setting
- No text truncation at large sizes — prefer wrapping over ellipsis
- All layouts must reflow correctly without overlapping or clipping at Dynamic Type XXL
- Avoid fixed heights on elements that contain text — use dynamic sizing
- Test at: Settings → Accessibility → Display & Text Size → Larger Text (max slider)

### 8. Content & Structure (WCAG 1.3.1, 2.4.6, 2.4.2)
- Single `<h1>` per page; heading hierarchy is logical (no skipped levels)
- Page has a descriptive `<title>`
- Link text is descriptive standalone ("Read the docs" not "Click here")
- Tables have `<th>` headers with appropriate scope
- Language declared (`<html lang="en">`)

## Generate Report

Write findings to `tasks/accessibility-findings.md`:

```markdown
# Accessibility Audit — YYYY-MM-DD

**Scope:** [design spec | changed files on branch `<branch>`]
**Standard:** WCAG 2.1 AA

## Failures (must fix)

- [ ] **[Component/File:Line]** Description
  **Criterion:** WCAG X.X.X — [Name]
  **Impact:** [Who is affected and how]
  **Recommendation:** [How to fix]

- [x] **[Component/File:Line]** Description *(resolved)*
  **Criterion:** WCAG X.X.X — [Name]
  **Impact:** [Who is affected and how]
  **Recommendation:** [How to fix]

## Warnings (should fix)

- [ ] **[Component/File:Line]** Description
  **Criterion:** WCAG X.X.X — [Name]
  **Recommendation:** [How to fix]

## Manual Checks Required

- [ ] [Things that require human/screen reader testing]

## Passed Checks

- [Categories that passed with no findings]

## Summary

| Level    | Open | Resolved this run |
|----------|------|-------------------|
| Failures | N    | N                 |
| Warnings | N    | N                 |
| Manual   | N    | N                 |
```

**Never overwrite** `tasks/accessibility-findings.md` — append new audits with a date header.

## When Done

Tell the user:

> "Accessibility audit complete. Findings saved to `tasks/accessibility-findings.md`.
> - **Failures:** N | **Warnings:** N | **Manual checks:** N
>
> Address failures before implementation, then run `/sk:write-plan` to proceed."

If there are no failures:
> "No accessibility failures found. N warnings noted. Run `/sk:write-plan` to proceed."

---

## Model Routing

Read `.shipkit/config.json` from the project root if it exists.

- If `model_overrides["sk:accessibility"]` is set, use that model — it takes precedence.
- Otherwise use the `profile` field. Default: `balanced`.

| Profile | Model |
|---------|-------|
| `full-sail` | sonnet |
| `quality` | sonnet |
| `balanced` | sonnet |
| `budget` | haiku |

> `opus` = inherit (uses the current session model). When spawning sub-agents via the Agent tool, pass `model: "<resolved-model>"`.

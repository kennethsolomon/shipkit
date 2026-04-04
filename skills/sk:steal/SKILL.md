---
name: sk:steal
description: "Review an external source (GitHub repo, article, screenshot, URL) and extract ideas to adapt into ShipKit or the current project. Use when the user shares a link, screenshot, or reference and wants to evaluate what's useful, compare with existing capabilities, and implement adaptations."
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Agent, WebFetch, WebSearch, mcp__plugin_context-mode_context-mode__ctx_batch_execute, mcp__plugin_context-mode_context-mode__ctx_search, mcp__plugin_context-mode_context-mode__ctx_fetch_and_index, mcp__plugin_context-mode_context-mode__ctx_execute
---

# Steal & Adapt

Review external sources, extract what's useful, and adapt it into the project.

## Input Detection

Classify the source type from the user's input:

| Source | How to Fetch |
|--------|-------------|
| **GitHub repo URL** | Use `ctx_batch_execute` to fetch README, tree, key files via GitHub raw/API URLs |
| **Article / blog URL** | Use `ctx_fetch_and_index` to fetch and index the page content |
| **Screenshot / image path** | Use `Read` to view the image, then describe what you see |
| **Pasted text / code block** | Already in context — proceed to analysis |
| **npm / PyPI / crate** | Fetch the package page + repo README |

For GitHub repos, prioritize fetching: README, directory tree, config files (CLAUDE.md, settings.json, package.json), then key source files based on what looks interesting from the tree.

## Analysis — 3 Parallel Lanes

Run these in parallel using subagents when the source is large enough to warrant it:

### Lane 1: Extract Ideas

Identify concrete, actionable ideas from the source:
- Patterns, techniques, workflows, or conventions
- Specific implementations worth replicating
- Architectural decisions or design approaches
- Tools, hooks, configs, or automation

For each idea, capture:
- **What**: One-line description
- **Why it's good**: What problem it solves or what it improves
- **Effort**: Low / Medium / High to adapt

### Lane 2: Compare with Existing

For each extracted idea, check what we already have:
- Grep/glob the codebase for equivalent functionality
- Check skills/, commands/, hooks, settings, CLAUDE.md
- Classify: **New** (we don't have it) / **Better** (theirs is better) / **Covered** (we already handle it) / **Worse** (ours is better)

### Lane 3: Adaptation Plan

For ideas classified as **New** or **Better**, draft how to adapt:
- Which files to create or modify
- How to integrate with existing patterns (skill format, hook format, etc.)
- Any dependencies or prerequisites

## Output — Steal Report

Present findings in this format:

```
## Steal Report: [Source Name]

### Worth Stealing
| # | Idea | Status | Effort | Adaptation |
|---|------|--------|--------|------------|
| 1 | [idea] | New | Low | [how] |
| 2 | [idea] | Better | Med | [how] |

### Already Covered
| Idea | Our Equivalent | Verdict |
|------|---------------|---------|
| [their thing] | [our thing] | Ours is [better/equivalent] because [why] |

### Not Worth It
| Idea | Why Skip |
|------|----------|
| [idea] | [reason — too niche, wrong stack, over-engineered, etc.] |
```

## Implementation

After presenting the report:

1. Ask the user which items to implement (suggest a default set)
2. For each approved item:
   - If it's a **new skill**: use `/sk:skill-creator` conventions (SKILL.md with frontmatter)
   - If it's a **hook**: write to `.claude/hooks/` following existing hook patterns
   - If it's a **rule/config change**: edit the appropriate file
   - If it's a **pattern/convention**: update CLAUDE.md or relevant docs
3. Never copy code verbatim from the source — adapt to our conventions and style
4. Credit the source in a comment or commit message

## Rules

- Always compare before suggesting — don't recommend what we already have
- Prefer adapting over wholesale copying
- Skip ideas that only work for a specific tech stack we don't use
- Be honest about "not worth it" — not everything external is better
- If the source is a competitor/alternative to ShipKit, focus on feature gaps, not replacement
- Keep token cost in mind — don't recommend always-loaded rules for niche concerns

---
name: sk:learn
description: "Extract reusable patterns from the current session into learned instincts."
---

# /sk:learn — Extract Reusable Patterns

Analyzes the current session for extractable patterns and saves them as learned instincts. Patterns evolve from tentative observations into strong conventions over time.

## Usage

```
/sk:learn                  # analyze current session
/sk:learn --list           # show all learned patterns
/sk:learn --promote <id>   # promote project pattern to global
/sk:learn --export         # export patterns as shareable file
```

## Model Routing

Read `.shipkit/config.json` from the project root if it exists.

| Profile | Model |
|---------|-------|
| `full-sail` | haiku |
| `quality` | haiku |
| `balanced` | haiku |
| `budget` | haiku |

> Pattern detection is lightweight keyword matching — haiku is sufficient.

## How It Works

### Phase 1: Session Analysis

Scan the current conversation for extractable patterns:

1. **Error resolutions** — problems encountered and how they were solved
2. **Debugging techniques** — investigation steps that led to root causes
3. **Workarounds** — non-obvious solutions to framework/tool limitations
4. **Project conventions** — naming patterns, file organization, code style decisions
5. **Tool usage patterns** — effective tool combinations and sequences

Filter out trivial items:
- Typo fixes, syntax errors, simple formatting
- One-off configuration changes
- Standard framework usage (documented in official docs)

### Phase 2: Pattern Extraction

For each candidate pattern, extract:

```markdown
---
name: [descriptive-slug]
type: [error-resolution | debugging | workaround | convention | tool-usage]
confidence: [0.3 | 0.5 | 0.7 | 0.9]
scope: [project | global]
created: [YYYY-MM-DD]
seen_count: 1
---

## Problem
[What triggered this pattern]

## Solution
[What resolved it — specific steps]

## Example
[Concrete code or command example]

## When to Apply
[Conditions that indicate this pattern is relevant]
```

### Phase 3: Confidence Scoring

| Score | Label | Meaning |
|-------|-------|---------|
| 0.3 | tentative | Seen once, might be coincidence |
| 0.5 | emerging | Seen in similar contexts, likely a real pattern |
| 0.7 | strong | Proven effective multiple times |
| 0.9 | near-certain | Battle-tested, consistently reliable |

New patterns start at 0.3. Confidence increases when:
- Same pattern seen again in a different session (+0.2)
- User explicitly confirms the pattern (+0.2)
- Pattern seen in a different project (+0.1, also promotes to global)

### Phase 4: Storage

- **Project patterns**: `~/.claude/skills/learned/[project-name]/[pattern-name].md`
- **Global patterns**: `~/.claude/skills/learned/global/[pattern-name].md`

### Phase 5: User Confirmation

Present extracted patterns and ask for confirmation before saving:

```
Extracted 3 patterns from this session:

1. [error-resolution] "laravel-queue-retry-after" (0.3 tentative)
   Problem: Queue jobs silently failing after Redis timeout
   Solution: Set retry_after in queue config > job timeout

2. [convention] "api-resource-wrapping" (0.3 tentative)
   Problem: Inconsistent API response format
   Solution: Always wrap in ApiResource with data key

3. [tool-usage] "parallel-explore-before-implement" (0.3 tentative)
   Problem: Missing context leads to wrong implementation
   Solution: Launch 3 Explore agents before writing code

Save patterns? (all / 1,3 / none)
```

### Phase 6: Skill Improvement Pass

After saving patterns, scan the current session for evidence that any ShipKit skill underperformed:

**Signals to look for:**
- A skill was invoked, then its output was immediately corrected or overridden by the user
- A gate skill (lint, security, perf, deps-audit, review) failed to catch something that was caught later
- The user said "no", "don't", "wrong", "instead", or "again" in response to a skill's output
- A skill ran 2+ retries because its first attempt was wrong

**If signals found**, present:
```
Skill improvement candidates:
1. sk:finish-feature — CI monitor loop timed out twice before CI passed (suggest: increase default poll interval)
2. sk:gates — deps-audit was skipped but CVE was found in security-reviewer (suggest: always run deps-audit)

Improve any of these? (1 / 2 / all / none)
```

If user confirms → open the skill's SKILL.md and propose a targeted diff to address the specific failure. Use `/sk:skill-creator` to apply the change.

If no signals found → skip silently (no output for this phase).

## Promotion: Project to Global

A pattern is auto-promoted to global when:
- Same pattern (by name or content similarity) appears in 2+ projects
- Confidence >= 0.7 in both projects
- User hasn't marked it as project-specific

Manual promotion: `/sk:learn --promote <pattern-id>`

## Export / Import

Export all patterns for sharing:
```
/sk:learn --export > my-patterns.json
```

Import from a colleague:
```
/sk:learn --import colleague-patterns.json
```

Imported patterns start at 0.3 confidence regardless of source confidence.

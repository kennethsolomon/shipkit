# Findings — 2026-03-16 — New Skill: sk:seo-audit

## Problem Statement

Freelance developers need a way to audit and fix common SEO issues across client projects, regardless of framework. No current skill in the workflow addresses SEO. Missing meta tags, broken robots.txt, duplicate title tags, and missing alt text are objective, measurable issues that directly impact search rankings and are fully automatable — but they go undetected without a dedicated tool.

## Key Decisions Made

- **Skill type:** Standalone optional command (not a numbered workflow step). Like `/sk:debug` — invokable at any time, not tied to step order. No workflow renumbering required.
- **Audit mode:** Dual-mode — primary pass reads source template files (`.blade.php`, `.jsx`, `.tsx`, `.vue`, `.html`, etc.), secondary pass fetches from running dev server if detected. Degrades gracefully if no server is running.
- **Fix mode:** Ask-before-fix — audit first, present grouped mechanical fixes, ask once "Apply N fixes?", then apply. Never auto-applies without confirmation.
- **Findings output:** `tasks/seo-findings.md` — consistent with sk:perf, sk:accessibility. Never overwrite; append with date header.
- **Content strategy:** Included as a clearly labeled "Content Strategy — Manual Action" section at the bottom of the same `tasks/seo-findings.md` file. These are advisory notes, not code fixes.

## Chosen Approach: Approach B — Dual-Mode (Source + Dev Server)

### What it does

**Phase 1 — Source Audit**
- Detect template files: `.blade.php`, `.jsx`, `.tsx`, `.vue`, `.html`, `.ejs`, `.njk`, `.twig`
- Audit Technical SEO: robots.txt (exists, not blocking all), sitemap.xml (exists, referenced in robots.txt), HTTPS signals (mixed content in templates), canonical tags
- Audit On-Page SEO: title tags (present, unique, 50-60 chars), meta descriptions (present, unique, 150-160 chars), H1 structure (exactly one per page), alt text on images, internal link anchors
- Audit Content Signals: schema/structured data presence (JSON-LD), Open Graph tags, Twitter Card tags

**Phase 2 — Server Audit (optional, degrades gracefully)**
- Detect running dev server on common ports: 3000, 5173, 8000, 8080, 4321
- Fetch key pages (/, /about, any pages found in sitemap or nav) via curl/fetch
- Cross-reference: do rendered pages match what source templates declare?
- Flag mismatches (e.g., framework overriding meta tags at runtime)
- Note what can't be checked without external tools (Google Rich Results Test for structured data validation)

**Phase 3 — Ask Before Fix**
- Group all mechanical fixes with descriptions
- Show list: "Found N auto-fixable issues. Apply mechanical fixes? [y/N]"
- On yes: apply fixes to source files, log each fix
- On no: include fixes in findings as manual action items

**Phase 4 — Report**
- Write to `tasks/seo-findings.md` — append with date header, never overwrite
- Every finding is a **checkbox** (`- [ ]` or `- [x]`)
- Items auto-fixed this run → pre-checked `- [x]` with *(auto-fixed)* label
- Items still failing → unchecked `- [ ]` (user checks off as they manually fix)
- Items from previous run that now pass → moved to "Passed Checks" in new section
- Content strategy items → always `- [ ]` (user decides when done)
- Sections:
  - Critical / High / Medium / Low (technical + on-page findings, all as checkboxes)
  - Content Strategy — Manual Action (advisory checkboxes, not code fixes)
  - Passed Checks (resolved since last run)
  - Summary table (counts of checked vs unchecked per severity)

### Mechanical fixes the skill can apply
- Add/fix `<title>` tags in templates
- Add/fix `<meta name="description">` tags
- Add missing `alt` attributes on `<img>` tags (with placeholder text for user to fill)
- Add `<link rel="canonical">` when missing
- Create/scaffold `robots.txt` if missing
- Create/scaffold `sitemap.xml` if missing
- Fix heading hierarchy (multiple H1s → demote extras to H2)
- Add Open Graph basic tags (`og:title`, `og:description`, `og:url`) if missing
- Add `<html lang="">` attribute if missing

### Manual-only items (content strategy section)
- Keyword targeting per page
- Content depth and E-E-A-T signals
- Backlink profile
- Google Search Console submission
- Schema markup validation (requires Google Rich Results Test)
- Competitor gap analysis

### Audit depth
- Technical SEO: crawlability, robots.txt, sitemap, HTTPS signals, canonical, redirects
- On-Page SEO: titles, meta descriptions, headings, alt text, internal links, image filenames
- Content signals: structured data presence (JSON-LD), OG tags, Twitter Cards, page language

## Scope Expansion: Checklist Format for All Audit Skills

The checkbox/actionable checklist pattern (`- [ ]` / `- [x]`) applies to ALL audit skill findings files for consistency:

| Skill | Findings file | Notes |
|-------|--------------|-------|
| sk:seo-audit | `tasks/seo-findings.md` | new skill — built with checkboxes from the start |
| sk:perf | `tasks/perf-findings.md` | update report format section in SKILL.md |
| sk:accessibility | `tasks/accessibility-findings.md` | update report format section in SKILL.md |
| sk:security-check | `tasks/security-findings.md` | append-only rule preserved; checkboxes per dated section; old run checkboxes stay as-is (audit trail) |

**Logic for all audit skills:**
- Items auto-fixed / resolved this run → `- [x]` with *(auto-fixed)* or *(resolved)* label
- Items still failing → `- [ ]`
- Items from previous run that now pass → moved to "Passed Checks" in the new section
- Advisory/manual items → `- [ ]` (user marks done when handled)

## Files to Create/Update

### New file
- `skills/sk:seo-audit/SKILL.md` — full standalone skill

### Files to update (standalone command, no renumbering)
- `CLAUDE.md` — add to commands table
- `README.md` — add to commands section
- `.claude/docs/DOCUMENTATION.md` — add to skills section
- `install.sh` — add `sk:seo-audit` to workflow commands echo block
- `tasks/lessons.md` — append: update the "update ALL files" list to include seo-audit docs

### Files to update (checklist format rollout to existing audit skills)
- `skills/sk:perf/SKILL.md` — update "Generate Report" section to use checkbox format
- `skills/sk:accessibility/SKILL.md` — update "Generate Report" section to use checkbox format
- `skills/sk:security-check/SKILL.md` — update report format to use checkbox format (preserve append-only rule)

## Open Questions
- None — design is locked

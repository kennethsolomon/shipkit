---
name: sk:seo-audit
description: "SEO audit for web projects. Dual-mode: scans source templates + optionally fetches from running dev server. Ask-before-fix for mechanical issues. Outputs checklist findings to tasks/seo-findings.md."
license: Complete terms in LICENSE.txt
model: haiku
context: fork
agent: general-purpose
---

# /sk:seo-audit

## Purpose

Standalone optional command — audits any web project for SEO issues (Laravel, Next.js, Nuxt, plain HTML, etc.). Run independently like `/sk:debug`, not a numbered workflow step.

Two modes:
- **Source mode** (always): scans template files directly
- **Server mode** (optional): fetches from running dev server to validate rendered output

## Hard Rules

- Never auto-apply fixes without explicit user confirmation.
- Every finding must cite a specific `file:line`.
- Every finding is a checkbox: `- [ ]` (open) or `- [x]` (auto-fixed this run).
- Append to `tasks/seo-findings.md` with date header — never overwrite.
- Degrade gracefully if no server running — skip Phase 2, note in report.
- Structured data validation requires external tools (Google Rich Results Test) — flag it, don't skip silently.

## Before You Start

1. Read `tasks/findings.md` if exists — look for site context, target audience, business type.
2. Read `tasks/lessons.md` if exists — apply any SEO-related lessons.
3. Check `tasks/seo-findings.md` if exists — read last dated section to populate "Passed Checks".

## Mode Detection

### Source Mode — Always Active

Scan for template files:

| Extension | Framework |
|-----------|-----------|
| `.blade.php` | Laravel |
| `.jsx`, `.tsx` | React / Next.js |
| `.vue` | Vue / Nuxt |
| `.html` | Plain HTML / static |
| `.ejs` | Express / Node |
| `.njk` | Nunjucks |
| `.twig` | Twig / Symfony |
| `.erb` | Ruby on Rails |
| `.astro` | Astro |

Print: `"Source mode: found N template files ([extensions detected])"`

### Server Mode — Optional

Probe ports in parallel (background curl): `curl -s -I --max-time 2 http://localhost:PORT`

Ports: 3000, 5173, 8000, 8080, 4321, 4000, 8888

Use first port returning HTTP 200 **and** `Content-Type: text/html` header. Skip ports without `text/html` (may be DB, gRPC, etc.).

- Qualifies: `"Server mode: detected running dev server at http://localhost:PORT"`
- None qualify: `"Server mode: no dev server detected — skipping Phase 2. Start your dev server and re-run for full audit."`

Confirm detected URL looks correct before trusting Phase 2 results.

## Phase 1 — Source Audit

### Technical SEO

- `robots.txt` — exists in project root or `public/`; does NOT contain `Disallow: /`
- `sitemap.xml` — exists in project root or `public/`; referenced in `robots.txt` via `Sitemap:` directive
- `<html lang="">` — present and non-empty on all layout/root templates
- Canonical tags — `<link rel="canonical">` present on key page templates
- No accidental `<meta name="robots" content="noindex">` on public-facing pages
- No hardcoded `http://` asset URLs (mixed content risk)

### On-Page SEO

- `<title>` — present in `<head>`, unique across pages, 50–60 chars
- `<meta name="description">` — present in `<head>`, unique across pages, 150–160 chars
- Exactly one `<h1>` per page template
- Heading hierarchy not skipped (no jumping from `<h2>` to `<h4>`)
- All `<img>` tags have `alt` attribute — flag empty alt on non-decorative images
- Internal `<a>` link text is descriptive — flag: "click here", "here", "read more", "link", "this"
- Image filenames are descriptive — flag: `img001`, `IMG_`, `photo`, `image`, `DSC_`, `screenshot` with no context

### Content Signals

- OG tags: `og:title`, `og:description`, `og:url`, `og:image` all present in layout
- Twitter Card: `twitter:card` present
- JSON-LD: look for `<script type="application/ld+json">` — note presence/absence; do NOT validate schema
- `<html lang="">` matches expected locale

## Phase 2 — Server Audit (Optional)

If server detected:

1. Fetch `/` and discover up to 4 additional pages (from `<a>` hrefs or sitemap.xml).
2. For each page, compare rendered vs source template: `<title>`, `<meta name="description">`, `<h1>`, OG tags.
3. Flag mismatches: `"/about — Source template declares X but rendered output shows Y — framework may be overriding"`
4. Check HTTP status codes — flag any key page returning non-200.
5. Check for redirect chains (e.g., / → /home → /index).

Note in report: "Structured data detected but NOT validated — use Google Rich Results Test (https://search.google.com/test/rich-results) to verify schema markup."

## Phase 3 — Ask Before Fix

After Phase 1 (and Phase 2 if run):

1. Collect all auto-fixable findings.
2. Display numbered list:

```
Found N auto-fixable issues:
1. Missing <title> in resources/views/layouts/app.blade.php
2. Missing alt attribute on <img> in resources/views/home.blade.php:42
3. Missing robots.txt
... (all N items)

Apply mechanical fixes? [y/N]
```

3. Wait for user response.
4. On `y`: apply each fix, log `"Fixed: [description] in [file:line]"`, mark `- [x]`. On failure: log error, mark `- [ ]`, continue.
5. On `n`: mark all `- [ ]` with fix instructions.

## Mechanical Fixes Reference

**Can auto-apply (with confirmation):**

| Issue | Fix Applied |
|-------|------------|
| Missing `<title>` | Add `<title>TODO: Add page title (50-60 chars)</title>` |
| Missing `<meta name="description">` | Add `<meta name="description" content="TODO: Add description (150-160 chars)">` |
| `<img>` missing `alt` | Add `alt="TODO: Describe this image for screen readers"` |
| Missing `<link rel="canonical">` | Add `<link rel="canonical" href="TODO: Add canonical URL">` |
| Missing `robots.txt` | Create `robots.txt`: `User-agent: *\nAllow: /\nSitemap: /sitemap.xml` |
| Missing `sitemap.xml` | Create scaffold with homepage entry |
| Multiple `<h1>` | Demote 2nd, 3rd... `<h1>` to `<h2>` |
| Missing OG tags | Add `og:title`, `og:description`, `og:url` block (TODO placeholders) |
| Missing `<html lang="">` | Add `lang="en"` — note: verify correct language code |

**Cannot auto-apply (report only):**
- Content quality, keyword targeting, title/description content, schema markup content, backlink strategy
- `<meta name="robots" content="noindex">` removal — developer must confirm intentional noindex

## Generate Report

Append to `tasks/seo-findings.md` with date header. Never overwrite.

```markdown
# SEO Audit — YYYY-MM-DD

**Mode:** Source only | Source + Server (`http://localhost:PORT`)
**Templates scanned:** N files ([detected extensions])
**Pages fetched:** N | none — server not detected

---

## Critical

- [x] `resources/views/layouts/app.blade.php` — Missing `<title>` tag *(auto-fixed — add real title)*
- [ ] `resources/views/about.blade.php:1` — Missing `<meta name="description">`
  **Impact:** Google may auto-generate a description from page content, often poorly.
  **Fix:** Add `<meta name="description" content="150-160 char description">` in `<head>`

## High

- [ ] `public/robots.txt` — File missing
  **Impact:** Search engines have no crawl guidance — may index unwanted pages.
  **Fix:** Create `robots.txt` with `User-agent: *`, `Allow: /`, `Sitemap:` directive

## Medium

- [ ] `resources/views/home.blade.php:42` — `<img src="hero.jpg">` missing alt attribute
  **Impact:** Accessibility violation + missed keyword opportunity.
  **Fix:** Add descriptive `alt="..."` text

## Low

- [ ] Image filename `IMG_4521.jpg` — not descriptive
  **Impact:** Minor missed keyword signal.
  **Fix:** Rename to describe the image content

## Content Strategy — Manual Action

- [ ] No JSON-LD structured data detected — consider adding schema markup (Article / Product / LocalBusiness / FAQPage). Validate at: https://search.google.com/test/rich-results
- [ ] `og:image` missing — social shares will have no preview image. Add a default OG image in layout.
- [ ] Submit `sitemap.xml` to Google Search Console for faster indexing
- [ ] Title tags present but content is generic ("TODO") — research target keywords per page

## Passed Checks

- `robots.txt` exists and allows crawling *(was: missing — fixed in 2026-03-10 audit)*
- All `<img>` tags have alt attributes
- Single `<h1>` per page

(or "First run — no prior baseline to compare against")

## Applied Fixes

- Fixed: Added `<title>` placeholder to `resources/views/layouts/app.blade.php`
- Fixed: Created `public/robots.txt`

(or "No fixes applied this run")

---

## Summary

| Severity | Open | Fixed this run |
|----------|------|----------------|
| Critical | 1 | 1 |
| High | 1 | 0 |
| Medium | 3 | 0 |
| Low | 2 | 0 |
| Content Strategy | 4 | — |
| **Total** | **11** | **1** |
```

## When Done

- Critical or High open: `"SEO audit complete. N critical/high issues need attention before this site will rank well. Findings in tasks/seo-findings.md."`
- Only Medium/Low/Content Strategy open: `"Technical SEO is solid. N medium/low polish items and N content strategy items noted in tasks/seo-findings.md."`
- All clean: `"SEO audit passed — no issues found. tasks/seo-findings.md updated with clean baseline."`
- Fixes declined: `"SEO audit complete. N auto-fixable issues left open (fixes declined). Checklist in tasks/seo-findings.md."`

---

## Fix & Retest Protocol

Classify each SEO fix before committing:

**a. Template/config change** (adding meta tag, fixing alt text, scaffolding robots.txt, adding lang, creating sitemap.xml) → commit and re-run `/sk:seo-audit`. No test update needed.

**b. Logic change** (changing how framework generates meta tags, modifying layout data-fetching/rendering, changing routing affecting canonical URLs):
1. Update or add failing unit tests for new behavior
2. Re-run `/sk:test` — must pass at 100% coverage
3. Commit tests + fix together
4. Re-run `/sk:seo-audit` to verify fix resolved the finding

Common logic-change examples:
- Changing a Next.js `generateMetadata()` function → update tests asserting metadata output
- Modifying a Laravel controller setting page title → update feature tests
- Changing a Vue component injecting `<head>` tags → update component tests

---

## Model Routing

Read `.shipkit/config.json` from project root if it exists.

- If `model_overrides["sk:seo-audit"]` is set, use that model — takes precedence.
- Otherwise use `profile` field. Default: `balanced`.

| Profile | Model |
|---------|-------|
| `full-sail` | sonnet |
| `quality` | sonnet |
| `balanced` | sonnet |
| `budget` | haiku |

When spawning sub-agents via the Agent tool, pass `model: "<resolved-model>"`.

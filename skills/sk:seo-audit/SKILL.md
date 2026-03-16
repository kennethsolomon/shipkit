---
name: sk:seo-audit
description: "SEO audit for web projects. Dual-mode: scans source templates + optionally fetches from running dev server. Ask-before-fix for mechanical issues. Outputs checklist findings to tasks/seo-findings.md."
license: Complete terms in LICENSE.txt
---

# /sk:seo-audit

## Purpose

Standalone optional command — audits any web project for SEO issues regardless of framework (Laravel, Next.js, Nuxt, plain HTML, etc.). Run at any point after implementation is complete. NOT a numbered workflow step — invoke it independently like `/sk:debug`.

Two modes:
- **Source mode** (always runs): scans template files directly for SEO signals
- **Server mode** (optional): fetches from a running dev server to validate rendered output

Run when: before shipping a client site, after adding new pages, or any time you want to check SEO health.

## Hard Rules

- **Never auto-apply fixes without explicit user confirmation.**
- **Every finding must cite a specific `file:line`.**
- **Every finding is a checkbox:** `- [ ]` (open) or `- [x]` (auto-fixed this run)
- **Append to `tasks/seo-findings.md`** — never overwrite (use date header per run)
- **Degrade gracefully** if no server is running — skip Phase 2, note it in report
- **Structured data validation requires external tools** (Google Rich Results Test) — flag it, don't skip silently

## Before You Start

1. Read `tasks/findings.md` if it exists — look for site context, target audience, business type (helps tailor content strategy recommendations)
2. Read `tasks/lessons.md` if it exists — apply any SEO-related lessons
3. Check if `tasks/seo-findings.md` exists — if yes, read the last dated section to identify previously flagged items (used to populate "Passed Checks" in the new report)

## Mode Detection

### Source Mode — Always Active

Scan the project for template files:

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

Probe ports in parallel (background curl processes) to avoid 14-second worst-case serial timeout:
- Ports: 3000, 5173, 8000, 8080, 4321, 4000, 8888
- Command: `curl -s -I --max-time 2 http://localhost:PORT` (HEAD request to capture both status code and headers)
- Use the first port that returns HTTP 200 **and** has a `Content-Type: text/html` response header

If a port returns 200 but no `Content-Type: text/html` header, skip it — it is likely a non-HTTP service (e.g., a database, gRPC server) and not a web app. Try the next port.

If any port qualifies: `"Server mode: detected running dev server at http://localhost:PORT"`

If none respond or qualify: `"Server mode: no dev server detected — skipping Phase 2. Start your dev server and re-run for full audit."`

> Note: confirm the detected URL looks correct before trusting Phase 2 results.

## Phase 1 — Source Audit

### Technical SEO

- `robots.txt` — exists in project root or `public/`; does NOT contain `Disallow: /` blocking all crawlers
- `sitemap.xml` — exists in project root or `public/`; referenced in `robots.txt` via `Sitemap:` directive
- `<html lang="">` — present on all layout/root templates (not empty)
- Canonical tags — `<link rel="canonical">` present on key page templates
- No accidental `<meta name="robots" content="noindex">` on public-facing pages
- No hardcoded `http://` asset URLs in templates (mixed content risk)

### On-Page SEO

- `<title>` — present in `<head>`, unique across pages, 50–60 characters
- `<meta name="description">` — present in `<head>`, unique across pages, 150–160 characters
- Exactly one `<h1>` per page template (not zero, not two+)
- Heading hierarchy not skipped (no jumping from `<h2>` to `<h4>`)
- All `<img>` tags have `alt` attribute (even if empty for decorative — but flag empty alt on non-decorative images)
- Internal `<a>` link text is descriptive — flag anchors with text: "click here", "here", "read more", "link", "this"
- Image filenames are descriptive — flag patterns like `img001`, `IMG_`, `photo`, `image`, `DSC_`, `screenshot` with no context

### Content Signals

- Open Graph tags: `og:title`, `og:description`, `og:url`, `og:image` all present in layout
- Twitter Card tags: `twitter:card` present
- JSON-LD structured data block: look for `<script type="application/ld+json">` — note presence/absence; do NOT validate schema (requires external tool)
- Page `<html lang="">` matches expected locale

## Phase 2 — Server Audit (Optional)

If server detected:

1. Fetch `/` and discover up to 4 additional pages (from `<a>` href values in homepage, or from sitemap.xml)
2. For each page fetched, extract and compare:
   - Rendered `<title>` vs source template value
   - Rendered `<meta name="description">` vs source template value
   - Rendered `<h1>` vs source template value
   - Rendered OG tags vs source template
3. Flag mismatches: `"/about — Source template declares <title>About Us</title> but rendered output shows <title>My App</title> — framework may be overriding"`
4. Check HTTP status codes — flag any key page returning non-200
5. Check for redirect chains on common pages (/ → /home → /index is a chain)

> Note in report: "Structured data detected but NOT validated — use Google Rich Results Test (https://search.google.com/test/rich-results) to verify schema markup."

## Phase 3 — Ask Before Fix

After completing Phase 1 (and Phase 2 if run):

1. Collect all auto-fixable findings (see Mechanical Fixes Reference below)
2. Display numbered list:

```
Found N auto-fixable issues:
1. Missing <title> in resources/views/layouts/app.blade.php
2. Missing alt attribute on <img> in resources/views/home.blade.php:42
3. Missing robots.txt
... (all N items)

Apply mechanical fixes? [y/N]
```

3. Wait for user response
4. On `y`: apply each fix in order, log `"Fixed: [description] in [file:line]"`, mark as `- [x]` in report. On individual fix failure: log the error, mark that item `- [ ]`, and continue with remaining fixes.
5. On `n`: mark all as `- [ ]` in report with Fix instructions

## Mechanical Fixes Reference

What this skill CAN auto-apply when user confirms:

| Issue | Fix Applied |
|-------|------------|
| Missing `<title>` in `<head>` | Add `<title>TODO: Add page title (50-60 chars)</title>` |
| Missing `<meta name="description">` | Add `<meta name="description" content="TODO: Add description (150-160 chars)">` |
| `<img>` missing `alt` attribute | Add `alt="TODO: Describe this image for screen readers"` |
| Missing `<link rel="canonical">` | Add `<link rel="canonical" href="TODO: Add canonical URL">` |
| Missing `robots.txt` | Create `robots.txt`: `User-agent: *\nAllow: /\nSitemap: /sitemap.xml` |
| Missing `sitemap.xml` | Create `sitemap.xml` scaffold with homepage entry |
| Multiple `<h1>` on same page | Demote 2nd, 3rd... `<h1>` to `<h2>` |
| Missing OG tags | Add `og:title`, `og:description`, `og:url` block (with TODO placeholders) |
| Missing `<html lang="">` | Add `lang="en"` — **note in output: verify correct language code** |

Things this skill CANNOT auto-apply (report only):
- Content quality improvements
- Keyword targeting
- Title/description CONTENT (only adds TODOs)
- Schema markup content (only flags missing)
- Backlink strategy
- `<meta name="robots" content="noindex">` removal — only the developer can confirm whether a page is intentionally noindexed

## Generate Report

Write to `tasks/seo-findings.md` — append with date header, never overwrite.

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

- [ ] No JSON-LD structured data detected — consider adding schema markup (Article / Product / LocalBusiness / FAQPage) based on your content type. Validate at: https://search.google.com/test/rich-results
- [ ] `og:image` missing — social shares will have no preview image. Add a default OG image in your layout.
- [ ] Submit `sitemap.xml` to Google Search Console for faster indexing
- [ ] Title tags are present but content is generic ("TODO") — research target keywords for each page

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

**Never overwrite** `tasks/seo-findings.md` — append new audits with a date header.

## When Done

If Critical or High items are open:
> "SEO audit complete. **N critical/high issues** need attention before this site will rank well. Findings and checklist in `tasks/seo-findings.md`."

If only Medium/Low/Content Strategy open:
> "Technical SEO is solid. **N medium/low polish items** and **N content strategy items** noted in `tasks/seo-findings.md`. Check off items as you address them."

If all clean:
> "SEO audit passed — no issues found. `tasks/seo-findings.md` updated with clean baseline."

If fixes were declined (`n`):
> "SEO audit complete. **N auto-fixable issues** left open (fixes declined). Checklist in `tasks/seo-findings.md` — check off items as you manually address them."

---

## Fix & Retest Protocol

When applying an SEO fix, classify it before committing:

**a. Template/config change** (adding a meta tag, fixing alt text, scaffolding robots.txt, adding lang attribute, creating sitemap.xml) → commit and re-run `/sk:seo-audit`. No test update needed.

**b. Logic change** (changing how a framework generates meta tags, modifying a layout component's data-fetching or rendering logic, changing routing that affects canonical URLs) → trigger protocol:
1. Update or add failing unit tests for the new behavior
2. Re-run `/sk:test` — must pass at 100% coverage
3. Commit (tests + fix together in one commit)
4. Re-run `/sk:seo-audit` to verify the fix resolved the finding

**Common logic-change SEO fixes:**
- Changing a Next.js `generateMetadata()` function → update tests asserting metadata output
- Modifying a Laravel controller that sets page title → update feature tests
- Changing a Vue component that injects `<head>` tags → update component tests

---

## Model Routing

Read `.shipkit/config.json` from the project root if it exists.

- If `model_overrides["sk:seo-audit"]` is set, use that model — it takes precedence.
- Otherwise use the `profile` field. Default: `balanced`.

| Profile | Model |
|---------|-------|
| `full-sail` | sonnet |
| `quality` | sonnet |
| `balanced` | sonnet |
| `budget` | haiku |

> `opus` = inherit (uses the current session model). When spawning sub-agents via the Agent tool, pass `model: "<resolved-model>"`.

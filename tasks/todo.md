# TODO — 2026-03-16 — New Skill: sk:seo-audit + Checklist Format Rollout

## Goal

Create `sk:seo-audit` as a standalone optional skill: dual-mode SEO audit (source templates + running dev server), ask-before-fix for mechanical issues, checklist output format in `tasks/seo-findings.md`. Also roll out the checkbox findings format to the three existing audit skills (sk:perf, sk:accessibility, sk:security-check) for consistency.

## Constraints (from lessons.md)

- All commands must use `/sk:` prefix
- Never overwrite `tasks/lessons.md` — append only
- Any new skill added to install.sh echo block
- New skill docs must be added to: CLAUDE.md commands table, README.md, DOCUMENTATION.md
- `tasks/lessons.md` must be updated to include seo-audit in the "update ALL files" list

---

## Milestone 1: Tests (write failing tests first — TDD red phase)

#### Wave 1 (first — tests must exist before implementation)

- [x] Update `tests/verify-workflow.sh` — add assertions for sk:seo-audit and checklist format
  - `assert_file_exists` — `skills/sk:seo-audit/SKILL.md` exists
  - `assert_contains` — SKILL.md contains `"running dev server"` (dual-mode)
  - `assert_contains` — SKILL.md contains `"Apply"` and `"fixes"` (ask-before-fix prompt)
  - `assert_contains` — SKILL.md contains `"- [ ]"` (checklist format)
  - `assert_contains` — SKILL.md contains `"seo-findings.md"` (output file)
  - `assert_contains` — SKILL.md contains `"Fix & Retest Protocol"` (gate protocol)
  - `assert_contains` — SKILL.md contains `"sk:seo-audit"` in model routing section
  - `assert_contains` — `CLAUDE.md` contains `"sk:seo-audit"` (in commands table)
  - `assert_contains` — `README.md` contains `"sk:seo-audit"`
  - `assert_contains` — `.claude/docs/DOCUMENTATION.md` contains `"sk:seo-audit"`
  - `assert_contains` — `install.sh` contains `"sk:seo-audit"`
  - `assert_contains` — `skills/sk:perf/SKILL.md` contains `"- [ ]"` (checklist rollout)
  - `assert_contains` — `skills/sk:accessibility/SKILL.md` contains `"- [ ]"`
  - `assert_contains` — `skills/sk:security-check/SKILL.md` contains `"- [ ]"`

---

## Milestone 2: New Skill + Checklist Rollout (all independent — run in parallel)

#### Wave 2 (parallel — all skill SKILL.md files, independent of each other)

- [x] Create `skills/sk:seo-audit/SKILL.md` — full standalone skill
  - **Frontmatter:** `name: sk:seo-audit`, description: SEO audit for web projects — dual-mode (source + dev server), ask-before-fix, checklist output
  - **Purpose:** Standalone optional command — audits any web project for SEO issues regardless of framework. Run at any point after implementation. Not a numbered workflow step.
  - **Hard Rules:**
    - Never auto-apply fixes without asking
    - Every finding must cite file:line
    - Every finding is a checkbox `- [ ]` or `- [x]`
    - Append to `tasks/seo-findings.md`, never overwrite
    - Degrade gracefully if no server is running (skip Phase 2, note it)
  - **Before You Start:** read `tasks/findings.md` (site context), read `tasks/lessons.md`, check if prior `tasks/seo-findings.md` exists (read last section for resolved items)
  - **Mode Detection:**
    - Source mode (always): scan for template files — `.blade.php`, `.jsx`, `.tsx`, `.vue`, `.html`, `.ejs`, `.njk`, `.twig`
    - Server mode (optional): probe ports 3000, 5173, 8000, 8080, 4321 with a HEAD request; if any responds, run Phase 2
  - **Phase 1 — Source Audit:**
    - *Technical SEO:* robots.txt exists + not blocking all crawlers; sitemap.xml exists + referenced in robots.txt; `<html lang="">` present; canonical tags present on key pages; no `<meta name="robots" content="noindex">` on public pages; HTTPS — no `http://` hardcoded asset URLs in templates
    - *On-Page SEO:* `<title>` present, unique across pages, 50–60 chars; `<meta name="description">` present, unique, 150–160 chars; exactly one `<h1>` per page; `<h2>`–`<h6>` hierarchy not skipped; all `<img>` have `alt` attribute; internal `<a>` anchors are descriptive (not "click here"); image filenames are descriptive (not `img001.jpg`)
    - *Content Signals:* Open Graph tags (`og:title`, `og:description`, `og:url`, `og:image`); Twitter Card tags; JSON-LD structured data block present (type not validated — note external tool needed)
  - **Phase 2 — Server Audit (optional):**
    - Fetch `/` and up to 4 other key pages (from sitemap or nav links)
    - Cross-reference rendered `<title>`, `<meta description>`, `<h1>` vs source templates
    - Flag mismatches: "Source says X but rendered output shows Y"
    - Note: structured data validation requires Google Rich Results Test (external)
    - If no server detected: note "Server audit skipped — no dev server found on ports 3000/5173/8000/8080/4321. Start your dev server and re-run for full audit."
  - **Phase 3 — Ask Before Fix:**
    - Group all auto-fixable findings into a numbered list with descriptions
    - Output: "Found N auto-fixable issues: [list]. Apply mechanical fixes? [y/N]"
    - On `y`: apply each fix, log "Fixed: [description] in [file:line]"
    - On `n`: mark all as `- [ ]` in findings report (user applies manually)
    - On `y` with partial failures: apply what works, log failures, mark remaining as `- [ ]`
  - **Mechanical Fixes Reference** (what the skill CAN auto-apply):
    - Missing `<title>` → add `<title>TODO: page title</title>` in `<head>`
    - Missing `<meta name="description">` → add with placeholder
    - Missing `alt` on `<img>` → add `alt="TODO: describe this image"`
    - Missing `<link rel="canonical">` → add with current page URL pattern
    - Missing `robots.txt` → scaffold with `User-agent: *\nAllow: /\nSitemap: /sitemap.xml`
    - Missing `sitemap.xml` → scaffold with XML structure and homepage entry
    - Multiple `<h1>` tags → demote 2nd+ to `<h2>`
    - Missing OG tags → add `og:title`, `og:description`, `og:url` block in `<head>`
    - Missing `<html lang="">` → add `lang="en"` (note: user should verify correct language)
  - **Generate Report** — write to `tasks/seo-findings.md` (append, date header):
    ```
    # SEO Audit — YYYY-MM-DD
    **Mode:** Source only | Source + Server (http://localhost:PORT)
    **Templates scanned:** N files
    **Pages fetched:** N (or "none — server not detected")

    ## Critical
    - [x] `file:line` — description *(auto-fixed)*
    - [ ] `file:line` — description
      **Impact:** ...
      **Fix:** ...

    ## High / Medium / Low  (same format)

    ## Content Strategy — Manual Action
    - [ ] No structured data detected — consider adding JSON-LD (Article / Product / LocalBusiness)
    - [ ] Submit sitemap to Google Search Console
    - [ ] [other advisory items]

    ## Passed Checks
    - Items from previous run that now pass (or "First run — no prior baseline")

    ## Applied Fixes
    - Fixed: [description] in `file:line`
    (or "No fixes applied this run")

    ## Summary
    | Severity | Open | Fixed this run |
    |----------|------|----------------|
    | Critical | N    | N              |
    | High     | N    | N              |
    | Medium   | N    | N              |
    | Low      | N    | N              |
    | Content Strategy | N | — |
    ```
  - **When Done:** conditional message:
    - If Critical/High open: "SEO audit complete. N critical/high issues need attention before this site will rank well. Findings in `tasks/seo-findings.md`."
    - If only Medium/Low/Content: "Technical SEO is solid. N medium/low polish items and N content strategy items noted in `tasks/seo-findings.md`."
    - If all clean: "SEO audit passed — no issues found. `tasks/seo-findings.md` updated."
  - **Fix & Retest Protocol** (same pattern as all gate skills):
    - Template/config change (adding a meta tag, fixing alt text, scaffolding robots.txt) → commit and re-run `/sk:seo-audit`. No test update needed.
    - Logic change (changing how a framework generates meta tags, modifying a layout component's data flow) → trigger protocol: update/add tests → `/sk:test` clean → commit → re-run `/sk:seo-audit`
  - **Model Routing:** `.shipkit/config.json` → `model_overrides["sk:seo-audit"]` takes precedence; otherwise profile table: `full-sail` → sonnet, `quality` → sonnet, `balanced` → sonnet, `budget` → haiku

- [x] Update `skills/sk:perf/SKILL.md` — rollout checklist format to "Generate Report" section
  - Change all `- **[FILE:LINE]**` finding lines to `- [ ] **[FILE:LINE]**`
  - Add `- [x] **[FILE:LINE]** ... *(resolved)*` pattern description for re-runs
  - Add "Passed Checks" section to report template (items from previous run now passing)
  - Update Summary table to include "Open" and "Fixed/Resolved this run" columns
  - Note: "Never overwrite `tasks/perf-findings.md` — append with date header" (already present, keep it)

- [x] Update `skills/sk:accessibility/SKILL.md` — rollout checklist format to "Generate Report" section
  - Change Failures/Warnings lines to `- [ ]` format
  - Add `- [x]` pattern for auto-resolved items
  - Add "Passed Checks" section to report template
  - Update Summary table to include "Open" and "Resolved this run" columns

- [x] Update `commands/sk/security-check.md` — rollout checklist format (read file first to understand current format)
  - Change finding lines to `- [ ]` format
  - Add `- [x]` pattern for resolved items
  - Preserve append-only rule — old run checkboxes stay as-is (audit trail)
  - Add "Passed Checks" section to report template
  - Update Summary table

---

## Milestone 3: Documentation Updates (parallel — depends on Milestone 2 being clear on what sk:seo-audit does)

#### Wave 3 (parallel — all documentation files)

- [x] Update `CLAUDE.md` — add `sk:seo-audit` to commands table
  - Add row in Commands table: `| \`/sk:seo-audit\` | SEO audit — dual-mode (source + dev server), ask-before-fix, checklist output |`
  - Place under the quality/audit group (near sk:perf, sk:accessibility)

- [x] Update `README.md` — add `sk:seo-audit` to commands section
  - Same row as CLAUDE.md in the equivalent commands/skills table
  - Place near sk:perf and sk:accessibility

- [x] Update `.claude/docs/DOCUMENTATION.md` — add `sk:seo-audit` to skills section
  - Add subsection entry describing the skill: purpose, when to run, output file, modes
  - Place in the audit/quality group with sk:perf, sk:accessibility, sk:security-check

- [x] Update `install.sh` — add `sk:seo-audit` to workflow commands echo block
  - Add `echo "  /sk:seo-audit    — SEO audit (standalone, any time after implementation)"` in the commands listing section

- [x] Append `tasks/lessons.md` — update "Update ALL files" list
  - Append new entry: "[2026-03-16] sk:seo-audit added — update its docs when skill changes"
  - Note the 5 files that reference sk:seo-audit: CLAUDE.md, README.md, DOCUMENTATION.md, install.sh, and its own SKILL.md

---

## Verification

```bash
# Confirm new skill file exists
ls skills/sk:seo-audit/SKILL.md

# Confirm dual-mode and ask-before-fix documented
grep -i "running dev server" skills/sk:seo-audit/SKILL.md
grep -i "Apply.*fixes" skills/sk:seo-audit/SKILL.md

# Confirm checklist format in new skill
grep "\- \[ \]" skills/sk:seo-audit/SKILL.md

# Confirm checklist format rolled out to existing audit skills
grep "\- \[ \]" skills/sk:perf/SKILL.md
grep "\- \[ \]" skills/sk:accessibility/SKILL.md
grep "\- \[ \]" skills/sk:security-check/SKILL.md

# Confirm sk:seo-audit in all documentation files
grep "sk:seo-audit" CLAUDE.md
grep "sk:seo-audit" README.md
grep "sk:seo-audit" .claude/docs/DOCUMENTATION.md
grep "sk:seo-audit" install.sh

# Confirm /sk: prefix used (no bare /seo-audit reference)
grep -r '`/seo-audit`' CLAUDE.md README.md .claude/docs/DOCUMENTATION.md

# Run full test suite
bash tests/verify-workflow.sh
```

## Acceptance Criteria

- [ ] `skills/sk:seo-audit/SKILL.md` exists with all required sections: Purpose, Hard Rules, Mode Detection, Phase 1–3, Mechanical Fixes Reference, Generate Report (checkbox format), When Done, Fix & Retest Protocol, Model Routing
- [ ] Dual-mode documented: source template scan + optional dev server probe (ports 3000/5173/8000/8080/4321)
- [ ] Ask-before-fix: prompt shows grouped list, applies only on `y`
- [ ] Output uses `- [ ]` / `- [x]` checkboxes, appends to `tasks/seo-findings.md`
- [ ] Content Strategy section in report (advisory, `- [ ]` only)
- [ ] Checklist format rolled out to sk:perf, sk:accessibility, sk:security-check SKILL.md files
- [ ] `sk:seo-audit` present in CLAUDE.md commands table, README.md, DOCUMENTATION.md, install.sh
- [ ] Fix & Retest Protocol present in sk:seo-audit SKILL.md
- [ ] Model routing section present in sk:seo-audit SKILL.md
- [ ] `tasks/lessons.md` updated (appended, not overwritten)
- [ ] All tests in `tests/verify-workflow.sh` pass

## Risks/Unknowns

- `skills/sk:security-check/SKILL.md` current report format unknown — read before editing to avoid breaking its structure
- Checklist format on security findings has an edge case: security is a hard gate (must fix all), so `- [ ]` items block progress. Make sure the report wording still conveys urgency.
- Server port detection via HEAD request may produce false positives on some machines — note in SKILL.md that user should confirm the detected URL is correct before trusting Phase 2 results

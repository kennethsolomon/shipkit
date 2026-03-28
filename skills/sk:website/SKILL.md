---
name: sk:website
description: Build a complete, client-deliverable multi-page marketing website from a brief, URL, or one sentence. NOT a prototype — a real site you hand to a client. Auto-builds from intake to handoff package. Use --revise for change iterations after initial build.
---

# /sk:website — Client Website Builder

Turn a brief, URL, or one sentence into a production-ready multi-page marketing website with real copy, real SEO, and a full client handoff package. Runs autonomously from intake to delivery.

## This is NOT sk:mvp

| | sk:website | sk:mvp |
|---|---|---|
| **Purpose** | Client deliverable | Market validation |
| **Copy** | Real, business-specific | Placeholder/generic |
| **Data** | Real structure | Fake data |
| **Deploy** | Production-ready | Local prototype |
| **Handoff** | Full client package | Docs only |

## Hard Rules

- **Real copy always** — never Lorem ipsum, never `[Your Headline Here]`. Extract real facts and write specific copy.
- **Multi-page by default** — Home, About, Services/Menu, Contact + niche-specific extras.
- **Default stack: Next.js + Tailwind** — always respect existing project stack.
- **WhatsApp is default contact for local businesses in PH/SEA** — auto-detect and inject.
- **Lighthouse 90+ required before handoff** — loop and fix until passing.
- **Never invent business facts** — no fake testimonials, invented certifications, or made-up outcomes.
- **Parallel agents for speed** — strategy + copy + art direction run simultaneously.
- **Revision mode is targeted** — never rebuild the whole site for small changes.

---

## Mode Detection

| Invocation | Mode |
|---|---|
| `/sk:website` | Full build mode (Steps 1–7) |
| `/sk:website --revise` | Revision mode (Steps R1–R6) |

---

## Full Build Mode

### Step 1 — Brief Extraction

Accept any input. Never block on a missing detail — infer and proceed.

**Option A: URL input**

Use WebFetch to extract facts from any URL the user provides:
- **Google Maps URL** → business name, category, address, phone, hours, rating count, description
- **Existing website URL** → name, tagline, services list, contact details, current copy, page structure
- **Facebook/Instagram business page** → name, description, contact, category

**Option B: Plain text / one sentence**

Extract: business name, type, location, services, CTA intent. Infer reasonable defaults for anything missing.

**After extraction**, display a compact confirmation and auto-proceed:

```
[Business Name] — [Type], [Location]
Services: [list]
CTA: [primary action]
Pages: [inferred page set]
Style: [inferred from type + location]

Building...
```

Do NOT wait for approval — auto-advance unless extracted facts are clearly ambiguous or contradictory.

---

### Step 2 — Parallel Research

Launch 3 agents simultaneously using the Agent tool (all in a single message, `subagent_type="general-purpose"`):

**Agent 1 — Strategy Agent**
- Detect niche from business type using the niche detection table at the bottom of this file.
- Read `references/niche/[detected-niche].md`.
- Plan: final page set, sitemap, per-page section structure, CTA flow across all pages, shared nav/footer structure.
- Output a structured plan with all pages + section outlines.

**Agent 2 — Copy Agent**
- Read `references/content-seo.md`.
- Read `references/niche/[detected-niche].md` for industry-specific messaging rules.
- Write real copy using ONLY facts from Step 1. Never invent:
  - Hero headline + subheadline (specific to this business)
  - About section copy
  - Services/offerings copy (use real service names from the brief)
  - CTA copy aligned with the primary action
  - Footer tagline
  - Page title tag + meta description for every page
  - H1 for every page
- Output all copy ready to inject directly into the build.

**Agent 3 — Art Direction Agent**
- Read `references/art-direction.md`.
- Based on business type + location + tone keywords in the brief, determine:
  - Dominant aesthetic direction (one of 7 — see reference)
  - 2–4 signature design moves
  - Typography pairing (display + body, not system fonts)
  - Custom color palette (NOT default Tailwind palette colors)
  - Motion stance
- Output a complete design spec for the build step.

Collect all 3 agent outputs before proceeding to Step 3.

---

### Step 3 — Build

Implement the full site using all 3 agent outputs as inputs.

**3a. Project setup**
- Detect existing framework. If present, work within it and preserve conventions.
- If no framework: scaffold Next.js App Router + Tailwind CSS (TypeScript).
- Apply the custom color palette from the art direction spec to `tailwind.config.js`.
- Configure typography (Google Fonts via `next/font`, or direct import).

**3b. Site configuration**
- Create a typed site config file (`content/site.ts` or equivalent) with all pages, copy, and metadata from the research agents.
- Organize for easy future editing — named fields, not magic strings.

**3c. Page generation**
For each page in the sitemap:
1. Implement with semantic HTML (landmarks, heading hierarchy, descriptive links).
2. Inject real copy from the Copy Agent — no placeholders anywhere.
3. Apply visual system from Art Direction Agent (typography, palette, design moves).
4. Add per-page SEO: unique title tag, meta description, canonical, OG/Twitter tags.
5. Add structured data where appropriate (LocalBusiness, Organization, BreadcrumbList).
6. Ensure responsiveness: mobile, tablet, desktop.

**3d. WhatsApp CTA injection**
Read `references/whatsapp-cta.md`.

Auto-detect SEA local business using the detection table at the bottom of this file.

Conditions for injection (ANY of these):
- Location explicitly in PH/SEA signals table AND business is local type
- Business is local type AND location is unknown (default to inject with placeholder)
- User explicitly mentioned WhatsApp in the brief

Implementation:
- Use the component pattern from `references/whatsapp-cta.md`
- Wire to extracted phone number, or use `+[PHONE]` placeholder with a clear note for the client
- Position: fixed bottom-right floating button

If Messenger is preferred (user mentioned it, or location is Philippines): implement Messenger alternative from reference.

**3e. Contact handling**

Choose based on business type:
- **Local hospitality** (cafe, restaurant): WhatsApp button + simple reservation/inquiry form
- **Service business**: inquiry form with honeypot protection + WhatsApp fallback
- **Professional services**: consultation booking form
- **SaaS/product**: contact form + optional demo CTA
- **Portfolio**: minimal contact form or email link

**3f. Sitemap + robots**
Generate `sitemap.xml` and `robots.txt` where the framework supports it (Next.js: `app/sitemap.ts`, `app/robots.ts`).

---

### Step 4 — Lighthouse Enforcement Loop

**If Playwright MCP is available:**
1. Start the dev server.
2. Run Lighthouse on each page.
3. Target: Performance ≥ 90, Accessibility ≥ 90, SEO ≥ 90, Best Practices ≥ 90.
4. For any page failing:
   - Read the specific failing audit items.
   - Fix: image sizing, missing meta tags, contrast, heading order, font loading, etc.
   - Re-run Lighthouse on that page only.
5. Repeat until all pages pass all 4 categories.
6. Maximum 3 fix iterations per page. If still failing after 3: flag specific issues to the user and proceed.

**If Playwright MCP is NOT available:**
Run a static quality pass instead:
- Every page has a unique title and meta description ✓
- No duplicate H1s, no skipped heading levels ✓
- All images have descriptive alt text ✓
- Color contrast is not obviously broken (verify palette choices) ✓
- Sitemap + robots.txt are generated ✓
- `next build` (or equivalent) passes without errors ✓

Report: `Quality: [N] issues fixed. Build passing.`

---

### Step 5 — Launch Audit

Read `references/launch-checklist.md`.

Run through all 5 audit categories:
1. Search and metadata
2. Conversion and content
3. Accessibility and UX
4. Performance and implementation
5. Launch operations

Fix all blockers immediately. Log medium-priority and optional polish items for the handoff document.

---

### Step 6 — Handoff Package

Read `references/handoff-template.md`.

Generate 3 files at the project root using the templates:

**`HANDOFF.md`** — Client-facing project summary:
- What was built (pages, features, integrations)
- What needs replacing (image placeholders, phone numbers, API keys)
- How to make simple content edits with specific file paths
- Contact for technical help

**`DEPLOY.md`** — Deployment guide:
- Vercel one-click deploy + CLI steps
- Netlify as alternative
- Required environment variables with descriptions
- Domain configuration steps
- Estimated monthly cost (Vercel free tier, domain ~$12/yr)

**`CONTENT-GUIDE.md`** — Non-technical editing guide (written FOR the client):
- Plain language: "To change your opening hours, open `content/site.ts` and find `hours:`"
- Covers: business name, tagline, contact details, services list, hours, social links
- No developer jargon

---

### Step 7 — Final Output

```
## [Business Name] — Website Complete

**Stack:** [framework] + Tailwind CSS
**Pages:** [list all pages]
**Style:** [aesthetic direction] — [2-4 signature moves]
**WhatsApp CTA:** [included at wa.me/[PHONE] / not applicable]
**Quality:** [Lighthouse 90+ on all pages / static checks passed]

### Run locally
[exact command]

### Client deliverables
- `HANDOFF.md` — what was built + what to replace
- `DEPLOY.md` — how to go live on Vercel (free tier)
- `CONTENT-GUIDE.md` — how to update content without a developer

### Still needs
- [ ] [specific placeholders — e.g., hero photo, WhatsApp number, GA4 ID]
```

---

## Revision Mode (`--revise`)

Use after the initial build when the client has feedback.

### Step R1 — Read current state
- Read existing site files.
- Read `HANDOFF.md` if it exists for context on what was built.

### Step R2 — Collect changes

If not already provided in the invocation, ask:
> **What changes does the client want?**
> Plain language — e.g., "make the hero warmer", "add a gallery section", "update the CTA to Book a Table", "the mobile nav is broken"

### Step R3 — Classify and apply

For each change, identify type and act:

| Type | Examples | Action |
|---|---|---|
| Copy change | Updated headline, new CTA text, service names | Direct edit to config/content file |
| Style change | Warmer colors, bigger fonts, more spacing | Targeted Tailwind/CSS edit only |
| Structure change | New section, new page, reordering sections | Implement using existing component patterns |
| Feature change | Gallery, new contact form, WhatsApp, map | Implement + update handoff docs |

**Rule: never rebuild the whole site for targeted feedback.** Edit only what changed.

### Step R4 — Quality re-check
Run the same Lighthouse/quality checks from Step 4. Fix any regressions introduced by the changes.

### Step R5 — Update handoff docs
If the structure changed (new page, new section), update `HANDOFF.md` and `CONTENT-GUIDE.md` with new file references and editing instructions.

### Step R6 — Summarize
```
## Revision Applied

**Changes made:**
- [each change with file:line reference]

**Quality:** [passed / N issues fixed]
**Handoff docs:** [updated / unchanged]
```

---

## Niche Detection

Auto-detect from brief text. Read the matched reference file in Step 2.

| Business type signals | Reference file |
|---|---|
| cafe, coffee, espresso, bakery, brunch, brew, roaster, barista | `references/niche/cafe.md` |
| restaurant, dining, bistro, brasserie, eatery, food, cuisine | `references/niche/restaurant.md` |
| law, attorney, legal, litigation, counsel, solicitor | `references/niche/law-firm.md` |
| plumber, HVAC, roofing, cleaning, landscaping, handyman, pest control | `references/niche/home-services.md` |
| dentist, dental, orthodont, oral, clinic (dental context) | `references/niche/dentist.md` |
| gym, fitness, yoga, pilates, trainer, crossfit, workout | `references/niche/gym.md` |
| real estate, property, agent, broker, realty, realtor | `references/niche/real-estate.md` |
| accountant, bookkeeper, tax, CPA, CFO, advisory, audit | `references/niche/accountant.md` |
| med spa, aesthetics, injectables, botox, filler, skin clinic | `references/niche/med-spa.md` |
| wedding, bridal, venue, florist, event planner | `references/niche/wedding.md` |
| agency, studio, creative, consultancy, design firm | `references/niche/agency.md` |
| portfolio, freelance, designer, developer, photographer, illustrator | `references/niche/portfolio.md` |
| shop, store, ecommerce, products, catalog, DTC | `references/niche/ecommerce.md` |
| SaaS, software, app, platform, tool, B2B | `references/niche/saas.md` |
| (default — any local service business) | `references/niche/local-business.md` |

---

## SEA Location Detection

Used in Step 3d to determine WhatsApp CTA injection.

Inject when ALL of:
1. Business is a local business (not SaaS, not portfolio, not ecommerce-only)
2. Location matches any signal below OR location is unknown

| Location signals | Region |
|---|---|
| Philippines, PH, Manila, QC, Quezon City, Cebu, Davao, BGC, Makati, Taguig, Pasig, Parañaque, Mandaluyong, Alabang | Philippines |
| Singapore, SG | Singapore |
| Malaysia, MY, KL, Kuala Lumpur, Penang, Johor, Petaling Jaya | Malaysia |
| Indonesia, ID, Jakarta, Bali, Surabaya, Bandung, Medan | Indonesia |
| Thailand, TH, Bangkok, Phuket, Chiang Mai | Thailand |
| Vietnam, VN, Ho Chi Minh, HCMC, Hanoi, Da Nang | Vietnam |
| Hong Kong, HK | Hong Kong |

When location is unknown and business is local: inject with `+[PHONE]` placeholder and note.

---

## Model Routing

Read `.shipkit/config.json` from the project root if it exists.

- If `model_overrides["sk:website"]` is set, use that model — it takes precedence.
- Otherwise use the `profile` field. Default: `balanced`.

| Profile | Orchestrator | Research agents (Step 2) | Build agent (Step 3) |
|---|---|---|---|
| `full-sail` | opus (inherit) | sonnet | opus (inherit) |
| `quality` | opus (inherit) | sonnet | opus (inherit) |
| `balanced` | sonnet | haiku | sonnet |
| `budget` | sonnet | haiku | sonnet |

> `opus` = inherit (uses current session model). When spawning sub-agents via the Agent tool, pass `model: "<resolved-model>"`.

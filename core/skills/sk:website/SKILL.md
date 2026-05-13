---
name: sk:website
description: Build a complete, client-deliverable multi-page marketing website from a brief, URL, or one sentence. NOT a prototype — a real site you hand to a client. Auto-builds from intake to handoff package. Use --revise for change iterations after initial build.
argument-hint: "[--revise] [URL or brief]"
---

# /sk:website — Client Website Builder

Turn a brief, URL, or one sentence into a production-ready multi-page marketing website with real copy, real SEO, and a full client handoff package.

## This is NOT sk:mvp

| | sk:website | sk:mvp |
|---|---|---|
| **Purpose** | Client deliverable | Market validation |
| **Copy** | Real, business-specific | Placeholder/generic |
| **Data** | Real structure | Fake data |
| **Deploy** | Production-ready | Local prototype |
| **Handoff** | Full client package | Docs only |

## Hard Rules

- **Real copy always** — never Lorem ipsum, never `[Your Headline Here]`. Extract real facts, write specific copy.
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
| `/sk:website --stack nuxt` | Full build mode using Nuxt 3 + Vue 3 |
| `/sk:website --stack laravel` | Full build mode using Laravel 11 + Blade |
| `/sk:website --deploy` | Full build mode + Step 8 (deploy after build) |
| Flags combine freely | e.g., `--stack nuxt --deploy`, `--stack laravel --revise` |

---

## Stack Detection

| Priority | Signal | Stack |
|---|---|---|
| 1 | `--stack nuxt` flag | Nuxt 3 + Vue 3 + Tailwind → `references/stacks/nuxt.md` |
| 2 | `--stack laravel` flag | Laravel 11 + Blade + Tailwind → `references/stacks/laravel.md` |
| 3 | `package.json` contains `"nuxt"` | Nuxt 3 (existing project) |
| 4 | `composer.json` exists | Laravel (existing project) |
| 5 | `package.json` contains `"next"` | Next.js (existing project) |
| 6 | No signals | Default: Next.js App Router → `references/stacks/nextjs.md` |

Read the matched stack reference at the start of Step 3 before writing any code.

---

## Full Build Mode

### Step 1 — Brief Extraction

Accept any input. Never block on a missing detail — infer and proceed.

**Option A: URL input** — Use WebFetch to extract:
- Google Maps URL → business name, category, address, phone, hours, rating count, description
- Existing website URL → name, tagline, services, contact details, copy, page structure
- Facebook/Instagram business page → name, description, contact, category

If WebFetch fails (JS-only page, redirect, paywall): fall back to Option B immediately. Don't retry.

**Option B: Plain text / one sentence** — Extract: business name, type, location, services, CTA intent. Infer reasonable defaults for anything missing.

**After extraction**, display and auto-proceed:

```
[Business Name] — [Type], [Location]
Services: [list]
CTA: [primary action]
Pages: [inferred page set]
Style: [inferred from type + location]
Stack: [detected stack — Next.js / Nuxt 3 / Laravel]

Building...
```

Auto-advance unless extracted facts are clearly ambiguous or contradictory.

---

### Step 2 — Parallel Research

Launch 3 agents simultaneously via Agent tool (all in one message, `subagent_type="general-purpose"`):

**Agent 1 — Strategy Agent**
- Detect niche using the niche detection table below. Read `references/niche/[detected-niche].md`.
- Output: final page set, sitemap, per-page section structure, CTA flow, shared nav/footer structure.

**Agent 2 — Copy Agent**
- Read `references/content-seo.md` and `references/niche/[detected-niche].md`.
- Write real copy using ONLY facts from Step 1. Never invent.
- Output (ready to inject): hero headline + subheadline, about section, services copy, CTA copy, footer tagline, title tag + meta description + H1 for every page.

**Agent 3 — Art Direction Agent**
- Read `references/art-direction.md`.
- Output: dominant aesthetic direction (one of 7), 2–4 signature design moves, typography pairing (display + body, not system fonts), custom color palette (NOT default Tailwind colors), motion stance.

Each agent writes output to a temp doc. Collect all 3 before proceeding.

---

### Step 3 — Build

Implement the full site using all 3 agent outputs as inputs.

**3a. Project setup**
- Run stack detection (see table above). Read `references/stacks/[stack].md` before writing any code.
- If existing framework: work within it, preserve conventions.
- If no framework: scaffold using detected stack reference.
- Apply custom color palette to `tailwind.config.js` / `tailwind.config.ts`.
- Configure typography (Google Fonts — see stack reference for correct import method).

**3b. Site configuration**
- Create typed site config (`content/site.ts` or equivalent) with all pages, copy, and metadata from research agents. Named fields, not magic strings.

**3c. Page generation** — for each page in the sitemap:
1. Semantic HTML (landmarks, heading hierarchy, descriptive links).
2. Inject real copy from Copy Agent — no placeholders.
3. Apply visual system from Art Direction Agent (typography, palette, design moves).
4. Per-page SEO: unique title tag, meta description, canonical, OG/Twitter tags.
5. Structured data where appropriate (LocalBusiness, Organization, BreadcrumbList).
6. Responsive: mobile, tablet, desktop.

**3d. WhatsApp CTA injection**
Read `references/whatsapp-cta.md`. Auto-detect SEA local business using the detection table below.

Inject when ANY of:
- Location in PH/SEA signals table AND business is local type
- Business is local type AND location is unknown (inject with placeholder)
- User explicitly mentioned WhatsApp in the brief

| Stack | Component pattern |
|---|---|
| Next.js | `components/WhatsAppButton.tsx` (`'use client'`) — see `references/stacks/nextjs.md` |
| Nuxt 3 | `components/WhatsAppButton.vue` (`defineProps`) — see `references/stacks/nuxt.md` |
| Laravel | `resources/views/components/whatsapp-button.blade.php` (`@props`) — see `references/stacks/laravel.md` |

- Wire to extracted phone (E.164 without `+`: e.g., `639171234567`), or use `[PHONE]` placeholder with client note.
- Position: fixed bottom-right floating button.
- If Messenger preferred (user mentioned it, or location is Philippines): implement Messenger alternative from reference.

**3e. Contact handling**

| Business type | Contact implementation |
|---|---|
| Local hospitality (cafe, restaurant) | WhatsApp button + reservation/inquiry form |
| Service business | Inquiry form with honeypot + WhatsApp fallback |
| Professional services | Consultation booking form |
| SaaS/product | Contact form + optional demo CTA |
| Portfolio | Minimal contact form or email link |

**3f. Sitemap + robots**
Generate `sitemap.xml` and `robots.txt` (Next.js: `app/sitemap.ts`, `app/robots.ts`).

---

### Step 4 — Lighthouse Enforcement Loop

**If Playwright MCP is available:**
1. Start dev server.
2. Run Lighthouse on each page. Target: Performance ≥ 90, Accessibility ≥ 90, SEO ≥ 90, Best Practices ≥ 90.
3. For any failing page: read failing audit items, fix (image sizing, missing meta, contrast, heading order, font loading), re-run that page only.
4. Repeat until all pages pass all 4 categories. Max 3 fix iterations per page — if still failing, flag to user and proceed.

**If Playwright MCP is NOT available** — static quality pass:
- Every page has unique title and meta description ✓
- No duplicate H1s, no skipped heading levels ✓
- All images have descriptive alt text ✓
- Color contrast not obviously broken ✓
- Sitemap + robots.txt generated ✓
- `next build` (or equivalent) passes without errors ✓

Report: `Quality: [N] issues fixed. Build passing.`

---

### Step 5 — Launch Audit

Read `references/launch-checklist.md`. Run all 5 audit categories:
1. Search and metadata
2. Conversion and content
3. Accessibility and UX
4. Performance and implementation
5. Launch operations

Fix all blockers immediately. Log medium-priority and optional polish items for the handoff document.

---

### Step 6 — Handoff Package

Read `references/handoff-template.md`. Generate 3 files at project root:

**`HANDOFF.md`** — Client-facing:
- What was built (pages, features, integrations)
- What needs replacing (image placeholders, phone numbers, API keys)
- How to make simple content edits with specific file paths
- Contact for technical help

**`DEPLOY.md`** — Deployment guide:
- Vercel one-click deploy + CLI steps; Netlify as alternative
- Required environment variables with descriptions
- Domain configuration steps
- Estimated monthly cost (Vercel free tier, domain ~$12/yr)

**`CONTENT-GUIDE.md`** — Non-technical editing (written FOR the client):
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
**WhatsApp CTA:** [included — wa.me/[PHONE_NUMBER] / not applicable]
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

### Step 8 — Deploy (only when `--deploy` flag is provided)

Skip entirely if `--deploy` was NOT passed. DEPLOY.md covers manual deploy for all cases.

**8a. Detect deploy tool**
```
vercel --version  → if found: use Vercel
netlify --version → if found: use Netlify
neither found     → skip deploy, instruct user (see 8c)
```

**8b. Confirm before deploying** — ALWAYS ask before running any deploy command:
```
Ready to deploy to [Vercel/Netlify]? (y/n)

This will push the site live. Make sure:
- HANDOFF.md placeholders are replaced (or noted)
- Environment variables are configured
- The client has approved the build
```
Wait for explicit `y`. Never auto-deploy.

**8c. If no CLI found**
```
Vercel CLI not found. To deploy manually:
1. Run: npm install -g vercel
2. Run: vercel --prod
   (or follow DEPLOY.md for Netlify or other hosts)
```

**8d. Deploy**
```bash
vercel --prod        # Vercel
netlify deploy --prod  # Netlify
```
For Laravel (no Vercel/Netlify support): output recommended hosts and point to DEPLOY.md.

**8e. After successful deploy**
1. Display the live URL.
2. Update `HANDOFF.md`: append "Live URL" section with URL and deploy date.
3. Update `DEPLOY.md`: mark as "Deployed" with live URL.

```
## [Business Name] — Deployed

Live URL: https://[project].vercel.app
Deployed: [date]

Update HANDOFF.md with the final custom domain once DNS is configured.
```

---

## Revision Mode (`--revise`)

### Step R1 — Read current state
- Read existing site files and `HANDOFF.md` (if exists) for build context.

### Step R2 — Collect changes
If not provided in the invocation, ask:
> **What changes does the client want?**
> Plain language — e.g., "make the hero warmer", "add a gallery section", "update the CTA to Book a Table", "the mobile nav is broken"

### Step R3 — Classify and apply

| Type | Examples | Action |
|---|---|---|
| Copy change | Updated headline, new CTA text, service names | Direct edit to config/content file |
| Style change | Warmer colors, bigger fonts, more spacing | Targeted Tailwind/CSS edit only |
| Structure change | New section, new page, reordering | Implement using existing component patterns |
| Feature change | Gallery, new contact form, WhatsApp, map | Implement + update handoff docs |

Never rebuild the whole site for targeted feedback. Edit only what changed.

### Step R4 — Quality re-check
Run same Lighthouse/quality checks from Step 4. Fix any regressions.

### Step R5 — Update handoff docs
If structure changed (new page, new section), update `HANDOFF.md` and `CONTENT-GUIDE.md` with new file references and editing instructions.

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

Auto-detect from brief text. Read matched reference file in Step 2.

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

Used in Step 3d for WhatsApp CTA injection.

Inject when ALL of:
1. Business is local (not SaaS, not portfolio, not ecommerce-only)
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

Read `.shipkit/config.json` from project root if it exists.

- If `model_overrides["sk:website"]` is set, use that model — takes precedence.
- Otherwise use the `profile` field. Default: `balanced`.

| Profile | Orchestrator | Research agents (Step 2) | Build agent (Step 3) |
|---|---|---|---|
| `full-sail` | opus (inherit) | sonnet | opus (inherit) |
| `quality` | opus (inherit) | sonnet | opus (inherit) |
| `balanced` | sonnet | haiku | sonnet |
| `budget` | sonnet | haiku | sonnet |

> `opus` = inherit (uses current session model). When spawning sub-agents via the Agent tool, pass `model: "<resolved-model>"`.

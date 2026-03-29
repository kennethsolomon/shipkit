---
name: sk:mvp
description: Generate a complete MVP validation app from a prompt — landing page with waitlist + working app with fake data. Use this skill when the user wants to quickly validate a product idea, build a proof of concept, create a landing page with email collection, scaffold an MVP, build a prototype for market validation, or test if an idea is worth pursuing. Produces a full working codebase locally.
compatibility: Optional — Pencil MCP (for visual mockups), Playwright MCP (for visual validation)
---

# /sk:mvp — MVP Validation App Generator

Generate a complete, aesthetically polished MVP from a single idea prompt. Outputs a landing page with waitlist email collection + a working app with fake data. Purpose: validate market interest before investing in a full build.

## Hard Rules

- Generate ALL code locally — never deploy, push, or publish anything.
- Landing page is MANDATORY for every MVP. Never skip it.
- Use FAKE data only — no real databases, no auth systems, no third-party API integrations.
- Every page must be functional: buttons navigate, forms submit, modals open/close.
- Design must be distinctive and polished — never use default Tailwind colors or generic layouts. Read `references/design-system.md` for aesthetic guidelines.
- Keep the app secure enough (no XSS, no open redirects) but don't over-engineer security for a prototype.

---

## Step 1 — Gather the Idea

Ask: **"What's your product idea? Describe it in 1-3 sentences — what does it do and who is it for?"**

Extract and confirm before proceeding:
- **Product name** (or ask them to pick one)
- **One-line value proposition**
- **Target audience**
- **Key features** (3-5 core features)

---

## Step 2 — Pick a Tech Stack

Present options:

| # | Stack | Notes |
|---|-------|-------|
| 1 | **Next.js + Tailwind** | React, SSR, API routes built-in |
| 2 | **Nuxt + Tailwind** | Vue, SSR, server routes built-in |
| 3 | **Laravel + Blade + Tailwind** | PHP, full backend, Blade templates |
| 4 | **React + Vite + Tailwind** | Lightweight SPA, no backend (waitlist via Formspree) |

Or accept a custom stack. Note the selection for Step 6.

---

## Step 3 — Optional Design Phase (Pencil MCP)

Check for `--pencil` flag or ask: **"Design UI visually in Pencil before coding? (y/n)"**

### If YES — Pencil MCP Design Phase

**3a.** Check `docs/design/` for existing `.pen` file. If found: `open_document(filePath)` → skip to 3c. If not: `open_document('new')` → save to `docs/design/{product-slug}.pen`.

**3b.** Load design context:
1. `get_guidelines(topic='landing-page')`
2. `get_style_guide_tags` → `get_style_guide(tags)` — pick tags matching product tone.

**3c.** Set color palette via `set_variables`:
```json
{
  "color-bg": "#xxxxxx",
  "color-fg": "#xxxxxx",
  "color-accent": "#xxxxxx",
  "color-muted": "#xxxxxx"
}
```

**3d.** Use `batch_design` (one frame per call) to create:
1. Landing page — hero, features, pricing, waitlist section
2. App main screen — dashboard or primary view
3. App secondary screen — detail view or key interaction

**3e.** After each frame: `get_screenshot` → if off, `snapshot_layout` → fix → iterate until correct.

**3f.** Ask: **"Does this design direction look good? Any changes before I start coding?"** Wait for explicit approval before proceeding.

**3g.** Note the `.pen` file path. Design decisions (colors, typography, layout) carry forward into code.

### If NO — Skip to Step 4

Use `references/design-system.md` for design choices. State the chosen direction (color scheme, typography, layout style) briefly.

---

## Step 4 — Scaffold the Project

Read the stack-specific reference file:
- Next.js → `references/stacks/nextjs.md`
- Nuxt → `references/stacks/nuxt.md`
- Laravel → `references/stacks/laravel.md`
- React + Vite → `references/stacks/react-vite.md`

Run the scaffold command from the reference file. Customize Tailwind config with the chosen color palette and typography.

---

## Step 5 — Generate the Landing Page

Read `references/landing-page.md`. Generate all 9 mandatory sections:

1. **Navbar** — logo + nav links (Features, Pricing, Waitlist) + CTA button
2. **Hero** — benefit-driven headline + subheadline + primary CTA + hero visual
3. **Social proof bar** — "Trusted by X+" or logo strip (placeholders)
4. **Features grid** — 3-6 cards with icons, titles, descriptions (from Step 1 features)
5. **How it works** — 3-step numbered process
6. **Pricing** — 2-3 tier cards (Free / Pro / Enterprise) with fake realistic pricing
7. **Testimonials** — 2-3 fake cards with names, roles, placeholder avatars
8. **Waitlist / CTA** — email input + submit + success message + validation
9. **Footer** — product name, links, copyright

### Waitlist Email Collection

**Stacks with backend (Next.js, Nuxt, Laravel):**
- API route: POST `{ email }` → validate server-side → read `waitlist.json` → append `{ email, timestamp }` → write back → return JSON.
- Wire form to POST via fetch. Show success ("You're on the list!") and error states.

**Static stacks (React + Vite):**
- Use Formspree: `action="https://formspree.io/f/{form_id}"`.
- Add comment instructing user to create a free Formspree account and replace `{form_id}`.
- Handle success/error client-side.

---

## Step 6 — Generate the App

Generate a working multi-page app with these 5 pages:

1. **Navigation** — sidebar or top nav, links to all pages, active state highlighting.
2. **Dashboard / Home** — summary cards, simple CSS/SVG charts, recent activity list (fake data).
3. **Primary feature page** — main product function, functional UI, client-side only (buttons, modals, forms work).
4. **Secondary feature page** — supporting feature, table/list with client-side filtering/sorting.
5. **Settings / Profile** — form with fake prefilled data, save button shows toast.

### Design Standards (every page)

Read `references/design-system.md`:
- Custom Tailwind colors — never defaults.
- Google Fonts — pair display + body font.
- Consistent spacing rhythm (e.g., 4/8/12/16/24/32/48).
- Rounded corners, shadows, hover states, transitions.
- Responsive — mobile and desktop.
- Fake data must feel realistic (real-sounding names, numbers, dates).

---

## Step 7 — Visual Validation (Playwright MCP)

**If Playwright MCP available:**
1. Start dev server (stack's dev command from reference file).
2. Navigate to each page: `/`, `/dashboard`, each app page.
3. Screenshot at desktop (1280px) and mobile (375px).
4. Check for: broken layouts, missing content, non-functional interactions, visual inconsistency.
5. Fix issues and re-validate.

**If Playwright MCP NOT available:**
Tell user: `"Playwright MCP not connected — start the dev server with {dev command} and check pages manually."`

---

## Step 8 — Quality Loop

1. Fix issues found in Step 7.
2. Re-run Playwright validation.
3. Repeat until all pages pass. Max 3 iterations — if issues persist, present remaining issues and ask how to proceed.

---

## Step 9 — Generate Project Context Docs

Generate 3 files in `docs/` using information from Steps 1-2. No new questions.

**`docs/vision.md`**
```markdown
# [Product Name]

## Value Proposition
[One-line value prop]

## Target Audience
[Target audience]

## Key Features
[Bullet list of 3-5 features]

## North Star Metric
[One metric measuring core value]
```

**`docs/prd.md`**
```markdown
# PRD — [Product Name]

## Overview
[1-2 sentence description]

## User Stories
[Per key feature: "As a [audience], I want to [feature] so that [benefit]"]

## Feature Acceptance Criteria
[Per feature: 2-3 concrete criteria]

## Out of Scope (MVP)
- Real authentication
- Real database
- Third-party integrations
- Deployment
```

**`docs/tech-design.md`**
```markdown
# Tech Design — [Product Name]

## Stack
- **Framework:** [chosen stack]
- **Styling:** Tailwind CSS
- **Fonts:** [chosen fonts]

## Project Structure
[Key directories and files from scaffolding]

## Component Map
### Landing Page
[All 9 sections and their components]

### App Pages
[Each page and its key components]

## Data Model
### Waitlist
- email: string (validated)
- timestamp: ISO 8601 string

### Fake Data Entities
[Fake data structures used in the app]
```

Output after generating: `"Context docs generated: docs/vision.md, docs/prd.md, docs/tech-design.md — Run /sk:context to load vision.md into the session brief."`

---

## Step 10 — Present the Output

```
## MVP Generated

**Product:** {name}
**Stack:** {stack}
**Files:** {count} files generated

### Landing Page
- URL: http://localhost:{port}/
- Sections: hero, features, pricing, waitlist, testimonials
- Waitlist: {API route path or Formspree}

### App Pages
- Dashboard: http://localhost:{port}/dashboard
- {Feature 1}: http://localhost:{port}/{path}
- {Feature 2}: http://localhost:{port}/{path}
- Settings: http://localhost:{port}/settings

### Start the dev server
{exact command to run}

### What's next
- Review the generated code and tweak the design to your liking
- Replace placeholder content with your real copy
- Replace fake data with real API integrations when ready
- Deploy when you're happy with it
```

---

## Model Routing

Read `.shipkit/config.json` from the project root if it exists.

- If `model_overrides["sk:mvp"]` is set, use that model — it takes precedence.
- Otherwise use the `profile` field. Default: `balanced`.

| Profile | Model |
|---------|-------|
| `full-sail` | opus (inherit) |
| `quality` | opus (inherit) |
| `balanced` | sonnet |
| `budget` | sonnet |

> `opus` = inherit (uses the current session model). When spawning sub-agents via the Agent tool, pass `model: "<resolved-model>"`.

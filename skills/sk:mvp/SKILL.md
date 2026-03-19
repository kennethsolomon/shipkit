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

Ask the user to describe their product idea. If not already provided, ask:

> **What's your product idea? Describe it in 1-3 sentences — what does it do and who is it for?**

Extract from their answer:
- **Product name** (or ask them to pick one)
- **One-line value proposition**
- **Target audience**
- **Key features** (3-5 core features for the app)

Confirm your understanding before proceeding.

---

## Step 2 — Pick a Tech Stack

Present these preset options:

> **Pick a tech stack:**
>
> 1. **Next.js + Tailwind** — React ecosystem, SSR, API routes built-in
> 2. **Nuxt + Tailwind** — Vue ecosystem, SSR, server routes built-in
> 3. **Laravel + Blade + Tailwind** — PHP ecosystem, full backend, Blade templates
> 4. **React + Vite + Tailwind** — Lightweight SPA, no backend (waitlist via Formspree)
>
> Or type your own stack (I'll adapt).

Once the user picks, note the selection and load the corresponding reference file in Step 6.

---

## Step 3 — Optional Design Phase (Pencil MCP)

Check if the user invoked with `--pencil` flag or ask:

> **Would you like to design the UI visually in Pencil before coding? (Requires Pencil app + MCP) (y/n)**
>
> If no, I'll go straight to code generation with a great default design.

### If YES — Pencil MCP Design Phase

Follow this flow (adapted from sk:frontend-design):

**3a. Find or create .pen file**
- Check `docs/design/` for existing `.pen` file matching this MVP.
- Existing: `open_document(filePath)` → skip to 3c.
- None: `open_document('new')` → save to `docs/design/{product-slug}.pen`.

**3b. Load design context**
1. `get_guidelines(topic='landing-page')` — load landing page design rules.
2. `get_style_guide_tags` → `get_style_guide(tags)` — pick tags matching the product's tone (e.g., modern, SaaS, minimal, bold).

**3c. Set color palette as variables**
Decide a distinctive color palette based on the product's tone and audience. Call `set_variables` with the palette:
```json
{
  "color-bg": "#xxxxxx",
  "color-fg": "#xxxxxx",
  "color-accent": "#xxxxxx",
  "color-muted": "#xxxxxx"
}
```

**3d. Build mockup screens**
Use `batch_design` to create:
1. Landing page frame — hero, features, pricing, waitlist section
2. App main screen frame — dashboard or primary view
3. App secondary screen frame — detail view or key interaction

Work one frame per `batch_design` call. Apply the color variables and typography.

**3e. Validate and iterate**
After each frame: `get_screenshot` to inspect. If off: `snapshot_layout` → fix with `batch_design`. Iterate until the design matches the vision.

**3f. Get user approval**
Present screenshots and ask:
> **Does this design direction look good? Any changes before I start coding?**

Wait for approval. Apply feedback if given. Do not proceed to code without explicit approval.

**3g. Record the design**
Note the `.pen` file path. The design decisions (colors, typography, layout) carry forward into code generation.

### If NO — Skip to Step 4

Use the aesthetic guidelines from `references/design-system.md` to make distinctive design choices automatically. Briefly state the design direction chosen (color scheme, typography, layout style) so the user knows what to expect.

---

## Step 4 — Scaffold the Project

Read the stack-specific reference file:
- Next.js → `references/stacks/nextjs.md`
- Nuxt → `references/stacks/nuxt.md`
- Laravel → `references/stacks/laravel.md`
- React + Vite → `references/stacks/react-vite.md`

Run the scaffold command from the reference file. Then customize the Tailwind config with the chosen color palette and typography.

---

## Step 5 — Generate the Landing Page

Read `references/landing-page.md` for section patterns and structure.

Generate a complete landing page with these sections (all mandatory):

1. **Navbar** — logo/product name + nav links (Features, Pricing, Waitlist) + CTA button
2. **Hero** — headline (benefit-driven) + subheadline + primary CTA + hero visual/illustration area
3. **Social proof bar** — "Trusted by X+" or logo strip (use placeholder logos)
4. **Features grid** — 3-6 feature cards with icons, titles, descriptions (based on the key features from Step 1)
5. **How it works** — 3-step process with numbered steps and descriptions
6. **Pricing** — 2-3 tier cards (Free / Pro / Enterprise) with fake but realistic pricing
7. **Testimonials** — 2-3 fake testimonial cards with names, roles, photos (use placeholder avatars)
8. **Waitlist / CTA section** — email input + submit button + success message + form validation
9. **Footer** — product name, links, copyright

### Waitlist Email Collection

**For stacks with backend (Next.js, Nuxt, Laravel):**
- Create an API route that accepts POST `{ email }`.
- Validate the email format server-side.
- Read existing `waitlist.json`, append the new entry with timestamp, write back.
- Return success/error JSON response.
- Wire the landing page form to POST to this route via fetch.
- Show success state ("You're on the list!") and error state on the form.

**For static stacks (React + Vite):**
- Use Formspree: form action points to `https://formspree.io/f/{form_id}`.
- Add a comment/note telling the user to create a free Formspree account and replace `{form_id}`.
- Handle success/error states client-side.

---

## Step 6 — Generate the App

Generate a working multi-page app with:

1. **Navigation** — sidebar or top nav with links to all pages. Active state highlighting.
2. **Dashboard / Home** — summary cards, charts (use simple CSS/SVG charts or placeholder), recent activity list. All fake data.
3. **Primary feature page** — the main thing the product does. Functional UI with fake data. Buttons, modals, forms all work (client-side only).
4. **Secondary feature page** — a supporting feature. Table or list view with filtering/sorting (client-side).
5. **Settings / Profile page** — simple form with fake prefilled data. Save button shows a toast/notification.

### Design Standards (apply to every page)

Read `references/design-system.md` and apply:
- Distinctive color palette — never default Tailwind. Custom `tailwind.config` colors.
- Thoughtful typography — use Google Fonts. Pair a display font with a body font.
- Consistent spacing scale — use a rhythm (e.g., 4/8/12/16/24/32/48).
- Polished components — rounded corners, shadows, hover states, transitions.
- Responsive — must look good on mobile and desktop.
- Fake data should feel realistic — use real-sounding names, numbers, dates.

---

## Step 7 — Visual Validation (Playwright MCP)

After code generation is complete, validate the output visually.

**If Playwright MCP is available:**

1. Start the dev server (use the stack's dev command from the reference file).
2. Use Playwright MCP to navigate to each page:
   - Landing page (`/`)
   - Dashboard (`/dashboard`)
   - Each app page
3. Take screenshots of each page at desktop (1280px) and mobile (375px) widths.
4. Check for:
   - Broken layouts (overlapping elements, overflow, misaligned sections)
   - Missing content (empty sections, broken images, placeholder text not filled)
   - Non-functional interactions (click buttons, submit forms, open modals)
   - Visual consistency (colors match palette, typography is consistent)
5. If issues found: fix them and re-validate.

**If Playwright MCP is NOT available:**

Tell the user:
> Playwright MCP is not connected — skipping visual validation. Start the dev server with `{dev command}` and check the pages manually.

---

## Step 8 — Quality Loop

If visual validation found issues:

1. Fix the identified issues.
2. Re-run Playwright validation (Step 7).
3. Repeat until all pages pass — no broken layouts, all interactions work, design is consistent.

Maximum 3 loop iterations. If issues persist after 3 loops, present remaining issues to the user and ask how to proceed.

---

## Step 9 — Generate Project Context Docs

Generate 3 lightweight documentation files in `docs/` from information already gathered in Steps 1-2. No new questions — use the product name, value prop, audience, features, and tech stack already captured.

### Files to Generate

**`docs/vision.md`**
```markdown
# [Product Name]

## Value Proposition
[One-line value prop from Step 1]

## Target Audience
[Target audience from Step 1]

## Key Features
[Bullet list of 3-5 features from Step 1]

## North Star Metric
[Suggest one metric that measures core value — e.g., "weekly active waitlist signups" or "daily feature usage"]
```

**`docs/prd.md`**
```markdown
# PRD — [Product Name]

## Overview
[1-2 sentence product description]

## User Stories
[For each key feature from Step 1, write a user story: "As a [audience], I want to [feature] so that [benefit]"]

## Feature Acceptance Criteria
[For each feature, list 2-3 concrete acceptance criteria]

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
- **Framework:** [chosen stack from Step 2]
- **Styling:** Tailwind CSS
- **Fonts:** [chosen fonts]

## Project Structure
[List the key directories and files generated during scaffolding]

## Component Map
### Landing Page
[List all 9 sections and their components]

### App Pages
[List each page and its key components]

## Data Model
### Waitlist
- email: string (validated)
- timestamp: ISO 8601 string

### Fake Data Entities
[List the fake data structures used in the app]
```

After generating the docs, output:
> **Context docs generated:** `docs/vision.md`, `docs/prd.md`, `docs/tech-design.md`
> These persist context for future sessions. Run `/sk:context` to load them.

---

## Step 10 — Present the Output

Summarize what was generated:

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

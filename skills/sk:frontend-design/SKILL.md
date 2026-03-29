---
name: sk:frontend-design
description: Create distinctive, production-grade frontend interfaces with high design quality. Use this skill when the user asks to build web components, pages, artifacts, posters, or applications (examples include websites, landing pages, dashboards, React components, HTML/CSS layouts, or when styling/beautifying any web UI). Produces design direction, mockups, and visual specifications — NOT code. Use --pencil flag to also generate a Pencil visual mockup (requires Pencil app + MCP).
license: Complete terms in LICENSE.txt
---

## CRITICAL: Design Phase Only — NO CODE

This skill produces design artifacts only. Implementation happens in `/sk:execute-plan`.

- No code: no React, HTML/CSS/JS, file edits, or use of Edit/Write/Bash tools
- Pencil MCP tools ARE allowed — they create visual design artifacts, not code
- Produce: design direction, ASCII mockups, layout specs, component structure, color/typography decisions, interaction notes

## Before You Start

1. If `tasks/findings.md` exists and has content, read it in full — use the agreed approach as the design brief.
2. If `tasks/lessons.md` exists, read it in full — apply every active lesson as a constraint, especially Bug entries related to frontend structure, component architecture, or styling conventions.

## Design Thinking

Before designing, commit to a BOLD aesthetic direction:
- **Purpose**: What problem does this interface solve? Who uses it?
- **Tone**: Pick an extreme: brutally minimal, maximalist chaos, retro-futuristic, organic/natural, luxury/refined, playful/toy-like, editorial/magazine, brutalist/raw, art deco/geometric, soft/pastel, industrial/utilitarian, etc.
- **Constraints**: Technical requirements (framework, performance, accessibility).
- **Differentiation**: What makes this UNFORGETTABLE? What's the one thing someone will remember?

**CRITICAL**: Choose a clear conceptual direction and execute it with precision. Bold maximalism and refined minimalism both work — the key is intentionality, not intensity.

Then produce a **design artifact** — not code — that includes:
- ASCII or text-based layout mockups for key screens/states
- Color palette (hex values, CSS variable names)
- Typography choices (font families, sizes, weights, tracking)
- Component structure description (what elements exist, their hierarchy)
- Interaction notes (hover states, transitions, animations to implement)
- Any specific Tailwind classes or CSS patterns to use during implementation

## Frontend Aesthetics Guidelines

- **Typography**: Choose beautiful, unique, unexpected fonts. Avoid generic families (Arial, Inter, Roboto, Space Grotesk). Pair a distinctive display font with a refined body font.
- **Color & Theme**: Commit to a cohesive aesthetic. Use CSS variables for consistency. Dominant colors with sharp accents outperform timid, evenly-distributed palettes.
- **Motion**: Animate for micro-interactions and effects. Prefer CSS-only for HTML; use Motion library for React. One well-orchestrated page load with staggered reveals creates more delight than scattered micro-interactions. Use scroll-triggering and hover states that surprise.
- **Spatial Composition**: Unexpected layouts. Asymmetry. Overlap. Diagonal flow. Grid-breaking elements. Generous negative space OR controlled density.
- **Backgrounds & Visual Details**: Create atmosphere and depth. Add gradient meshes, noise textures, geometric patterns, layered transparencies, dramatic shadows, decorative borders, custom cursors, grain overlays — match the aesthetic.

NEVER use generic AI aesthetics: overused fonts (Inter, Roboto, Arial, system fonts, Space Grotesk), cliched purple-gradient-on-white color schemes, predictable layouts, or cookie-cutter patterns. Vary between light/dark themes, different fonts, and different aesthetics across generations.

**IMPORTANT**: Match design detail to the aesthetic vision. Maximalist designs need elaborate layout descriptions, rich animation notes, and dense component specs. Minimalist designs need precise spacing rules, restrained color notes, and careful typographic ratios. Commit to the vision fully.

## UX Quality Constraints

Hard constraints during design, ordered by priority. Skip categories irrelevant to the current design (e.g., Charts for a landing page).

| Priority | Category | Impact | Key Rule |
|---|---|---|---|
| 1 | Accessibility | CRITICAL | Contrast 4.5:1, keyboard nav, aria-labels, focus rings |
| 2 | Touch & Interaction | CRITICAL | Min 44×44px targets, tap feedback, no hover-only |
| 3 | Performance | HIGH | WebP/AVIF images, lazy load, skeleton screens, no layout shift |
| 4 | Style Selection | HIGH | Match style to product type, SVG icons (never emoji), one primary CTA |
| 5 | Layout & Responsive | HIGH | Mobile-first, breakpoints 375/768/1024/1440, no horizontal scroll |
| 6 | Typography & Color | MEDIUM | Base 16px body, line-height 1.5, semantic color tokens |
| 7 | Animation | MEDIUM | 150–300ms duration, transform/opacity only, respect prefers-reduced-motion |
| 8 | Forms & Feedback | MEDIUM | Visible labels, error near field, loading → success/error on submit |
| 9 | Navigation | HIGH | Bottom nav ≤5 items, predictable back, deep linking |
| 10 | Charts & Data | LOW | Match chart to data type, accessible colors, legend visible |

### 1. Accessibility (CRITICAL)

- Minimum 4.5:1 contrast ratio for normal text (large text 3:1)
- Visible focus rings on all interactive elements (2–4px outline)
- Descriptive alt text on all meaningful images
- `aria-label` on icon-only buttons
- Tab order matches visual order; full keyboard navigation supported
- `label[for]` on every form input — never placeholder-only
- Never convey information by color alone (add icon or text)
- Respect `prefers-reduced-motion` — reduce or disable animations when set
- Sequential heading hierarchy h1→h6, no skipped levels
- Screen reader logical reading order; meaningful accessibilityLabel/Hint
- Skip-to-main-content link for keyboard users

### 2. Touch & Interaction (CRITICAL)

- Minimum 44×44pt (iOS) / 48×48dp (Android) tap target — expand hitSlop if icon is smaller
- Minimum 8px gap between adjacent touch targets
- Never rely on hover-only for primary interactions — use click/tap
- Disable buttons during async operations; show spinner or progress
- Add `cursor-pointer` to all clickable elements (web)
- Provide visual feedback on press within 100ms (ripple, opacity, elevation)
- Use `touch-action: manipulation` to eliminate 300ms tap delay (web)
- Avoid horizontal swipe on scrollable content — prefer vertical scroll
- Don't block system gestures (back swipe, Control Center, home indicator)

### 3. Performance (HIGH)

- Use WebP/AVIF with `srcset`/`sizes`; lazy load non-hero images
- Declare `width`/`height` or `aspect-ratio` on images to prevent CLS
- Use `font-display: swap` or `optional` to avoid FOIT
- Preload only critical fonts — avoid preloading every weight variant
- Lazy load non-hero components via dynamic import / route-level splitting
- Load third-party scripts `async`/`defer`
- Reserve space for async content to avoid layout jumps (CLS < 0.1)
- Virtualize lists with 50+ items
- Use skeleton/shimmer for loads >300ms — never a blank frame
- Keep per-frame work <16ms (60fps); move heavy tasks off main thread
- Debounce/throttle scroll, resize, and input handlers

### 4. Style Selection (HIGH)

- Match style to product type and industry — no random style mixing
- Use SVG icons (Heroicons, Lucide) — never emojis as structural icons
- Use one icon set throughout — consistent stroke width, corner radius, filled vs outline
- Each screen has exactly one primary CTA; secondary actions are visually subordinate
- Apply a consistent elevation/shadow scale — no arbitrary shadow values
- Design light and dark variants together; don't assume light values work in dark mode
- Blur signals background dismissal (modals, sheets) — not decoration
- Respect platform idioms (iOS HIG vs Material Design) for navigation, controls, motion

### 5. Layout & Responsive (HIGH)

- `<meta name="viewport" content="width=device-width, initial-scale=1">` — never disable zoom
- Design mobile-first; scale up to 768, 1024, 1440
- No horizontal scroll on mobile; all content fits viewport width
- Use 4pt/8dp incremental spacing system throughout
- Consistent `max-w-6xl`/`7xl` container on desktop
- Define a z-index scale (e.g., 0 / 10 / 20 / 40 / 100 / 1000) — no arbitrary values
- Fixed navbars/bottom bars must pad underlying scroll content
- Use `min-h-dvh` instead of `100vh` on mobile
- Establish hierarchy via size, spacing, contrast — not color alone
- Core content first on mobile; fold or hide secondary content

### 6. Typography & Color (MEDIUM)

- Minimum 16px body text on mobile (prevents iOS auto-zoom)
- Line-height 1.5–1.75 for body text
- 60–75 characters per line on desktop; 35–60 on mobile
- Consistent type scale (e.g., 12 / 14 / 16 / 18 / 24 / 32)
- Bold headings (600–700), regular body (400), medium labels (500)
- Define semantic color tokens (`--color-primary`, `--color-error`, `--color-surface`) — never raw hex in components
- Dark mode: use desaturated/lighter tonal variants, not inverted colors; test contrast independently
- All foreground/background pairs must meet 4.5:1 (AA); use a contrast checker
- Use tabular/monospaced figures for prices, data columns, and timers
- Use whitespace intentionally to group related items and separate sections

### 7. Animation (MEDIUM)

- Duration: 150–300ms for micro-interactions; complex transitions ≤400ms; never >500ms
- Animate `transform` and `opacity` only — never `width`, `height`, `top`, `left`
- Use ease-out for entering elements; ease-in for exiting
- Every animation expresses cause-effect — no purely decorative motion
- State changes (hover, active, expanded, modal) animate smoothly — no snapping
- Page transitions maintain spatial continuity (shared element, directional slide)
- Exit animations should be 60–70% of enter duration to feel responsive
- Stagger list/grid item entrance by 30–50ms per item
- Animations must be interruptible — user tap cancels in-progress animation immediately
- Never block user input during an animation
- Scale feedback on press: subtle 0.95–1.05 scale on tappable cards/buttons
- `prefers-reduced-motion` must reduce or disable animations entirely

### 8. Forms & Feedback (MEDIUM)

- Every input has a visible label — never placeholder-only
- Show errors immediately below the related field (not only at the top)
- Mark required fields (asterisk or explicit label)
- Submit button: loading state → success or error state
- Auto-dismiss toasts in 3–5s; toasts must not steal focus (`aria-live="polite"`)
- Confirm before destructive actions (modals, undo toasts)
- Validate on blur, not on every keystroke
- Use semantic input types (`email`, `tel`, `number`) for correct mobile keyboard
- Provide show/hide toggle on password fields
- Error messages state the cause + how to fix — not just "Invalid input"
- Multi-step forms show a step indicator and allow back navigation
- After submit error, auto-focus the first invalid field

### 9. Navigation (HIGH)

- Bottom navigation: maximum 5 items with both icon and text label
- Back navigation is predictable and restores scroll/filter state
- All key screens are deep-linkable via URL/route
- Current location is visually highlighted in navigation (color, weight, indicator)
- Modals have a clear close affordance; support swipe-down to dismiss on mobile
- Never use modals for primary navigation flows
- Large screens (≥1024px) prefer sidebar; small screens use bottom/top nav
- Don't mix Tab + Sidebar + Bottom Nav at the same hierarchy level
- Dangerous actions (logout, delete account) are visually separated from normal nav
- After route change, move focus to main content region for screen readers

### 10. Charts & Data (when applicable)

- Match chart type to data: trend → line, comparison → bar, proportion → pie/donut
- Avoid pie/donut for >5 categories — use bar chart instead
- Use accessible color palettes; never red/green only (colorblind users)
- Always show a legend near the chart (not below a scroll fold)
- Provide tooltips/data labels on hover (web) or tap (mobile)
- Label all axes with units; avoid rotated labels on mobile
- Charts must reflow on small screens (horizontal bar instead of vertical, fewer ticks)
- Show skeleton/shimmer while chart data loads — never an empty axis frame
- Grid lines should be low-contrast (e.g., `gray-200`) so they don't compete with data
- Provide a text summary or `aria-label` describing the chart's key insight

---

## Professional UI Anti-Patterns

Frequently overlooked issues that make UI look unprofessional. Flag any of these in the design spec.

### Icons & Visual Elements
- **No emoji as icons** — use Heroicons, Lucide, or equivalent SVG sets
- **No raster icons** — SVG only; PNGs blur and can't adapt to dark mode
- **No mixed icon styles** — pick one set; consistent stroke width and fill style throughout
- **No inconsistent sizing** — define icon size tokens (sm/md/lg = 16/20/24pt)
- **Pressed states must not shift layout** — use opacity/color/elevation, not transforms that reflow siblings

### Interaction
- **No tap-only no-feedback** — every tappable element responds visually within 100ms
- **No hover-only states on mobile** — hover states are fine for desktop, never the only affordance
- **No disabled elements that look enabled** — use `opacity: 0.38–0.5` + `cursor: not-allowed` + semantic `disabled` attribute
- **No precision-required targets** — avoid requiring taps on thin edges or pixel-perfect areas

### Light/Dark Mode
- **No hardcoded hex in components** — use semantic tokens that map per theme
- **No light-mode-only testing** — always verify dark mode contrast independently
- **No weak modal scrims** — use 40–60% black so background doesn't compete with foreground
- **No color-only state indicators** — always pair color with icon or label

### Layout & Spacing
- **No safe-area violations** — respect notch, Dynamic Island, and gesture bar on mobile
- **No scroll content hidden behind fixed bars** — add correct insets
- **No random spacing** — every gap follows the 4/8dp rhythm
- **No edge-to-edge paragraphs on tablets** — constrain long-form text width for readability

---

## Pre-Delivery Checklist

Include this checklist at the end of every design output. Implementation must pass all applicable items before shipping.

```
### Pre-Delivery Checklist

**Accessibility**
- [ ] All text contrast ≥4.5:1 (normal) or ≥3:1 (large/UI)
- [ ] Focus rings visible on all interactive elements
- [ ] All images/icons have alt text or aria-label
- [ ] No color-only information conveyance
- [ ] prefers-reduced-motion respected

**Touch & Interaction**
- [ ] All tap targets ≥44×44pt
- [ ] Every tappable element has pressed-state feedback
- [ ] No hover-only interactions on mobile
- [ ] cursor-pointer on all clickable web elements

**Layout**
- [ ] No horizontal scroll at 375px
- [ ] Safe areas respected (notch, gesture bar, tab bar)
- [ ] Scroll content not hidden behind fixed bars
- [ ] 4/8dp spacing rhythm consistent throughout

**Typography & Color**
- [ ] Body text ≥16px on mobile
- [ ] Semantic color tokens used (no raw hex in components)
- [ ] Dark mode contrast verified independently

**Performance**
- [ ] Images use WebP/AVIF with declared dimensions
- [ ] Skeleton/shimmer shown for loads >300ms
- [ ] No layout shift from async content (CLS < 0.1)

**Animation**
- [ ] All transitions 150–300ms
- [ ] Only transform/opacity animated (no width/height/top/left)
- [ ] Animations interruptible; no input blocking

**Icons**
- [ ] No emojis used as icons (SVG only)
- [ ] Consistent icon family and stroke style throughout
```

## Output Format

End every `/sk:frontend-design` session with a structured summary:

```
## Design Summary

### Aesthetic Direction
[One paragraph describing the tone, feel, and visual identity]

### Color Palette
- Background: #xxxxxx (--var-name)
- Foreground: #xxxxxx (--var-name)
- Accent: #xxxxxx (--var-name)

### Typography
- Display: [Font name] — [weight/size/tracking notes]
- Body: [Font name] — [weight/size notes]

### Layout Mockup
[ASCII or text mockup of the key screen(s)]

### Component Notes
[Description of each component: structure, states, interactions]

### Animation & Motion
[What moves, when, how — described in words]

### Implementation Notes
[Specific Tailwind classes, CSS patterns, or gotchas for /sk:execute-plan]

### Pre-Delivery Checklist
[Copy the checklist from the UX Quality Constraints section above and mark which items are covered by this design, and which need special attention during implementation]
```

After presenting the design summary, you **MUST** stop and ask — do not continue or summarize further:

> **"Would you like me to create a Pencil visual mockup? (Requires Pencil app open + Pencil MCP connected) (y/n)"**

Wait for the user's response before doing anything else.

You can also trigger the Pencil phase directly by running `/sk:frontend-design --pencil`.

---

## Pencil Visual Mockup Phase

Only run this phase if:
- The user answers **y** or **yes** to the prompt above, OR
- The user invoked the skill with `--pencil`

### Step 1 — Derive the filename and open the .pen file

Before opening any Pencil document:

1. Read `tasks/todo.md` and extract the task name from the first `# TODO` heading:
   - Pattern: `# TODO — YYYY-MM-DD — <task-name>`
   - Convert to kebab-case (e.g., `"Gate Auto-Commit + Tech Debt"` → `gate-auto-commit-tech-debt`)
   - If no `# TODO` heading exists, derive a slug from the design subject instead (e.g., `dashboard-analytics`)

2. Target path: `docs/design/[task-name].pen`

3. Call `open_document('docs/design/[task-name].pen')` — use the full path whether the file exists or not. The tool auto-detects existence: opens the file if it's already there, creates it on disk if not.

The `.pen` file is created at `docs/design/[task-name].pen` before any design work begins, ensuring the design is saved to disk and committable.

### Step 2 — Load design context

Run these two calls before drawing anything:

1. `get_guidelines(topic)` — pick the closest topic:
   - `web-app` → dashboards, SaaS, admin panels
   - `landing-page` → marketing sites, portfolios, product pages
   - `mobile-app` → mobile-first interfaces
   - `design-system` → component libraries, style guides
   - `table` → data-heavy UIs
   - `slides` → presentations

2. `get_style_guide_tags` → then `get_style_guide(tags, name)` — pick tags that match the aesthetic direction decided in the design summary (e.g., dark, minimal, editorial, playful, corporate, luxury). This gives Pencil a visual language to work from.

### Step 3 — Set the color palette as variables

Call `set_variables` to register the color palette from the Design Summary as Pencil variables so they can be referenced throughout the design:

```
{
  "color-bg": "#xxxxxx",
  "color-fg": "#xxxxxx",
  "color-accent": "#xxxxxx"
  // + any other palette values
}
```

### Step 4 — Build the mockup

Use `batch_design` to construct the visual. Work screen by screen:

1. Create a **frame** for each key screen identified in the Layout Mockup.
2. Inside each frame, add sections matching the component hierarchy from Component Notes.
3. Reuse components from the design system where they fit (buttons, inputs, cards, tables, etc.) — these are already available as reusable components in the canvas.
4. Apply the color variables and typography direction to every element.
5. Keep batches focused: aim for one screen per batch_design call to stay within limits.

### Step 5 — Validate and iterate

After each screen is built, call `get_screenshot` to visually inspect the result.

- If layout or spacing is off: call `snapshot_layout` to inspect computed positions, then fix with another `batch_design` call.
- Iterate until the screen faithfully represents the Design Summary.

### Step 6 — Handle existing file updates

When opening an existing `.pen` file to update a design:

1. Call `get_editor_state(include_schema: false)` to see current top-level nodes.
2. Call `snapshot_layout` on affected frames to understand what's there.
3. Use `batch_design` with `update` or `replace` operations — do not delete and recreate unless necessary.
4. Validate with `get_screenshot` after each batch.

### Step 7 — Finish

Tell the user the path to the saved `.pen` file and confirm which screens were created or updated.

Then tell the user: **"Run `/sk:write-plan` to turn this design into an implementation plan."**

---

## Model Routing

Read `.shipkit/config.json` from the project root if it exists.

- If `model_overrides["sk:frontend-design"]` is set, use that model — it takes precedence.
- Otherwise use the `profile` field. Default: `balanced`.

| Profile | Model |
|---------|-------|
| `full-sail` | opus (inherit) |
| `quality` | opus (inherit) |
| `balanced` | sonnet |
| `budget` | sonnet |

> `opus` = inherit (uses the current session model). When spawning sub-agents via the Agent tool, pass `model: "<resolved-model>"`.

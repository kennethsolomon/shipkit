# Design System — MVP Aesthetic Guidelines

Guidelines for generating visually distinctive MVPs that don't look like generic AI output.

---

## Core Principle

Every MVP must look **intentionally designed**, not template-generated. The goal is to make visitors think "this looks legit" — good enough to trust with their email and time.

---

## Typography

### Rules
- Always use **two fonts**: one display/heading font + one body font.
- Source from Google Fonts. Never use system fonts, Inter, Roboto, or Arial as the primary choice.
- Vary choices between projects — do not converge on the same fonts repeatedly.

### Suggested Pairings (rotate, don't default to #1)
1. **DM Serif Display** + **DM Sans** — editorial, trustworthy
2. **Playfair Display** + **Source Sans 3** — luxury, refined
3. **Space Grotesk** + **Inter** — tech, modern (use sparingly, very common)
4. **Sora** + **Nunito Sans** — friendly, approachable SaaS
5. **Clash Display** + **Satoshi** — bold, contemporary
6. **Fraunces** + **Commissioner** — warm, distinctive
7. **Cabinet Grotesk** + **General Sans** — clean, startup
8. **Bricolage Grotesque** + **Geist** — editorial tech

### Scale
Use a consistent type scale. Recommended base: `16px`.

| Element | Size | Weight | Tracking |
|---------|------|--------|----------|
| H1 (hero) | 48-72px | 700-800 | -0.02em |
| H2 (section) | 32-40px | 600-700 | -0.01em |
| H3 (card title) | 20-24px | 600 | normal |
| Body | 16-18px | 400 | normal |
| Small/caption | 13-14px | 400-500 | 0.01em |

---

## Color

### Rules
- Never use default Tailwind color names without customization (`blue-500`, `gray-100` raw).
- Define a custom palette in `tailwind.config` under `extend.colors`.
- Every palette needs: background, foreground, primary accent, secondary accent, muted, border, success, error.
- Commit to a mood — don't mix warm and cool randomly.

### Palette Strategies (pick one per project)
1. **Dark + neon accent** — dark bg (#0a0a0a), light text (#fafafa), vibrant accent (#6366f1 or #22d3ee)
2. **Warm neutral + earth accent** — warm white (#faf9f6), dark text (#1a1a1a), terracotta/amber accent
3. **Cool minimal** — pure white (#ffffff), slate text (#334155), single accent color
4. **Bold saturated** — deep colored bg (#1e1b4b), contrasting text, bright accent
5. **Soft pastel** — light tinted bg (#f0fdf4), dark text, pastel accent palette

### Contrast
- Text on background must meet WCAG AA (4.5:1 for body text, 3:1 for large text).
- Test accent colors against both light and dark surfaces.

---

## Spacing

Use a **4px base unit** with a consistent scale:

| Token | Value | Use for |
|-------|-------|---------|
| `xs` | 4px | Icon gaps, tight padding |
| `sm` | 8px | Inline spacing, compact cards |
| `md` | 16px | Default padding, form gaps |
| `lg` | 24px | Card padding, section content |
| `xl` | 32px | Section gaps |
| `2xl` | 48px | Between major sections |
| `3xl` | 64px | Hero padding, page-level spacing |
| `4xl` | 96px | Landing page section separation |

### Layout Rhythm
- Sections on the landing page should have `py-20` to `py-28` (80-112px) vertical padding.
- Cards should have consistent `p-6` to `p-8` padding.
- The max content width should be `max-w-6xl` or `max-w-7xl`, centered.

---

## Components

### Buttons
- Primary: filled with accent color, white text, `rounded-lg` or `rounded-xl`, `px-6 py-3`.
- Secondary: outlined or ghost, accent color border/text.
- Hover: subtle scale (`hover:scale-105`) or color shift. Add `transition-all duration-200`.
- Never use default browser button styles.

### Cards
- Background slightly offset from page bg (e.g., white card on gray bg, or lighter card on dark bg).
- Consistent `rounded-xl` or `rounded-2xl`.
- Subtle shadow: `shadow-sm` or `shadow-md`. On dark themes use border instead.
- Hover state for interactive cards: lift (`hover:-translate-y-1 hover:shadow-lg`).

### Forms / Inputs
- Inputs: `rounded-lg`, visible border, generous padding (`px-4 py-3`).
- Focus state: accent-colored ring (`focus:ring-2 focus:ring-accent`).
- Labels above inputs, not floating.
- Error states: red border + error message below.

### Navigation
- Sticky/fixed navbar with blur backdrop (`backdrop-blur-md bg-white/80`).
- Logo/name on left, links center or right, CTA button far right.
- Mobile: hamburger menu with slide-in drawer or dropdown.

---

## Anti-Patterns — NEVER Do These

1. **Default Tailwind colors** — `bg-blue-500 text-gray-700` without custom palette
2. **System fonts** — `-apple-system, BlinkMacSystemFont` or `font-sans` without override
3. **Flat layouts** — sections that all look the same width/padding/structure
4. **Missing hover states** — buttons/links that don't respond to hover
5. **Placeholder.com images** — use gradient boxes, SVG illustrations, or emoji as placeholders instead
6. **Lorem ipsum** — generate realistic fake content based on the product context
7. **Inconsistent spacing** — mixing random padding/margin values
8. **Tiny click targets** — buttons and links must be minimum 44x44px touch targets
9. **No visual hierarchy** — everything same size/weight, no emphasis
10. **Generic hero** — "Welcome to [Product]" with no visual interest

---

## Responsive Design

- **Mobile-first** approach — design for 375px width, enhance for desktop.
- Breakpoints: `sm` (640px), `md` (768px), `lg` (1024px), `xl` (1280px).
- Hero text scales down: 48px desktop → 32px mobile.
- Feature grids: 3 columns desktop → 1 column mobile.
- Navigation: full links desktop → hamburger mobile.
- Cards: horizontal layout desktop → stacked mobile.
- Always test that nothing overflows horizontally on mobile.

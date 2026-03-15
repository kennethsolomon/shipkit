---
name: frontend-design
description: Create distinctive, production-grade frontend interfaces with high design quality. Use this skill when the user asks to build web components, pages, artifacts, posters, or applications (examples include websites, landing pages, dashboards, React components, HTML/CSS layouts, or when styling/beautifying any web UI). Produces design direction, mockups, and visual specifications — NOT code.
license: Complete terms in LICENSE.txt
---

## CRITICAL: Design Phase Only — NO CODE

**This skill is a design phase, not an implementation phase.**

- **DO NOT** write, edit, or generate any code (no React, no HTML/CSS/JS, no file edits)
- **DO NOT** use file editing tools (Edit, Write, Bash)
- **Pencil MCP tools ARE allowed** — they create visual design artifacts, not code
- **DO produce** design direction, ASCII mockups, layout specs, component structure descriptions, color/typography decisions, and interaction notes
- Implementation happens in `/execute-plan` — not here

This skill guides the design of distinctive, production-grade frontend interfaces that avoid generic "AI slop" aesthetics. Output is a design artifact: a clear, decision-complete visual specification that `/write-plan` and `/execute-plan` can use to implement.

The user provides frontend requirements: a component, page, application, or interface to design. They may include context about the purpose, audience, or technical constraints.

## Before You Start

1. If `tasks/findings.md` exists and has content, read it in full. Use the agreed
   approach and requirements as the design brief — this replaces the need to ask the
   user to re-explain what was already decided in brainstorming.

2. If `tasks/lessons.md` exists, read it in full. Apply every active lesson as a
   constraint during design — particularly any patterns flagged under **Bug** that
   relate to frontend structure, component architecture, or styling conventions.

## Design Thinking

Before coding, understand the context and commit to a BOLD aesthetic direction:
- **Purpose**: What problem does this interface solve? Who uses it?
- **Tone**: Pick an extreme: brutally minimal, maximalist chaos, retro-futuristic, organic/natural, luxury/refined, playful/toy-like, editorial/magazine, brutalist/raw, art deco/geometric, soft/pastel, industrial/utilitarian, etc. There are so many flavors to choose from. Use these for inspiration but design one that is true to the aesthetic direction.
- **Constraints**: Technical requirements (framework, performance, accessibility).
- **Differentiation**: What makes this UNFORGETTABLE? What's the one thing someone will remember?

**CRITICAL**: Choose a clear conceptual direction and execute it with precision. Bold maximalism and refined minimalism both work - the key is intentionality, not intensity.

Then produce a **design artifact** — not code — that includes:
- ASCII or text-based layout mockups for key screens/states
- Color palette (hex values, CSS variable names)
- Typography choices (font families, sizes, weights, tracking)
- Component structure description (what elements exist, their hierarchy)
- Interaction notes (hover states, transitions, animations to implement)
- Any specific Tailwind classes or CSS patterns to use during implementation

## Frontend Aesthetics Guidelines

Focus on:
- **Typography**: Choose fonts that are beautiful, unique, and interesting. Avoid generic fonts like Arial and Inter; opt instead for distinctive choices that elevate the frontend's aesthetics; unexpected, characterful font choices. Pair a distinctive display font with a refined body font.
- **Color & Theme**: Commit to a cohesive aesthetic. Use CSS variables for consistency. Dominant colors with sharp accents outperform timid, evenly-distributed palettes.
- **Motion**: Use animations for effects and micro-interactions. Prioritize CSS-only solutions for HTML. Use Motion library for React when available. Focus on high-impact moments: one well-orchestrated page load with staggered reveals (animation-delay) creates more delight than scattered micro-interactions. Use scroll-triggering and hover states that surprise.
- **Spatial Composition**: Unexpected layouts. Asymmetry. Overlap. Diagonal flow. Grid-breaking elements. Generous negative space OR controlled density.
- **Backgrounds & Visual Details**: Create atmosphere and depth rather than defaulting to solid colors. Add contextual effects and textures that match the overall aesthetic. Apply creative forms like gradient meshes, noise textures, geometric patterns, layered transparencies, dramatic shadows, decorative borders, custom cursors, and grain overlays.

NEVER use generic AI-generated aesthetics like overused font families (Inter, Roboto, Arial, system fonts), cliched color schemes (particularly purple gradients on white backgrounds), predictable layouts and component patterns, and cookie-cutter design that lacks context-specific character.

Interpret creatively and make unexpected choices that feel genuinely designed for the context. No design should be the same. Vary between light and dark themes, different fonts, different aesthetics. NEVER converge on common choices (Space Grotesk, for example) across generations.

**IMPORTANT**: Match design detail to the aesthetic vision. Maximalist designs need elaborate layout descriptions, rich animation notes, and dense component specs. Minimalist designs need precise spacing rules, restrained color notes, and careful typographic ratios. Elegance comes from committing to the vision fully.

Remember: Claude is capable of extraordinary creative thinking. Don't hold back on the design direction — show what can be envisioned when thinking outside the box and committing fully to a distinctive aesthetic.

## Output Format

End every `/frontend-design` session with a structured summary:

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
[Specific Tailwind classes, CSS patterns, or gotchas for /execute-plan]
```

After presenting the design summary, ask the user:

**"Would you like me to create a Pencil visual mockup? (y/n)"**

---

## Pencil Visual Mockup Phase

Only run this phase if the user answers **y** or **yes**.

### Step 1 — Find or create the .pen file

Check `docs/design/` for an existing `.pen` file that matches this design (by name or topic).

- **Existing file found**: call `open_document(filePath)` to open it, then skip to Step 3.
- **No file found**: call `open_document('new')` to create a fresh canvas.
  - The file will be saved to `docs/design/{design-name}.pen` — use a slug derived from the design subject (e.g., `docs/design/dashboard-analytics.pen`).

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

Then tell the user: **"Run `/write-plan` to turn this design into an implementation plan."**

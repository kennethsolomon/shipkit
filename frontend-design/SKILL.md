---
name: frontend-design
description: Create distinctive, production-grade frontend interfaces with high design quality. Use this skill when the user asks to build web components, pages, artifacts, posters, or applications (examples include websites, landing pages, dashboards, React components, HTML/CSS layouts, or when styling/beautifying any web UI). Produces design direction, mockups, and visual specifications — NOT code.
license: Complete terms in LICENSE.txt
---

## CRITICAL: Design Phase Only — NO CODE

**This skill is a design phase, not an implementation phase.**

- **DO NOT** write, edit, or generate any code (no React, no HTML/CSS/JS, no file edits)
- **DO NOT** use file editing tools (Edit, Write, Bash)
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

After presenting the design summary, tell the user: **"Run `/write-plan` to turn this into an implementation plan."**

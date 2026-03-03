---
name: frontend-design
description: Create distinctive, production-grade frontend interfaces with high design quality. Use this skill when the user asks to build web components, pages, artifacts, posters, or applications (examples include websites, landing pages, dashboards, React components, HTML/CSS layouts, or when styling/beautifying any web UI). Generates creative, polished code and UI design that avoids generic AI aesthetics.
license: Complete terms in LICENSE.txt
---

This skill guides creation of distinctive, production-grade frontend interfaces that avoid generic "AI slop" aesthetics. Implement real working code with exceptional attention to aesthetic details and creative choices.

The user provides frontend requirements: a component, page, application, or interface to build. They may include context about the purpose, audience, or technical constraints.

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

Then implement working code (HTML/CSS/JS, React, Vue, etc.) that is:
- Production-grade and functional
- Visually striking and memorable
- Cohesive with a clear aesthetic point-of-view
- Meticulously refined in every detail

## Frontend Aesthetics Guidelines

Focus on:
- **Typography**: Choose fonts that are beautiful, unique, and interesting. Avoid generic fonts like Arial and Inter; opt instead for distinctive choices that elevate the frontend's aesthetics; unexpected, characterful font choices. Pair a distinctive display font with a refined body font.
- **Color & Theme**: Commit to a cohesive aesthetic. Use CSS variables for consistency. Dominant colors with sharp accents outperform timid, evenly-distributed palettes.
- **Motion**: Use animations for effects and micro-interactions. Prioritize CSS-only solutions for HTML. Use Motion library for React when available. Focus on high-impact moments: one well-orchestrated page load with staggered reveals (animation-delay) creates more delight than scattered micro-interactions. Use scroll-triggering and hover states that surprise.
- **Spatial Composition**: Unexpected layouts. Asymmetry. Overlap. Diagonal flow. Grid-breaking elements. Generous negative space OR controlled density.
- **Backgrounds & Visual Details**: Create atmosphere and depth rather than defaulting to solid colors. Add contextual effects and textures that match the overall aesthetic. Apply creative forms like gradient meshes, noise textures, geometric patterns, layered transparencies, dramatic shadows, decorative borders, custom cursors, and grain overlays.

NEVER use generic AI-generated aesthetics like overused font families (Inter, Roboto, Arial, system fonts), cliched color schemes (particularly purple gradients on white backgrounds), predictable layouts and component patterns, and cookie-cutter design that lacks context-specific character.

Interpret creatively and make unexpected choices that feel genuinely designed for the context. No design should be the same. Vary between light and dark themes, different fonts, different aesthetics. NEVER converge on common choices (Space Grotesk, for example) across generations.

**IMPORTANT**: Match implementation complexity to the aesthetic vision. Maximalist designs need elaborate code with extensive animations and effects. Minimalist or refined designs need restraint, precision, and careful attention to spacing, typography, and subtle details. Elegance comes from executing the vision well.

Remember: Claude is capable of extraordinary creative work. Don't hold back, show what can truly be created when thinking outside the box and committing fully to a distinctive vision.

## Browser Verification

After generating code, verify it visually using the Playwright MCP plugin if a browser target exists.

**When the user mentions a local dev server** (e.g. `localhost:3000`, `localhost:5173`, etc.):

1. **Navigate** — open the URL:
   ```
   mcp__plugin_playwright_playwright__browser_navigate({ url: "http://localhost:3000" })
   ```

2. **Screenshot at desktop** — capture the initial render:
   ```
   mcp__plugin_playwright_playwright__browser_take_screenshot({ type: "png" })
   ```

3. **Test responsive breakpoints** — resize and screenshot at each:
   - Mobile: `browser_resize({ width: 375, height: 812 })`
   - Tablet: `browser_resize({ width: 768, height: 1024 })`
   - Desktop: `browser_resize({ width: 1440, height: 900 })`

4. **Check for JS errors** — catch any runtime issues:
   ```
   mcp__plugin_playwright_playwright__browser_console_messages({ level: "error" })
   ```
   If errors are found, fix them before presenting the final result.

5. **Present screenshots** inline in the response so the user can see visual verification without leaving the terminal.

**When no dev server is running** (standalone HTML file or no URL provided): skip browser verification and note that the user can open the file locally to preview. Do not attempt to navigate to a file path directly unless it is a valid `file://` URL the user has specified.

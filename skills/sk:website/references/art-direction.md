# Art Direction Reference

Use this when building or reviewing the visual system for a website. Translate the business brief into a deliberate visual direction that can be implemented in code without drifting into generic AI-generated styling.

## Workflow

1. Pick one dominant aesthetic direction from the list below.
2. Define 2–4 signature design moves.
3. Choose a type strategy, palette behavior, spacing rhythm, and motion stance.
4. Verify the style still supports clarity, trust, and conversion.

---

## Aesthetic Directions

Choose exactly one dominant direction. Do not mix multiple directions without a clear hierarchy.

### Restrained Editorial

Good for: architecture studios, fashion-adjacent brands, premium consultants, galleries, publishing.

Signals:
- Strong typographic contrast (large serif headline, small sans body)
- Generous whitespace — sections breathe
- Sparse palette (warm white + dark neutral + one muted accent)
- Image restraint — one strong image per section, not a grid

Avoid:
- Decorative layers that break the calm
- Loud CTA styling that contradicts the quiet tone

### Premium Product-Led

Good for: SaaS, devices, premium consumer products, DTC hero pages.

Signals:
- Crisp hierarchy with product at the center
- Focused product framing (screenshot, mockup, or isolated product shot)
- Clear product storytelling — one benefit per section
- Controlled accent color on a near-white or dark background

Avoid:
- Fake dashboards with no real product
- Overstuffed hero sections with too many messages

### Bold Brand-Forward

Good for: agencies, challenger brands, culture-led products, streetwear, creative studios.

Signals:
- Strong contrast between sections
- Daring type scale — headline that dominates the viewport
- Sharper section transitions (hard cuts, not gentle fades)
- High visual recall through one repeating graphic pattern or color block

Avoid:
- Sacrificing legibility for attitude
- Using bold direction for trust-sensitive businesses (law, medical, finance)

### Warm Hospitality

Good for: cafes, boutique hotels, restaurants, lifestyle spaces, florists, bakeries.

Signals:
- Tactile, atmosphere-first imagery (real textures, warm light, food close-ups)
- Warm neutrals — cream, sand, olive, terracotta, warm grey
- Editorial pacing — section rhythm like a magazine spread
- Practical info (hours, address, reservation CTA) stays visible and easy to find

Avoid:
- Corporate UI chrome that breaks the atmosphere
- Hiding menu, hours, location, or booking link behind design
- Stock cafe imagery when real photography is the point

### Sharp Technical

Good for: developer tools, B2B platforms, infrastructure products, data products, security tools.

Signals:
- Precise grid with tight alignment
- Low visual noise — very few decorative elements
- Strong information hierarchy — function drives layout
- Restrained motion — only when it explains something

Avoid:
- Playful or warm treatments that undermine technical credibility
- Dense copy with no visual breathing room

### Playful Contemporary

Good for: consumer apps, EdTech, food delivery, kids products, lifestyle brands targeting under-35.

Signals:
- Rounded forms, approachable typography
- Brighter palette with confident accent colors
- Motion used generously but purposefully
- Illustration or character work where appropriate

Avoid:
- Looking cheap or juvenile for a premium audience
- Overanimation that obscures the product

### Quiet Luxury

Good for: premium services, interior design, high-end hospitality, luxury retail, wellness brands.

Signals:
- Restraint above all — nothing superfluous
- Tactile material cues (fabric textures, paper grain, stone)
- Elegant typography contrast (fine serif + sparse uppercase tracking)
- Limited palette — usually 2–3 colors maximum

Avoid:
- Gimmicky animation that breaks the calm
- Shiny, trend-driven effects (glass, neon, gradients)
- Too much copy — quiet luxury lets the brand speak with less

---

## Signature Design Moves

Every strong site has 2–4 memorable moves. Choose moves that fit the direction and stick with them.

Examples:
- Oversized serif headline with tight sans-serif body underneath
- Muted palette with one decisive high-contrast accent color
- Image-first storytelling with minimal interface chrome around it
- Rigid grid with one intentionally broken element per section
- Soft material textures behind simple white interface frames
- Full-bleed photography sections alternating with dense-type sections
- Sticky navigation that changes color on scroll

**Rule:** Two strong moves beat six weak ones. Restraint is a design decision.

---

## Typography Mood

Choose typography to express the brand's confidence level and audience — not just to look fashionable.

| Mood | Type strategy |
|---|---|
| Elegant and assured | Serif headline + restrained supporting sans (e.g., Playfair Display + Inter) |
| Modern and precise | Neo-grotesk or geometric sans with strong scale control (e.g., DM Sans, Plus Jakarta Sans) |
| Warm and neighborhood-focused | Soft serif or humanist sans pairings (e.g., Lora + Nunito, Fraunces + Manrope) |
| Technical and credible | Clean sans with tight hierarchy, minimal ornament (e.g., IBM Plex Sans, Space Grotesk) |
| Bold brand-forward | Display face with strong personality (e.g., Syne, Cabinet Grotesk, Clash Display) |
| Quiet luxury | Fine-weight serif or high-tracking uppercase (e.g., Cormorant Garamond, Libre Baskerville) |

**Rules:**
- Use contrast in scale, weight, and rhythm to create hierarchy before adding more colors.
- Never use system fonts (Arial, Helvetica, Times) — always pick with intention.
- Two fonts maximum. One display + one body. A third only if very controlled.

---

## Color Behavior

- One strong accent is often enough. Neutrals do most of the structural work.
- Color guides attention — it should not paint every surface.
- Strong contrast can come from spacing and scale, not just saturated color.
- Trust-sensitive businesses (legal, medical, finance) need calm palettes even when layout is bold.
- If photography is strong, reduce color complexity — let the images carry the warmth.

**Custom palette rules:**
- Never use raw Tailwind palette colors (blue-500, gray-200, etc.) — always define custom values.
- Name colors semantically: `brand`, `accent`, `surface`, `text`, `muted`.
- Define in `tailwind.config.js` under `theme.extend.colors`.

---

## Motion Stance

| Level | When to use | What to use |
|---|---|---|
| None | Trust-sensitive, performance-critical | No animation |
| Subtle | Most business sites | Fade + translate on scroll reveal, 200–300ms |
| Moderate | Consumer brands, hospitality | Stagger reveals, gentle parallax, hover transitions |
| Expressive | Agencies, entertainment, playful brands | Page transitions, character animation, scroll-driven |

**Rules:**
- Motion should support pacing, reveal hierarchy, or reinforce affordances — not decorate.
- `transform` and `opacity` only — never animate layout properties (width, height, margin).
- Respect `prefers-reduced-motion` — wrap all animations in the media query.
- If the page relies on performance or trust, reduce animation density.

---

## Anti-Patterns

Avoid in all cases:
- Random mix of brutalism, glassmorphism, and luxury minimalism in the same page
- Default AI startup gradients (purple → blue, dark mode glow) unless clearly warranted
- Decorative visuals that weaken the CTA or bury practical information
- Style direction that contradicts the business category (bold agency aesthetic for a law firm)
- Fake UI, fake charts, fake product screenshots, fake reviews
- Overanimated entrance sequences that delay time to content

By direction:
- **SaaS**: fake dashboards, purple glow overload, feature-card sprawl with no story
- **Agency**: dramatic visuals with vague copy, no real proof of work
- **Local business**: beautiful design but phone, hours, and service area are buried
- **Hospitality**: atmospheric imagery but no menu, reservation link, or location

**Recovery moves when it feels generic:**
1. Remove one full visual layer
2. Choose one dominant type contrast and commit to it
3. Reduce palette to neutrals + one accent
4. Simplify motion to a single reveal family
5. Move practical business information higher on the page

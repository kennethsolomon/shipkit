# Landing Page — SaaS Section Patterns

Structure and patterns for the mandatory MVP landing page.

---

## Required Sections (in order)

Every landing page must include ALL of these sections. Do not skip any.

### 1. Navbar

```
[Logo/Name]          [Features] [Pricing] [Waitlist]     [Join Waitlist →]
```

- Sticky at top with backdrop blur.
- Logo or product name (text logo is fine — use display font).
- 2-4 nav links that scroll to sections (anchor links).
- CTA button on the right that scrolls to waitlist section.
- Mobile: collapse to hamburger.

### 2. Hero Section

```
┌─────────────────────────────────────────────────┐
│                                                 │
│        [small eyebrow badge or label]           │
│                                                 │
│     Big Bold Headline That Sells               │
│     the Benefit, Not the Feature               │
│                                                 │
│     A subheadline that elaborates in 1-2        │
│     sentences. Specific, not vague.             │
│                                                 │
│     [Primary CTA Button]  [Secondary Link]      │
│                                                 │
│     ┌─────────────────────────────────┐         │
│     │   Hero visual / app preview /   │         │
│     │   illustration / gradient box   │         │
│     └─────────────────────────────────┘         │
│                                                 │
└─────────────────────────────────────────────────┘
```

- **Headline**: Benefit-driven ("Ship faster" not "Project management tool"). 5-10 words max.
- **Subheadline**: Explain what it does and for whom. 1-2 sentences.
- **CTA**: Action verb + outcome ("Join the waitlist", "Get early access", "Start free").
- **Visual**: App screenshot mockup, abstract gradient, or SVG illustration. Never leave empty.
- **Eyebrow**: Optional small badge above headline ("Now in beta", "For developers", "AI-powered").

### 3. Social Proof Bar

```
Trusted by 500+ early adopters
[Logo] [Logo] [Logo] [Logo] [Logo]
```

- Single line below hero.
- Use placeholder company names/logos (styled as gray text or simple SVG shapes).
- Alternatively: "Join 500+ people on the waitlist" with a count (fake but plausible).
- Keep subtle — muted colors, small text.

### 4. Features Grid

```
┌──────────┐ ┌──────────┐ ┌──────────┐
│  🎯 Icon │ │  ⚡ Icon │ │  🔒 Icon │
│  Title   │ │  Title   │ │  Title   │
│  2-line  │ │  2-line  │ │  2-line  │
│  desc    │ │  desc    │ │  desc    │
└──────────┘ └──────────┘ └──────────┘
```

- 3-6 features in a grid (3 columns desktop, 1 mobile).
- Each card: icon/emoji + title (3-5 words) + description (1-2 sentences).
- Icons: use emoji or simple SVG. Heroicons or Lucide if the stack supports it.
- Feature text must match the key features from Step 1.

### 5. How It Works

```
Step 1              Step 2              Step 3
  ①                   ②                   ③
Sign up          Connect your         See results
and set up       data source          in minutes
your account     in one click
```

- 3 steps (rarely 4). Numbered or with icons.
- Each step: number/icon + title + 1-sentence description.
- Optional: connecting line or arrow between steps.
- Explains the user journey from signup to value.

### 6. Pricing

```
┌──────────┐  ┌──────────────┐  ┌──────────┐
│  Free    │  │  Pro ⭐       │  │Enterprise│
│  $0/mo   │  │  $29/mo      │  │  Custom  │
│          │  │              │  │          │
│  • 3 feat│  │  • All free  │  │  • All   │
│  • Basic │  │  • 5 more    │  │  • Custom│
│          │  │  • Priority  │  │  • SLA   │
│ [Start]  │  │ [Get Pro]    │  │ [Contact]│
└──────────┘  └──────────────┘  └──────────┘
```

- 2-3 tiers. Middle tier highlighted (border, scale, badge).
- Prices should be fake but realistic for the product type.
- Each tier: name, price, feature list (5-7 items), CTA button.
- Free tier CTA → waitlist. Paid tier CTAs → waitlist (it's an MVP).
- All buttons route to the waitlist since nothing is real yet.

### 7. Testimonials

```
┌──────────────────────────────────┐
│  "This changed how I work..."    │
│                                  │
│  [Avatar]  Jane Smith            │
│            CTO, TechCo           │
└──────────────────────────────────┘
```

- 2-3 testimonial cards. Carousel or grid.
- Each: quote (1-3 sentences), name, role/company, avatar placeholder.
- Generate realistic-sounding quotes that align with the product's value prop.
- Avatars: use gradient circles with initials, or `ui-avatars.com` service.
- Mark clearly in code comments that these are placeholder testimonials.

### 8. Waitlist / CTA Section

```
┌─────────────────────────────────────────────────┐
│                                                 │
│     Ready to try {Product}?                     │
│     Join the waitlist for early access.          │
│                                                 │
│     [email@example.com        ] [Join →]        │
│                                                 │
│     ✓ No spam. We'll only email you when        │
│       we launch.                                │
│                                                 │
└─────────────────────────────────────────────────┘
```

- Prominent section near bottom (but before footer).
- Headline: compelling CTA ("Ready to X?", "Be the first to try").
- Email input + submit button on one line (desktop), stacked (mobile).
- Trust line below: "No spam" or "Join X others".
- States:
  - **Default**: input + button enabled.
  - **Loading**: button shows spinner, input disabled.
  - **Success**: replace form with "You're on the list! We'll notify you at {email}."
  - **Error**: show error message below input (invalid email, server error).

### 9. Footer

```
{Product Name}                    Features | Pricing | Waitlist
Built with ♥                     © 2026 {Product}. All rights reserved.
```

- Simple. Product name, nav links (repeat from navbar), copyright.
- Optional: social links (use # placeholders).
- Dark or muted background to separate from content.

---

## Waitlist Backend Patterns

### Backend Stacks (Next.js, Nuxt, Laravel)

**API Route Pattern:**

```
POST /api/waitlist
Body: { "email": "user@example.com" }

→ Validate email format (regex or built-in validator)
→ Read waitlist.json from disk (create if doesn't exist)
→ Check for duplicate email
→ Append { email, timestamp, source: "landing-page" }
→ Write back to waitlist.json
→ Return { success: true, message: "You're on the list!" }

Errors:
→ Invalid email: 400 { success: false, message: "Please enter a valid email." }
→ Duplicate: 200 { success: true, message: "You're already on the list!" }
→ Server error: 500 { success: false, message: "Something went wrong. Try again." }
```

**waitlist.json format:**
```json
{
  "entries": [
    {
      "email": "user@example.com",
      "timestamp": "2026-03-18T10:30:00Z",
      "source": "landing-page"
    }
  ]
}
```

The waitlist.json file should be in a non-public location:
- Next.js: project root `./waitlist.json` (outside `public/`)
- Nuxt: project root `./waitlist.json`
- Laravel: `storage/app/waitlist.json`

### Static Stacks (React + Vite)

**Formspree Pattern:**

```html
<form action="https://formspree.io/f/{your-form-id}" method="POST">
  <input type="email" name="email" required />
  <button type="submit">Join Waitlist</button>
</form>
```

- Handle submission via JavaScript fetch for better UX (show loading/success states).
- Add a code comment: `// Replace {your-form-id} with your Formspree form ID — create one free at formspree.io`
- Handle Formspree's response format for success/error states.

---

## Copywriting Guidelines

- **Headlines**: Lead with the benefit, not the feature. "Save 10 hours a week" > "Task management tool".
- **Subheadlines**: Be specific about who and what. "For freelancers who juggle too many clients" > "For everyone".
- **CTAs**: Action verb + outcome. "Get early access" > "Submit". "Join the waitlist" > "Sign up".
- **Feature descriptions**: Problem → solution format. "Stop losing track of invoices. Auto-track every payment in real time."
- **Tone**: Match the product. B2B SaaS = professional but warm. Dev tools = casual and direct. Consumer = friendly and energetic.
- **Never use**: "Revolutionize", "leverage", "synergy", "disrupt", "cutting-edge" (overused startup jargon).

# Launch Checklist

Run this before generating the handoff package. The site must not only look complete — it must be operationally ready to ship.

---

## 1. Search and Metadata

- [ ] Every page has a unique title tag (not "Home | Site Name" cloned across pages)
- [ ] Every page has a unique, useful meta description (150–160 chars)
- [ ] OG title, description, and image are defined (check `layout.tsx` or equivalent)
- [ ] Twitter card metadata defined
- [ ] Canonical URL handling in place (no duplicate content risk)
- [ ] Structured data present where appropriate (LocalBusiness, Organization, etc.)
- [ ] All important images have descriptive alt text (not empty, not "image.jpg")
- [ ] `sitemap.xml` is generating correctly (visit `/sitemap.xml`)
- [ ] `robots.txt` is correct (`/robots.txt` — no `Disallow: /` in production)

---

## 2. Conversion and Content

- [ ] Clear primary CTA visible above the fold on the homepage
- [ ] CTA is consistent and repeated across all key pages
- [ ] No placeholder copy remains (`[Business Name]`, `Lorem ipsum`, `TODO`, `PLACEHOLDER`)
- [ ] No invented testimonials, fake reviews, or made-up certifications
- [ ] Contact information is real and visible (phone, email, address, hours)
- [ ] WhatsApp link is wired (if injected) — test that `wa.me/[NUMBER]` opens correctly
- [ ] Contact form submits without error (test in dev)
- [ ] Booking/reservation link works (if applicable)
- [ ] Footer includes business name, key navigation links, and contact info

---

## 3. Accessibility and UX

- [ ] One H1 per page — no pages have multiple H1s
- [ ] Heading hierarchy is correct — no skipping H2 → H4
- [ ] Semantic landmarks in place: `<header>`, `<main>`, `<footer>`, `<nav>`
- [ ] Interactive elements are keyboard-navigable (tab through the page)
- [ ] Focus rings are visible (not `outline: none` without a replacement)
- [ ] Color contrast passes AA (4.5:1 for body text, 3:1 for large text)
- [ ] Images have alt text — decorative images have `alt=""`
- [ ] No horizontal scroll on mobile (375px viewport)
- [ ] Touch targets are at least 44×44px
- [ ] `prefers-reduced-motion` is respected for animations

---

## 4. Performance and Implementation

- [ ] No unnecessary client-side JS (prefer server/static rendering for marketing content)
- [ ] Images are optimized — use Next.js `<Image>` or equivalent, specify `width`/`height`
- [ ] No layout shift visible on load (set explicit dimensions on media)
- [ ] Google Fonts loaded via `next/font` or with `display=swap` (no FOIT)
- [ ] `next build` (or equivalent) passes without errors or warnings
- [ ] No broken internal links or dead routes
- [ ] No console errors in the browser
- [ ] Required environment variables are documented in `.env.example`

---

## 5. Launch Operations

- [ ] Analytics placeholder noted (GA4 measurement ID or Plausible domain to configure)
- [ ] Consent banner approach defined if analytics requires it (GDPR/PH data privacy consideration)
- [ ] Contact form submission endpoint configured or clearly marked as pending
  - Local: API route created and tested
  - External: Formspree/webhook endpoint documented
- [ ] WhatsApp number placeholder clearly flagged in HANDOFF.md if not provided
- [ ] `NEXT_PUBLIC_SITE_URL` or equivalent set for canonical and OG URL generation
- [ ] Favicon is present (`/public/favicon.ico` or via `app/icon.tsx`)
- [ ] Social preview image present (1200×630px OG image or dynamic via `/api/og`)
- [ ] Privacy policy and terms pages exist or are noted as needed
- [ ] Domain setup documented in DEPLOY.md

---

## Blocker vs. Polish

**Must fix before handoff (blockers):**
- Missing title/meta on any page
- Broken contact form
- Placeholder copy visible to users
- `next build` failing
- Broken navigation links
- WhatsApp link not working

**Medium priority (note in HANDOFF.md):**
- Missing OG image
- Analytics not yet configured
- No privacy policy page
- Lighthouse score 80–89 on any metric

**Optional polish (mention, don't block):**
- Additional page transitions
- Image optimization for LCP
- Schema markup enrichment
- Blog or news section

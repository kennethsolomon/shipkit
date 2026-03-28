# sk:website — Complete Guide

Build production-ready, client-deliverable websites from a brief, URL, or one sentence.

---

## What it does

`/sk:website` runs a full autonomous build pipeline:

1. Extracts business facts from a URL or plain text brief
2. Spawns 3 parallel research agents (strategy, copy, art direction)
3. Builds a complete multi-page site with real copy — no placeholders
4. Injects a WhatsApp floating CTA (auto-detected for PH/SEA local businesses)
5. Enforces Lighthouse 90+ on every page
6. Generates a client handoff package: `HANDOFF.md`, `DEPLOY.md`, `CONTENT-GUIDE.md`

---

## When to use it vs. sk:mvp

| | `/sk:website` | `/sk:mvp` |
|---|---|---|
| **Use when** | Client needs a real deliverable | Validating a product idea |
| **Copy** | Real, business-specific | Generic placeholders |
| **Data** | Real structure | Fake data |
| **Goal** | Launch-ready site | Working prototype |
| **Handoff** | Full client package | Technical docs only |

**Rule of thumb:** If someone is paying you for it, use `/sk:website`. If you're testing whether an idea is worth building, use `/sk:mvp`.

---

## Quick Start

### Fastest — paste a URL
```
/sk:website

https://maps.google.com/?q=Corner+Brew+BGC+Taguig

Goal: replace old site with something modern and bookable
CTA: Reserve a Spot
```

### One-liner
```
/sk:website

Corner Brew — specialty coffee shop in BGC, Taguig. CTA: Reserve a Spot
```

### Revision after build
```
/sk:website --revise

Changes the client wants:
1. Make the hero section warmer and more inviting
2. Add a gallery section to the Home page
3. Change the CTA from "Contact Us" to "Book a Table"
```

---

## Full Brief Format

For more control over the output:

```
/sk:website

**Business:** [name]
**Type:** [cafe / law firm / freelance designer / etc.]
**Location:** [city, region — required for local SEO]
**Goal:** [what success looks like]
**Audience:** [who visits or buys]
**Primary CTA:** [the one action you want]

**Pages needed:**
- Home
- About
- [Services / Menu / Work]
- Contact
- [FAQ / Gallery — optional]

**Tone:** [warm / premium / editorial / bold / minimal / etc.]
**Primary keyword:** [what people search to find this business]

**Real info to include:**
- Address: [if physical location]
- Phone: [for WhatsApp — format: +63XXXXXXXXXX]
- Hours: [e.g., Mon–Fri 7am–6pm]
- Services: [list what the business actually offers]
- Trust signals: [certifications, years open, anything real]

**Visual direction (optional):**
- Brand adjectives: [e.g., cozy, artisan, warm, minimal]
- Colors to use or avoid:
- Inspiration: [URL] for [what to borrow]

**Avoid:** [patterns you don't want]
```

---

## Prompt Examples by Business Type

### Cafe

```
/sk:website

Corner Brew — specialty coffee shop in BGC, Taguig, Philippines.

Goal: drive foot traffic and reservation inquiries.
Audience: young professionals and remote workers near BGC.
CTA: Reserve a Spot

Pages: Home, Menu, About, Find Us, Contact
Tone: warm, artisan, neighborhood — not corporate

Real info:
- Address: 5th Ave, BGC, Taguig
- Phone: +63917XXXXXXX (for WhatsApp)
- Hours: Mon–Fri 7am–7pm, Sat–Sun 8am–6pm
- Menu highlights: single-origin espresso, matcha, house-made croissants

Primary keyword: coffee shop BGC
```

---

### Restaurant

```
/sk:website

Luto — modern Filipino restaurant in Poblacion, Makati.

Goal: generate reservation bookings and private dining inquiries.
Audience: food-curious Metro Manila diners aged 25–45.
CTA: Book a Table

Pages: Home, Menu, About, Reservations, Contact
Tone: warm, editorial — modern with Filipino soul

Real info:
- Address: Poblacion, Makati
- Phone: +6325XXXXXXXX
- Hours: Tue–Sun 6pm–11pm, closed Monday
- Signature dish: kare-kare with bone marrow, lechon belly sisig

Primary keyword: modern Filipino restaurant Makati
```

---

### Law Firm

```
/sk:website

Reyes & Santos Law — criminal defense attorneys in Quezon City, Philippines.

Goal: generate consultation bookings from individuals facing criminal charges.
Audience: individuals and families dealing with criminal legal matters.
CTA: Schedule a Free Consultation

Pages: Home, Practice Areas, About Our Team, Contact, FAQ
Tone: calm, authoritative, trustworthy — not aggressive

Real info:
- Office: Quezon City, Metro Manila
- Phone: +63917XXXXXXX
- Practice areas: criminal defense, drug cases, cybercrime, white-collar
- Credentials: 15 years combined practice, IBP members

Primary keyword: criminal defense lawyer Quezon City
Avoid: stock courthouse imagery, aggressive language
```

---

### Dentist

```
/sk:website

BrightSmile Dental Clinic — family dentist in Tomas Morato, Quezon City.

Goal: drive appointment bookings.
Audience: families and working adults in QC seeking regular dental care.
CTA: Book an Appointment

Pages: Home, Services, About Us, Book Appointment, Contact
Tone: clean, warm, reassuring

Real info:
- Address: Tomas Morato Ave, Quezon City
- Phone: +63917XXXXXXX (for WhatsApp)
- Hours: Mon–Sat 9am–6pm
- Services: cleaning, whitening, braces, implants, pediatric dentistry
- Dentist: Dr. Maria Santos, DMD

Primary keyword: dentist Quezon City
```

---

### Freelance Designer

```
/sk:website

Jason Reyes — freelance UI/UX designer based in Manila, Philippines.
Available for remote work worldwide.

Goal: attract freelance product design contracts.
Audience: startup founders and product managers who need design help.
CTA: Hire Me

Pages: Home, Work, About, Contact
Tone: clean, minimal, modern — confident without being flashy

Primary keyword: freelance UI designer Manila
Inspiration: [URL] for the restrained editorial feel
Avoid: excessive animation, stock design imagery
```

---

### Home Services

```
/sk:website

Metro Aircon Services — aircon installation, cleaning, and repair in Metro Manila.

Goal: generate service inquiries and quote requests.
Audience: homeowners and property managers across NCR.
CTA: Get a Free Quote

Pages: Home, Services, About, Contact, FAQ
Tone: professional, dependable, direct

Real info:
- Service area: Metro Manila (NCR)
- Phone: +63917XXXXXXX (WhatsApp + calls)
- Services: aircon installation, cleaning, gas recharge, repair
- Availability: 7 days a week, emergency available

Primary keyword: aircon cleaning Metro Manila
```

---

### SaaS Product

```
/sk:website

Trackly — time tracking software for freelancers and agencies.

Goal: drive free trial signups.
Audience: freelancers and small agencies who overbill or underbill clients.
CTA: Start Free Trial

Pages: Home, Features, Pricing, About, Contact
Tone: clean, modern, product-led — no generic SaaS clichés

Real info:
- Pricing: Free (1 project), Pro $9/mo (unlimited), Team $29/mo
- Key features: automatic time tracking, client reports, invoice export
- Integrations: Notion, Linear, Slack

Primary keyword: time tracking software for freelancers
```

---

### Portfolio

```
/sk:website

Ana Cruz — brand identity designer based in Cebu, Philippines.
Works with startups and consumer brands across SEA.

Goal: attract brand identity projects from growing startups.
Audience: founders and marketing leads who need brand design.
CTA: View My Work / Hire Me

Pages: Home, Work, About, Contact
Tone: editorial, precise, a little playful

Primary keyword: brand identity designer Philippines
Inspiration: [URL] for clean project framing
```

---

## Understanding WhatsApp CTA

The skill auto-injects a floating WhatsApp button when:
- Business is a local type (cafe, restaurant, service, clinic, etc.)
- Location signals are in the Philippines, Singapore, Malaysia, Indonesia, Thailand, Vietnam, or Hong Kong

**If your phone number isn't in the brief**, a `[PHONE]` placeholder is used. Replace it in `app/layout.tsx`:

```tsx
// Find this in app/layout.tsx and replace [PHONE] with your number
// Format: country code + number, no + symbol
// Philippines: 639171234567 (63 + mobile number)
// Singapore: 6591234567

<WhatsAppButton phone="639171234567" />
```

**To disable WhatsApp CTA**, mention it in your brief:
```
Avoid: WhatsApp button (we use email for all inquiries)
```

**For Messenger instead of WhatsApp**, mention it:
```
Use Messenger CTA instead of WhatsApp (our Facebook page: @cornerbrew)
```

---

## Understanding the Handoff Package

After the build completes, 3 files appear at the project root:

### HANDOFF.md
What the client receives first. Contains:
- Summary of all pages built
- List of what still needs replacing (hero photo, WhatsApp number, etc.)
- How to edit content in plain terms

### DEPLOY.md
Step-by-step deployment guide:
- Vercel one-click deploy (free tier available)
- Netlify as alternative
- Required environment variables
- Domain setup
- Estimated monthly costs (usually just the domain: ~$12/year)

### CONTENT-GUIDE.md
Non-technical editing guide written for the client:
- No developer jargon
- Specific: "To change your opening hours, open `content/site.ts` and find `hours:`"
- Covers the most common edits: name, hours, contact, services, social links

---

## Revision Mode (`--revise`)

Use after the initial build when the client has feedback.

```
/sk:website --revise

Changes:
1. The hero feels too cold — make it warmer and more inviting
2. Add a before/after gallery to the About page
3. Change the CTA everywhere from "Contact Us" to "Book a Consultation"
4. The mobile nav doesn't close when you tap outside it
```

What it does:
- Reads current site state
- Classifies each change (copy / style / structure / feature)
- Applies targeted edits only — never rebuilds the whole site
- Re-runs quality checks to catch regressions
- Updates HANDOFF.md if structure changed

---

## Niche Guides

The skill loads an industry-specific reference when building your site. 15 are included:

| Business type | Reference | Best art direction |
|---|---|---|
| Cafe, coffee, bakery | `niche/cafe.md` | Warm Hospitality |
| Restaurant, dining | `niche/restaurant.md` | Warm Hospitality |
| Law firm, attorney | `niche/law-firm.md` | Restrained Editorial |
| Home services (plumbing, HVAC, etc.) | `niche/home-services.md` | Restrained Editorial |
| Dentist, dental clinic | `niche/dentist.md` | Restrained Editorial |
| Gym, yoga, fitness | `niche/gym.md` | Bold Brand-Forward |
| Real estate agent | `niche/real-estate.md` | Premium Product-Led |
| Accountant, bookkeeper | `niche/accountant.md` | Restrained Editorial |
| Med spa, aesthetics | `niche/med-spa.md` | Quiet Luxury |
| Wedding, bridal, events | `niche/wedding.md` | Quiet Luxury |
| Agency, studio, consultancy | `niche/agency.md` | Restrained Editorial or Bold |
| Portfolio, freelance | `niche/portfolio.md` | Varies by creator |
| Ecommerce, DTC products | `niche/ecommerce.md` | Premium Product-Led |
| SaaS, software | `niche/saas.md` | Premium Product-Led |
| Any local business (default) | `niche/local-business.md` | Restrained Editorial |

---

## Art Direction Reference

The skill picks one of 7 aesthetic directions based on business type + brief tone:

| Direction | Best for | Signals |
|---|---|---|
| Restrained Editorial | Law, architecture, premium consulting | Generous whitespace, strong typography, sparse palette |
| Premium Product-Led | SaaS, devices, DTC | Product-first framing, crisp hierarchy, controlled accent |
| Bold Brand-Forward | Agencies, challenger brands | Strong contrast, daring type scale, high visual recall |
| Warm Hospitality | Cafes, restaurants, boutique hotels | Tactile imagery, warm neutrals, editorial pacing |
| Sharp Technical | Developer tools, B2B platforms | Precise grid, low noise, strong information hierarchy |
| Playful Contemporary | Consumer apps, EdTech, lifestyle | Rounded forms, brighter palette, expressive motion |
| Quiet Luxury | Med spa, luxury retail, high-end hospitality | Restraint, material cues, elegant typography |

---

## Lighthouse Quality Gate

After the build, the skill enforces Lighthouse 90+ before generating the handoff package.

**If Playwright MCP is connected:**
- Runs Lighthouse on every page
- Fixes failing audits (image optimization, missing meta, contrast issues, etc.)
- Loops up to 3 times per page
- Reports remaining issues if still failing after 3 attempts

**If Playwright MCP is NOT connected:**
Runs a static pass instead:
- Unique title + meta description per page
- No duplicate H1s, no skipped heading levels
- All images have alt text
- Sitemap + robots.txt generated
- `next build` passes without errors

To connect Playwright MCP: enable `playwright@claude-plugins-official` in Claude Code settings under Plugins.

---

## Troubleshooting

**"The URL didn't load"**
→ The skill falls back to plain-text extraction. Describe the business manually.

**"WhatsApp button appears but I'm not in Philippines/SEA"**
→ Add `Avoid: WhatsApp button` to your brief, or edit `app/layout.tsx` to remove it.

**"The site has placeholder [PHONE] in the WhatsApp link"**
→ Open `app/layout.tsx`, find `phone="[PHONE]"`, replace with your number in E.164 format without `+` (e.g., `639171234567`).

**"I want to change the language from English to Filipino"**
→ Run `/sk:website --revise` and specify: "Translate all page copy to Filipino (Tagalog). Keep English for navigation and CTAs."

**"I need a page that wasn't in the original build"**
→ Run `/sk:website --revise` and specify: "Add a new Catering page with [details]."

---

## Related Commands

| Command | When to use |
|---|---|
| `/sk:website --revise` | Client has feedback on the initial build |
| `/sk:seo-audit` | After launch — audit an existing live site for SEO gaps |
| `/sk:frontend-design` | When you want to design UI for a feature (not a full site build) |
| `/sk:mvp` | When you're validating a product idea, not delivering to a client |
| `/sk:accessibility` | WCAG 2.1 audit after any frontend changes |

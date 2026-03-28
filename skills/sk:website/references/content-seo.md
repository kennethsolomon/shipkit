# Content & SEO Reference

Use when writing copy, metadata, or reviewing content for a website. Helps the site communicate clearly to humans and search engines without sounding generic, manipulative, or keyword-stuffed.

---

## Messaging Rules

- Start from the business, audience, and page goal — not from a template.
- Lead with concrete value, not vague brand language.
- Prefer simple claims the business can credibly support.
- Keep headings short and scannable — under 10 words where possible.
- Use CTAs that match the actual conversion step (not "Learn More" when you mean "Book a Table").
- Avoid filler: "innovative solutions", "next-level", "cutting-edge", "world-class", "passionate about".

**Good headline pattern:** [Who you help] + [specific outcome] + [where/context]
- "Hand-pulled espresso and house-made pastries in the heart of BGC"
- "Tax prep for freelancers and small businesses in Metro Manila"
- "Criminal defense attorneys serving Houston and surrounding counties"

**Bad headline pattern:** vague + buzzword + generic
- "Crafting memorable coffee experiences" — says nothing
- "Your trusted partner in financial success" — could be anyone
- "Excellence in legal representation" — no specifics

---

## SEO Rules

- Match the title tag and meta description to the page's actual search intent.
- One primary keyword or search theme per page is usually enough.
- Support the primary intent with natural secondary terms in headings, body copy, alt text, and internal links.
- Do not force exact-match keyword repetition — write for humans, let intent match naturally.
- Keep important marketing content in HTML (not JS-only rendered) for crawlability.

**Title tag formula:** [Primary keyword] | [Brand name]
- "Coffee Shop in BGC Taguig | Corner Brew"
- "Small Business Tax Accountant Austin TX | Davis & Co."

**Meta description formula:** [Audience problem or intent] + [service/offer] + [location/differentiator] + [CTA]
- "Looking for great coffee near BGC? Corner Brew serves specialty espresso, fresh pastries, and free WiFi on 26th Street. Visit us today."
- 150–160 characters. Every page gets a unique one.

---

## Local SEO

Use when the business serves a geographic area — cafes, restaurants, law firms, clinics, contractors, etc.

**Always confirm these inputs:**
- Primary service and secondary services
- City, metro area, or specific neighborhood
- Secondary service areas (if any)
- Contact phone number
- Street address (if physical location)
- Business hours
- Appointment/booking CTA

**Content placement:**
- Mention service + city in the hero headline naturally — not as a keyword dump
- Add a short service-area statement in the footer or about section ("Serving Quezon City and nearby areas")
- Include trust sections that fit: process, years in business, certifications, FAQs — only if real
- Use FAQ sections for genuine customer objections, not SEO filler

**Local metadata checklist:**
- Title tag: [Service] in [City] | [Brand] (e.g., "Cafe in Tomas Morato | Kape Republic")
- Meta description: mentions the audience, service, and location in plain language
- H1: reflects the page's local search intent
- Footer: include full address, phone, and hours where applicable
- Structured data: `LocalBusiness` (or a more specific subtype)

**Structured data — LocalBusiness:**
```json
{
  "@context": "https://schema.org",
  "@type": "[BusinessType]",
  "name": "[Business Name]",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "[Street]",
    "addressLocality": "[City]",
    "addressRegion": "[Region]",
    "addressCountry": "[Country Code]"
  },
  "telephone": "[Phone]",
  "openingHours": ["Mo-Fr 08:00-18:00", "Sa 09:00-17:00"],
  "url": "[Site URL]"
}
```

Use `CafeOrCoffeeShop` for cafes, `Restaurant` for restaurants, `LegalService` for law firms, `Dentist` for dental, `MedicalBusiness` for clinics, `LocalBusiness` as fallback.

**Avoid:**
- Thin city pages with near-duplicate copy
- Fake office locations
- Invented reviews or star ratings
- Keyword repetition that makes copy sound mechanical
- Separate "city pages" unless each one is genuinely different

---

## Page-Level SEO Checklist

For every page generated, verify:

- [ ] Unique `<title>` tag (not duplicated from another page)
- [ ] Unique meta description (150–160 characters)
- [ ] One H1 that matches the page's primary intent
- [ ] Supporting H2s and H3s that structure the content logically
- [ ] OG `title`, `description`, and `image` defined
- [ ] Twitter card metadata defined
- [ ] Canonical URL set (no duplicate content)
- [ ] Structured data where applicable
- [ ] All important text is in HTML (not JS-rendered)
- [ ] Internal links to related pages (e.g., Services → Contact)

---

## Internal Linking Strategy

- Home → Services, About, Contact (primary CTAs in nav and hero)
- Services → Contact (each service should have a CTA to book/inquire)
- About → Services, Contact (trust-building page leads to action)
- Blog/FAQ posts → relevant service pages (if applicable)
- Footer: always links to all top-level pages + legal pages

---

## Content Anti-Patterns

Never produce:
- "Lorem ipsum" or any placeholder body copy
- Generic `[Your Headline Here]` style template text
- Invented testimonials, star ratings, or review counts
- Made-up certifications, awards, or rankings
- Fake "as seen in" media logos
- Invented pricing or "starting from" numbers without real data
- Claims like "best in [city]" without real proof

Always prefer:
- Specific over vague ("3 espresso origins rotating weekly" > "quality coffee")
- Verifiable over invented ("Open since 2019" vs. "20 years of experience" when unknown)
- Direct over clever ("Book a table" vs. "Experience our hospitality")

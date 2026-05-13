# Website Brief Template

Use this when prompting `/sk:website`. Fill in what you have — the skill will infer the rest.

The fastest way to start: paste a Google Maps URL or existing website URL. The skill extracts everything automatically.

---

## Minimal brief (enough to start)

```
/sk:website

[Business name] — [type of business] in [city/location].
Goal: [what the site should achieve — bookings, inquiries, orders, etc.]
CTA: [primary action — "Book a Table", "Get a Quote", "Contact Us"]
```

**Example:**
```
/sk:website

Corner Brew — specialty coffee shop in BGC, Taguig.
Goal: drive foot traffic and reservation inquiries.
CTA: Reserve a Spot
```

---

## Full brief (more control)

```
/sk:website

**Business:** [name]
**Type:** [cafe / law firm / freelance designer / etc.]
**Location:** [city, region — required for local SEO]
**Goal:** [what success looks like for this site]
**Audience:** [who visits this business / who buys]
**Primary CTA:** [the one action you want visitors to take]

**Pages needed:**
- Home
- About
- [Services / Menu / Work]
- Contact
- [FAQ / Gallery / Blog — optional]

**Tone:** [warm and neighborhood / premium and editorial / bold and modern / etc.]
**Primary keyword:** [what people search to find this business]

**Real info to include:**
- Address: [full address if applicable]
- Phone: [for WhatsApp CTA — format: +63XXXXXXXXXX]
- Hours: [e.g., Mon–Fri 7am–6pm, Sat–Sun 8am–5pm]
- Services: [list what the business actually offers]
- Trust signals: [certifications, years open, anything real]

**Visual direction (optional):**
- Brand adjectives: [e.g., cozy, artisan, warm, minimal]
- Colors to use or avoid:
- Inspiration: [URL] for [what to borrow from it]

**Avoid:**
- [patterns or styles you don't want]
```

---

## URL-first brief (fastest)

Just paste a URL — the skill fetches and extracts everything:

```
/sk:website

[Google Maps URL or existing website URL]

Goal: [what to improve or achieve]
CTA: [primary action]
```

**Example:**
```
/sk:website

https://maps.google.com/?q=Corner+Brew+BGC

Goal: replace the outdated site with something modern and bookable.
CTA: Reserve a Table
```

---

## Revision brief

Use `/sk:website --revise` when you have an existing build and client feedback:

```
/sk:website --revise

Changes from the client:
1. [Change 1 — e.g., "make the hero image warmer and more inviting"]
2. [Change 2 — e.g., "add a gallery section on the Home page"]
3. [Change 3 — e.g., "change the CTA from 'Contact Us' to 'Book a Table'"]
```

---

## Business type examples

| Business | CTA | Key pages | Niche guide |
|---|---|---|---|
| Specialty cafe | Visit Us / Reserve a Spot | Home, Menu, About, Find Us | cafe |
| Restaurant | Book a Table / Order Online | Home, Menu, About, Reservations | restaurant |
| Law firm | Schedule a Consultation | Home, Practice Areas, About, Contact | law-firm |
| Dentist | Book an Appointment | Home, Services, About Us, Contact | dentist |
| Yoga studio | Try a Free Class | Home, Classes, About, Schedule, Contact | gym |
| Accountant | Get a Free Consultation | Home, Services, About, Contact, FAQ | accountant |
| Freelance designer | View My Work / Hire Me | Home, Work, About, Contact | portfolio |
| Real estate agent | Search Listings / Get a Valuation | Home, Listings, About, Contact | real-estate |

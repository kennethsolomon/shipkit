---
description: Build a complete, client-deliverable multi-page marketing website from a brief, URL, or one sentence. Auto-builds from intake to handoff. Use --revise for client feedback iterations.
---

Build a production-ready multi-page marketing website for delivery to a client. This is NOT a prototype or MVP — it outputs real copy, real structure, and a full client handoff package (HANDOFF.md, DEPLOY.md, CONTENT-GUIDE.md).

Read and follow `skills/sk:website/SKILL.md` exactly.

## Quick start

**From a URL (fastest):**
```
/sk:website
https://maps.google.com/?q=Your+Business

Goal: [what to improve]
CTA: [primary action]
```

**From a one-liner:**
```
/sk:website
[Business name] — [type] in [city]. Goal: [goal]. CTA: [action].
```

**With full brief:**
See `skills/sk:website/references/brief-template.md` for the complete brief format.

**For revisions after initial build:**
```
/sk:website --revise
Changes: [list changes in plain language]
```

## What gets built

- Multi-page site (Home, About, Services/Menu, Contact + niche extras)
- Real copy — no Lorem ipsum, no `[placeholder]` headlines
- SEO metadata on every page (title, description, OG, structured data)
- WhatsApp floating CTA (auto-injected for local businesses in PH/SEA)
- Lighthouse 90+ quality enforcement loop
- Client handoff package (HANDOFF.md, DEPLOY.md, CONTENT-GUIDE.md)

## Reference files

All references live in `skills/sk:website/references/`:
- `brief-template.md` — intake format and examples
- `art-direction.md` — 7 aesthetic directions
- `content-seo.md` — messaging + local SEO rules
- `launch-checklist.md` — prelaunch audit
- `whatsapp-cta.md` — WhatsApp/Messenger implementation
- `handoff-template.md` — 3 client deliverable templates
- `niche/[type].md` — 15 industry-specific guides

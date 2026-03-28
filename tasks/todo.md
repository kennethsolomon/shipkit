# TODO — 2026-03-28 — sk:website Client Website Builder

## Goal

Build `/sk:website` — a new ShipKit skill that generates a complete, client-deliverable multi-page marketing website from a brief, URL, or one sentence. Ports the best of website-studio into shipkit, making website-studio deprecated.

## Features

1. Brief extraction from URL (Google Maps, existing site, plain text)
2. Real copy generation — no placeholders
3. Client handoff package (HANDOFF.md, DEPLOY.md, CONTENT-GUIDE.md)
4. WhatsApp/Messenger floating CTA (SEA-first, auto-detect)
5. Lighthouse enforcement loop (90+ on all pages)
6. Parallel agent build (strategy + copy + art direction simultaneously)
7. Revision mode (`--revise` flag)

## Scope — 23 files

```
skills/sk:website/
  SKILL.md
  references/
    niche/
      cafe.md
      restaurant.md
      law-firm.md
      local-business.md
      saas.md
      agency.md
      portfolio.md
      accountant.md
      gym.md
      dentist.md
      real-estate.md
      med-spa.md
      home-services.md
      wedding.md
      ecommerce.md
    art-direction.md
    content-seo.md
    launch-checklist.md
    brief-template.md
    whatsapp-cta.md
    handoff-template.md
commands/sk/website.md
```

---

## Checklist

### Wave 1 — Core skill + shared references (parallel)

- [ ] Create `skills/sk:website/SKILL.md` — full 8-step workflow
- [ ] Create `skills/sk:website/references/art-direction.md` — 7 aesthetic directions
- [ ] Create `skills/sk:website/references/content-seo.md` — messaging + local SEO
- [ ] Create `skills/sk:website/references/launch-checklist.md` — prelaunch audit
- [ ] Create `skills/sk:website/references/brief-template.md` — intake template

### Wave 2 — New reference files (parallel)

- [ ] Create `skills/sk:website/references/whatsapp-cta.md` — implementation guide
- [ ] Create `skills/sk:website/references/handoff-template.md` — 3-file template

### Wave 3 — Niche guides batch A (parallel)

- [ ] Create `skills/sk:website/references/niche/cafe.md`
- [ ] Create `skills/sk:website/references/niche/restaurant.md`
- [ ] Create `skills/sk:website/references/niche/law-firm.md`
- [ ] Create `skills/sk:website/references/niche/local-business.md`
- [ ] Create `skills/sk:website/references/niche/saas.md`
- [ ] Create `skills/sk:website/references/niche/agency.md`
- [ ] Create `skills/sk:website/references/niche/portfolio.md`
- [ ] Create `skills/sk:website/references/niche/accountant.md`

### Wave 4 — Niche guides batch B (parallel)

- [ ] Create `skills/sk:website/references/niche/gym.md`
- [ ] Create `skills/sk:website/references/niche/dentist.md`
- [ ] Create `skills/sk:website/references/niche/real-estate.md`
- [ ] Create `skills/sk:website/references/niche/med-spa.md`
- [ ] Create `skills/sk:website/references/niche/home-services.md`
- [ ] Create `skills/sk:website/references/niche/wedding.md`
- [ ] Create `skills/sk:website/references/niche/ecommerce.md`

### Wave 5 — Command + verification (sequential)

- [ ] Create `commands/sk/website.md` — slash command
- [ ] Run `bash tests/verify-workflow.sh` — must still pass (no existing files modified)

---

## Verification

```bash
bash tests/verify-workflow.sh
```

Expected: all existing assertions pass (no regressions). New skill files are purely additive.

## Acceptance Criteria

- [ ] `skills/sk:website/SKILL.md` exists with all 7 features
- [ ] 15 niche reference files exist under `references/niche/`
- [ ] `references/whatsapp-cta.md` includes Next.js/Tailwind implementation code
- [ ] `references/handoff-template.md` includes all 3 client files (HANDOFF.md, DEPLOY.md, CONTENT-GUIDE.md)
- [ ] `commands/sk/website.md` exists
- [ ] `bash tests/verify-workflow.sh` exits 0 (no regressions)

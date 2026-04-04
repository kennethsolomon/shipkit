# Findings — 2026-04-04 — Study App V1: AI-Powered Spaced Repetition Platform

## Problem Statement

Build a responsive PWA web app for students that turns class material (topic or PDF) into a structured study system with 5 card formats, then helps users retain knowledge through adaptive spaced repetition review. AI generates draft decks that users review before publishing. Sharing creates independent copies via link or class code.

## Key Decisions Made

1. **Next.js 15 full-stack** — single codebase, single Vercel deployment, free tier hosting
2. **Supabase as unified backend** — consolidates database (PostgreSQL), auth, and file storage into one free-tier service
3. **OpenRouter free model** — nvidia/nemotron-3-super-120b-a12b:free via OpenAI-compatible SDK for AI card generation (zero cost)
4. **Prisma ORM** — type-safe database access, migrations, works with Supabase PostgreSQL
5. **SM-2 spaced repetition** — proven algorithm, SQL-native queries for scheduling
6. **Copy-based sharing** — no live sync, simpler architecture
7. **PWA with @serwist/next** — installable, offline review for recent decks

## Chosen Approach — Next.js + Supabase + OpenRouter (Zero-Cost Stack)

### Rationale
- **Vercel free tier** — zero hosting cost for initial launch
- **Supabase free tier** — 500MB DB, 1GB storage, 50K MAU auth
- **OpenRouter free model** — no AI generation costs
- **Single codebase** — Next.js App Router handles both UI and API routes
- **Supabase consolidation** — replaces 3 separate services (Auth.js + Vercel Blob + standalone Postgres) with one

### Tech Stack

| Layer | Choice |
|-------|--------|
| Framework | Next.js 15 (App Router) + React 19 + TypeScript |
| Styling | Tailwind CSS + shadcn/ui |
| Database | Supabase PostgreSQL via Prisma ORM |
| Auth | Supabase Auth (email/password + Google OAuth) |
| AI | OpenRouter API (nvidia/nemotron-3-super-120b-a12b:free) via OpenAI SDK |
| File Storage | Supabase Storage (PDFs) |
| PWA | @serwist/next (Workbox-based service worker) |
| Hosting | Vercel (free tier) |

### Architecture Notes
- Server Components for data fetching, Client Components for interactive study UI
- API routes for AI generation (streaming responses to review queue)
- Prisma for migrations and type-safe queries
- Supabase Auth middleware for protected routes
- Service worker caches recent decks for offline review

## Requirements Checklist

### Auth & Onboarding
1. [ ] Email/password sign up and log in (Supabase Auth)
2. [ ] Google OAuth sign in (Supabase Auth)
3. [ ] Onboarding flow: choose subjects/goals, then create first deck

### Deck Creation
4. [ ] Create deck from topic (AI-generated)
5. [ ] Create deck from PDF upload (AI-generated)
6. [ ] Create deck manually (hand-made cards)
7. [ ] Deck settings: difficulty, card count, question type mix
8. [ ] 5 card types: flashcard, MCQ, identification, true/false, cloze

### AI Draft Review
9. [ ] AI-generated cards enter review queue before publishing
10. [ ] Review queue actions: accept, edit, regenerate, remove, change type
11. [ ] Source-backed generation: cards tied to PDF/source chunks

### Study Modes
12. [ ] Learn/Review mode driven by SM-2 spaced repetition
13. [ ] Quick Quiz mode with mixed question types
14. [ ] Test mode with score-based self-check
15. [ ] Per-card review scheduling (ease, interval, next_review_at)
16. [ ] Session results: score, weak concepts, due tomorrow, retry misses

### Smart Features
17. [ ] Weak spots: detect repeatedly missed cards, surface focus session
18. [ ] Mistake notebook: auto-collect missed questions
19. [ ] Deck health score: flag ambiguous, duplicate, too-easy AI cards
20. [ ] Study streak + weekly goal tracking

### Sharing
21. [ ] Share deck by link (generates URL)
22. [ ] Share deck by class code (short code)
23. [ ] Recipient imports a personal copy (not live-synced)

### Cross-Device & PWA
24. [ ] Responsive design: phone, tablet, laptop
25. [ ] PWA: installable, service worker
26. [ ] Offline review for recent decks (degraded mode)
27. [ ] Account-based cloud sync across devices

### Tech Stack
28. [ ] Next.js 15 (App Router) + React 19 + TypeScript
29. [ ] Tailwind CSS + shadcn/ui
30. [ ] Supabase PostgreSQL via Prisma ORM
31. [ ] Supabase Auth (email/password + Google OAuth)
32. [ ] OpenRouter API (nvidia/nemotron-3-super-120b-a12b:free) via OpenAI SDK
33. [ ] Supabase Storage for PDF uploads
34. [ ] @serwist/next for PWA/service worker
35. [ ] Deploy on Vercel (free tier)

### Screens (9)
36. [ ] Dashboard/Home
37. [ ] Deck Library
38. [ ] Deck Detail
39. [ ] Create Deck
40. [ ] AI Review Queue
41. [ ] Study Session
42. [ ] Session Results
43. [ ] Shared Deck Import
44. [ ] Profile/Settings

## Open Questions

- **PDF size limit** — practical cap TBD during implementation (likely 10-20MB per file, 50 pages max for AI processing)
- **Max cards per deck** — TBD based on UI performance testing (likely 500-1000)
- **OpenRouter rate limits** — free model may have request limits; need fallback UX for rate-limited users

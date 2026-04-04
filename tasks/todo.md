# TODO — 2026-04-04 — Study App V1: AI-Powered Spaced Repetition Platform

## Goal

Build a zero-cost, responsive PWA study app with Next.js 15 + Supabase + OpenRouter. Students create decks from topics/PDFs via AI (with review queue), study with SM-2 spaced repetition, and share via link/class code.

## Constraints

- PDF upload cap: 20MB, 50 pages max (text-based PDFs only, no OCR)
- Max 500 cards per deck
- Offline mode: read-only (cached recent decks for review, no offline writes)
- SM-2 parameters: quality scale 0-5, initial ease_factor 2.5, initial interval 1 day, minimum ease 1.3
- Free tiers only: Vercel, Supabase (500MB DB, 1GB storage, 50K MAU), OpenRouter free model

---

### Milestone 1: Project Scaffolding & Infrastructure

#### Wave 1 (parallel)
- [ ] Initialize Next.js 15 project (App Router, TypeScript, Tailwind CSS, src/ directory)
- [ ] Set up Supabase project: create database, enable auth providers (email + Google), create storage bucket "pdfs" (20MB max file size)
- [ ] Install core dependencies: prisma, @supabase/supabase-js, @supabase/ssr, openai (for OpenRouter), @serwist/next, shadcn/ui

#### Wave 2 (depends on Wave 1)
- [ ] Configure Prisma with Supabase PostgreSQL connection (use DIRECT_URL for migrations, DATABASE_URL with pgbouncer for runtime)
- [ ] Configure Supabase Auth middleware for Next.js (protect all routes except /auth/*, /share/*)
- [ ] Configure @serwist/next: manifest.json (name, icons, theme_color), service worker with cache-first for static assets + stale-while-revalidate for API
- [ ] Set up OpenRouter client: OpenAI SDK with baseURL=https://openrouter.ai/api/v1, model=nvidia/nemotron-3-super-120b-a12b:free
- [ ] Configure shadcn/ui: install Button, Card, Input, Dialog, Sheet, Tabs, Badge, Avatar, Progress, Skeleton, Select, Form, Label, Textarea
- [ ] Create shared layout: responsive shell with mobile bottom nav (Home, Library, Create, Profile) + desktop sidebar

### Milestone 2: Database Schema

#### Wave 3 (depends on Wave 2)
- [ ] Create Prisma schema: User model (id UUID, email, display_name, avatar_url, preferences Json, streak_count Int default 0, weekly_goal Int default 5, streak_updated_at DateTime?, created_at)
- [ ] Create Prisma schema: Deck model (id UUID, owner_id FK→User, title, subject, description?, source_type enum[TOPIC/PDF/MANUAL], card_count Int default 0, is_shared Boolean default false, created_at, updated_at)
- [ ] Create Prisma schema: Card model (id UUID, deck_id FK→Deck, type enum[FLASHCARD/MCQ/IDENTIFICATION/TRUE_FALSE/CLOZE], prompt, answer, explanation?, options Json?, cloze_text?, source_chunk_id?, position Int, is_draft Boolean default true, created_at)
- [ ] Create Prisma schema: SourceDocument model (id UUID, deck_id FK→Deck, filename, mime_type, storage_path, extracted_text, chunks Json, uploaded_at)
- [ ] Create Prisma schema: StudySession model (id UUID, user_id FK→User, deck_id FK→Deck, mode enum[LEARN/QUIZ/TEST], total_cards Int, correct_count Int default 0, duration_seconds Int default 0, completed_at DateTime?, created_at)
- [ ] Create Prisma schema: SessionAnswer model (id UUID, session_id FK→StudySession, card_id FK→Card, is_correct Boolean, confidence Int?, response_time_ms Int?, created_at)
- [ ] Create Prisma schema: ReviewSchedule model (id UUID, user_id FK→User, card_id FK→Card, ease_factor Float default 2.5, interval_days Int default 0, repetitions Int default 0, next_review_at DateTime, last_reviewed_at DateTime?) + composite index on (user_id, next_review_at)
- [ ] Create Prisma schema: ShareArtifact model (id UUID, deck_id FK→Deck, creator_id FK→User, share_type enum[LINK/CODE], code String @unique, import_count Int default 0, expires_at DateTime?, created_at)
- [ ] Create Supabase database trigger: on auth.users INSERT → create matching public.User row (sync Supabase Auth identity with Prisma User model)
- [ ] Run prisma migrate dev, verify all tables + trigger created in Supabase dashboard

### Milestone 3: Auth & Onboarding

#### Wave 4 (depends on Wave 3)
- [ ] Create sign-up page (/auth/signup) — email/password form + Google OAuth button, redirects to /onboarding on success
- [ ] Create sign-in page (/auth/login) — email/password form + Google OAuth button, redirects to / on success
- [ ] Create auth callback route (/auth/callback) for OAuth redirect handling
- [ ] Implement Supabase Auth middleware: redirect unauthenticated users to /auth/login, skip /auth/* and /share/* routes
- [ ] Create onboarding page (/onboarding) — choose subjects/goals (multi-select from predefined list + custom), stored in User.preferences JSON
- [ ] Auto-redirect: new users (no preferences set) → /onboarding; completed onboarding → /decks/new

### Milestone 4: Deck CRUD & Card Types

#### Wave 5 (parallel — depends on Wave 4)
- [ ] Create Deck Library page (/decks) — grid/list of user's decks with search by title, filter by subject, sort by date/last studied
- [ ] Create Deck Detail page (/decks/[id]) — card list with type badges, deck stats (total cards, mastery %, last studied, health score), action buttons (Study, Share, Edit, Delete)
- [ ] Create Manual Deck Builder (/decks/new?mode=manual) — deck title/subject form, then add cards with type selector

#### Wave 6 (depends on Wave 5)
- [ ] Implement 5 card editor components: FlashcardEditor (front/back), McqEditor (prompt + 2-6 options, mark correct), IdentificationEditor (term/definition), TrueFalseEditor (statement + correct answer), ClozeEditor (text with {{blanks}})
- [ ] Implement 5 card study renderers: FlashcardStudy (tap to flip), McqStudy (select option), IdentificationStudy (type answer), TrueFalseStudy (tap true/false), ClozeStudy (fill blank)
- [ ] Card CRUD server actions: create card, update card, delete card, reorder cards (update position)
- [ ] Card validation: MCQ requires 2-6 options with exactly 1 correct; cloze requires at least one {{blank}}; all types require non-empty prompt + answer
- [ ] Implement is_draft → published transition: "Publish Deck" button sets all is_draft=false cards and makes deck study-ready; unpublished cards are excluded from study modes

### Milestone 5: AI Generation

#### Wave 7 (parallel — depends on Wave 4)
- [ ] Create deck creation entry page (/decks/new) — three cards: "From Topic", "Upload PDF", "Build Manually"
- [ ] Create topic generation API route (POST /api/generate/topic) — accepts {topic, difficulty, card_count (max 50), type_mix}; streams JSON cards from OpenRouter; saves as is_draft=true cards
- [ ] Create PDF generation flow: upload PDF to Supabase Storage (enforce 20MB/50 page limit), extract text via pdf-parse, chunk into ~500-word segments, create SourceDocument, generate cards from chunks via OpenRouter with source_chunk_id references
- [ ] Create AI Review Queue page (/decks/[id]/review) — shows is_draft=true cards one by one; actions: Accept (set is_draft=false), Edit (inline edit + accept), Regenerate (call /api/generate/regenerate with source context), Remove (delete card), Change Type (convert to different card type)
- [ ] Create regenerate API route (POST /api/generate/regenerate) — accepts {card_id, source_chunk_id?, new_type?}; generates replacement card; auto-saves as draft
- [ ] "Publish All" action on review queue: set remaining is_draft=true cards to is_draft=false, update deck.card_count, redirect to deck detail

### Milestone 6: Study Engine

#### Wave 8 (depends on Wave 6)
- [ ] Implement SM-2 algorithm as pure function: sm2(quality: 0-5, prevEase: float, prevInterval: int, prevReps: int) → {ease: float, interval: int, reps: int}. Rules: quality<3 resets reps/interval to 0; ease = max(1.3, prevEase + 0.1 - (5-quality) * (0.08 + (5-quality) * 0.02)); interval: rep0=1day, rep1=6days, rep2+=round(prevInterval*ease)
- [ ] Create Learn/Review mode: fetch cards WHERE (next_review_at <= NOW() OR ReviewSchedule not exists) AND is_draft=false, ordered by next_review_at ASC, limit 20 per session
- [ ] Create Quick Quiz mode: fetch random 20 cards (is_draft=false) from deck, mixed types, no spaced repetition weighting
- [ ] Create Test mode: fetch ALL cards (is_draft=false) from deck in order, score-only, no immediate feedback per card

#### Wave 9 (depends on Wave 8)
- [ ] Create Study Session page (/decks/[id]/study) — mode selector (Learn, Quiz, Test), card presentation using type-specific renderers, quality rating after each answer (Learn mode: Again/Hard/Good/Easy → quality 1/2/3/5)
- [ ] Create Session Results page (/decks/[id]/study/results/[sessionId]) — score (correct/total as % and fraction), list of weak cards (incorrect answers), count of cards due tomorrow, "Retry Misses" button (starts new session with only missed cards)
- [ ] Record SessionAnswer per card: is_correct, confidence (self-rated), response_time_ms
- [ ] Auto-create ReviewSchedule on first study: when a card has no ReviewSchedule for this user, create one with defaults (ease=2.5, interval=0, reps=0, next_review_at=NOW())
- [ ] Update ReviewSchedule after each answer in Learn mode using SM-2 function

### Milestone 7: Smart Features

#### Wave 10 (parallel — depends on Wave 9)
- [ ] Weak spots: query cards with ease_factor < 2.0 OR (incorrect answers / total answers) > 0.5 in last 30 days; show "Focus on Weak Areas" button on dashboard and deck detail; starts Learn session filtered to weak cards only
- [ ] Mistake notebook: query SessionAnswer WHERE is_correct=false in last 7 days, grouped by card; show as virtual "Mistakes" deck on dashboard; tapping starts a review session with those cards
- [ ] Deck health score: analyze deck cards for — duplicate prompts (Levenshtein similarity > 0.8), too-short answers (< 10 chars for flashcard/identification), missing explanations, MCQ with < 3 options; score = 100 - (issues * 10), show as badge on deck detail (Good/Fair/Needs Review)
- [ ] Study streak: on each study session completion, if streak_updated_at is not today, increment streak_count and set streak_updated_at=today; if streak_updated_at is before yesterday, reset to 1. Weekly goal: count sessions this week vs weekly_goal target; show progress bar on dashboard

### Milestone 8: Sharing

#### Wave 11 (depends on Wave 5)
- [ ] Share actions on deck detail: "Copy Link" generates UUID-based URL (/share/[code]), "Generate Class Code" creates 6-char alphanumeric code; both stored as ShareArtifact
- [ ] Create public share import page (/share/[code]) — shows deck preview (title, subject, card count, creator name) without auth; "Import to My Library" button requires auth (redirect to login then back)
- [ ] Implement deck deep-copy: clone Deck (new owner_id) + clone all non-draft Cards (new deck_id, reset source_chunk_id); increment ShareArtifact.import_count; redirect to new deck detail

### Milestone 9: Dashboard & Polish

#### Wave 12 (depends on Wave 10, Wave 11)
- [ ] Create Dashboard/Home page (/) — due reviews count with "Start Review" button, "Continue Last Deck" card, streak flame + count, weekly goal progress bar (X/Y sessions), quick actions (Create Deck, Weak Spots, Mistake Notebook)
- [ ] Create Profile/Settings page (/settings) — edit display_name, change password (Supabase Auth), manage subjects/preferences, set weekly_goal target, sign out

#### Wave 13 (depends on Wave 12)
- [ ] Responsive design pass: verify all 9 screens at 375px (mobile), 768px (tablet), 1280px (desktop); fix any layout breaks
- [ ] Offline support: service worker caches last 5 studied decks + their cards as JSON in Cache Storage; study session works read-only offline; show "Offline — answers will sync when online" banner; on reconnect, POST queued quality ratings
- [ ] PWA polish: 512px app icon, splash screen, theme_color in manifest, verify installability in Chrome/Safari
- [ ] Onboarding UX: after first deck creation + publish, show "Ready to study!" prompt that starts first study session

---

## Verification

```bash
# Build passes
npm run build

# Type check passes
npx tsc --noEmit

# Prisma schema valid + migrations applied
npx prisma validate && npx prisma migrate status

# All tests pass (once written)
npm test

# PWA installable (check via Lighthouse in Chrome DevTools on Vercel preview)
```

## Acceptance Criteria

- [ ] Sign up with email/password creates account and redirects to onboarding
- [ ] Sign in with Google OAuth creates account and syncs to Prisma User table via trigger
- [ ] Onboarding saves subject preferences and redirects to deck creation
- [ ] Manual deck builder: create deck with 10 cards across all 5 types, all save correctly
- [ ] Topic AI generation: entering "Biology cell structure" with 10 cards produces 10 draft cards in review queue within 30 seconds
- [ ] PDF AI generation: uploading a 5-page PDF (< 20MB) produces draft cards tied to source chunks
- [ ] Review queue: accept/edit/regenerate/remove/change-type all work; "Publish All" transitions deck to study-ready
- [ ] SM-2 correctness: quality=3 on a new card → ease=2.5, interval=1, reps=1; quality=3 again → interval=6; quality=0 → resets to reps=0, interval=1
- [ ] Learn mode shows only cards with next_review_at <= now; completing updates schedule per SM-2
- [ ] Quick Quiz presents random cards without spaced repetition; Test mode shows all cards with end-of-test scoring
- [ ] Session results display: score as X/Y (Z%), list of missed cards, tomorrow's due count, retry button works
- [ ] Weak spots: cards with ease < 2.0 appear in "Focus on Weak Areas" session
- [ ] Mistake notebook: shows cards answered incorrectly in last 7 days
- [ ] Deck health: deck with 3 duplicate prompts scores < 80
- [ ] Streak increments daily on study; resets if a day is skipped
- [ ] Share link: copy URL, open in incognito, preview shows deck info, import after login creates independent copy
- [ ] Class code: 6-char code resolves to same deck; import works
- [ ] Responsive: all screens usable at 375px width without horizontal scroll
- [ ] PWA: passes Lighthouse installability check; app icon and name show in install prompt
- [ ] Offline: with network disabled, last studied deck opens and cards display; "offline" banner visible
- [ ] Deployed on Vercel free tier with Supabase free tier backend

## Risks / Unknowns

- **OpenRouter rate limits:** free model may throttle under load; UX shows "AI is busy, try again in 30s" with retry button
- **PDF text extraction:** pdf-parse handles text-based PDFs only; scanned/image PDFs return empty text — show "Could not extract text from this PDF" error
- **Supabase free tier limits:** 500MB DB, 1GB storage, 50K MAU — add dashboard warning at 80% usage
- **Prisma ↔ Supabase Auth sync:** database trigger keeps User rows in sync; if trigger fails, auth works but profile is missing — add fallback to create User on first authenticated request
- **Offline sync:** V1 uses read-only offline (cached decks for review); quality ratings from offline sessions are queued and POSTed on reconnect; if conflict, server state wins (last-write-wins)

# Spec: Study App V1 — AI-Powered Spaced Repetition Study Platform

## Metadata
- Interview rounds: 0 (pre-filled — input exceeded clarity threshold)
- Final ambiguity: 14.7%
- Status: PASSED
- Generated: 2026-04-04

## Goal
Build a responsive PWA web app that lets students turn class material (topic or PDF) into a structured study system with 5 card formats, then retain it through spaced repetition. AI generates draft decks that users review before publishing. Sharing creates independent copies via link or class code.

## Constraints
- V1 is a responsive PWA, not a native mobile app
- Account-based cloud sync (no local-only mode for primary data)
- AI-generated cards always enter a review/edit queue before becoming study-ready
- Sharing is copy-based — no live sync between original and imported decks
- 5 card types only: flashcard, multiple choice, identification, true/false, cloze
- Student-first UX — no teacher/admin dashboards in V1
- Spaced repetition is the primary study engine; quiz and test modes are secondary
- Offline support limited to recent decks with degraded functionality

## Non-Goals (explicitly excluded)
- Live collaborative editing of decks
- Teacher dashboards, assignment tracking, or grading
- Class role permissions (teacher/student/TA)
- Public marketplace or deck discovery/browsing
- Heavy gamification, leaderboards, XP systems
- Native mobile apps (iOS/Android)
- Real-time multiplayer study sessions

## Core Flows

### 1. New User Flow
1. Sign up or log in
2. Choose subjects/goals (e.g., "Biology midterms")
3. Choose creation method: topic, PDF upload, or manual
4. Create first deck immediately
5. Enter first study session within the same visit

### 2. AI Deck Generation Flow
1. Enter topic or upload PDF
2. Configure: difficulty, card count, question type mix
3. AI generates draft deck
4. User reviews cards in approval queue: accept, edit, regenerate, remove, change type
5. Publish deck
6. App schedules first review session automatically

### 3. Study Flow
1. Home shows: due reviews, continue last deck, focus on weak spots
2. User starts session
3. Each answer records: correctness, confidence/difficulty, response speed
4. Spaced repetition updates next review per card
5. Session end shows: score, weak concepts, cards due tomorrow, retry misses option

### 4. Share Flow
1. Open deck, tap Share
2. Generate share link or class code
3. Recipient opens link/code, imports personal copy
4. Recipient studies/edits independently
5. No live sync between copies

## Entities

| Entity | Key Fields |
|--------|-----------|
| **User** | id, email, password_hash, display_name, preferences, streak_count, weekly_goal, created_at |
| **Deck** | id, owner_id, title, subject, description, source_type (topic/pdf/manual), card_count, shared_status, created_at |
| **Card** | id, deck_id, type (flashcard/mcq/identification/true_false/cloze), prompt, answer, explanation, options (for mcq), cloze_text, source_chunk_id, position, created_at |
| **Source Document** | id, deck_id, filename, mime_type, extracted_text, chunks (JSON), uploaded_at |
| **Study Session** | id, user_id, deck_id, mode (learn/quiz/test), total_cards, correct_count, duration_seconds, completed_at |
| **Review Schedule** | id, user_id, card_id, ease_factor, interval_days, repetitions, next_review_at, last_reviewed_at |
| **Share Artifact** | id, deck_id, creator_id, share_type (link/code), code, import_count, expires_at, created_at |

## Screens

1. **Dashboard / Home** — due reviews, streaks, continue studying, quick actions
2. **Deck Library** — all decks, search/filter, sort by subject/date/activity
3. **Deck Detail** — card list, deck stats, study/share/edit actions
4. **Create Deck** — topic input, PDF upload, or manual card entry
5. **AI Review Queue** — card-by-card approval with edit/regenerate/remove/change-type
6. **Study Session** — card presentation by type, answer input, immediate feedback
7. **Session Results** — score, weak areas, next review schedule, retry misses
8. **Shared Deck Import** — preview deck before importing copy
9. **Profile / Settings** — account, preferences, streak/goal config, devices

## Extra Features (V1)

| Feature | Purpose |
|---------|---------|
| **Weak Spots** | Detect repeatedly missed cards, surface "Focus on weak areas" session |
| **Mistake Notebook** | Auto-save missed questions into dedicated review set |
| **Deck Health Score** | Flag low-quality AI cards: ambiguous, duplicate, too-easy |
| **Source-Backed Generation** | Keep cards tied to PDF/source chunks for grounded regeneration |
| **Study Streak + Weekly Goal** | Light motivation without gamification |
| **Offline Review** | Recent decks reviewable when network drops |

## Acceptance Criteria
- [ ] User can sign up, log in, and set subject preferences
- [ ] User can create a deck from a topic with AI generation
- [ ] User can create a deck by uploading a PDF with AI generation
- [ ] User can create a deck manually with hand-made cards
- [ ] AI-generated cards enter a review queue before becoming study-ready
- [ ] Review queue supports: accept, edit, regenerate, remove, change card type
- [ ] All 5 card types (flashcard, MCQ, identification, T/F, cloze) render and function correctly
- [ ] All card types work on mobile and desktop viewports
- [ ] Learn/Review mode uses spaced repetition (SM-2 or similar) to schedule per-card reviews
- [ ] Quick Quiz mode presents mixed question types from a deck
- [ ] Test mode runs a scored self-check and shows results
- [ ] Spaced repetition schedules next review dates per card after each session
- [ ] Session results show score, weak concepts, tomorrow's due cards, retry option
- [ ] User can resume study seamlessly on another device after login
- [ ] Share by link generates a URL that lets recipients import a personal copy
- [ ] Share by class code generates a short code that does the same
- [ ] Imported copies are independent — edits don't propagate
- [ ] Weak spots session can be started from recent mistakes
- [ ] Mistake notebook auto-collects missed cards
- [ ] Deck health score flags low-quality AI cards
- [ ] Study streak and weekly goal tracking visible on dashboard
- [ ] PWA is installable and responsive across phone, tablet, and laptop
- [ ] Recent decks remain reviewable with degraded behavior offline

## Assumptions Exposed
| Assumption | How Surfaced | Resolution |
|------------|-------------|------------|
| PWA over native | Provided in input | Confirmed — V1 is web-only PWA |
| Copy-based sharing | Provided in input | Confirmed — no live sync |
| AI as draft, not instant publish | Provided in input | Confirmed — mandatory review queue |
| SM-2 or similar for spaced repetition | Implied by "spaced repetition engine" | Default to SM-2; can swap algorithm later |
| Tech stack unspecified | Not addressed in input | TBD in brainstorm — frontend framework, backend, DB, AI provider, auth, hosting |
| PDF size/page limits | Not addressed | TBD — needs a practical cap for AI processing |
| Class code expiration | Not addressed | Default: codes don't expire in V1 |
| Max cards per deck | Not addressed | TBD — may need limits for performance |
| AI provider for card generation | Not addressed | TBD in brainstorm |
| Auth method | Not addressed | TBD — email/password baseline, social login optional |

## Technical Context
Greenfield — no existing codebase. Tech stack decisions deferred to `/sk:brainstorm`:
- Frontend framework (React/Next.js, Vue/Nuxt, Svelte, etc.)
- Backend framework and language
- Database (PostgreSQL, SQLite, etc.)
- AI provider and model for card generation
- Auth system (custom, Auth.js, Clerk, Supabase Auth, etc.)
- File storage for PDFs
- Hosting/deployment target
- PWA tooling (Workbox, Vite PWA plugin, etc.)

## Ontology
**Core entity:** Deck (the central object users create, study, and share)
**Supporting concepts:** Card, User, Study Session, Review Schedule, Source Document, Share Artifact

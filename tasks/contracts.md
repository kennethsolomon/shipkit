# API Contracts — Study App V1

## Architecture Note

Next.js 15 App Router uses **Server Actions** for most mutations (deck CRUD, card CRUD, study answers, sharing). **API routes** are used only for streaming AI generation and public share endpoints.

---

## API Routes (Streaming / Public)

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | /api/generate/topic | Required | Generate cards from a topic via OpenRouter (streaming) |
| POST | /api/generate/pdf | Required | Upload PDF, extract text, generate cards (streaming) |
| POST | /api/generate/regenerate | Required | Regenerate a single card with optional source context |
| GET | /api/share/[code] | Public | Fetch deck preview for share import page |

## Request / Response Shapes

### POST /api/generate/topic
**Request:**
```json
{
  "deckId": "uuid",
  "topic": "string",
  "difficulty": "easy | medium | hard",
  "cardCount": "number (1-50)",
  "typeMix": {
    "flashcard": "number (0-100, percentage)",
    "mcq": "number",
    "identification": "number",
    "true_false": "number",
    "cloze": "number"
  }
}
```
**Response (200, streaming NDJSON):**
```json
{"type": "card", "data": {"type": "FLASHCARD", "prompt": "...", "answer": "...", "explanation": "..."}}
{"type": "card", "data": {"type": "MCQ", "prompt": "...", "answer": "...", "options": ["A","B","C","D"], "explanation": "..."}}
{"type": "done", "data": {"totalGenerated": 10}}
```
**Errors:** 400 (invalid input), 401 (unauthorized), 429 (OpenRouter rate limit), 500 (generation failure)

### POST /api/generate/pdf
**Request:** `multipart/form-data`
```
file: PDF file (max 20MB, max 50 pages)
deckId: uuid
difficulty: easy | medium | hard
cardCount: number (1-50)
typeMix: JSON string (same shape as topic endpoint)
```
**Response (200, streaming NDJSON):**
```json
{"type": "source", "data": {"documentId": "uuid", "filename": "bio.pdf", "pageCount": 12, "chunkCount": 8}}
{"type": "card", "data": {"type": "FLASHCARD", "prompt": "...", "answer": "...", "sourceChunkId": "uuid"}}
{"type": "done", "data": {"totalGenerated": 15}}
```
**Errors:** 400 (invalid file type, too large, too many pages), 401, 422 (could not extract text — likely scanned PDF), 429, 500

### POST /api/generate/regenerate
**Request:**
```json
{
  "cardId": "uuid",
  "sourceChunkId": "uuid | null",
  "newType": "FLASHCARD | MCQ | IDENTIFICATION | TRUE_FALSE | CLOZE | null"
}
```
**Response (200):**
```json
{
  "card": {
    "id": "uuid",
    "type": "MCQ",
    "prompt": "...",
    "answer": "...",
    "options": ["A","B","C","D"],
    "explanation": "...",
    "isDraft": true
  }
}
```
**Errors:** 400 (invalid card type), 401, 404 (card not found), 429, 500

### GET /api/share/[code]
**Request:** No body. `code` is URL parameter.
**Response (200):**
```json
{
  "deck": {
    "title": "Biology 101",
    "subject": "Biology",
    "description": "...",
    "cardCount": 25,
    "creatorName": "Jane D."
  },
  "shareType": "LINK | CODE"
}
```
**Errors:** 404 (invalid/expired code)

---

## Server Actions (Authenticated Mutations)

These are Next.js Server Actions called directly from Client Components — no REST endpoints.

| Action | Input | Output | Description |
|--------|-------|--------|-------------|
| createDeck | {title, subject, description?, sourceType} | Deck | Create empty deck |
| updateDeck | {deckId, title?, subject?, description?} | Deck | Update deck metadata |
| deleteDeck | {deckId} | void | Delete deck + cascade cards |
| createCard | {deckId, type, prompt, answer, explanation?, options?, clozeText?} | Card | Add card to deck |
| updateCard | {cardId, type?, prompt?, answer?, explanation?, options?, clozeText?} | Card | Edit card |
| deleteCard | {cardId} | void | Remove card from deck |
| reorderCards | {deckId, cardIds: string[]} | void | Set card positions |
| publishDeck | {deckId} | Deck | Set all is_draft=false, update card_count |
| publishCard | {cardId} | Card | Set single card is_draft=false |
| startSession | {deckId, mode} | StudySession | Create session, fetch cards |
| submitAnswer | {sessionId, cardId, isCorrect, confidence?, responseTimeMs?} | void | Record answer + update SM-2 (learn mode) |
| completeSession | {sessionId, durationSeconds} | StudySession | Mark session complete |
| createShareArtifact | {deckId, shareType} | ShareArtifact | Generate link/code |
| importSharedDeck | {code} | Deck | Deep-copy deck into user's library |
| updateProfile | {displayName?, weeklyGoal?, preferences?} | User | Update user settings |
| completeOnboarding | {subjects: string[], goals?: string} | User | Save onboarding preferences |

---

## Auth Requirements

- **Method:** Supabase Auth (JWT via cookie)
- **Middleware:** Next.js middleware checks Supabase session on every request
- **Public routes:** /auth/*, /share/[code] (GET only — preview)
- **Protected routes:** everything else
- **API routes:** validate Supabase session from cookie; return 401 if missing/invalid
- **Server Actions:** automatically authenticated via Next.js middleware; access user via Supabase server client

## Mocking Boundary

**Frontend mocks (for isolated development):**
- OpenRouter streaming responses (mock NDJSON stream)
- Supabase Auth session (mock user object)
- Database queries (mock Prisma responses)

**Backend owns (source of truth):**
- SM-2 calculation logic
- PDF text extraction + chunking
- OpenRouter prompt construction
- Share code generation (nanoid, 6-char alphanumeric)
- Deck deep-copy logic
- Supabase Auth ↔ Prisma User sync trigger

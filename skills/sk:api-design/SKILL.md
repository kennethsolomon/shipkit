---
name: sk:api-design
description: Design REST or GraphQL API contracts before implementation. Use this skill when the user needs to design API endpoints, request/response shapes, authentication patterns, error codes, or data contracts. Produces an API specification — NOT code.
license: Complete terms in LICENSE.txt
---

## CRITICAL: Design Phase Only — NO CODE

**This skill is a design phase, not an implementation phase.**

- **DO NOT** write, edit, or generate any code (no controllers, routes, models, migrations)
- **DO NOT** use file editing tools (Edit, Write, Bash)
- **DO produce** endpoint contracts, request/response shapes, error codes, auth flows, and data models
- Implementation happens in `/sk:execute-plan` — not here

This skill designs clear, consistent API contracts that `/sk:write-plan` and `/sk:execute-plan` can implement without ambiguity.

## Before You Start

1. If `tasks/findings.md` exists and has content, read it in full. Use the agreed approach and requirements as the design brief.
2. If `tasks/lessons.md` exists, read it in full. Apply every active lesson as a constraint — particularly patterns flagged under **Bug** that relate to API structure, auth, or data validation.

## API Context

Establish these before designing:

- **API type**: REST, GraphQL, or both?
- **Consumers**: Who calls this API? (web app, mobile app, third-party, internal service)
- **Auth method**: JWT, API key, OAuth2, session cookie, or none?
- **Versioning strategy**: URL prefix (`/v1/`), header (`Accept-Version`), or none?
- **Transport**: HTTPS only. No exceptions.

If context is unclear from `tasks/findings.md`, ask the user before proceeding.

## Design Thinking

Before designing endpoints, model the domain:

- **Resources**: What are the core entities? (e.g., User, Order, Product)
- **Relationships**: How do resources relate? (ownership, nesting, references)
- **Actions**: What operations exist? (CRUD + custom actions like `/publish`, `/archive`)
- **Invariants**: What rules can never be violated? (e.g., a published post can't be deleted)

**CRITICAL**: Design for the consumer, not the database. An API that mirrors the database schema 1:1 is usually wrong — design for what clients actually need.

## API Design Guidelines

### REST Endpoints
- **Nouns, not verbs** in URLs: `/orders` not `/getOrders`
- **Plural resources**: `/users`, `/posts`, `/comments`
- **Nested only one level deep**: `/users/{id}/orders` ✓ — `/users/{id}/orders/{id}/items` ✗ (use `/order-items?orderId=`)
- **HTTP methods map to actions**: GET (read), POST (create), PUT (full replace), PATCH (partial update), DELETE (remove)
- **Custom actions**: use POST + verb suffix: `POST /orders/{id}/cancel`

### Request Design
- Use JSON request bodies for POST/PUT/PATCH
- URL params for resource IDs
- Query params for filtering, sorting, pagination
- Headers for auth tokens and content negotiation

### Response Design
- Consistent envelope: `{ data, meta, errors }` or resource-direct — pick one and use it everywhere
- Pagination: `{ data: [...], meta: { total, page, per_page, last_page } }`
- Timestamps: ISO 8601 (`2026-03-15T22:00:00Z`)
- IDs: strings (not integers) — avoids enumeration attacks

### Status Codes
- `200` OK (GET, PUT, PATCH success)
- `201` Created (POST success)
- `204` No Content (DELETE success)
- `400` Bad Request (validation failure)
- `401` Unauthenticated (missing/invalid token)
- `403` Forbidden (authenticated but not authorized)
- `404` Not Found
- `409` Conflict (duplicate, state violation)
- `422` Unprocessable Entity (business rule violation)
- `429` Too Many Requests (rate limited)
- `500` Internal Server Error

### Error Format
Standardize error responses:
```json
{
  "errors": [
    {
      "code": "VALIDATION_FAILED",
      "field": "email",
      "message": "Email is already taken"
    }
  ]
}
```

### Auth Design
- JWT: short-lived access token (15min–1hr) + refresh token (7–30 days)
- API keys: prefix with service identifier (`sk_live_`, `pk_test_`)
- Never return tokens in URL params — headers or response body only
- Document which endpoints require auth and what permissions

### Rate Limiting
- Define limits per endpoint tier (public, authenticated, admin)
- Return `Retry-After` header on `429`

## Output Format

End every `/sk:api-design` session with a structured specification:

```
## API Design Specification

### Overview
[API purpose, consumers, base URL pattern, versioning approach]

### Authentication
[Auth method, token format, how to include in requests, refresh flow]

### Resource Models
[Core entities with their fields, types, and constraints]

### Endpoints

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET    | /v1/resource | required | List resources |
| ...    | ...  | ...  | ... |

### Endpoint Details
[For each endpoint: request params/body shape, success response shape, error cases]

### Error Codes Reference
[Application-specific error codes and when they occur]

### Rate Limits
[Per-tier limits, headers returned]

### Versioning & Breaking Changes
[What constitutes a breaking change, deprecation policy]
```

After presenting the specification, tell the user: **"Run `/sk:write-plan` to turn this into an implementation plan."**

---

## Model Routing

Read `.shipkit/sk:config.json` from the project root if it exists.

- If `model_overrides["sk:api-design"]` is set, use that model — it takes precedence.
- Otherwise use the `profile` field. Default: `balanced`.

| Profile | Model |
|---------|-------|
| `full-sail` | opus (inherit) |
| `quality` | opus (inherit) |
| `balanced` | sonnet |
| `budget` | sonnet |

> `opus` = inherit (uses the current session model). When spawning sub-agents via the Agent tool, pass `model: "<resolved-model>"`.

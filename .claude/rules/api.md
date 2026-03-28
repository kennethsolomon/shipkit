---
paths:
  - "routes/api.php"
  - "app/Http/Controllers/**"
  - "**/controllers/**"
  - "**/handlers/**"
  - "src/api/**"
---

# API Design Rules

- RESTful naming: nouns for resources (`/users`, `/orders`), not verbs (`/getUser`)
- HTTP methods: GET (read), POST (create), PUT (full replace), PATCH (partial update), DELETE (remove)
- Status codes: 200 ok, 201 created, 204 no content, 400 bad request, 401 unauthenticated, 403 forbidden, 404 not found, 422 validation failed, 429 rate limited, 500 server error
- Consistent error shape: `{ "message": "...", "errors": { "field": ["..."] } }`
- Validate all inputs at the API boundary — never trust client-provided data
- Paginate all list endpoints — never return unbounded arrays
- Version with URL prefix (`/api/v1/`) before shipping breaking changes
- Auth: Bearer tokens in `Authorization` header — never in URL query params
- Rate limit all public-facing endpoints
- CORS: whitelist specific origins — never `*` in production
- Never leak internal stack traces, SQL errors, or sensitive IDs in error responses
- Log all requests at INFO, all errors at ERROR with request context (method, path, status)

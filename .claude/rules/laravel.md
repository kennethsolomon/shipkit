---
paths:
  - "app/**/*.php"
  - "routes/**/*.php"
  - "config/**/*.php"
  - "database/**/*.php"
---

# Laravel Rules

- Follow PSR-12 coding standards; use typed properties and return types (PHP 8.1+)
- Eloquent: always eager-load relationships with `with()`/`load()` to prevent N+1 queries
- Use Form Requests for validation — never validate inline in controllers
- Keep controllers thin — business logic belongs in Service classes
- Use Repository pattern when a model has 3+ distinct query methods
- Use `$fillable` not `$guarded` — explicit allowlists are safer than blocklists
- Wrap multi-step writes in database transactions
- Use `->firstOrFail()` when a record must exist; return 404 automatically
- Read config with `config('app.key')` — never `env('KEY')` outside of config files
- Tag Redis caches so related keys can be flushed together on invalidation
- Queue jobs: implement `ShouldBeUnique` for idempotent operations
- Never commit `dd()`, `dump()`, or `var_dump()` — use logs or tests instead

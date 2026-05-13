---
name: sk:schema-migrate
description: "/sk:schema-migrate — Multi-ORM Schema Change Analysis"
allowed-tools: Read, Glob, Grep, Bash, Agent
---

# /sk:schema-migrate — Multi-ORM Schema Change Analysis

**Invocation:** `/sk:schema-migrate`

Analyzes pending schema changes across **5 ORMs** and provides safe, dialect-specific migration
guidance. Auto-detects the ORM from project files — no configuration needed.

**Supported:** Drizzle ORM · Prisma · Laravel + Eloquent · SQLAlchemy + Alembic · Rails + ActiveRecord

---

## Overview: 5-Phase Analysis

1. **Detect ORM** — Read project files, identify ORM + dialect, load the correct analysis module
2. **Classify Changes** — Parse diffs, categorize by risk, detect unsafe patterns
3. **Present Risk Report** — Formatted report with warnings and dialect-specific notes
4. **Per-Change Migration Plans** — Concrete safe paths for breaking/risky changes
5. **Command Recommendations** — ORM-specific workflows and commands

---

## Phase 0: Auto-Detect Migration Changes

Before doing anything else, check whether the current branch has any migration-related changes:

```bash
git diff main..HEAD --name-only
```

Scan the output for migration-related files:
- Files under `migrations/`, `database/migrations/`, `prisma/migrations/`, `alembic/versions/`, `db/migrate/`
- Schema definition files: `prisma/schema.prisma`, `drizzle.config.ts`, `drizzle.config.js`, `alembic.ini`
- Any `*.sql` files in migration-related directories

**If NO migration-related files are found in the diff:**
> auto-skip: No migration changes detected in this branch — skipping `/sk:schema-migrate`.

Exit cleanly. Do not ask the user. Do not proceed to Phase 1.

**If migration-related files ARE found:** invoke the **`database-architect` agent** before proceeding to Phase 1:

```
Task: "Read tasks/findings.md, tasks/lessons.md, and the migration files in this diff.
Perform a migration safety analysis: flag breaking changes, missing indexes, NULL violations,
orphan rows, and data-loss risks. Recommend safe migration order and any needed index additions.
Read-only — no code changes."
```

Incorporate the `database-architect`'s safety report into your Phase 2-4 risk analysis. Then proceed to Phase 1 (ORM Detection) below.

---

## Phase 1: ORM Detection

### Step 1 — Read in Parallel

Read the following files simultaneously (read-only, tolerate missing files):

```
drizzle.config.ts        prisma/schema.prisma
drizzle.config.js        composer.json
alembic.ini              Gemfile
package.json             supabase/sk:config.toml
```

### Step 2 — Apply Priority Rules (first match wins)

| Priority | ORM | Definitive Signal | Secondary Check |
|----------|-----|-------------------|-----------------|
| 1 | Drizzle | `drizzle.config.ts` or `drizzle.config.js` exists | `package.json` → `drizzle-orm` dep |
| 2 | Prisma | `prisma/schema.prisma` exists | `package.json` → `@prisma/client` |
| 3 | Laravel | `composer.json` → `laravel/framework` key | `database/migrations/` exists |
| 4 | SQLAlchemy | `alembic.ini` exists | `alembic/versions/` exists |
| 5 | Rails | `Gemfile` → `rails` or `activerecord` gem | `db/migrate/` + `db/schema.rb` |

**Supabase overlay (independent check):** If `supabase/sk:config.toml` exists → set `isSupabase = true`. This adds Supabase CLI commands in Phase 5, alongside standard ORM commands.

**Ambiguity:** If two definitive signals match (e.g., monorepo), ask the user before proceeding:
> "Found both `drizzle.config.ts` (Drizzle) and `composer.json` (Laravel). Which ORM should I analyze?"

**Unknown:** If no signal matches any ORM, report:
> "Could not detect ORM. Checked for: drizzle.config.ts, prisma/schema.prisma, composer.json (laravel/framework), alembic.ini, Gemfile (rails/activerecord). Please specify which ORM this project uses."

For more detailed detection heuristics and dialect rules, see `references/detection.md`.

### Step 3 — Report Detection Result

```
Detected: [ORM] ([dialect]) — loading orms/[orm].md
```

Examples:
- `Detected: Drizzle ORM (SQLite) — loading orms/drizzle.md`
- `Detected: Prisma (PostgreSQL + Supabase) — loading orms/prisma.md`
- `Detected: Laravel + Eloquent (MySQL) — loading orms/laravel.md`
- `Detected: SQLAlchemy + Alembic (PostgreSQL) — loading orms/sqlalchemy.md`
- `Detected: Rails + ActiveRecord (PostgreSQL) — loading orms/rails.md`

### Step 4 — Load and Execute ORM Module

Read the appropriate file from `orms/` and execute **Phases 2 through 5** as defined there:

| ORM | File |
|-----|------|
| Drizzle | `orms/drizzle.md` |
| Prisma | `orms/prisma.md` |
| Laravel | `orms/laravel.md` |
| SQLAlchemy | `orms/sqlalchemy.md` |
| Rails | `orms/rails.md` |

---

## Safety Contract

✅ **Read-only analysis** — this skill never modifies files, schemas, or databases

✅ **No auto-execution** — never runs `db:push`, `db:generate`, `db:migrate`, `prisma migrate`, `php artisan migrate`, `alembic upgrade`, `rails db:migrate`, or `supabase push` automatically

✅ **User confirms** — user must read and understand the risk report before proceeding

✅ **ORM + dialect-specific guidance** — recommendations are tailored to the detected stack

✅ **Data safety first** — flags orphan rows, duplicates, NULL violations, and breaking changes before they cause data loss

---

## Known Limitations

1. **MongoDB (Prisma):** Prisma + MongoDB does not use migration files — schema-migrate reports this and stops analysis
2. **Autogenerate blindspots (SQLAlchemy):** Alembic cannot detect column renames, check constraints, or server defaults from model files alone
3. **Remote schema sync:** Supabase remote schema comparison requires a valid `SUPABASE_ACCESS_TOKEN` — falls back to local-only analysis if unavailable
4. **Custom SQL migrations:** Manually written SQL migration files (outside ORM conventions) cannot be fully parsed — user must verify independently
5. **Type cast validation:** Cannot predict if a type cast will succeed at runtime — always recommend staging test first

---

## Model Routing

Read `.shipkit/config.json` from the project root if it exists.

- If `model_overrides["sk:schema-migrate"]` is set, use that model — it takes precedence.
- Otherwise use the `profile` field. Default: `balanced`.

| Profile | Model |
|---------|-------|
| `full-sail` | opus (inherit) |
| `quality` | sonnet |
| `balanced` | sonnet |
| `budget` | haiku |

> `opus` = inherit (uses the current session model). When spawning sub-agents via the Agent tool, pass `model: "<resolved-model>"`.

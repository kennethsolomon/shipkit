# /schema-migrate — ORM Detection Heuristics

Used by `SKILL.md` Phase 1 to detect the active ORM and route to the correct `orms/[orm].md` file.

---

## Detection Priority Order

First match wins. Check signals in this order:

| Priority | ORM | Definitive Signal | Secondary Check |
|----------|-----|-------------------|-----------------|
| 1 | Drizzle | `drizzle.config.ts` or `drizzle.config.js` exists | `package.json` → `drizzle-orm` dep |
| 2 | Prisma | `prisma/schema.prisma` exists | `package.json` → `@prisma/client` |
| 3 | Laravel | `composer.json` → `laravel/framework` | `database/migrations/` exists |
| 4 | SQLAlchemy | `alembic.ini` exists | `alembic/versions/` exists |
| 5 | Rails | `Gemfile` → `rails` or `activerecord` gem | `db/migrate/` + `db/schema.rb` |

---

## Supabase Overlay

Supabase is detected **alongside** the ORM, not instead of it.

**Signal:** `supabase/config.toml` exists → set `isSupabase = true`

Effect: The detected ORM file's Phase 5 commands will include Supabase CLI workflow in addition to the standard ORM commands. Supabase overlay applies primarily to Drizzle and Prisma projects (both use PostgreSQL under Supabase).

---

## Ambiguity Handling

If two definitive signals match (e.g., monorepo with both `drizzle.config.ts` and `composer.json`), ask the user:

> "Found both `drizzle.config.ts` (Drizzle ORM) and `composer.json` (Laravel). Which ORM should I analyze?"

Do not guess — wait for explicit confirmation.

---

## Detection Flow (Phase 1 Steps)

```
Step 1: Read in parallel —
        drizzle.config.ts, drizzle.config.js,
        prisma/schema.prisma,
        composer.json,
        alembic.ini,
        Gemfile,
        package.json,
        supabase/config.toml

Step 2: Apply priority rules →
        - Does drizzle.config.ts/js exist? → ORM = Drizzle
        - Else does prisma/schema.prisma exist? → ORM = Prisma
        - Else does composer.json have laravel/framework? → ORM = Laravel
        - Else does alembic.ini exist? → ORM = SQLAlchemy
        - Else does Gemfile have rails or activerecord? → ORM = Rails
        - Else: Unknown — report error and ask user to specify

        Supabase check (independent):
        - Does supabase/config.toml exist? → isSupabase = true

Step 3: Report detection result:
        "Detected: [ORM] ([dialect]) — loading orms/[orm].md"
        e.g., "Detected: Drizzle ORM (SQLite) — loading orms/drizzle.md"
        e.g., "Detected: Prisma (PostgreSQL + Supabase) — loading orms/prisma.md"

Step 4: Load orms/[orm].md and execute its Phase 2 through Phase 5
```

---

## Dialect Detection (per ORM)

After the ORM is identified, detect the database dialect:

### Drizzle
- Read `drizzle.config.ts` → `dialect` field: `sqlite` | `postgres` | `mysql`
- Supabase: `dialect === 'postgres'` + URL contains `supabase`

### Prisma
- Read `prisma/schema.prisma` → `datasource db { provider = "..." }`
- Values: `postgresql` | `mysql` | `sqlite` | `sqlserver` | `mongodb`
- Note: MongoDB does not support migrations — flag this to the user

### Laravel
- Read `.env` → `DB_CONNECTION` value: `mysql` | `pgsql` | `sqlite`
- Fallback: read `config/database.php` → `default` key
- Default if undetectable: `mysql`

### SQLAlchemy
- Read `alembic.ini` → `sqlalchemy.url` value
- Prefix: `postgresql` | `mysql` | `sqlite` | `mssql`

### Rails
- Read `config/database.yml` → `adapter:` value under `development:`
- Values: `postgresql` | `mysql2` | `sqlite3`

---

## ORM → File Map

| Detected ORM | File to Load |
|--------------|-------------|
| Drizzle | `orms/drizzle.md` |
| Prisma | `orms/prisma.md` |
| Laravel | `orms/laravel.md` |
| SQLAlchemy (Alembic) | `orms/sqlalchemy.md` |
| Rails (ActiveRecord) | `orms/rails.md` |

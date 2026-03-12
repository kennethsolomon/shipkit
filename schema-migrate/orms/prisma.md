# /schema-migrate — Prisma Analysis (Phases 2–5)

> This file is loaded by `SKILL.md` when Prisma ORM is detected.
> Execute Phase 2 through Phase 5 below, then return the final report.

---

## Phase 2: Classify Changes

### Files to Scan (read in parallel)

1. **`prisma/schema.prisma`** — full schema definition
   - Parse all `model`, `enum`, `datasource`, `generator` blocks
   - Track: models, fields, types, attributes (`@id`, `@unique`, `@@index`, `@relation`, `?`)

2. **`prisma/migrations/`** — migration history directory
   - List all migration folders (timestamp-named)
   - Read latest migration SQL file

3. **`migration_lock.toml`** — migration lock file
   - Verify provider matches `schema.prisma` datasource

4. **`package.json`** — scripts and dependencies
   - Detect: `prisma migrate dev`, `prisma migrate deploy`, `prisma db push`
   - Confirm `@prisma/client` and `prisma` in devDependencies

5. **`.env`** — environment config
   - Extract `DATABASE_URL` → parse dialect from connection string prefix

6. **`git diff HEAD -- prisma/schema.prisma`** — uncommitted changes (what's pending)

7. **`git log --oneline -5 -- prisma/schema.prisma`** — recent schema commit history

### Dialect Detection

From `datasource db { provider = "..." }` in `prisma/schema.prisma`:

| Provider | Dialect |
|----------|---------|
| `postgresql` | PostgreSQL |
| `mysql` | MySQL |
| `sqlite` | SQLite |
| `sqlserver` | SQL Server |
| `mongodb` | MongoDB ⚠️ (no migrations — flag to user) |

**MongoDB note:** Prisma does not generate migration files for MongoDB. If detected, report: "Prisma + MongoDB detected — migration analysis not applicable. Prisma uses `prisma db push` only for MongoDB."

### Risk Matrix

| Change | Risk | Notes |
|--------|------|-------|
| Add new model | 🟢 Safe | Additive — new table created |
| Add optional field (`field?` or with default) | 🟢 Safe | No impact on existing rows |
| Add `@@index` | 🟢 Safe | Non-blocking index creation |
| Add enum value | 🟡 Careful | PostgreSQL: irreversible `ALTER TYPE ADD VALUE` — cannot be in a transaction |
| Add required field with default | 🟡 Careful | All existing rows get default value — verify acceptability |
| Add unique constraint | 🟡 Careful | Fails if duplicate values exist in current data |
| Add `@relation` to existing field | 🟡 Careful | Orphan row check required; SQLite recreates full table |
| Remove `?` (make field required) | 🔴 Breaking | Any NULL rows will fail migration |
| Rename field (no `@map`) | 🔴 Breaking | Prisma sees as drop + add → data loss |
| Change field type | 🔴 Breaking | Review generated SQL; SQLite requires full table recreation |
| Remove field | 🔴 Breaking | Data permanently lost — check all code usages first |
| Remove model | 🔴 Breaking | Destructive — check all code and FK references |
| Remove enum value | 🔴 Breaking | PostgreSQL: cannot drop a value that rows reference |

### Also Detect

- ⚠️ **Migration drift**: Run `prisma migrate status` — flags migrations applied to DB but not in `prisma/migrations/`
- ⚠️ **Missing baseline migration**: Database exists but no `_prisma_migrations` table — needs `prisma migrate baseline`
- ⚠️ **Shadow DB not configured**: MySQL and SQL Server require a shadow database URL for `prisma migrate dev`
- ⚠️ **`migration_lock.toml` provider mismatch**: Lock file provider differs from schema datasource provider

---

## Phase 3: Present Risk Report

### Report Format

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  /schema-migrate — Schema Change Analysis
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ORM:              Prisma
Dialect:          PostgreSQL
Workflow:         prisma migrate dev (versioned migrations)
Schema:           prisma/schema.prisma
Migrations dir:   prisma/migrations/
Last migration:   20250228120000_add_profiles_table

Status:
  📁 Migration history: IN SYNC
  📝 Schema file: MODIFIED (uncommitted)
  ✅ Lock file: provider matches

Detected Changes (since last commit):
──────────────────────────────────────────

🟢 SAFE (2 changes)
  • Job model: Added optional field `appliedNotes` (String?)
  • Job model: Added @@index on [status]

🟡 CAREFUL (1 change — review before migrating)
  • Profile model: Added required field `email String @default("")`
    ↳ All existing rows will get empty string value
    ↳ Is "" an acceptable initial value? Consider String? first.

🔴 BREAKING (1 change — stop and read migration plan)
  • Job model: Field `jobType` changed String → Int
    ↳ Prisma will generate SQL to ALTER column type
    ↳ Review generated migration SQL before applying
    ↳ SQLite: full table recreation required

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Dialect-Specific Notes

#### PostgreSQL
- ✅ Full ALTER TABLE support — most changes are online
- ⚠️ `ALTER TYPE ADD VALUE` for enums cannot be rolled back
- ⚠️ Long-running ALTER may briefly lock large tables
- ✅ Prisma generates versioned migration SQL — review before applying

#### MySQL
- ⚠️ Requires shadow database URL for `prisma migrate dev`
- ⚠️ Rename field: check if `doctrine/dbal` equivalent needed (Prisma handles natively)
- ✅ Online DDL available for MySQL 8.0+
- ⚠️ Type casts may fail silently — verify generated SQL

#### SQLite
- 🚨 Prisma recreates entire table for most structural changes (ALTER limitation)
- ✅ Table recreation is safe but slower for large tables
- ⚠️ Foreign key changes always trigger table recreation

#### SQL Server
- ⚠️ Requires shadow database configured in `.env` as `SHADOW_DATABASE_URL`
- ⚠️ Some ALTER operations not supported — review generated SQL

---

## Phase 4: Per-Change Migration Plans

### Scenario: Rename Field (No `@map`)

```
Problem: Without @map, Prisma sees rename as drop old + add new → data loss!

Safe path via @map (zero data loss):
  1. Add @map annotation — keep DB column name, rename Prisma field only:
     oldName  String  @map("old_name")  →  newName  String  @map("old_name")
  2. prisma migrate dev --name rename_field_to_new_name
  3. Review generated SQL — should only be a comment change (no ALTER)
  4. Apply migration
  5. Update all code references from oldName → newName
  6. Later (optional): rename underlying column with separate migration

Safe path via add/backfill/drop (if column must also be renamed in DB):
  1. Add new field: newName String? (nullable)
  2. prisma migrate dev --name add_new_name
  3. Backfill: UPDATE table SET new_name = old_name
  4. Remove old field from schema, make newName required
  5. prisma migrate dev --name remove_old_name
  6. Data preserved ✅
```

---

### Scenario: Remove `?` (Make Required)

```
Problem: Any NULL values in existing rows will cause migration to fail.

Pre-check SQL:
  SELECT COUNT(*) FROM [table] WHERE [field] IS NULL;

If NULLs found:
  Option A (backfill then migrate):
    1. Run UPDATE [table] SET [field] = [value] WHERE [field] IS NULL
    2. Remove ? from schema
    3. prisma migrate dev

  Option B (add default then migrate):
    1. Add default: field String @default("value")
    2. prisma migrate dev → existing NULLs get default
    3. Optionally remove default later if not needed

  Option C (keep optional):
    - Reconsider requirement — keep field nullable if data is legitimately absent
```

---

### Scenario: Add Relation FK to Existing Field

```
Pre-check for orphan rows:
  SELECT COUNT(*) FROM [table]
  WHERE [foreignKey] NOT IN (SELECT id FROM [referencedTable]);

If orphans found:
  Option A: Delete orphan rows (data loss — review first)
  Option B: Set orphans to NULL (if FK field is nullable)
  Option C: Update orphans to valid reference

After orphans cleaned:
  Add @relation to schema
  prisma migrate dev

SQLite note:
  - Prisma will recreate the full table (SQLite limitation)
  - All data preserved, but takes longer for large tables
  - Test on a copy of data if concerned about recreation time
```

---

### Scenario: Change Field Type

```
Pre-review generated migration SQL:
  prisma migrate dev --create-only --name change_type
  # Review prisma/migrations/[timestamp]_change_type/migration.sql

PostgreSQL:
  - Review if CAST is present in generated SQL
  - If no CAST: Prisma expects types to be compatible
  - If data incompatible: manually add USING clause in migration SQL
  - Apply: prisma migrate dev (after editing migration.sql)

SQLite:
  - Prisma will generate a table recreation script (shadow table approach)
  - Verify generated SQL includes data copy: INSERT INTO new SELECT ... FROM old
  - Apply: prisma migrate dev

MySQL:
  - Review ALTER TABLE ... MODIFY COLUMN ... in migration.sql
  - Check for silent truncation (e.g., TEXT → VARCHAR(100))
```

---

### Scenario: Add Enum Value on PostgreSQL

```
⚠️ PostgreSQL: ALTER TYPE ADD VALUE cannot be run inside a transaction.
Prisma wraps migrations in transactions by default — this will FAIL.

Workaround:
  1. Create migration manually:
     prisma migrate dev --create-only --name add_enum_value
  2. Edit migration.sql — add at the TOP:
     -- prisma-client-js
     -- This migration is run outside of a transaction because of ALTER TYPE ADD VALUE
  3. In migration.sql, use: ALTER TYPE "MyEnum" ADD VALUE 'NEW_VALUE';
  4. Mark migration as non-transactional in schema.prisma:
     generator client {
       provider = "prisma-client-js"
       previewFeatures = ["postgresqlExtensions"]
     }
  5. Apply: prisma migrate dev
  6. Note: This enum value addition is IRREVERSIBLE — cannot be removed later
```

---

## Phase 5: Command Recommendations

### Core Commands

```bash
# Check migration status
npx prisma migrate status

# Generate and apply migration (development)
npx prisma migrate dev --name [describe_change]

# Create migration SQL without applying (for review)
npx prisma migrate dev --create-only --name [describe_change]

# Apply pending migrations (production — no interactive prompts)
npx prisma migrate deploy

# Reset database and reapply all migrations (dev only — DESTRUCTIVE)
npx prisma migrate reset

# Push schema changes without migration files (prototyping/SQLite dev)
npx prisma db push

# Regenerate Prisma Client after schema changes
npx prisma generate

# Pull current DB schema into schema.prisma (for baseline)
npx prisma db pull

# Baseline an existing database (first-time migration setup)
npx prisma migrate resolve --applied [migration_name]
```

### Workflow: Development (with migration files)

```bash
# 1. Review changes
/schema-migrate

# 2. Generate migration (review SQL before applying)
npx prisma migrate dev --create-only --name [describe_change]
cat prisma/migrations/[latest]/migration.sql

# 3. If SQL looks correct, apply
npx prisma migrate dev --name [describe_change]

# 4. Commit
git add prisma/schema.prisma prisma/migrations/
git commit -m "feat(schema): [describe change]"
```

### Workflow: Production Deployment

```bash
# 1. Migrations committed and reviewed
# 2. Deploy application
npx prisma migrate deploy  # applies all pending migrations
npx prisma generate        # regenerate client if needed
```

### Supabase + Prisma Workflow

```bash
# 1. Generate migration
npx prisma migrate dev --create-only --name [describe_change]

# 2. Review generated SQL
cat prisma/migrations/[timestamp]_[describe_change]/migration.sql

# 3. Create Supabase migration
supabase migration new [describe_change]
# Copy SQL from prisma migration into supabase/migrations/[timestamp]_[describe_change].sql

# 4. Test locally
supabase db reset

# 5. Apply prisma migration (links Prisma state)
npx prisma migrate dev

# 6. Push to staging
supabase link --project-ref=[staging-ref]
supabase push --linked

# 7. Promote to production
supabase link --project-ref=[prod-ref]
supabase push --linked

# 8. Commit
git add prisma/ supabase/migrations/
git commit -m "feat(schema): [describe change]"
```

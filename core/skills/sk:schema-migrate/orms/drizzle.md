# /schema-migrate — Drizzle ORM Analysis (Phases 2–5)

> This file is loaded by `SKILL.md` when Drizzle ORM is detected.
> Execute Phase 2 through Phase 5 below, then return the final report.

---

## Phase 2: Classify Changes

Parse `git diff HEAD -- [schema_file]` and classify each change:

### Files to Scan (read in parallel)

1. **`drizzle.config.ts` / `drizzle.config.js`**
   - Extract: `dialect` (sqlite | postgres | mysql), `schema`, `out`, `dbCredentials`
   - Detect Supabase: `dialect === 'postgres'` + `dbCredentials.url` contains `supabase` or `supabaseUrl` is set

2. **Schema file** (from config or default `src/db/schema.ts`)
   - Parse all `export const [table] = ...` definitions
   - Track: table names, columns, constraints, indexes, FKs, defaults

3. **`drizzle/meta/_journal.json`**
   - List migration entries + timestamps
   - Track: last migration name and date

4. **`drizzle/meta/` latest snapshot** (e.g., `0000_colorful_nebula.json`)
   - Last recorded schema state from migrations
   - Used to detect "out of sync" condition (pushed changes without `db:generate`)

5. **`package.json`** scripts
   - Detect: `db:push`, `db:migrate`, `db:generate` commands
   - Detect: `supabase push`, `supabase migration` scripts (if Supabase)

6. **`git diff HEAD -- [schema_file]`**
   - Uncommitted schema changes (what's pending)

7. **`git log --oneline -5 -- [schema_file]`**
   - Recent schema commit history

8. **`supabase/config.toml`** (if Supabase project detected)
   - Project ID, region, API settings
   - Check if local migrations exist (`supabase/migrations/`)

9. **Schema version on remote** (Supabase only)
   - If Supabase: fetch schema introspection from `{project_url}/rest/v1/?apikey={key}`
   - Compare local schema against remote to detect sync issues

### Risk Matrix

| Change Type | Risk | SQLite | Postgres | MySQL | Supabase | Notes |
|---|---|---|---|---|---|---|
| Add new table | 🟢 Safe | ✅ | ✅ | ✅ | ✅ | Unless FK targets are missing |
| Add nullable column | 🟢 Safe | ✅ | ✅ | ✅ | ✅ | Standard additive change |
| Add index | 🟢 Safe | ✅ | ✅ | ✅ | ✅ | Non-breaking |
| Add comment | 🟢 Safe | ✅ | ✅ | ✅ | ✅ | Metadata only |
| Change default value | 🟢 Safe | ✅ | ✅ | ✅ | ✅ | Only affects new rows |
| Remove `.notNull()` | 🟢 Safe | ✅ | ✅ | ✅ | ✅ | Relaxing constraint |
| Add `.primaryKey()` to new col | 🟢 Safe | ✅ | ✅ | ✅ | ✅ | New table schema only |
| Add NOT NULL col + default | 🟡 Careful | ✅ | ✅ | ✅ | ✅ | Existing rows get default |
| Add unique constraint | 🟡 Careful | ✅ | ✅ | ✅ | ✅ | Fails if duplicates exist |
| Add FK to existing col | 🟡 Careful | ⚠️ Table recreation | ✅ | ⚠️ Online DDL | ✅ | Check for orphan rows first |
| Add/change CASCADE behavior | 🟡 Careful | ⚠️ Table recreation | ✅ | ✅ | ✅ | Behavioral change, data safety |
| Add check constraint | 🟡 Careful | ⚠️ Table recreation | ✅ | ✅ | ✅ | SQLite requires table recreation |
| Add RLS policy (Supabase only) | 🟡 Careful | N/A | N/A | N/A | ⚠️ Auth-dependent | Review security implications |
| Add NOT NULL col (no default) | 🔴 Breaking | ❌ | ❌ | ❌ | ❌ | Fails on non-empty tables |
| Rename column | 🔴 Breaking | ❌ → data loss | ✅ | ✅ | ✅ | Drizzle sees as drop+add |
| Change column type | 🔴 Breaking | ⚠️ Table recreation | ⚠️ May fail | ⚠️ May fail | ⚠️ May fail | Cast failures, data loss risk |
| Drop column | 🔴 Breaking | ⚠️ Data loss | ❌ Data loss | ❌ Data loss | ❌ Data loss | Check usages in code first |
| Drop table | 🔴 Breaking | ❌ Data loss | ❌ Data loss | ❌ Data loss | ❌ Data loss | Check usages in code first |
| Add edge function (Supabase) | 🟢 Safe | N/A | N/A | N/A | ✅ | Deployment via Supabase CLI |
| Modify RLS policy (Supabase) | 🟡 Careful | N/A | N/A | N/A | ⚠️ Auth-dependent | Test auth flows after change |
| Enable realtime (Supabase) | 🟡 Careful | N/A | N/A | N/A | ⚠️ Performance | Large tables may impact realtime |

### Also Detect

- ⚠️ **Migration snapshot out of sync**: Latest snapshot JSON doesn't match schema file
  - Indicates: schema changes have been pushed without `db:generate`

- ⚠️ **Uncommitted schema changes**: Diff includes non-schema files (e.g., seed.ts modified)

- ⚠️ **Supabase sync issue**: Remote schema differs from local schema
  - Run `supabase db pull` to sync

- 🔴 **RLS policies in schema without auth context**: Supabase security issue
  - Policies must reference `auth.uid()` correctly or deny all access

---

## Phase 3: Present Risk Report

### Report Format

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  /schema-migrate — Schema Change Analysis
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ORM:              Drizzle ORM
Dialect:          PostgreSQL (Supabase)
Project:          my-project (region: us-east-1)
Workflow:         db:migrate (versioned migrations)
Schema:           src/db/schema.ts
Migrations dir:   drizzle/
Last migration:   2025-02-28 (0003_add_profiles_table.sql)
Supabase local:   supabase/migrations/

Status:
  📁 Migration snapshot: IN SYNC
  📝 Schema file: COMMITTED
  🌐 Remote schema: IN SYNC with local
  ✅ All systems ready for push

Detected Changes (since last commit):
──────────────────────────────────────────

🟢 SAFE (2 changes)
  • jobs: Added nullable column `applied_notes` (text)
  • jobs: Added index on `status`

🟡 CAREFUL (1 change — review before pushing)
  • profile: Added `email text NOT NULL DEFAULT ''`
    ↳ All existing rows will get empty string value
    ↳ Is '' an acceptable initial value? Consider nullable first.
    ↳ Supabase: Run seed/trigger to populate meaningful defaults

🔴 BREAKING (1 change — stop and read migration plan)
  • jobs: Column `job_type` changed text → integer
    ↳ PostgreSQL can auto-cast, but verify casts don't lose data
    ↳ See safe migration path below
    ↳ Supabase: Test on staging env first

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Dialect-Specific Notes

#### SQLite
- 🚨 **No ALTER COLUMN TYPE** — must recreate table
- 🚨 **No ADD FOREIGN KEY to existing column** — must recreate table
- ✅ Table recreation is safe, but slower for large tables
- ✅ Foreign key constraints enabled by default (Drizzle handles this)

#### PostgreSQL
- ✅ Full `ALTER TABLE` support — changes are online
- ✅ Type casts usually safe (explicit `CAST` syntax supported)
- ⚠️ Long-running `ALTER` may lock table briefly
- ✅ Migrations are versioned and reversible

#### MySQL
- ⚠️ Partial `ALTER TABLE` — some operations trigger table recreation
- ⚠️ Type casts may fail silently (use `CAST` explicitly)
- ⚠️ Foreign key constraints must be managed carefully
- ✅ Online DDL available in MySQL 8.0+

#### Supabase (PostgreSQL + managed features)
- ✅ All PostgreSQL features available
- ⚠️ RLS policies require careful auth context review
- ⚠️ Realtime subscriptions on large tables may impact performance
- ✅ Remote schema introspection available via Supabase API
- ✅ Local migrations sync with `supabase push` / `supabase pull`
- ⚠️ Edge functions deployed via `supabase functions deploy`
- ✅ Can test changes locally before pushing to production

---

## Phase 4: Per-Change Migration Plans

### Scenario: NOT NULL Column Without Default

#### Safe Path (db:push / PostgreSQL / Supabase)
```
Option A (nullable first — most conservative):
  1. Schema: text('col')  [no .notNull()]
  2. db:push
  3. Data: backfill values with SQL or migration script
  4. Schema: text('col').notNull()
  5. db:push

Option B (with default — immediate):
  1. Schema: text('col').notNull().default('')
  2. db:push
  3. All existing rows get '' (or your default)
  ⚠️ Verify '' is acceptable for your use case

Option C (pre-populate — scripted):
  1. Create a migration script that backfills values
  2. Apply script
  3. Schema: text('col').notNull()
  4. db:push
```

#### Supabase-Specific Notes
- Use `supabase migration new [name]` to create custom migration with backfill logic
- Test on staging env: `supabase push --linked` (push to remote staging)
- Then promote to production

---

### Scenario: Column Type Change (PostgreSQL / Supabase)

#### Safe Path (PostgreSQL can auto-cast)
```
PostgreSQL/Supabase:
  1. Schema: Change column type from text to integer
  2. db:push  (generates migration)
  3. Review generated SQL — PostgreSQL will attempt CAST
  4. If migration succeeds: done ✅
  5. If migration fails: review data for non-numeric values, fix, retry

Supabase:
  1. Test on local/staging first:
     supabase migration new change_type_to_integer
     [Edit migration to include: ALTER TABLE ... ALTER COLUMN ... USING CAST(...) ]
  2. Test locally: supabase db reset (or supabase push --linked)
  3. Verify data integrity
  4. Promote to production: supabase push
```

#### SQLite (Requires Table Recreation)

```
SQLite (zero data loss — table recreation):
  1. Add new column with new type: col_new: integer('col_new')
  2. db:push → column added, existing data untouched
  3. Write conversion script: UPDATE table SET col_new = CAST(col AS INTEGER)
  4. Remove original column from schema: delete text('col')
  5. db:push → original column dropped
  6. Rename in schema: col_new → col
  7. db:push → final shape

Note: Step 3 may need custom conversion logic for non-trivial casts
      (e.g., "full-time" → cannot cast to integer → must map manually)
```

---

### Scenario: Rename Column

#### Safe Path (All Dialects via Drizzle)

```
Problem: Drizzle sees rename as DROP old + ADD new → data loss!

Safe path (add column, backfill, drop old):
  1. Schema: Add new_name: text('new_name') [nullable]
  2. db:push
  3. Backfill: UPDATE table SET new_name = old_name
  4. Remove old_name from schema
  5. db:push → old column drops, data preserved ✅
  6. (Optional) Rename in schema: new_name → desired_name
  7. db:push

Supabase note:
  - Wrap steps 1-3 in a single migration: supabase migration new rename_column
  - Test on staging: supabase db reset
  - Then push to production

Alternative for Postgres/Supabase (direct migration):
  - Create manual migration file with: ALTER TABLE table RENAME COLUMN old TO new
  - BUT: also update Drizzle schema to match, or next db:generate will conflict
  - Not recommended — add/backfill/drop is safer and Drizzle-friendly
```

---

### Scenario: Unique Constraint on Existing Data

#### Pre-Check Before Pushing

```
SQL to check for duplicates:
  SELECT [col], COUNT(*) FROM [table]
  GROUP BY [col] HAVING COUNT(*) > 1;

If duplicates found:
  Option A: Remove duplicates (keep latest/earliest)
  Option B: Add unique constraint only to new data (not retroactive)
  Option C: Use nullable column (allow NULL to bypass unique)

After duplicates removed:
  Schema: text('col').unique()
  db:push → constraint added
```

#### Supabase-Specific
- If using managed auth, check `auth.users` table for unique email — already enforced
- For custom tables, test constraint on staging first

---

### Scenario: Add Foreign Key to Existing Column (Supabase / PostgreSQL)

#### Pre-Check for Orphan Rows

```
SQL to check for orphan rows:
  SELECT COUNT(*) FROM [table]
  WHERE [col] NOT IN (SELECT id FROM [referenced_table]);

If orphans found:
  Option A: Delete orphan rows (data loss — review first)
  Option B: Set orphans to NULL (if col is nullable)
  Option C: Update orphans to valid reference
  Option D: Don't add FK constraint (allow data quality drift)

After orphans cleaned:
  Schema: int('col').references(() => other_table.id)
  db:push → FK constraint added

Supabase:
  - RLS policies must permit the JOIN for app code
  - Test ON DELETE / ON UPDATE behavior (CASCADE, SET NULL, RESTRICT)
```

#### SQLite (Requires Table Recreation)
```
SQLite cannot add FK to existing column directly.
Follow same orphan-check process, then:
  1. Schema: int('col').references(() => other_table.id)
  2. db:push → Drizzle recreates table with FK
  3. All data preserved ✅

⚠️ Large tables will be slow during recreation (single-threaded)
```

---

### Scenario: Add/Change CASCADE Behavior (Supabase / PostgreSQL)

#### Before Changing

```
Review current ON DELETE / ON UPDATE clauses:
  - CASCADE: delete child rows when parent deleted
  - SET NULL: set foreign key to NULL
  - RESTRICT: prevent parent deletion if children exist
  - NO ACTION: (default) similar to RESTRICT

Behavioral change example:
  Before: ON DELETE RESTRICT (prevent deletion if children exist)
  After: ON DELETE CASCADE (delete all children too)

  Impact: If parent record deleted, child records silently deleted

Safety checklist:
  ✅ Is cascade the intended behavior?
  ✅ Are there dependent triggers/views that rely on old behavior?
  ✅ Will data loss be acceptable?
  ✅ Test on staging: attempt parent deletion, verify children deleted

After approval:
  Schema: .references(() => parent.id, { onDelete: 'cascade' })
  db:push / supabase push
```

---

### Scenario: Enable Realtime Subscriptions (Supabase)

#### Performance Considerations

```
⚠️ Realtime subscriptions on large tables (1M+ rows) may:
  - Increase latency on INSERT/UPDATE/DELETE
  - Consume more server resources
  - Send unnecessary updates to many clients

Before enabling:
  1. Estimate table size and update frequency
  2. Test on staging with realistic load
  3. Consider filtering subscriptions (WHERE clauses)
  4. Use `realtimeEnabled: true` selectively on tables that benefit

Schema example:
  export const jobs = pgTable('jobs', { ... }, (table) => ({
    realtimeEnabled: true,
  }))

Supabase dashboard:
  - Verify in Supabase project: Database > Replication > Enable for [table]
  - Confirm clients can subscribe: .on('*', callback)
```

---

### Scenario: Add RLS Policy (Supabase)

#### Auth Context Review

```
⚠️ RLS policies require careful auth setup. If policy is wrong, table is inaccessible.

Policy template:
  CREATE POLICY "Users can read own jobs"
  ON jobs FOR SELECT
  USING (auth.uid() = user_id);

Before adding policy:
  ✅ Is `user_id` column present and populated?
  ✅ Is `auth.uid()` available (Supabase Auth enabled)?
  ✅ Will SELECT/INSERT/UPDATE/DELETE still work for expected users?
  ✅ Are service roles (admin) exempted?

Test on staging:
  1. Set up test user in Supabase Auth
  2. Query table as test user (use user's JWT token)
  3. Verify policy allows expected rows, blocks others
  4. Retry as different user — verify isolation
  5. Retry as service role — verify bypass

If policy blocks all access:
  - Disable policy temporarily: ALTER POLICY ... DISABLE
  - Review policy logic
  - Re-enable after fix
```

---

## Phase 5: Command Recommendations

### SQLite (db:push workflow)

```bash
# 1. View pending changes
git diff HEAD -- src/db/schema.ts

# 2. Review with /schema-migrate
/schema-migrate

# 3. If safe changes only:
npm run db:push

# 4. After pushing, update snapshot
npm run db:generate
git add drizzle/
git commit -m "chore(schema): sync migration snapshot"

# 5. If breaking changes:
# — Fix schema first (follow per-change migration plan)
# — Then db:push when ready
```

### PostgreSQL (db:migrate workflow)

```bash
# 1. Review changes
/schema-migrate

# 2. Generate migration from schema diff
npm run db:generate

# 3. Review generated SQL
cat drizzle/[latest-file].sql

# 4. Test migration locally (if possible)
npm run db:migrate

# 5. If migration succeeds:
git add src/db/schema.ts drizzle/
git commit -m "feat(schema): [describe change]"

# 6. Deploy to production (via CI/CD or manual migration)
```

### MySQL (db:migrate workflow + online DDL)

```bash
# 1. Check MySQL version (8.0+ for online DDL)
mysql --version

# 2. Review changes
/schema-migrate

# 3. For large tables, enable online DDL (MySQL 8.0+)
# — Drizzle will use ALGORITHM=INSTANT where possible
# — Some operations still require table rebuild

npm run db:generate

# 4. Review and test
cat drizzle/[latest-file].sql
npm run db:migrate

# 5. Commit
git add src/db/schema.ts drizzle/
git commit -m "feat(schema): [describe change]"
```

### Supabase (db:migrate + supabase CLI workflow)

```bash
# 1. Review changes
/schema-migrate

# 2. Generate migration from schema diff
npm run db:generate

# 3. Review generated migration SQL
cat drizzle/[latest-file].sql

# 4. Create Supabase migration with same changes
supabase migration new [describe_change]
# Edit supabase/migrations/[timestamp]_[describe_change].sql
# Copy SQL from drizzle/[latest-file].sql

# 5. Test on local environment
supabase start
supabase db reset  # or supabase push (to local)

# 6. Test on linked staging environment
supabase link --project-ref=[staging-project]
supabase push --linked

# 7. Verify on staging (Supabase dashboard or API tests)

# 8. Promote to production
supabase link --project-ref=[prod-project]
supabase push --linked

# 9. Commit both schema and migration
git add src/db/schema.ts drizzle/ supabase/migrations/
git commit -m "feat(schema): [describe change]"
```

#### Supabase-Specific Commands

```bash
# Pull remote schema changes (if someone edited via dashboard)
supabase db pull

# Create a custom migration (e.g., backfill data)
supabase migration new backfill_user_emails

# Test migrations locally
supabase db reset
supabase db push  # or supabase push --local

# Check status
supabase status

# Reset to clean state
supabase db reset

# View migration history
ls supabase/migrations/
```

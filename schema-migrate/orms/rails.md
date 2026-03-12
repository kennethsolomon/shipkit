# /schema-migrate — Rails + ActiveRecord Analysis (Phases 2–5)

> This file is loaded by `SKILL.md` when Rails + ActiveRecord is detected.
> Execute Phase 2 through Phase 5 below, then return the final report.

---

## Phase 2: Classify Changes

### Files to Scan (read in parallel)

1. **`Gemfile`** — dependencies
   - Confirm `rails` or `activerecord` gem version
   - Check for `strong_migrations` gem (adds safety checks)
   - Check for database adapter gem: `pg`, `mysql2`, `sqlite3`

2. **`Gemfile.lock`** — locked gem versions for exact version info

3. **`config/database.yml`** — database configuration
   - Extract `adapter:` under `development:` entry
   - Values: `postgresql` | `mysql2` | `sqlite3`

4. **`db/schema.rb`** or **`db/structure.sql`** — current schema state
   - Track: table definitions, column types, indexes, constraints
   - Note: `structure.sql` used when `config.active_record.schema_format = :sql`

5. **`db/migrate/`** — migration history
   - List all migration files sorted by timestamp
   - Read the most recent migration file(s)
   - Compare latest timestamp with `db/schema.rb` version line

6. **`git diff HEAD -- db/migrate/ db/schema.rb`** — uncommitted migration changes

7. **`git log --oneline -5 -- db/migrate/ db/schema.rb`** — recent migration commit history

### Dialect Detection

From `config/database.yml` → `adapter:` under `development:`:

| Adapter | Dialect |
|---------|---------|
| `postgresql` | PostgreSQL |
| `mysql2` | MySQL |
| `sqlite3` | SQLite |
| `trilogy` | MySQL (alternative adapter) |

### Risk Matrix

| Change | Risk | Notes |
|--------|------|-------|
| `create_table` | 🟢 Safe | Additive — no existing data affected |
| `add_column` (nullable, no default) | 🟢 Safe | Standard additive change |
| `add_index` | 🟢 Safe | Non-blocking (unless large table — see PostgreSQL note) |
| `add_column` with default | 🟡 Careful | Existing rows get default — verify acceptability |
| `add_index unique: true` | 🟡 Careful | Fails if duplicate values exist |
| `add_reference` / `add_foreign_key` | 🟡 Careful | Orphan row check; MySQL online DDL |
| `add_column` NOT NULL without default | 🔴 Breaking | Existing rows need a value — migration fails |
| `change_column` (type change) | 🔴 Breaking | SQLite: no ALTER; PostgreSQL: CAST required |
| `remove_column` | 🔴 Breaking | Check model usage — `$casts`, queries, serializers |
| `drop_table` | 🔴 Breaking | Destructive — check all model and FK references |
| `rename_column` | 🟡 Careful | Safe in modern Rails; update model attribute too |
| `rename_table` | 🟡 Careful | Update `self.table_name` in model + all references |

### Also Detect

- ⚠️ **`schema.rb` version drift**: `ActiveRecord::Schema[X.Y].define(version: TIMESTAMP)` version doesn't match latest migration timestamp
- ⚠️ **Missing `down` on `def up` migrations**: Old-style `def up` / `def down` with empty `down` — rollback does nothing
- ⚠️ **MySQL strict mode warnings**: Adding column with large default on a table with many rows → metadata lock risk
- ⚠️ **`strong_migrations` gem detected**: Certain operations require `safety_assured { }` wrapper — flag which operations need it
- ⚠️ **PostgreSQL large table index**: Adding `add_index` without `algorithm: :concurrently` will lock the table

---

## Phase 3: Present Risk Report

### Report Format

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  /schema-migrate — Schema Change Analysis
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ORM:              Rails + ActiveRecord
Dialect:          PostgreSQL
Workflow:         rails db:migrate (versioned migrations)
Migrations dir:   db/migrate/
Schema file:      db/schema.rb (version: 20250228120000)

Status:
  📁 Migration history: IN SYNC with schema.rb
  📝 Pending: 1 uncommitted migration
  🔧 strong_migrations: NOT DETECTED

Detected Changes (since last commit):
──────────────────────────────────────────

🟢 SAFE (1 change)
  • jobs: add_column :applied_notes, :text (nullable)

🟡 CAREFUL (1 change — review before migrating)
  • profile: add_column :email, :string, default: '', null: false
    ↳ All existing rows will get empty string value
    ↳ Is '' an acceptable default? Consider nullable: true first.

🔴 BREAKING (1 change — stop and read migration plan)
  • jobs: change_column :job_type, :string → :integer
    ↳ PostgreSQL: requires USING cast
    ↳ SQLite: no ALTER support — table recreation required
    ↳ Review migration SQL before applying

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Dialect-Specific Notes

#### PostgreSQL
- ✅ Full ALTER TABLE support — most changes are online
- ⚠️ `change_column` for type changes may need explicit USING cast
- ⚠️ Adding `add_index` on large tables without `algorithm: :concurrently` will lock table
- ✅ `rename_column` is safe and fast (metadata-only change)

#### MySQL
- ⚠️ Online DDL available for MySQL 8.0+ (ALGORITHM=INPLACE for many operations)
- ⚠️ Adding column with large default on large tables may hold metadata lock
- ⚠️ MySQL strict mode: invalid data rejected rather than silently truncated

#### SQLite
- 🚨 No `change_column` support — requires table recreation workaround
- 🚨 No `rename_column` support in older SQLite (< 3.25) — Rails handles via `pragma_columns`
- ✅ Rails handles SQLite table recreation via `change_table` where possible

---

## Phase 4: Per-Change Migration Plans

### Scenario: `rename_column` — Zero-Downtime

```
Modern Rails (6.1+): rename_column is safe — atomic metadata rename.

Zero-downtime pattern for live systems:
  Step 1: Add alias (ignore_columns + new attribute)
    - app/models/user.rb: alias_attribute :new_name, :old_name
    - Deploy code that uses new_name (reads from old_name via alias)

  Step 2: Rename in migration
    rename_column :users, :old_name, :new_name

  Step 3: Remove alias after rename is stable
    - Remove alias_attribute line
    - Update any remaining references to old_name

After rename:
  ✅ Check model: attr_accessor, validates, scopes using old name
  ✅ Check serializers, API resources
  ✅ Check named scopes: where(old_name: ...)
  ✅ Run full test suite
```

---

### Scenario: `add_column` NOT NULL Without Default

```
Problem: Existing rows have no value → migration fails with NOT NULL constraint.

Safe path (nullable-first):
  Step 1: Add nullable column
    add_column :users, :email, :string  # nullable by default

  Step 2: Backfill data
    User.in_batches.update_all(email: '')
    # Or in migration: execute("UPDATE users SET email = '' WHERE email IS NULL")

  Step 3: Add NOT NULL constraint
    change_column_null :users, :email, false

Alternative (with default — single migration):
  add_column :users, :email, :string, default: '', null: false
  ⚠️ All existing rows get '' — verify this is acceptable

With strong_migrations gem:
  safety_assured do
    add_column :users, :email, :string, null: false, default: ''
  end
```

---

### Scenario: `change_column` Type Change

```
PostgreSQL — Review CAST:
  # Rails generates: ALTER TABLE jobs ALTER COLUMN job_type TYPE integer
  # May fail if data contains non-integer strings

  # Add explicit CAST in migration:
  execute <<~SQL
    ALTER TABLE jobs
    ALTER COLUMN job_type TYPE integer
    USING job_type::integer
  SQL

  # Pre-check for non-castable data:
  # SELECT job_type FROM jobs WHERE job_type !~ '^[0-9]+$';

SQLite — No ALTER support, use workaround:
  # Create new column, copy data, drop old, rename
  def up
    add_column :jobs, :job_type_int, :integer
    execute("UPDATE jobs SET job_type_int = CAST(job_type AS INTEGER)")
    remove_column :jobs, :job_type
    rename_column :jobs, :job_type_int, :job_type
  end

  def down
    add_column :jobs, :job_type_str, :string
    execute("UPDATE jobs SET job_type_str = CAST(job_type AS TEXT)")
    remove_column :jobs, :job_type
    rename_column :jobs, :job_type_str, :job_type
  end
```

---

### Scenario: Large Table Index on PostgreSQL

```
Problem: add_index on a large PostgreSQL table locks the table for writes
         during index creation.

Fix: Use concurrent index creation

  def change
    disable_ddl_transaction!  # ← required for concurrent indexes
    add_index :jobs, :status, algorithm: :concurrently
  end

Rules:
  ✅ disable_ddl_transaction! must be the first line in change/up
  ✅ algorithm: :concurrently only works outside of transactions
  ✅ Cannot be combined with other migration operations in same file
  ⚠️ May leave invalid index if cancelled — check with \di in psql

Cleanup invalid index:
  REINDEX INDEX CONCURRENTLY jobs_status_idx;
  # or
  DROP INDEX CONCURRENTLY jobs_status_idx;
```

---

### Scenario: `strong_migrations` Gem Detected

```
If strong_migrations gem is present in Gemfile:

Unsafe operations are blocked by default. To bypass:
  safety_assured do
    # your unsafe operation here
  end

Operations that require safety_assured:
  - add_column with NOT NULL and no default (use nullable-first instead)
  - change_column (use separate steps)
  - add_index without algorithm: :concurrently (on large tables)
  - rename_column / rename_table (use alias pattern)
  - remove_column (ensure ActiveRecord ignores column before removing)

Best practice: Fix the underlying issue rather than using safety_assured.
strong_migrations provides the correct safe pattern in its error message.
```

---

## Phase 5: Command Recommendations

### Core Commands

```bash
# Check migration status
rails db:migrate:status

# Run pending migrations
rails db:migrate

# Rollback last migration
rails db:rollback STEP=1

# Rollback to specific version
rails db:migrate:down VERSION=[timestamp]

# Check current schema version
rails db:version

# Generate new migration
rails generate migration [MigrationName] [optional_columns]
rails generate migration AddEmailToUsers email:string:uniq
rails generate migration CreateJobs title:string status:string

# Reset database (dev only — DESTRUCTIVE)
rails db:reset    # drop + create + schema + seed
rails db:drop && rails db:create && rails db:migrate && rails db:seed
```

### Workflow: Development

```bash
# 1. Review pending migrations
/schema-migrate

# 2. Preview migration (check db/schema.rb after migrate on test db)
RAILS_ENV=test rails db:migrate

# 3. Apply to development
rails db:migrate

# 4. Verify status
rails db:migrate:status

# 5. Run tests
bundle exec rspec  # or: rails test

# 6. Commit
git add db/migrate/ db/schema.rb
git commit -m "feat(schema): [describe change]"
```

### Workflow: PostgreSQL — Concurrent Indexes

```bash
# Migration file must have disable_ddl_transaction! + algorithm: :concurrently
# See Scenario: Large Table Index above

rails db:migrate
# Monitor with: SELECT * FROM pg_stat_progress_create_index;
```

### Workflow: Production Deployment

```bash
# 1. Migrations committed and reviewed
# 2. Check status before deploying
rails db:migrate:status

# 3. Apply (in deployment script or Capistrano task)
rails db:migrate RAILS_ENV=production

# 4. Verify
rails db:version RAILS_ENV=production
```

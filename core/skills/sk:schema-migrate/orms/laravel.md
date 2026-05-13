# /schema-migrate — Laravel + Eloquent Analysis (Phases 2–5)

> This file is loaded by `SKILL.md` when Laravel ORM is detected.
> Execute Phase 2 through Phase 5 below, then return the final report.

---

## Phase 2: Classify Changes

### Files to Scan (read in parallel)

1. **`composer.json`** — framework and package versions
   - Confirm `laravel/framework` version
   - Check for `doctrine/dbal` (required for column renames on MySQL < 8.0)

2. **`.env`** — environment config
   - Extract `DB_CONNECTION`: `mysql` | `pgsql` | `sqlite`
   - Extract `DB_HOST`, `DB_DATABASE` for context

3. **`config/database.php`** — database configuration
   - Fallback if `.env` unreadable
   - Read `default` connection key

4. **`database/migrations/*.php`** — migration files
   - List all files sorted by timestamp
   - Read the most recent migration(s) for pending changes

5. **`app/Models/`** — Eloquent model files
   - Check `$table`, `$casts`, `$fillable`, `$guarded` properties
   - Identify models affected by pending migration changes

6. **`git diff HEAD -- database/migrations/`** — uncommitted migration changes

7. **`git log --oneline -5 -- database/migrations/`** — recent migration commit history

### Dialect Detection

From `.env` `DB_CONNECTION` or `config/database.php`:

| Value | Dialect |
|-------|---------|
| `mysql` | MySQL |
| `pgsql` | PostgreSQL |
| `sqlite` | SQLite |
| `sqlsrv` | SQL Server |

Default if undetectable: MySQL

### Risk Matrix

| Change | Risk | Notes |
|--------|------|-------|
| Add new table (`Schema::create`) | 🟢 Safe | Additive — no existing data affected |
| Add nullable column (`->nullable()`) | 🟢 Safe | Standard additive change |
| Add index (`->index()`) | 🟢 Safe | Non-blocking for most engines |
| Add column with default (`->default(value)`) | 🟡 Careful | Existing rows get default value — verify acceptability |
| Add unique index (`->unique()`) | 🟡 Careful | Fails if duplicate values exist |
| Add FK constraint | 🟡 Careful | Orphan row check required; MySQL online DDL |
| Add NOT NULL column without default | 🔴 Breaking | Existing rows have no value → migration fails |
| Change column type (`->change()`) | 🔴 Breaking | MySQL online DDL; SQLite: table recreation required |
| Drop column (`->dropColumn()`) | 🔴 Breaking | Check model `$casts`, `$fillable`, queries |
| Drop table (`Schema::drop`) | 🔴 Breaking | Check all model references and FK constraints |
| Rename column (`->renameColumn()`) | 🔴 Breaking | Requires `doctrine/dbal` on MySQL < 8.0 |
| Rename table (`Schema::rename`) | 🟡 Careful | Update model `$table` property and any hardcoded references |

### Also Detect

- ⚠️ **Missing `down()` method**: Migration has empty `down()` — rollback silently does nothing
- ⚠️ **Missing `Schema::disableForeignKeyConstraints()`**: MySQL drops with FK constraints will fail without this wrapper
- ⚠️ **SQLite ALTER TABLE limitations**: SQLite does not support most column modifications — requires table recreation
- ⚠️ **Missing `doctrine/dbal`**: `renameColumn()` / `change()` on MySQL < 8.0 requires this package

---

## Phase 3: Present Risk Report

### Report Format

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  /schema-migrate — Schema Change Analysis
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ORM:              Laravel + Eloquent
Dialect:          MySQL 8.0+
Workflow:         php artisan migrate (versioned migrations)
Migrations dir:   database/migrations/
Last migration:   2025_02_28_120000_add_applied_notes_to_jobs_table

Status:
  📁 Migration files: COMMITTED
  📝 Pending: 1 uncommitted migration
  🔧 doctrine/dbal: INSTALLED ✅

Detected Changes (since last commit):
──────────────────────────────────────────

🟢 SAFE (1 change)
  • jobs: Added nullable column `applied_notes` (text, nullable)

🟡 CAREFUL (1 change — review before migrating)
  • profile: Added column `email` (string, NOT NULL, default: '')
    ↳ All existing rows will get empty string value
    ↳ Is '' an acceptable default? Consider nullable first.

🔴 BREAKING (1 change — stop and read migration plan)
  • jobs: Column `job_type` changed from string → integer
    ↳ MySQL online DDL will attempt MODIFY COLUMN
    ↳ Review for silent truncation or cast failures
    ↳ Test with --pretend first

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Dialect-Specific Notes

#### MySQL
- ✅ Online DDL available in MySQL 8.0+ (ALGORITHM=INPLACE for many operations)
- ⚠️ `renameColumn()` and `change()` require `doctrine/dbal` on MySQL < 8.0
- ⚠️ FK drops require `Schema::disableForeignKeyConstraints()` wrapper
- ⚠️ Strict mode warnings: large table defaults may trigger metadata lock

#### PostgreSQL
- ✅ Full ALTER TABLE support — most changes are online
- ✅ Column type changes generally safe with implicit casts
- ⚠️ Long-running ALTER may briefly lock large tables

#### SQLite
- 🚨 Cannot rename columns or change column types directly
- 🚨 Must recreate table via raw SQL in migration (see Scenario below)
- ✅ All other additive changes work normally

---

## Phase 4: Per-Change Migration Plans

### Scenario: Add NOT NULL Column Without Default

```
Problem: Existing rows have no value for the new column → migration fails.

Safe path (nullable-first deploy):
  Step 1: Create migration with nullable column
    $table->string('email')->nullable();
    php artisan migrate

  Step 2: Backfill existing rows
    DB::table('users')->whereNull('email')->update(['email' => '']);
    # Or use a separate data migration

  Step 3: Create second migration to add NOT NULL constraint
    $table->string('email')->nullable(false)->change();
    php artisan migrate

Alternative (with default — single migration):
  $table->string('email')->default('');
  php artisan migrate
  ⚠️ All existing rows get '' — verify this is acceptable
```

---

### Scenario: Rename Column

```
Check doctrine/dbal requirement:
  MySQL < 8.0: composer require doctrine/dbal --dev
  MySQL 8.0+: Native rename support (no doctrine/dbal needed)
  PostgreSQL: Native rename support
  SQLite: Not supported — requires table recreation (see below)

Migration:
  $table->renameColumn('old_name', 'new_name');

After migrating:
  ✅ Update model $casts, $fillable, $guarded arrays
  ✅ Search codebase for 'old_name' string references
  ✅ Update any API resources / form requests referencing the old name

Zero-downtime rename (for production with live traffic):
  Step 1: Add new column (nullable): $table->string('new_name')->nullable();
  Step 2: Deploy code that writes to both old_name AND new_name
  Step 3: Backfill: UPDATE table SET new_name = old_name WHERE new_name IS NULL;
  Step 4: Deploy code that reads from new_name only
  Step 5: Remove old_name column in final migration
```

---

### Scenario: SQLite Destructive Change (Column Type / Rename)

```
SQLite does not support ALTER COLUMN — must recreate the table.

Migration template using raw SQL:
  public function up(): void
  {
      // 1. Create new table with desired schema
      DB::statement('CREATE TABLE users_new (
          id INTEGER PRIMARY KEY,
          name TEXT NOT NULL,
          new_column INTEGER NOT NULL DEFAULT 0,  -- changed type
          created_at DATETIME,
          updated_at DATETIME
      )');

      // 2. Copy data from old table
      DB::statement('INSERT INTO users_new (id, name, new_column, created_at, updated_at)
          SELECT id, name, CAST(old_column AS INTEGER), created_at, updated_at
          FROM users');

      // 3. Drop old table
      Schema::drop('users');

      // 4. Rename new table
      DB::statement('ALTER TABLE users_new RENAME TO users');
  }

  public function down(): void
  {
      // Reverse the process with original schema
  }
```

---

### Scenario: Missing `down()` Method

```
Problem: Laravel's rollback calls down() — if it's empty, rollback silently does nothing.

Detection: Check if down() is empty (just {}) or missing.

Template for correct down() methods:

  // For: $table->string('new_column')
  // Down should be:
  public function down(): void
  {
      Schema::table('users', function (Blueprint $table) {
          $table->dropColumn('new_column');
      });
  }

  // For: Schema::create('new_table', ...)
  // Down should be:
  public function down(): void
  {
      Schema::dropIfExists('new_table');
  }

  // For: $table->renameColumn('old', 'new')
  // Down should be:
  public function down(): void
  {
      Schema::table('users', function (Blueprint $table) {
          $table->renameColumn('new', 'old');
      });
  }
```

---

### Scenario: FK Constraint Ordering Issue

```
Detection: A migration creates a FK reference to a table that is created
           in a LATER migration file (by timestamp).

Example:
  2025_01_01_000000_create_posts_table.php → references users.id
  2025_01_01_000001_create_users_table.php → creates users table

This will fail because posts FK references users before users exists.

Fix options:
  Option A: Rename migration files to fix timestamp ordering
    - Change 2025_01_01_000000_create_posts_table.php to a later timestamp

  Option B: Split FK creation into separate migration
    - Create posts table without FK first
    - Add FK in a third migration after users table migration

  Option C: Add FK in the users migration
    - After creating users table, add FK to posts in same migration file
```

---

## Phase 5: Command Recommendations

### Core Commands

```bash
# Check migration status
php artisan migrate:status

# Run pending migrations
php artisan migrate

# Preview SQL without executing (dry run)
php artisan migrate --pretend

# Rollback last batch of migrations
php artisan migrate:rollback --step=1

# Roll back a specific migration
php artisan migrate:rollback --step=1

# Roll back to specific migration version
php artisan migrate:down --path=database/migrations/[filename].php

# Check current migration version
php artisan migrate:status

# Create a new migration file
php artisan make:migration [describe_change] --table=[table_name]
php artisan make:migration create_[table_name]_table

# Reset all migrations and re-run (dev only — DESTRUCTIVE)
php artisan migrate:fresh
php artisan migrate:fresh --seed  # with seeders
```

### Workflow: Development

```bash
# 1. Review pending migrations
/schema-migrate

# 2. Preview SQL (dry run)
php artisan migrate --pretend

# 3. If SQL looks correct, apply
php artisan migrate

# 4. Verify status
php artisan migrate:status

# 5. Commit
git add database/migrations/
git commit -m "feat(schema): [describe change]"
```

### Workflow: MySQL — Column Changes

```bash
# Check doctrine/dbal for rename/change operations
composer show doctrine/dbal  # must be installed for MySQL < 8.0

# Preview change
php artisan migrate --pretend

# Apply
php artisan migrate
```

### Workflow: SQLite — Destructive Changes

```bash
# SQLite: always use raw SQL for column type changes or renames
# See Scenario: SQLite Destructive Change above

# After writing raw SQL migration:
php artisan migrate --pretend  # verify SQL output
php artisan migrate            # apply
```

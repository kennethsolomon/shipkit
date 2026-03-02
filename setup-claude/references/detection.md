# Stack Detection Heuristics

Reference for Phase 2 detection logic in `/setup-claude`.

---

## Language & Framework Detection

### Node.js / JavaScript (parse `package.json`)

```javascript
const deps = { ...packageJson.dependencies, ...packageJson.devDependencies };

// Frameworks
const hasNext    = !!deps["next"];
const hasReact   = !!deps["react"] && !hasNext;
const hasExpress = !!deps["express"];
const hasRemix   = !!deps["@remix-run/node"];
const hasNuxt    = !!deps["nuxt"];
const hasAstro   = !!deps["astro"];
const hasSvelte  = !!deps["svelte"] || !!deps["@sveltejs/kit"];
const hasVue     = !!deps["vue"] || !!deps["@vue/core"];

// Language
const isTypeScript = fileExists("tsconfig.json") || hasDep("typescript");
const language = isTypeScript ? "TypeScript" : "JavaScript";
```

### PHP (parse `composer.json`)

```javascript
const phpDeps = composerJson.require || {};

const hasLaravel  = !!phpDeps["laravel/framework"];
const hasSymfony  = !!phpDeps["symfony/console"];
const hasWordPress = !!phpDeps["wordpress/core"] || fileExists("wp-config.php");

const language = "PHP";

// Laravel DB detection (from .env or config/database.php)
const laravelDb = envVar("DB_CONNECTION") || "mysql";
// "mysql" | "pgsql" | "sqlite"
// SQLite path: database/database.sqlite
```

### Python (parse `pyproject.toml` or `requirements.txt`)

```javascript
const hasFastAPI    = pythonDeps["fastapi"];
const hasDjango     = pythonDeps["django"];
const hasFlask      = pythonDeps["flask"];
const hasSQLAlchemy = pythonDeps["sqlalchemy"];
const hasAlembic    = pythonDeps["alembic"];

const language = "Python";
```

### Go (parse `go.mod`)

```javascript
// Read module name from go.mod first line
// Detect frameworks from imports in main files
const hasGin  = goImports["github.com/gin-gonic/gin"];
const hasFiber = goImports["github.com/gofiber/fiber"];
const hasEcho  = goImports["github.com/labstack/echo"];

const language = "Go";
```

### Ruby (parse `Gemfile`)

```javascript
const hasRails   = gemDeps["rails"];
const hasSinatra = gemDeps["sinatra"];
const hasActiveRecord = gemDeps["activerecord"];

const language = "Ruby";
```

---

## Database Detection

```javascript
// Node.js deps
const hasDrizzle     = !!deps["drizzle-orm"];
const hasSqlite      = !!deps["better-sqlite3"] || !!deps["sqlite3"];
const hasPg          = !!deps["pg"] || !!deps["postgres"];
const hasPrisma      = !!deps["prisma"] || !!deps["@prisma/client"];
const hasMongoose    = !!deps["mongoose"];
const hasTypeORM     = !!deps["typeorm"];

// Python
const hasSQLAlchemy  = pythonDeps["sqlalchemy"];

// Supabase (FRAMEWORK-AGNOSTIC — check across all languages)
const hasSupabase =
  !!deps["@supabase/supabase-js"] ||
  !!deps["supabase-js"] ||
  fileExists("supabase/config.toml") ||
  (fileExists(".env.local") && envContains("SUPABASE_URL")) ||
  (fileExists(".env") && envContains("SUPABASE_URL"));
```

**Key insight:** Supabase can be used with ANY framework. Detection must always be framework-agnostic.

---

## UI Framework Detection

```javascript
const hasTailwind = !!deps["tailwindcss"];
const hasShadcn   = !!deps["@shadcn/ui"] || dirExists("src/components/ui/");
const hasRadix    = Object.keys(deps).some(k => k.startsWith("@radix-ui/"));
const hasBootstrap = !!deps["bootstrap"];
const hasMUI      = !!deps["@mui/material"];
const hasChakra   = !!deps["@chakra-ui/react"];
```

---

## Other Tools Detection

```javascript
// Testing
const hasVitest    = !!deps["vitest"];
const hasJest      = !!deps["jest"];
const hasPlaywright = !!deps["@playwright/test"] || !!deps["playwright"];
const hasPytest    = pythonDeps["pytest"];

// AI / LLM
const hasOpenAI    = !!deps["openai"] || pythonDeps["openai"];
const hasAnthropic = !!deps["@anthropic-ai/sdk"] || pythonDeps["anthropic"];
const hasLangChain = !!deps["langchain"] || pythonDeps["langchain"];

// Auth
const hasAuthJs    = !!deps["next-auth"] || !!deps["@auth/core"];
const hasClerk     = !!deps["@clerk/nextjs"] || !!deps["@clerk/clerk-sdk-node"];
const hasSupabaseAuth = hasSupabase; // Supabase includes auth
const hasDevise    = gemDeps["devise"]; // Ruby/Rails

// Browser Automation
const hasPuppeteer = !!deps["puppeteer"];
const hasSelenium  = !!deps["selenium-webdriver"];
```

---

## Build & Run Command Extraction

```javascript
// From package.json scripts
const scripts = packageJson.scripts || {};
const devCmd   = scripts.dev   || scripts.start  || "npm run dev";
const buildCmd = scripts.build || "npm run build";
const lintCmd  = scripts.lint  || "npm run lint";
const testCmd  = scripts.test  ? `npm run test` : null;

// Python
const devCmd   = "uvicorn app.main:app --reload" or "python manage.py runserver";
const buildCmd = null; // usually no build step
const testCmd  = "pytest";

// Laravel
const devCmd   = "php artisan serve";
const buildCmd = scripts.build ? "npm run build" : null; // if has package.json for assets
const testCmd  = "php artisan test";
```

---

## Arch Log Directory Detection

```javascript
// Phase 2 — check BEFORE generating any file that references this path
const TYPO_DIR   = ".claude/docs/achritectural_change_log";
const CORRECT_DIR = ".claude/docs/architectural_change_log";

const ARCH_LOG_DIR = dirExists(TYPO_DIR) ? TYPO_DIR : CORRECT_DIR;

// All generated files use [ARCH_LOG_DIR] placeholder filled with this value
```

**Why:** Some projects were created with the typo `achritectural_change_log`. Always detect which exists and reference it consistently — never create a new dir if the typo one exists.

---

## Template Selection Logic

| Detected Stack | finish-feature Template |
|----------------|------------------------|
| Next.js + Supabase | "Next.js + Supabase" |
| Next.js + Drizzle ORM | "Next.js + Drizzle ORM" |
| Next.js + Prisma | "Next.js + Prisma" |
| Laravel + MySQL/Postgres/SQLite | "Laravel + Eloquent ORM" |
| Supabase + non-Next.js (Laravel, FastAPI, Rails) | "Supabase (Any Framework)" |
| Python + FastAPI + SQLAlchemy | "Python + FastAPI + SQLAlchemy" |
| Any other stack | "Generic / Minimal Stack" |

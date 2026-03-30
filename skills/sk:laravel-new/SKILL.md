---
name: sk:laravel-new
description: "Scaffold a fresh Laravel app and configure it with opinionated production-ready conventions. Usage: /laravel-new [project-name]"
---

# /laravel-new

Scaffold a fresh Laravel application and immediately configure it with production-ready conventions.

## Steps

### 1. Get Project Name
If no argument was provided, ask: "What should the project be named?"

### 2. Check Prerequisites
Verify these are available:
```bash
which composer
which laravel  # or: composer global show laravel/installer
```
If `laravel` installer is missing: `composer global require laravel/installer`

### 3. Scaffold the App
```bash
laravel new {{PROJECT_NAME}}
```

When prompted by the Laravel installer:
- Starter kit: choose based on user preference (ask if not specified — Inertia+React, Inertia+Vue, Livewire, or None/API)
- Testing framework: **Pest** (always)
- Database: ask user (default: SQLite for local dev)
- Run migrations: yes

### 4. Enter the Project Directory
```bash
cd {{PROJECT_NAME}}
```

### 5. Run /laravel-init
Immediately invoke the `setup-claude` skill to configure the project:
- Detect stack from what was just installed
- Install missing dev tools (PHPStan/Larastan, Rector, Pint)
- Publish config files
- Configure strict models
- Generate CLAUDE.md
- Bootstrap tasks/ files

### 6. Report
Show a summary:
```
Project: {{PROJECT_NAME}}
Stack: [detected]
Location: [path]

Files created:
  CLAUDE.md
  .mcp.json (laravel-boost MCP server)
  phpstan.neon
  rector.php
  pint.json
  tasks/findings.md (pre-seeded)
  tasks/lessons.md
  tasks/todo.md
  tasks/progress.md
  .claude/commands/sk:lint.md
  .claude/commands/sk:test.md

Next step: /sk:brainstorm
```

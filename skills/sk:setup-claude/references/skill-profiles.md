# ShipKit Skill Profiles — Stack-Based Filtering

**Last Updated:** 2026-03-30
**Total Skills:** 44 | **Agents:** 13 | **Rules:** 6 | **Project MCP:** 1

This file is the source of truth for which skills, agents, rules, and project-level MCP servers get installed per project. Read by `sk:setup-claude` (initial setup) and `sk:setup-optimizer` (ongoing sync).

---

## Universal Skills (always installed — 25 skills)

| Skill | Purpose |
|-------|---------|
| sk:start | Smart entry point — classifies task, routes to workflow |
| sk:context | Load project context + session brief |
| sk:brainstorm | Explore requirements before implementation |
| sk:write-plan | Decision-complete plan into todo.md |
| sk:execute-plan | Implement tasks in batches with progress logging |
| sk:write-tests | TDD: write failing tests before implementation |
| sk:test | Run all test suites, verify 100% coverage |
| sk:lint | Auto-detect and run all linters |
| sk:debug | Structured bug investigation |
| sk:review | 7-dimension self-review |
| sk:smart-commit | Conventional commit with approval |
| sk:gates | All quality gates in parallel batches |
| sk:safety-guard | Protect against destructive operations |
| sk:scope-check | Detect scope creep vs plan |
| sk:save-session | Save session state for continuity |
| sk:resume-session | Restore previously saved session |
| sk:learn | Extract reusable patterns from session |
| sk:retro | Post-ship retrospective |
| sk:health | Harness self-audit scorecard |
| sk:context-budget | Audit context window token consumption |
| sk:setup-claude | Bootstrap project scaffolding |
| sk:setup-optimizer | Diagnose + update workflow + enrich CLAUDE.md |
| sk:release | Version bump + changelog + tag |
| sk:fast-track | Abbreviated workflow for small changes |
| sk:skill-creator | Create or modify skills |

---

## Stack-Specific Skills

### Laravel (+4 skills)

| Skill | Purpose |
|-------|---------|
| sk:laravel-new | Scaffold fresh Laravel app |
| sk:laravel-init | Configure existing Laravel project |
| sk:laravel-deploy | Deploy to Laravel Cloud |
| sk:schema-migrate | Multi-ORM schema change analysis |

### Web (+5 skills)

| Skill | Purpose |
|-------|---------|
| sk:frontend-design | UI mockup before implementation |
| sk:accessibility | WCAG 2.1 AA audit |
| sk:seo-audit | SEO audit (source + dev server) |
| sk:website | Build multi-page marketing website |
| sk:mvp | Generate MVP with landing page + app |

### Database (+1 skill)

| Skill | Purpose |
|-------|---------|
| sk:schema-migrate | Multi-ORM schema change analysis |

### API (+2 skills)

| Skill | Purpose |
|-------|---------|
| sk:api-design | Design API contracts before implementation |
| sk:team | Parallel domain agents (BE + FE + QA) |

### Mobile (exclude from web)

No additional skills. **Exclude:** sk:e2e (Playwright), sk:seo-audit, sk:accessibility, sk:website.

---

## Opt-In Skills (manual activation only — 8 skills)

| Skill | Purpose | When to activate |
|-------|---------|-----------------|
| sk:autopilot | Hands-free workflow, all 8 steps | Well-defined tasks, minimal steering |
| sk:eval | Run evaluations for agent reliability | Eval-driven development |
| sk:ci | Set up GitHub Actions or GitLab CI | First-time CI setup |
| sk:reverse-doc | Generate docs from existing code | Onboarding, formalizing prototypes |
| sk:features | Sync feature specs with implementation | Feature spec maintenance |
| sk:e2e | E2E behavioral verification | Web projects with Playwright/Cypress |
| sk:dashboard | Workflow Kanban board (localhost) | Multi-worktree progress tracking |
| sk:plugin | Package skills as distributable plugin | Team skill sharing |

---

## Quality Gate Skills (part of sk:gates — always installed)

| Skill | Gate role |
|-------|----------|
| sk:perf | Performance audit |
| sk:security-check | OWASP security audit |

These are installed universally because they run inside `sk:gates`. Perf auto-skips if no frontend+DB keywords. Security always runs.

---

## Stack Detection Rules

| Priority | Signal | Detected Stack | Capabilities |
|----------|--------|---------------|-------------|
| 1 | `composer.json` + `laravel/framework` | laravel | web, database, api |
| 2 | `package.json` + `next` | nextjs | web |
| 3 | `package.json` + `nuxt` | nuxt | web |
| 4 | `package.json` + `react` (no next) | react | web |
| 5 | `package.json` + `vue` (no nuxt) | vue | web |
| 6 | `package.json` + `svelte` | svelte | web |
| 7 | `app.json` or `app.config.ts` | expo | mobile |
| 8 | `react-native.config.js` | react-native | mobile |
| 9 | `pubspec.yaml` | flutter | mobile |
| 10 | `package.json` + `express` | express | api |
| 11 | `go.mod` | go | api |
| 12 | `Cargo.toml` | rust | api |
| 13 | `pyproject.toml` / `requirements.txt` | python | api |
| 14 | `Gemfile` + `rails` | rails | web, database, api |

### Capability → Add-on mapping

| Capability | Add-on skills |
|-----------|---------------|
| web | sk:frontend-design, sk:accessibility, sk:seo-audit, sk:website, sk:mvp |
| database | sk:schema-migrate |
| api | sk:api-design, sk:team |
| laravel | sk:laravel-new, sk:laravel-init, sk:laravel-deploy |
| mobile | Exclude: sk:e2e, sk:seo-audit, sk:accessibility, sk:website |

### Database sub-detection (within any stack)

| Signal | ORM |
|--------|-----|
| `prisma/schema.prisma` | Prisma → add `database` capability |
| `drizzle.config.ts` / `.js` | Drizzle → add `database` capability |
| `database/migrations/` (Laravel) | Laravel migrations → add `database` capability |
| `alembic/` | SQLAlchemy → add `database` capability |
| `db/migrate/` (Rails) | Rails migrations → add `database` capability |

---

## Agent → Stack Mapping

| Agent | Stacks | Notes |
|-------|--------|-------|
| architect | all | System design, universal |
| backend-dev | laravel, express, go, python, rust, rails | Backend implementation |
| frontend-dev | react, nextjs, vue, nuxt, svelte | Frontend implementation |
| mobile-dev | expo, react-native, flutter | Mobile-specific |
| database-architect | any with `database` capability | Schema design, migrations |
| qa-engineer | all | E2E test scenarios, universal |
| debugger | all | Bug investigation, universal |
| code-reviewer | all | Code quality review, universal |
| security-reviewer | all | OWASP audit, universal |
| performance-optimizer | all | Performance analysis, universal |
| refactor-specialist | all | Safe refactoring, universal |
| tech-writer | all | Documentation, universal |
| doc-reviewer | all | Documentation review, universal |
| devops-engineer | all | CI/CD, deployment, universal |

---

## Rule → Stack Mapping

| Rule | Applies to stacks | Path patterns |
|------|------------------|---------------|
| tests.md | all | `tests/**`, `**/*.test.*`, `**/*.spec.*` |
| api.md | laravel, express, go, python, rails | `routes/api.php`, `**/controllers/**`, `src/api/**` |
| laravel.md | laravel | `app/**/*.php`, `routes/**`, `config/**` |
| react.md | react, nextjs | `**/*.{tsx,jsx}`, `resources/js/**` |
| vue.md | vue, nuxt | `**/*.vue`, `resources/js/**` |
| migrations.md | any with `database` capability | `database/migrations/**`, `prisma/**`, `db/migrate/**` |

---

## Project-Level MCP Server → Stack Mapping

MCP servers configured in the project's `.mcp.json` (not global `~/.mcp.json`). Managed by `sk:setup-claude` (initial setup) and `sk:setup-optimizer` (ongoing sync).

| MCP Server | Stack | Command | Purpose |
|-----------|-------|---------|---------|
| laravel-boost | laravel | `php artisan boost:mcp` (or `vendor/bin/sail artisan boost:mcp` for Sail) | Database schema, queries, docs search, logs, browser errors |

**Sync rules:**
- **Add** to `.mcp.json` when stack matches and entry is missing
- **Remove** from `.mcp.json` when stack no longer matches (e.g., project switched from Laravel to Next.js)
- **Update** existing entry if command is stale (e.g., Sail added/removed — switch between `php` and `vendor/bin/sail`)
- Never touch MCP entries not in this table (user-added entries are preserved)
- Sail detection: use `vendor/bin/sail` command variant if `vendor/bin/sail` exists
- **Ownership:** Project-level MCP is managed by `sk:setup-claude` (initial) and `sk:setup-optimizer` Step 0.5 (ongoing). Step 1.7 handles only global MCP.

---

## Installation Formula

For a given project with detected `stack` and `capabilities`:

```
installed_skills = universal_skills
                 + capability_add_ons(capabilities)
                 + config.skills.extra
                 - config.skills.disabled
                 - mobile_exclusions (if mobile stack)

installed_agents = universal_agents
                 + stack_specific_agents(stack)
                 - agents not matching any detected stack

installed_rules  = universal_rules (tests.md)
                 + stack_matching_rules(stack, capabilities)

project_mcp      = stack_matching_mcp(stack)
                 # Add matching entries to .mcp.json
                 # Remove non-matching entries from .mcp.json (only managed entries — never touch user-added)
```

User overrides (`extra`, `disabled`) are never touched by auto-detection.

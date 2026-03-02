# claude-skills

Custom Claude Code skills for bootstrapping and maintaining projects.

## Skills

### `/setup-claude`

Bootstrap or repair Claude Code infrastructure on any project.

**What it does:**
- Detects your tech stack (Next.js, Laravel, Python, Go, Ruby, etc.)
- Creates or optimizes `CLAUDE.md`, `finish-feature.md`, changelog guides, and planning files
- Adds `tasks/findings.md` + `tasks/progress.md` for persistent context across long sessions
- Installs `/plan` and `/status` commands for structured task tracking
- Fully idempotent — safe to re-run on existing projects

**Supported stacks:** Next.js + Drizzle, Next.js + Prisma, Next.js + Supabase, Laravel + Eloquent, Supabase (any framework), Python + FastAPI, Generic

## Installation

```bash
git clone https://github.com/kennethsolomon/claude-skills ~/.agents/skills
```

> If `~/.agents/skills` already exists, clone elsewhere and copy the skill folders manually.

## Requirements

- [Claude Code CLI](https://claude.ai/code) installed and configured

## Optional

- `/schema-migrate` skill — referenced in generated files for Drizzle/Supabase/Laravel projects. Install separately if needed.

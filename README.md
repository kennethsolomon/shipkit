# claude-skills

Custom [Claude Code](https://claude.ai/code) skills for bootstrapping and maintaining projects.

## Installation

```bash
git clone git@github.com:kennethsolomon/claude-skills.git
cd claude-skills
./install.sh
```

### Updating

```bash
cd claude-skills
git pull
```

No re-install needed — it's a symlink, so updates apply instantly.

### Uninstalling

```bash
cd claude-skills
./uninstall.sh
```

## Skills

| Skill | Command | What it does |
|-------|---------|--------------|
| `setup-claude` | `/setup-claude` | Bootstrap Claude Code scaffolding (CLAUDE.md, tasks/, commands/) |
| `brainstorming` | `/brainstorm` | Explore design before writing any code |
| `write-tests` | `/write-tests` | Generate comprehensive tests matching project conventions |
| `review` | `/review` | Self-review across 7 dimensions before merging |
| `debug` | `/debug` | Structured bug investigation — reproduce, isolate, fix |
| `smart-commit` | `/smart-commit` | Auto-generate conventional commit messages |
| `release` | `/release` | Bump version, update CHANGELOG, tag, push. `--ios` / `--android` for store audits |
| `features` | `/features` | Sync `docs/features/` specs with current codebase |
| `frontend-design` | `/frontend-design` | Design direction + specs for UI work |
| `web-design-guidelines` | `/review-ui` | Audit UI for accessibility and best practices |
| `schema-migrate` | `/schema-migrate` | Multi-ORM schema change analysis |
| `skill-creator` | `/skill-creator` | Create or improve skills |
| `setup-optimizer` | `/setup-optimizer` | Enrich CLAUDE.md with project context |
| `starter-setup` | `/starter-setup` | Create optimized CLAUDE.md via auto-detection |
| `claude-doctor` | `/claude-doctor` | Diagnose and improve your CLAUDE.md |
| `find-skills` | `/find-skills` | Discover installable skills |

## Workflow

```
/setup-claude     <- bootstrap project
/brainstorm       <- clarify design
/write-tests      <- generate tests
/review           <- self-review
/debug            <- fix issues
/smart-commit     <- commit
/release          <- ship it
```

## Full Documentation

See [DOCUMENTATION.md](.claude/docs/DOCUMENTATION.md) for detailed usage, tutorials, workflow diagrams, and per-skill reference.

# Steal Report — 2026-04-07

Sources reviewed:
- obra/superpowers — skills-based workflow system
- anthropics/claude-code-action — GitHub Action for @claude in PRs/issues
- thedotmack/claude-mem — persistent memory via hooks + SQLite/Chroma
- garrytan/gstack — sprint-based workflow with multi-role reviews

---

## 1. obra/superpowers

### Worth Stealing
| # | Idea | Status | Effort | Adaptation |
|---|------|--------|--------|------------|
| 1 | **subagent-driven-development** two-stage review (spec compliance → code quality) per-task | New | Med | Extend `/sk:execute-plan` with optional `--isolate` flag that dispatches each plan task to a fresh subagent with two-stage review |
| 2 | **receiving-code-review** as an explicit skill | New | Low | Add `/sk:respond-review` — structured protocol for responding to `/sk:review` findings (triage by severity, fix, defer, dispute) |
| 3 | **verification-before-completion** as a hard gate | New | Low | Add check inside `/sk:gates`: "did you verify the fix actually works, not just that tests pass" — diff of claims vs evidence |
| 4 | **dispatching-parallel-agents** as a discoverable skill | Better | Low | We embed this in `/sk:team` but don't have a general-purpose "fan out N agents with M tasks" skill. Worth promoting to first-class `/sk:dispatch` |

### Already Covered
| Their Skill | Our Equivalent | Verdict |
|------|---------------|---------|
| test-driven-development | `/sk:write-tests` → `/sk:execute-plan` → `/sk:test` | Ours is equivalent; ours auto-detects BE + FE stacks |
| systematic-debugging | `/sk:debug` + `/sk:deep-dive` | Ours is better — 2 flavors (known vs unknown cause), structured protocol |
| brainstorming | `/sk:brainstorm` + `/sk:deep-interview` | Ours is better — adds mathematical ambiguity scoring |
| writing-plans | `/sk:write-plan` | Equivalent |
| executing-plans | `/sk:execute-plan` | Equivalent |
| using-git-worktrees | `.claude/worktrees/` + agent `isolation: "worktree"` | Ours is equivalent, baked into agents |
| requesting-code-review | `/sk:review` | Ours is better — 8 dimensions with `<think>` reasoning |
| finishing-a-development-branch | `/sk:finish-feature` | Equivalent |
| writing-skills | `/sk:skill-creator` | Equivalent |

### Not Worth It
| Idea | Why Skip |
|------|----------|
| Multi-agent ecosystem distribution (Cursor, Codex, OpenCode, Copilot CLI, Gemini) | ShipKit is Claude Code-focused; supporting 5 agents doubles maintenance surface for minimal user gain |

---

## 2. anthropics/claude-code-action

### Worth Stealing
| # | Idea | Status | Effort | Adaptation |
|---|------|--------|--------|------------|
| 1 | **GitHub Action workflow template** — run `/sk:review` on every PR via `@claude` mention | New | Med | Add `/sk:ci-claude` command that scaffolds `.github/workflows/claude-review.yml` using `anthropics/claude-code-action@v1` with ShipKit's review prompt and our 8 dimensions |
| 2 | **Label-triggered automation** (`label_trigger: "claude"`) | New | Low | Document pattern in `/sk:ci-claude` — add a `claude` label to auto-invoke review on stale PRs |
| 3 | **Progress-tracking sticky comments** with dynamic checkboxes | New | Med | Optional `/sk:execute-plan --gh-progress` — mirror todo.md checkboxes into a sticky PR comment |
| 4 | **Structured outputs** (validated JSON) from automation runs | New | Med | `/sk:review --json` — emit machine-readable review results for downstream tools |
| 5 | **Commit signing** (`use_commit_signing`, `ssh_signing_key`) | New | Low | Document in `/sk:smart-commit` — opt-in signed commits for regulated environments |

### Already Covered
| Their Agent | Our Equivalent | Verdict |
|------|---------------|---------|
| `code-quality-reviewer.md` | `code-reviewer` subagent | Ours has 7 dimensions vs their narrow focus |
| `security-code-reviewer.md` | `security-reviewer` subagent | Ours is OWASP-aligned, equivalent |
| `performance-reviewer.md` | `performance-optimizer` subagent | Ours also fixes (not just reviews) |
| `documentation-accuracy-reviewer.md` | `doc-reviewer` subagent | Equivalent |
| `test-coverage-reviewer.md` | `/sk:test` gate at 100% coverage | Ours enforces rather than reviews |

### Not Worth It
| Idea | Why Skip |
|------|----------|
| `allowed_bots` / `allowed_non_write_users` | GitHub-Action-specific security concern — not applicable to local CLI use |
| Sticky comment classification of inline comments | Too niche; surface area > value |
| Bedrock/Vertex/Foundry provider routing | We already have `/sk:set-profile` |

---

## 3. thedotmack/claude-mem

### Worth Stealing
| # | Idea | Status | Effort | Adaptation |
|---|------|--------|--------|------------|
| 1 | **`<private>` tag convention** — exclude content from auto-memory | New | Low | Add rule to auto-memory section of CLAUDE.md: any message wrapped in `<private>...</private>` is never saved to memory files. Honor during Write to `memory/` |
| 2 | **Progressive disclosure with token cost** for memory loading | Better | Med | Update `memory/MEMORY.md` loader hook: show per-entry token estimate, let agent decide which to expand |
| 3 | **mem-search as a skill** — natural language query over past sessions | New | Med | Add `/sk:recall` — grep + FTS over `memory/*.md` + `tasks/progress.md` + `tasks/findings.md` with semantic ranking |
| 4 | **Citations by observation ID** — let responses reference specific memory entries | New | Low | Convention: when referencing memory, format as `[mem:user_role.md]` so user can locate source |

### Already Covered
| Idea | Our Equivalent | Verdict |
|------|---------------|---------|
| SessionStart/Stop hooks for context injection | ShipKit's session-start hook already loads MEMORY.md and tasks state | Ours is simpler and already working |
| Persistent context across sessions | `memory/` + `tasks/findings.md` + `tasks/lessons.md` | Ours is file-based, zero infrastructure |

### Not Worth It
| Idea | Why Skip |
|------|----------|
| SQLite database with FTS5 | Heavy; defeats ShipKit's zero-infra ethos — grep over markdown is Good Enough |
| Chroma vector DB for semantic search | Same reason; adds a Python/embedding dependency for marginal gain |
| Worker HTTP service on port 37777 | Background service is exactly what ShipKit avoids |
| Web viewer UI | Nice-to-have; our `/sk:dashboard` already covers workflow state |
| Endless Mode (biomimetic memory) | Beta-grade experimental; wait and see |

---

## 4. garrytan/gstack

### Worth Stealing
| # | Idea | Status | Effort | Adaptation |
|---|------|--------|--------|------------|
| 1 | **Multi-role plan reviews** — CEO/eng/design/devex passes before implementation | New | Med | Add `/sk:plan-review` with `--role=ceo\|eng\|design\|devex` — CEO asks "should we build this?", eng asks "is the plan sound?", design asks "is the UX right?", devex asks "will contributors understand it?" |
| 2 | **Sprint vocabulary** — "Think → Plan → Build → Review → Test → Ship → Reflect" | Better | Low | Update CLAUDE.md workflow table phrasing; more memorable than "Explore → Design → Plan → Branch → ..." |
| 3 | **`/sk:investigate`** — a focused "spelunk the codebase before touching it" skill | New | Med | Separate from `/sk:brainstorm` — pure read-only exploration with a written findings report, feeds into plan |
| 4 | **Parallel sprints documentation** — how to run 10+ worktree sessions concurrently | New | Low | Add `docs/parallel-sprints.md` explaining `.claude/worktrees/` usage + Conductor compatibility |

### Already Covered
| Their Skill | Our Equivalent | Verdict |
|------|---------------|---------|
| `/office-hours` | `/sk:brainstorm` + `/sk:deep-interview` | Ours is better — ambiguity scoring |
| `/autoplan` | `/sk:start` → `/sk:write-plan` or `/sk:autopilot` | Equivalent |
| `/review` | `/sk:review` | Ours is better — 8 dimensions, `<think>` reasoning |
| `/ship` | `/sk:finish-feature` + `/sk:release` | Equivalent |
| `/qa` | `/sk:e2e` | Equivalent |
| `/retro` | `/sk:retro` | Equivalent |
| `/learn` | `/sk:learn` | Equivalent |
| `/careful /freeze /guard /unfreeze` | `/sk:safety-guard` | Ours consolidates into one skill with modes — ours is cleaner |
| `/investigate` | Partial — `/sk:debug` + `/sk:deep-dive` cover bug cases but not feature-area exploration | NEW — feature-area case uncovered |
| `/cso` (security audit) | `/sk:security-check` | Equivalent |
| `/plan-design-review` | `/sk:frontend-design` | Partial — ours creates, theirs reviews |

### Not Worth It
| Idea | Why Skip |
|------|----------|
| `/browse` skill replacing Chrome MCP | We don't use Chrome MCP; Pencil + Context7 MCPs cover our needs |
| Voice-friendly trigger phrases | Skills already activate via slash commands; voice adds no value here |
| ClawHub / OpenClaw-specific setup instructions | ShipKit-agnostic distribution — no lock-in to that marketplace |

---

## Summary — Recommended Defaults to Implement

**High-value, low-effort (do first):**
1. `/sk:respond-review` — structured review-response skill (from superpowers)
2. `<private>` tag convention for auto-memory (from claude-mem)
3. `/sk:ci-claude` — scaffold claude-code-action GitHub workflow (from claude-code-action)
4. `/sk:investigate` — feature-area read-only exploration (from gstack)

**Medium-value (do if approved):**
5. `/sk:plan-review --role=ceo|eng|design|devex` — multi-role plan passes (from gstack)
6. `/sk:execute-plan --isolate` — subagent-per-task with two-stage review (from superpowers)
7. `/sk:recall` — natural-language memory/findings search (from claude-mem)
8. `docs/parallel-sprints.md` — worktree concurrency guide (from gstack)

**Low-priority (consider later):**
9. Progress-tracking sticky comments via claude-code-action
10. Structured JSON output mode for `/sk:review`
11. Signed-commit documentation in `/sk:smart-commit`
12. Sprint vocabulary refresh in CLAUDE.md

**Explicitly declined:**
- Claude-mem's SQLite/Chroma/worker stack (violates zero-infra ethos)
- Multi-agent distribution (Cursor/Codex/etc.)
- GitHub Action bot-allowlist security knobs (not applicable locally)
- Voice trigger phrases

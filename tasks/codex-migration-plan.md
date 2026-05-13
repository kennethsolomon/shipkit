# ShipKit → Codex Migration Plan

Generated: 2026-05-13
Status: Draft — awaiting user approval

## Goal

Add OpenAI Codex (CLI + Cloud) as a second supported target for ShipKit while keeping Claude Code as the priority target. Quality bar: a Codex user running `/sk:autopilot` (or its Codex equivalent) gets the same 8-step TDD workflow, the same gates, the same `tasks/` lab-notebook discipline as a Claude Code user.

## Source Documents

- `tasks/codex-migration-inventory.md` — 82+ Claude-Code-specific touchpoints inventoried
- `tasks/codex-migration-research.md` — Codex CLI + Cloud capability map (17 sources, 2026-05-13)

## Architecture: Shared Core + Adapters

```
shipkit/
├── core/                                # provider-agnostic
│   ├── workflows/                       # 8-step flow definition (YAML)
│   ├── skill-bodies/<name>.md           # skill markdown bodies (no provider frontmatter)
│   ├── command-bodies/sk/<name>.md      # command markdown bodies
│   ├── hook-scripts/*.sh                # POSIX shell hooks (already provider-agnostic)
│   ├── agent-bodies/<name>.md           # sub-agent instructions (no provider frontmatter)
│   └── tool-map.yaml                    # canonical tool names + per-provider mapping
├── adapters/
│   ├── claude/
│   │   ├── frontmatter-template.yaml    # name, description, allowed-tools, model
│   │   ├── settings-template.json       # hooks, MCP, permissions
│   │   ├── tool-aliases.yaml            # core name → Claude tool name
│   │   └── emit.js                      # writes .claude/skills/, .claude/commands/, settings.json, agents
│   └── codex/
│       ├── frontmatter-template.yaml    # name, description (skills)
│       ├── agents-md-template.md        # AGENTS.md sections
│       ├── config-toml-template.toml    # [agents], [mcp_servers], [profiles], [features]
│       ├── hooks-json-template.json     # PreToolUse/PostToolUse/etc. with codex matchers
│       ├── tool-aliases.yaml            # core name → Bash/apply_patch/etc.
│       └── emit.js                      # writes AGENTS.md, .agents/skills/, .codex/, hooks.json
├── bin/
│   └── shipkit.js                       # adds --target=claude|codex|both flag, dispatches to adapters
└── tasks/                                # unchanged — works for both providers
```

**Why this shape**:
- Single source of truth for skill/command bodies (prevents drift)
- Each adapter owns ONLY the provider-specific surface (frontmatter, settings, tool naming, hooks format)
- Adding a third target (Cursor, Aider, etc.) later means one new `adapters/<name>/` folder

## Translation Tables (Canonical)

### Tool name mapping

| Core name | Claude Code | Codex |
|---|---|---|
| `shell` | `Bash` | `Bash` (alias for `shell`/`local_shell`) |
| `read` | `Read` | `apply_patch` (no separate read) |
| `edit` | `Edit` | `apply_patch` |
| `write` | `Write` | `apply_patch` |
| `grep` | `Grep` | shell `rg` via `Bash` |
| `glob` | `Glob` | shell `find`/`fd` via `Bash` |
| `web-fetch` | `WebFetch` | `web_search` (no fetch-by-URL primitive) |
| `web-search` | `WebSearch` | `web_search` |
| `agent` | `Agent` | `.codex/agents/<name>.toml` invocation |
| `task-create` | `TaskCreate` | TODO: confirm Codex equivalent |
| `mcp:<server>:<tool>` | `mcp__<server>__<tool>` | `mcp__<server>__<tool>` |

### Hook event mapping

| Core event | Claude Code | Codex |
|---|---|---|
| session-start | `SessionStart` | `SessionStart` (matchers: `startup`/`resume`/`clear`) |
| pre-tool | `PreToolUse` | `PreToolUse` |
| post-tool | `PostToolUse` | `PostToolUse` |
| user-prompt | `UserPromptSubmit` | `UserPromptSubmit` |
| stop | `Stop` | `Stop` |
| permission-request | (built-in approval modes) | `PermissionRequest` |

Hooks are CLI-only in Codex. Cloud users get a degraded mode — see "Cloud constraints" below.

### Skill frontmatter mapping

| Field | Claude Code | Codex |
|---|---|---|
| `name` | required | required |
| `description` | required (auto-trigger match text) | required (progressive-disclosure text, ≤8KB) |
| `allowed-tools` | optional | not used — `[permissions]` profile instead |
| `model` | optional | not used — `model_reasoning_effort` per profile |

## Phased Rollout

### Phase 0 — Decision gates (no code) [0.5 day]
- User approves this plan
- Resolve open questions (see below)
- Pick representative pilot commands: `/sk:plan`, `/sk:gates`, `/sk:smart-commit`

### Phase 1 — Refactor existing tree into core + claude adapter [3 days]
- Move skill/command bodies into `core/skill-bodies/`, `core/command-bodies/`
- Extract Claude frontmatter into `adapters/claude/` templates
- Build `adapters/claude/emit.js` that reproduces today's `.claude/` output byte-for-byte
- Validation: `tests/verify-workflow.sh` still passes
- **No behavior change visible to Claude Code users**

### Phase 2 — Codex adapter: core workflow [4 days]
- Build `adapters/codex/emit.js`
- Port pilot 3 commands as Codex skills end-to-end
- Generate `AGENTS.md` from `CLAUDE.md` template (chunked if >32 KiB)
- Generate `.codex/config.toml` with MCP servers + profiles
- Generate `.codex/hooks.json` with the 8 existing shell hooks
- Validate manually: run `/sk:plan` equivalent in Codex CLI; confirm 8-step flow advances correctly
- Validate: `codex --cd` against a test repo with these files; confirm cloud-equivalent works by pushing to a branch and running in Codex Cloud

### Phase 3 — Full skill/command port [5 days]
- Translate remaining ~67 skills/commands using the established templates
- Audit each for tool-naming issues (every `Bash` → check; every Read/Edit/Write → confirm `apply_patch` works)
- Translate ~15 sub-agent definitions into `.codex/agents/*.toml`
- Add Codex profiles for ShipKit modes (autopilot, fast-track, hotfix)

### Phase 4 — Hard translations [4 days]
- **Parallel sub-agent batches** (`/sk:gates`, `/sk:team`, `/sk:deep-dive`): Rewrite as either (a) sequential agent invocations with progress reporting, or (b) `codex exec` shelled out from a wrapper script. Document the perf delta.
- **Worktree isolation**: Replace `isolation: "worktree"` with a shell helper that runs `git worktree add` + `codex --cd <path>`, captures the result, optionally merges back.
- **Pencil MCP**: Document that it works in Codex CLI (MCP supported) but not in Codex Cloud. Gate `/sk:frontend-design --pencil` behind environment detection.
- **context-mode plugin**: Codex equivalent unclear — flag as known gap; recommend skipping for v1 and revisiting after Codex docs evolve.

### Phase 5 — Cloud-mode degradation [2 days]
- Add `core/env-detect.sh` that detects Codex Cloud (no `~/.codex/`, no hooks)
- Each affected skill SHORT-CIRCUITS gracefully in cloud mode with a clear message
- AGENTS.md documents which `/sk:*` flows work in cloud vs. CLI vs. Claude Code

### Phase 6 — Distribution [2 days]
- `bin/shipkit.js --target=codex` writes Codex artifacts
- `bin/shipkit.js --target=both` writes both
- Publish as Codex Plugin (per Codex's `/plugins` recommendation)
- Keep `@kennethsolomon/shipkit` npm package as the primary install path
- Update README with three-way install matrix

### Phase 7 — Validation [2 days]
- Run `/sk:autopilot` end-to-end on a sample feature, on all three surfaces: Claude Code, Codex CLI, Codex Cloud
- Compare outputs; document any quality deltas in `tasks/codex-quality-deltas.md`
- Run existing `tests/verify-workflow.sh` against both adapter outputs

**Total estimate**: ~22 working days (with parallel work, real elapsed time is shorter)

## Cloud Constraints (Honest Quality Delta)

Things Codex Cloud users will NOT get (vs. Codex CLI or Claude Code):
- Hooks (no session-start, no pre-edit-format, no validate-commit)
- User-global `~/.codex/` configuration
- MCP servers not pre-configured in the cloud environment
- Background sub-agent execution

Mitigation: skills detect cloud env at start, log degraded-mode notice, and continue with reduced functionality rather than silently failing.

## Decisions Locked (2026-05-13)

1. **Versioning**: Bump to **v4.0.0** new major. `--target=claude` stays default so existing users see no break.
2. **Repo layout**: **Refactor in-place** — move `skills/` → `core/skill-bodies/`, `commands/` → `core/command-bodies/`. Cleaner final state, one-release transition.
3. **Distribution**: **npm only for v1**. Codex Plugin deferred until marketplace access is confirmed.
4. **Codex slash-command spec**: Skills are the primary surface; revisit custom slash commands only if a skill-only port leaves gaps.
5. **Tests**: Unify into one runner with `--target` flag — `tests/verify-workflow.sh --target=claude|codex|both`.

## Risk Register

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Parallel sub-agent perf degrades on Codex | High | High | Rewrite as sequential w/ progress; benchmark; document delta |
| Tool-naming differences break skills silently | Med | High | Audit pass in Phase 3; integration test per skill |
| Cloud env has undocumented constraints | Med | Med | Phase 7 cloud run; add detection + fallback per skill |
| AGENTS.md exceeds 32 KiB | Med | Low | Split into nested AGENTS.md per topic |
| Codex docs evolve mid-port | Med | Med | Pin to fetched-on date; document upgrade path |
| Pencil/context-mode have no Codex equivalent | High | Med | Gate behind env detection; flag as known gap |

## Success Criteria

- Claude Code behavior is byte-identical to v3.30.0 (no regression)
- Codex CLI user can run `/sk:autopilot` equivalent and complete an 8-step flow
- Codex Cloud user can run the workflow with documented degradations
- One config file change (`--target`) switches the emit
- New skills added to `core/` automatically work on both targets

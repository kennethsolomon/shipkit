# Codex Platform Research for ShipKit Port

Generated: 2026-05-13

Sources (all fetched 2026-05-13):
- https://github.com/openai/codex (README)
- https://agents.md/ (AGENTS.md community spec)
- https://developers.openai.com/codex/cli/features
- https://developers.openai.com/codex/config-basic
- https://developers.openai.com/codex/config-advanced
- https://developers.openai.com/codex/config-reference
- https://developers.openai.com/codex/guides/agents-md
- https://developers.openai.com/codex/cli/slash-commands
- https://developers.openai.com/codex/guides/slash-commands
- https://developers.openai.com/codex/skills
- https://developers.openai.com/codex/subagents
- https://developers.openai.com/codex/hooks
- https://developers.openai.com/codex/mcp
- https://developers.openai.com/codex/security
- https://developers.openai.com/codex/cloud
- https://developers.openai.com/codex/cloud/environments
- https://developers.openai.com/codex/app/worktrees
- https://developers.openai.com/codex/concepts/customization

## TL;DR Comparison Table

| Capability | Claude Code | Codex CLI | Codex Cloud (Web) |
|---|---|---|---|
| Instruction file | `CLAUDE.md` | `AGENTS.md` (32 KiB/file default, nested, `AGENTS.override.md`) | Same `AGENTS.md` honored by the cloud agent |
| Custom slash commands | `.claude/commands/*.md` | Built-in `/commands` + custom commands (docs reference `/codex/guides/slash-commands`); exact path not fully captured in fetched content — see Gaps | Not surfaced in cloud Web UI as user-defined slash commands |
| Skills (auto-trigger) | `skills/*/SKILL.md` + frontmatter, auto-loaded via description | **Yes** — `.agents/skills/<name>/SKILL.md` w/ YAML frontmatter; progressive disclosure (cap ~2% ctx or 8KB) | Inherits skills present in repo at `.agents/skills/` |
| Sub-agents | `Agent` tool, parallel | **Yes (explicit only)** — `[agents]` in `config.toml` + `.codex/agents/<name>.toml` | Cloud runs tasks in parallel containers; subagent model is CLI-side |
| Hooks | `settings.json` `hooks` | **Yes (experimental)** — `~/.codex/hooks.json` or inline `[hooks]` in `config.toml`; events: `PreToolUse`, `PostToolUse`, `PermissionRequest`, `SessionStart`, `UserPromptSubmit`, `Stop`; enable via `[features] codex_hooks = true` | Not documented for cloud |
| MCP | `~/.claude.json` mcpServers | **Yes** — `[mcp_servers.<id>]` in TOML, stdio + streamable HTTP | Honored where configured for the environment |
| Tool surface | Read/Edit/Write/Bash/Grep/Glob/WebFetch/WebSearch | `Bash` (shell/`local_shell`), `apply_patch` (Edit/Write alias), `web_search`, file search, MCP tools | Same plus container shell |
| Config location | `~/.claude/`, `.claude/` | `~/.codex/config.toml` + `.codex/config.toml` (`CODEX_HOME` overrides) | Container; AGENTS.md from repo |
| Approval modes | `acceptEdits`, plan mode, etc. | `approval_policy`: `untrusted` / `on-request` / `never` / `{ granular = {…} }`; sandbox: `read-only` / `workspace-write` / `danger-full-access`; built-in profiles `:read-only`, `:workspace`, `:danger-no-sandbox` | Per-task internet on/limited/off; sandboxed container |
| Worktree isolation | Agent `isolation: "worktree"` | Native via Codex App "Worktree" mode (UI); CLI works on whatever git tree you launch in | Each task runs in its own ephemeral container (worktree-equivalent isolation) |
| Plan mode | Built-in | `/plan` slash command; `read-only` sandbox = consultative mode | Implicit (review before applying diff/PR) |
| Memory | Auto-memory + `tasks/*` files | `~/.codex/history.jsonl`; `[memories]` consolidation config keys; `codex resume` | Per-task; no cross-task memory documented |
| Model selection | `model` setting | `model` + `model_reasoning_effort` (minimal/low/medium/high/xhigh); `[profiles.<name>]` named profiles; `model_catalog_json` | Selected per task in UI |
| Distribution | `.claude/` directory + npm package | `npm i -g @openai/codex`, `brew install --cask codex`, GitHub release binaries; user assets via repo + `.agents/skills/`, `$skill-installer`, **plugins** (`/plugins`) | Cloud picks up repo assets automatically |

## Detailed Findings

### 1. Instruction files (AGENTS.md)
- **CLI**: Discovery chain — Global (`$CODEX_HOME/AGENTS.override.md` then `AGENTS.md`, first non-empty wins) → Project (walk from project root down to CWD, at each dir try `AGENTS.override.md`, then `AGENTS.md`, then `project_doc_fallback_filenames`). Files concatenated root→leaf; later entries override. Per-file size cap = `project_doc_max_bytes` (default **32 KiB**). Project root detected by `.git` (configurable via `project_root_markers`). Nested AGENTS.md works monorepo-style — agents.md spec notes OpenAI's main repo has 88 of them.
- **Cloud**: "If your repo includes `AGENTS.md`, the agent uses it to find project-specific lint and test commands" (codex-cloud-env). Same file works.
- **Sections**: Not formally schema'd. agents.md spec recommends Setup, Build, Test, Style, PR conventions. No required headings.

### 2. Custom commands / prompts
- **CLI**: Built-in slash commands include `/plan`, `/init`, `/permissions`, `/plugins`, `/sandbox-add-read-dir`, `/review`, `/fork`, `/side`, etc. Docs state custom commands exist ("create custom ones for team-specific tasks or personal shortcuts") with a dedicated guide, **but the exact filesystem path/format was not captured in fetched content** — the slash-commands guide page redirects content not loaded here. Best practice from docs: prefer **Plugins** (distributable) or **Skills** (auto-triggered) over raw custom commands.
- **Cloud**: No equivalent of arbitrary user-defined slash commands surfaced in the cloud UI.
- **Migration note**: ShipKit's 70 `/sk:*` commands map most cleanly to **Skills** (auto-triggered) for both CLI and cloud, with optional `$skill-installer`-style invocation for explicit calls.

### 3. Skills auto-triggering
- **CLI**: First-class. Skills live in `$CWD/.agents/skills`, ancestor dirs up to repo root, `$HOME/.agents/skills` (user), `/etc/codex/skills` (admin). Each skill = folder with `SKILL.md` and YAML frontmatter (`name`, `description`). Codex uses **progressive disclosure**: names+descriptions injected (capped ~2% of ctx window or 8000 chars); full SKILL.md loaded only when triggered. Built on the open agentskills.io standard. `$skill-creator` and `$skill-installer` are built-in skills for authoring/installing.
- **Cloud**: Inherits repo-checked-in skills automatically.
- **Migration note**: This is the closest analogue to Claude Code skills and likely the primary porting target.

### 4. Sub-agents / parallel execution
- **CLI**: Subagents are explicit — defined via `[agents]` block in `config.toml` plus `.codex/agents/<name>.toml` with `name`, `description`, `model`, `model_reasoning_effort`, `sandbox_mode`, `developer_instructions`, optional `[mcp_servers.*]`. Knobs: `max_threads`, `max_depth`. **Codex only spawns subagents when explicitly asked**, and they consume more tokens. Non-interactive automation via `codex exec` and `codex exec resume`.
- **Cloud**: Cloud tasks can run in parallel containers; best-of-N via `--attempts 1..4` on `codex cloud exec`.
- **Migration note**: Maps to ShipKit's `Agent` tool / `/sk:team`. No background daemon equivalent of Claude Code's `run_in_background:true`; closest is `codex exec` invoked async by user/wrapper script.

### 5. Hooks
- **CLI (experimental)**: Loaded from `hooks.json` or inline `[hooks]` TOML at `~/.codex/` or `<repo>/.codex/`. Project hooks require project trust. Enable: `[features] codex_hooks = true`. Events: `PreToolUse`, `PostToolUse`, `PermissionRequest`, `SessionStart` (matchers `startup|resume|clear`), `UserPromptSubmit`, `Stop`. Matchers are regex on tool name (`Bash`, `apply_patch`/`Edit`/`Write`, `mcp__*`). Handler: `{ type = "command", command, timeout, statusMessage }`. Hook stdout JSON can deny actions via `hookSpecificOutput.permissionDecision = "deny"`.
- **Cloud**: Not documented.
- **Migration note**: Very close conceptual match to Claude Code hooks. ShipKit's `session-start.sh`, `validate-commit.sh`, `post-edit-format.sh`, `safety-guard.sh` can port nearly 1:1.

### 6. MCP support
- **CLI**: First-class. Configured under `[mcp_servers.<id>]` in `~/.codex/config.toml` (or project). STDIO transport (`command`, `args`, `env`, `env_vars`, `cwd`) or streamable HTTP (`url`, `bearer_token_env_var`, `http_headers`). Per-server: `enabled_tools`, `disabled_tools`, `startup_timeout_sec`, `tool_timeout_sec`, `enabled`. Also CLI: `codex mcp` commands. Codex can run **as** an MCP server.
- **Cloud**: Configured per environment.
- **Migration note**: Direct port — same MCP servers (context7, supabase, etc.) attach unchanged.

### 7. Tool surface
- **Tools**: `shell` (also `local_shell`, newer `unified_exec`), `apply_patch` (atomic edits; matcher aliases `Edit`/`Write`), `web_search`, file search/retrieval, tool search, image generation, code interpreter, computer use, MCP-exposed tools. Internally `tool_name` reports as `Bash`, `apply_patch`, or `mcp__<server>__<tool>` in hook inputs.
- **Naming deltas vs Claude Code**: `Bash` ≈ `shell`; `Read`/`Edit`/`Write` collapse into `apply_patch`; `Grep`/`Glob` are not first-class — invoked via shell `rg`/`find`; `WebFetch`/`WebSearch` available as built-ins. ShipKit `allowed-tools` lists must be rewritten.

### 8. Configuration
- `CODEX_HOME` (default `~/.codex/`). Files: `config.toml`, `auth.json` (or OS keychain), `history.jsonl`, `sessions/`. Project layer: `.codex/config.toml` (only loaded when project is "trusted"). Profiles via `[profiles.<name>]`, selected with `codex --profile <name>` or top-level `profile = "<name>"`. Reusable named permission profiles (`default_permissions`).

### 9. Approval modes / permissions / sandbox
- **Approval policy**: `untrusted` | `on-request` | `never` | `{ granular = { sandbox_approval, rules, mcp_elicitations, request_permissions, skill_approval } }`. Reviewer: `user` or `auto_review`.
- **Sandbox mode**: `read-only` | `workspace-write` | `danger-full-access`. Built-in profiles: `:read-only`, `:workspace`, `:danger-no-sandbox`. Custom profiles via `[permissions.<name>.filesystem]` + `[permissions.<name>.network]`. Workspace-write keeps `.git/` and `.codex/` read-only by default. Network defaults off; can `allow`/`deny` per domain.
- **Rules**: `.codex/rules` files + admin `requirements.toml` rules (prefix_rules with `pattern`+`decision` of `prompt`/`forbidden`/`allow`).

### 10. Worktree / isolation
- **CLI**: Operates in current git tree. No first-class `--worktree` flag found in fetched docs. Use `git worktree add` then `codex --cd <path>` or `codex resume --add-dir`.
- **App**: Native "Worktree" mode in the desktop/Codex app — base branch picker, detached HEAD, handoff to local checkout.
- **Cloud**: Each task = new container checkout (worktree-equivalent).

### 11. Cloud-specific (Codex Web)
- ChatGPT Plus/Pro/Business/Edu/Enterprise plans. GitHub-connected. Per task: new container, checkout, setup script, optional maintenance script on cache resume, internet policy (off/limited/unrestricted) applied. **`AGENTS.md` is honored** ("agent uses it to find project-specific lint and test commands"). Repo-checked-in `.agents/skills/`, `.codex/agents/`, `AGENTS.md`, and `.codex/config.toml` ride along. Hooks in cloud not documented. Local `~/.codex/` content does **not** apply.

### 12. Plan mode
- `/plan` slash command toggles plan mode. `read-only` sandbox is the durable equivalent ("consultative mode"). Codex app "Review" workflow surfaces diffs before apply.

### 13. Memory / persistence
- Local: `~/.codex/history.jsonl` (cap via `history.max_bytes`); disable via `[history] persistence = "none"`. Sessions stored under `~/.codex/sessions/`; `codex resume` (incl. `--last`, `--all`, `<SESSION_ID>`). Experimental `[memories]` keys: `consolidation_model`, `extract_model`, `generate_memories`, `max_rollouts_per_startup`, `max_unused_days`, `disable_on_external_context`. ShipKit's `tasks/*.md` "project memory" pattern still works (just files in the repo).

### 14. Model selection
- `model = "gpt-5.4"` etc. Latest tier referenced as **GPT-5.5** (May 2026). `model_reasoning_effort = minimal|low|medium|high|xhigh`. `model_reasoning_summary = auto|concise|detailed|none`. Profiles bundle model + effort + sandbox per task. `model_providers.<id>` lets you point at Bedrock, Azure, custom OpenAI-compatible endpoints. `openai_base_url` for proxies.

### 15. Distribution / install
- **CLI binary**: `npm i -g @openai/codex` or `brew install --cask codex` or GitHub Releases (`codex-aarch64-apple-darwin.tar.gz` etc.).
- **User assets**: drop into repo (`AGENTS.md`, `.agents/skills/`, `.codex/`), `$HOME/.agents/skills/`, or `/etc/codex/skills/`. Curated skills via `$skill-installer <name>`.
- **Plugins** are the recommended **distribution unit** (`/plugins` browser, plugin marketplaces). A ShipKit-for-Codex package most naturally ships as **(a) an npm package that scaffolds files** *and/or* **(b) a Codex Plugin** containing the skills + commands + hooks.

## Gaps That Will Hurt ShipKit Port

- **Custom slash command authoring path is documented but the exact directory/frontmatter schema was not in the fetched content** — needs follow-up against the live `/codex/guides/slash-commands` page; Codex appears to prefer skills + plugins over arbitrary user slash commands.
- **No background-task primitive** equivalent to Claude Code `run_in_background:true`. Long-running work must be invoked via `codex exec` from a wrapper or routed to Codex Cloud.
- **Hooks are experimental** and feature-flagged (`[features] codex_hooks = true`); not honored in cloud.
- **Subagents are token-expensive** and require explicit invocation — auto-parallelization patterns (e.g., `/sk:gates` Batch 3) need to be rewritten as explicit `[agents]` configs.
- **Cloud has no hooks, no `~/.codex/` user config, no MCP unless wired into the environment** — anything user-global must live in the repo to ride along.
- **Tool naming differs** (`apply_patch` vs `Read/Edit/Write`, no `Grep`/`Glob`): every `allowed-tools` frontmatter must be remapped.
- **No native `Agent`-tool style worktree isolation in the CLI** — must be scripted via `git worktree add` + `codex --cd`.
- **No auto-loaded "global memory" file** outside AGENTS.md hierarchy + history; ShipKit's `tasks/*.md` lab-notebook pattern still works but must be referenced from AGENTS.md.

## Recommended Adapter Approach

**Primary surface = Skills + AGENTS.md.** Port each `/sk:*` command to a Codex Skill at `.agents/skills/sk-<name>/SKILL.md` with YAML frontmatter (`name`, `description`). Skills auto-trigger from descriptions on both CLI and cloud, sidestep the "custom slash command" docs gap, and progressive-disclosure keeps the context cost low. Generate a top-level `AGENTS.md` (≤32 KiB) covering the 8-step workflow, write rules, and tool naming hints; for monorepos, generate sub-directory `AGENTS.md` files. Move ShipKit's CLAUDE.md content verbatim there.

**Secondary surface = Hooks + Subagents (CLI-only).** Translate ShipKit hooks (`session-start.sh`, `validate-commit.sh`, `post-edit-format.sh`, `safety-guard.sh`, `config-protection.sh`) to `~/.codex/hooks.json` + `<repo>/.codex/hooks.json`, matchers on `Bash`/`apply_patch`/`SessionStart`. Translate parallel-agent batches (`/sk:gates`, `/sk:team`) into `.codex/agents/*.toml` with `sandbox_mode`, `developer_instructions`, and per-agent MCP. Emit a Codex `[profiles.<name>]` for each ShipKit mode (autopilot, fast-track, hotfix) bundling model + reasoning_effort + sandbox.

**Distribution = npm scaffolder + Codex Plugin.** Ship `@kennethsolomon/shipkit-codex` (npm) whose CLI writes the `.agents/`, `.codex/`, `AGENTS.md`, and `~/.codex/hooks.json` files; additionally publish a Codex **Plugin** (recommended distribution unit per `/codex/plugins/build`) so users can install via `/plugins`. For Codex Web (cloud), the repo-checked-in `AGENTS.md` + `.agents/skills/` + `.codex/agents/` directories are picked up automatically — no extra wiring. Document that hooks, `~/.codex/` user config, and background execution **do not** work in cloud, and gate those features behind an environment detector at skill-start time.

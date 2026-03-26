# TODO — 2026-03-26 — MCP Servers & Plugins Installation

## Goal

Add Sequential Thinking MCP, Context7 plugin, and ccstatusline installation steps to `sk:setup-claude` and `sk:setup-optimizer`, plus documentation in README and DOCUMENTATION.md.

## Scope — 5 files

1. `skills/sk:setup-claude/SKILL.md` — new "MCP Servers & Plugins" section after LSP Integration
2. `skills/sk:setup-optimizer/SKILL.md` — new Step 1.7 after LSP check (Step 1.6)
3. `README.md` — new "MCP Servers & Plugins" section after Code Navigation (LSP)
4. `.claude/docs/DOCUMENTATION.md` — update infrastructure section
5. `tests/verify-workflow.sh` — add assertions for new content

## Tools to Install (all opt-in, idempotent)

- **Sequential Thinking MCP** — `npx -y @modelcontextprotocol/server-sequential-thinking` → `~/.mcp.json`
- **Context7** — `context7@claude-plugins-official` → `~/.claude/settings.json` enabledPlugins
- **ccstatusline** — `npx ccstatusline@latest`

---

## Checklist

### Milestone 1: Tests (TDD Red)

- [ ] Add to `tests/verify-workflow.sh`:
  - `assert_contains` — `skills/sk:setup-claude/SKILL.md` contains `"Sequential Thinking"`
  - `assert_contains` — `skills/sk:setup-claude/SKILL.md` contains `"context7"`
  - `assert_contains` — `skills/sk:setup-claude/SKILL.md` contains `"ccstatusline"`
  - `assert_contains` — `skills/sk:setup-optimizer/SKILL.md` contains `"Sequential Thinking"`
  - `assert_contains` — `skills/sk:setup-optimizer/SKILL.md` contains `"context7"`
  - `assert_contains` — `skills/sk:setup-optimizer/SKILL.md` contains `"ccstatusline"`
  - `assert_contains` — `README.md` contains `"Sequential Thinking"`
  - `assert_contains` — `README.md` contains `"context7"`
  - `assert_contains` — `README.md` contains `"ccstatusline"`

### Milestone 2: sk:setup-claude

- [ ] Add "### MCP Servers & Plugins" section after LSP Integration (line ~406):
  - Prompt: "Install recommended MCP servers & plugins? (Sequential Thinking, Context7, ccstatusline) [y/n]"
  - Sequential Thinking: check `~/.mcp.json`, add entry if missing
  - Context7: check `~/.claude/settings.json` enabledPlugins, add if missing
  - ccstatusline: run `npx ccstatusline@latest` if not already configured
  - Idempotency checks for each
  - Report format: `+ sequential-thinking MCP added to ~/.mcp.json`

### Milestone 3: sk:setup-optimizer

- [ ] Add "### Step 1.7: MCP Servers & Plugin Check" after Step 1.6 (LSP):
  - Check sequential-thinking in `~/.mcp.json`
  - Check context7 in `~/.claude/settings.json` enabledPlugins
  - Check ccstatusline in `~/.claude/settings.json` statusline config
  - Report: "MCP/Plugins: [X/3] configured"
  - Prompt: "Install missing? [y/n]"
  - Follow same install steps as setup-claude on yes

### Milestone 4: README.md

- [ ] Add "## MCP Servers & Plugins" section after Code Navigation (LSP) section (after line 291):
  - Intro paragraph explaining what these tools do
  - Sequential Thinking: Why + Benefit + Install note
  - Context7: Why + Benefit + Install note
  - ccstatusline: Why + Benefit + Install note

### Milestone 5: DOCUMENTATION.md

- [ ] Find setup-claude infrastructure section and add MCP/plugin note
- [ ] Reference Step 1.7 in setup-optimizer description

## Acceptance Criteria

- [ ] `bash tests/verify-workflow.sh` passes all new assertions
- [ ] sk:setup-claude SKILL.md has MCP section with all 3 tools, prompts, idempotency
- [ ] sk:setup-optimizer SKILL.md has Step 1.7 with check + prompt
- [ ] README.md has MCP section with why/benefit for each tool
- [ ] DOCUMENTATION.md references MCP installation

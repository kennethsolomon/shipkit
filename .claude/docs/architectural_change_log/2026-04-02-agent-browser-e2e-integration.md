# 2026-04-02 — agent-browser Integration into /sk:e2e

## Summary

agent-browser (vercel-labs/agent-browser) integrated as the preferred interactive E2E verification tool. Playwright CLI retains its role as the spec-file runner. Token savings: 10–20× fewer tokens than screenshot-based verification.

---

## Changes

### 1. Priority flip in `/sk:e2e`

**File:** `skills/sk:e2e/SKILL.md`

**Before:** Playwright CLI preferred; agent-browser fallback only if no playwright.config.ts detected.

**After:**
- **Priority 1** — Playwright CLI: only when `playwright.config.ts` AND spec files already exist. Tests are written — just run them.
- **Priority 2** — agent-browser: preferred for interactive verification / when no spec files exist.
- **Priority 3** — fallback: neither available; offer agent-browser as Option A (recommended).

**Why the flip:** Playwright CLI running existing `.spec.ts` files has no token overhead (headless, no screenshots). But when spec files don't exist and Claude must navigate interactively, agent-browser's accessibility tree refs (`@e1`, `@e2`) are text-only — 10–20× fewer tokens than screenshot-based approaches. The Playwright MCP (screenshot-heavy) is explicitly called out as the path this skill avoids.

### 2. agent-browser in setup flows

**Files:** `skills/sk:setup-claude/SKILL.md`, `skills/sk:setup-optimizer/SKILL.md`

- setup-claude: added as item 5 in MCP/plugins install prompt
- setup-optimizer Step 1.7: added as 5th check, report string updated from `X/4` to `X/5`
- Install: `npm install -g agent-browser && agent-browser install`
- Check: `agent-browser --version 2>/dev/null`

### 3. README documentation

**File:** `README.md`

New "Recommended CLI Tools" table added under MCP Servers section. agent-browser is the first entry — distinguishes CLI tools (npm install -g) from Claude plugins (/plugin marketplace add).

### 4. maintenance-guide CLI tool sub-type

**File:** `.claude/docs/maintenance-guide.md`

"When You Add/Remove a Community Plugin" section extended with two sub-types:
- **Claude Plugin** — check via `claude plugin list`, install via `/plugin`
- **CLI Tool** — check via `<cmd> --version`, install via `npm install -g`

agent-browser exposed this gap (first CLI tool recommendation in ShipKit).

---

## Design Decisions

**Why agent-browser over Playwright MCP for interactive verification?**
Playwright MCP takes screenshots on every interaction — each image is 1,000–3,000 tokens. agent-browser's `snapshot` command returns an accessibility tree as text with short refs. For a 5-step verification flow, this is typically 200–500 tokens vs 5,000–15,000 for screenshot-based navigation.

**Why keep Playwright CLI at all?**
Projects with existing `.spec.ts` files have invested in test infrastructure. Running those files via `npx playwright test` is already headless and token-free. Displacing them for agent-browser would break existing test suites. The two tools serve different jobs: Playwright runs pre-written assertions, agent-browser navigates interactively.

**Why classify agent-browser as CLI Tool (not community plugin)?**
It's installed via npm install -g, checked via `--version`, and invoked via Bash — not via Claude's plugin system. Adding it to the plugin install pattern would give wrong install instructions. The maintenance-guide sub-type distinction makes this explicit for future contributors.

'use strict';

// Codex adapter — emits Codex-format files from core/.
//
// Output layout (per destDir, which is the user's project root):
//   AGENTS.md                                        Codex instruction file (≤32 KiB per file)
//   .agents/skills/sk-<name>/SKILL.md                Codex skill (name + description frontmatter)
//   .agents/skills/sk-<name>/<asset files>           any non-SKILL.md assets copied verbatim
//   .codex/config.toml                               MCP servers, agents, profiles
//   .codex/hooks.json                                CLI-only hook config (Cloud ignores)
//
// Naming convention: `sk:foo` (Claude) becomes `sk-foo` (Codex) for filesystem-safe
// folder names. The frontmatter `name:` field follows the folder.

const fs   = require('fs');
const path = require('path');

// ── Frontmatter parsing ──────────────────────────────────────────────────────
function parseFrontmatter(content) {
  const m = content.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n?([\s\S]*)$/);
  if (!m) return { frontmatter: {}, body: content };
  const fm = {};
  for (const line of m[1].split(/\r?\n/)) {
    const kv = line.match(/^([A-Za-z][\w-]*):\s*(.*)$/);
    if (!kv) continue;
    let val = kv[2].trim();
    if ((val.startsWith('"') && val.endsWith('"')) ||
        (val.startsWith("'") && val.endsWith("'"))) {
      val = val.slice(1, -1);
    }
    fm[kv[1]] = val;
  }
  return { frontmatter: fm, body: m[2] };
}

function escapeYamlString(s) {
  return s.replace(/\\/g, '\\\\').replace(/"/g, '\\"');
}

function emitCodexFrontmatter({ name, description }) {
  return `---\nname: ${name}\ndescription: "${escapeYamlString(description)}"\n---\n`;
}

function toCodexName(claudeName) {
  // sk:status → sk-status (colon is unsafe in directory names on Windows + some CI)
  return claudeName.replace(/:/g, '-');
}

// ── Body transforms ─────────────────────────────────────────────────────────
// Path / config references that are safe to rewrite Claude → Codex without
// changing the meaning of the surrounding text.
//
// Skipped on purpose:
//   - Tool names (Read/Edit/Write/Bash/Grep/Glob) — Codex aliases these in its
//     hook matchers; skill bodies generally use them as actions, not tool calls.
//   - "Claude Code" / "CLAUDE.md" prose — agents read AGENTS.md and understand
//     the mapping from the header we inject there. Blind replacement risks
//     turning factual references ("Claude Code's plan mode") into nonsense.
//   - /sk:foo slash-command references — Codex auto-triggers on description;
//     the agent figures out the right skill name from context.
const BODY_TRANSFORMS = [
  // User-global paths (~/.claude/ → ~/.codex/ or ~/.agents/)
  [/~\/\.claude\/skills\/sk:/g, '~/.agents/skills/sk-'],
  [/~\/\.claude\/skills\//g,    '~/.agents/skills/'],
  [/~\/\.claude\/agents\//g,    '~/.codex/agents/'],
  [/~\/\.claude\/settings\.json/g, '~/.codex/config.toml'],
  [/~\/\.claude\/sessions\//g,  '~/.codex/sessions/'],
  [/~\/\.claude\//g,            '~/.codex/'],
  // Project-local paths
  [/\.claude\/agents\//g,       '.codex/agents/'],
  [/\.claude\/hooks\//g,        '.codex/hooks/'],
  [/\.claude\/skills\/sk:/g,    '.agents/skills/sk-'],
  [/\.claude\/skills\//g,       '.agents/skills/'],
  [/\.claude\/commands\/sk:/g,  '.agents/skills/sk-'],
  [/\.claude\/commands\/sk\//g, '.agents/skills/'],
  [/\.claude\/commands\//g,     '.agents/skills/'],
  [/\.claude\/docs\//g,         'docs/'],
  [/\.claude\/evals\//g,        '.codex/evals/'],
  [/\.claude\/rules\//g,        '.codex/rules/'],
  [/\.claude\/safety-guard/g,   '.codex/safety-guard'],
  [/\.claude\/settings\.json/g, '.codex/config.toml'],
  [/\.claude\/sessions\//g,     '~/.codex/sessions/'],
  [/\.claude\/mcp\.json/g,      '~/.codex/config.toml'],
];

function transformBody(body) {
  let out = body;
  let count = 0;
  for (const [pattern, replacement] of BODY_TRANSFORMS) {
    out = out.replace(pattern, () => { count++; return replacement; });
  }
  return { body: out, count };
}

// ── File helpers ────────────────────────────────────────────────────────────
function copyAsset(src, dest) {
  fs.mkdirSync(path.dirname(dest), { recursive: true });
  fs.copyFileSync(src, dest);
}

function copyAssetTree(srcDir, destDir, skipNames = new Set()) {
  for (const entry of fs.readdirSync(srcDir, { withFileTypes: true })) {
    if (skipNames.has(entry.name)) continue;
    const srcPath  = path.join(srcDir, entry.name);
    const destPath = path.join(destDir, entry.name);
    if (entry.isDirectory()) {
      copyAssetTree(srcPath, destPath, skipNames);
    } else {
      copyAsset(srcPath, destPath);
    }
  }
}

// ── Skill emit ──────────────────────────────────────────────────────────────
function emitSkill({ srcDir, skillName, destSkillsDir }) {
  const skillFile = path.join(srcDir, 'SKILL.md');
  if (!fs.existsSync(skillFile)) {
    return { skipped: true, reason: 'no SKILL.md' };
  }

  const raw = fs.readFileSync(skillFile, 'utf8');
  const { frontmatter, body } = parseFrontmatter(raw);

  const codexName = toCodexName(frontmatter.name || skillName);
  const description = frontmatter.description || '';
  if (!description) {
    return { skipped: true, reason: 'missing description' };
  }

  const destDir = path.join(destSkillsDir, codexName);
  fs.mkdirSync(destDir, { recursive: true });

  const { body: transformedBody, count: transforms } = transformBody(body);

  const newContent = emitCodexFrontmatter({ name: codexName, description })
    + '\n' + transformedBody.replace(/^\n+/, '');

  fs.writeFileSync(path.join(destDir, 'SKILL.md'), newContent, 'utf8');

  copyAssetTree(srcDir, destDir, new Set(['SKILL.md']));

  return { codexName, droppedFields: dropped(frontmatter), transforms };
}

function dropped(fm) {
  return Object.keys(fm).filter(k => !['name', 'description'].includes(k));
}

// ── Command emit (commands without a backing skill become skills on Codex) ──
function emitCommand({ srcFile, destSkillsDir }) {
  const raw = fs.readFileSync(srcFile, 'utf8');
  const { frontmatter, body } = parseFrontmatter(raw);

  const base = path.basename(srcFile, '.md');
  const codexName = `sk-${base}`;
  const description = frontmatter.description || `Slash command: /sk:${base}`;

  const destDir = path.join(destSkillsDir, codexName);
  fs.mkdirSync(destDir, { recursive: true });

  const { body: transformedBody } = transformBody(body);

  const newContent = emitCodexFrontmatter({ name: codexName, description })
    + '\n' + transformedBody.replace(/^\n+/, '');

  fs.writeFileSync(path.join(destDir, 'SKILL.md'), newContent, 'utf8');

  return { codexName };
}

// ── AGENTS.md emit ──────────────────────────────────────────────────────────
function emitAgentsMd({ destDir, repoRoot }) {
  const claudeMdPath = path.join(repoRoot, 'CLAUDE.md');
  let baseContent = '';
  if (fs.existsSync(claudeMdPath)) {
    baseContent = fs.readFileSync(claudeMdPath, 'utf8');
  }

  const header = `<!-- Generated by shipkit --target=codex -->

# AGENTS.md — ShipKit on OpenAI Codex

> Codex CLI + Codex Cloud both read this file. Local hooks and \`~/.codex/\` user config apply only to CLI; cloud installations skip those.

## Skill invocation on Codex

ShipKit slash commands like \`/sk:foo\` are emitted as Codex skills named \`sk-foo\` (colon → dash for filesystem safety). They auto-trigger on description match — no slash typing needed. To force-invoke, ask: "use the sk-foo skill".

## Tool naming differences (vs Claude Code)

| ShipKit reference | Codex equivalent |
|---|---|
| \`Read\` / \`Edit\` / \`Write\` | \`apply_patch\` |
| \`Bash\` | \`shell\` (also exposed as \`Bash\` in matchers) |
| \`Grep\` / \`Glob\` | shell \`rg\` / \`find\` / \`fd\` |
| \`WebFetch\` / \`WebSearch\` | \`web_search\` |
| Sub-agent (\`Agent\` tool) | \`.codex/agents/<name>.toml\` (CLI only; expensive — use sparingly) |

## What is NOT available in Codex Cloud

Codex Cloud (hosted, ChatGPT-side) installations skip:

- **Hooks** — \`.codex/hooks.json\` is CLI-only. SessionStart context loading, pre-commit validation, post-edit formatting, safety-guard, secret-scan, and config-protection hooks do not fire.
- **User-global config** — \`~/.codex/config.toml\` doesn't apply. MCP servers, profiles, and agent presets must ride along in the repo (\`.codex/config.toml\` in the repo root).
- **Background sub-agent execution** — \`codex exec\` from inside a cloud task may not spawn sub-tasks. Sub-agent invocations in skill bodies degrade to sequential in-process iteration.
- **Pencil MCP** (visual design editor) — Claude-native MCP. \`/sk-frontend-design --pencil\` and \`/sk-mvp\` Pencil step downgrade to pure-CSS mockups.
- **context-mode plugin** — Claude-Code-specific harness optimization. Skills using \`ctx_*\` MCP tools fall back to direct shell/file access.

### Detecting your environment

Skills can source \`.codex/lib/env-detect.sh\` to branch on environment:

\`\`\`bash
source .codex/lib/env-detect.sh
# Exports: SHIPKIT_TARGET, SHIPKIT_ENV (cli|cloud), SHIPKIT_HOOKS_OK, SHIPKIT_MCP_OK
\`\`\`

### Cloud-affected skills

| Skill | Cloud delta | Workaround |
|---|---|---|
| \`sk-safety-guard\` | Hook-driven blocking → advisory-only | None needed; logs warnings instead of blocking |
| \`sk-gates\` | Parallel batches → sequential | Slower but correct |
| \`sk-team\` | Parallel domain agents → sequential | Slower but correct |
| \`sk-frontend-design --pencil\` | Pencil unavailable → CSS-only mockups | Use CLI for design work |
| \`sk-mvp\` (Pencil step) | Same as above | Same |
| \`sk-setup-claude\` | Not applicable to Codex | Use \`sk-setup-codex\` (Phase 5 follow-up) |

See \`tasks/codex-quality-deltas.md\` for the full per-skill delta inventory.

---

## ShipKit Workflow Reference

`;

  const footer = `

---

## Skill Directory

ShipKit ships ${countSkills(destDir)} skills under \`.agents/skills/\`. Codex auto-loads names + descriptions on session start; full bodies load on demand. See \`tasks/codex-migration-plan.md\` in this repo for the migration status.

## Reporting

If a skill misbehaves on Codex but works on Claude Code, file under \`tasks/codex-quality-deltas.md\` so it can be addressed in a later phase.
`;

  // Strip Claude-specific banner if present
  const stripped = baseContent
    .replace(/^<!-- Generated by .* -->\n+/, '')
    .replace(/^Version: v[^\n]+\n+/m, '');

  const content = header + stripped + footer;

  // Per Codex spec, project-root AGENTS.md is hard-capped at 32 KiB by default.
  // If we exceed that, the project-doc loader truncates; warn and emit anyway.
  const bytes = Buffer.byteLength(content, 'utf8');
  fs.writeFileSync(path.join(destDir, 'AGENTS.md'), content, 'utf8');

  return { bytes, overLimit: bytes > 32 * 1024 };
}

function countSkills(destDir) {
  const skillsDir = path.join(destDir, '.agents', 'skills');
  if (!fs.existsSync(skillsDir)) return 0;
  return fs.readdirSync(skillsDir, { withFileTypes: true })
    .filter(e => e.isDirectory()).length;
}

// ── Sub-agent emit (.codex/agents/<name>.{toml,md}) ─────────────────────────
//
// Translates ShipKit's Claude-Code sub-agent definitions (from
// core/skills/sk:setup-claude/templates/.claude/agents/*.md) into Codex
// sub-agents:
//   .codex/agents/<name>.toml    config: model, reasoning_effort, sandbox_mode, instructions ref
//   .codex/agents/<name>.md       developer_instructions body
//
// Tool-set inference: Claude's `allowed-tools` field maps to Codex sandbox modes:
//   has Edit/Write/Bash     → workspace-write
//   only Read/Grep/Glob     → read-only
//   anything with side effects → workspace-write
//
// Model mapping: Claude `sonnet`/`opus`/`haiku` are advisory; we emit a
// reasonable Codex default and preserve the original as a comment.

const MODEL_MAP = {
  // Claude → Codex (best-fit; user can override in .codex/config.toml profiles)
  haiku: { model: 'gpt-5-haiku', effort: 'low' },
  sonnet: { model: 'gpt-5',       effort: 'medium' },
  opus:   { model: 'gpt-5',       effort: 'high' },
};

function tomlString(s) {
  return '"' + String(s).replace(/\\/g, '\\\\').replace(/"/g, '\\"') + '"';
}

function inferSandboxMode(allowedToolsStr) {
  // Read-only agents typically have: Read, Grep, Glob, Bash (Bash for git-diff etc.)
  // Mutating agents have: Edit, Write, NotebookEdit
  // Bash alone is ambiguous — Claude lets read-only agents use it for git/ls/grep;
  // we use Edit/Write as the differentiator instead.
  if (!allowedToolsStr) return 'workspace-write';
  const tools = allowedToolsStr.split(',').map(t => t.trim());
  const mutating = tools.some(t => /^(Edit|Write|NotebookEdit)$/i.test(t));
  return mutating ? 'workspace-write' : 'read-only';
}

function emitSubAgent({ srcFile, destAgentsDir }) {
  const raw = fs.readFileSync(srcFile, 'utf8');
  const { frontmatter, body } = parseFrontmatter(raw);

  const name = frontmatter.name;
  if (!name) return { skipped: true, reason: 'no name field' };

  const description    = frontmatter.description || '';
  const claudeModel    = (frontmatter.model || 'sonnet').toLowerCase();
  const allowedTools   = frontmatter['allowed-tools'] || frontmatter.tools || '';
  const sandboxMode    = inferSandboxMode(allowedTools);
  const { model, effort } = MODEL_MAP[claudeModel] || MODEL_MAP.sonnet;

  const tomlBody = `# Generated by shipkit --target=codex
# Source: core/skills/sk:setup-claude/templates/.codex/agents/${name}.md
# Claude original model: ${claudeModel}; allowed-tools: ${allowedTools || '(none)'}

name                   = ${tomlString(name)}
description            = ${tomlString(description)}
model                  = ${tomlString(model)}
model_reasoning_effort = ${tomlString(effort)}
sandbox_mode           = ${tomlString(sandboxMode)}
developer_instructions = ${tomlString(`.codex/agents/${name}.md`)}
`;

  fs.mkdirSync(destAgentsDir, { recursive: true });
  fs.writeFileSync(path.join(destAgentsDir, `${name}.toml`), tomlBody, 'utf8');

  const { body: transformedBody } = transformBody(body);
  fs.writeFileSync(
    path.join(destAgentsDir, `${name}.md`),
    transformedBody.replace(/^\n+/, ''),
    'utf8'
  );

  return { name, sandboxMode, model };
}

function emitSubAgents({ coreDir, destDir }) {
  const agentsSrc = path.join(
    coreDir, 'skills', 'sk:setup-claude', 'templates', '.claude', 'agents'
  );
  const agentsDest = path.join(destDir, '.codex', 'agents');

  const result = { count: 0, skipped: [], failed: [] };
  if (!fs.existsSync(agentsSrc)) return result;

  for (const entry of fs.readdirSync(agentsSrc, { withFileTypes: true })) {
    if (!entry.isFile() || !entry.name.endsWith('.md')) continue;
    try {
      const r = emitSubAgent({
        srcFile: path.join(agentsSrc, entry.name),
        destAgentsDir: agentsDest,
      });
      if (r.skipped) result.skipped.push({ name: entry.name, reason: r.reason });
      else result.count++;
    } catch (err) {
      result.failed.push({ name: entry.name, error: err.message });
    }
  }

  return result;
}

// ── config.toml emit ────────────────────────────────────────────────────────
function emitConfigToml({ destDir, subAgentNames }) {
  const content = `# Generated by shipkit --target=codex
# See https://developers.openai.com/codex/config-reference for full schema.

[features]
codex_hooks = true   # enable .codex/hooks.json (experimental in Codex CLI)

# ── MCP servers ─────────────────────────────────────────────────────────────
# Add servers used in your workflow. Example: context7 docs lookups.
# [mcp_servers.context7]
# command = "npx"
# args    = ["-y", "@upstash/context7-mcp"]

# ── Subagents (CLI-only) ────────────────────────────────────────────────────
# ShipKit ships per-agent configs under .codex/agents/. Codex CLI loads them
# from this directory automatically when the directory exists. Subagents are
# token-expensive — invoke only when needed.
#
# Currently configured agents (see .codex/agents/<name>.toml):
${(subAgentNames || []).map(n => `#   - ${n}`).join('\n') || '#   (none)'}

# ── Profiles ────────────────────────────────────────────────────────────────
[profiles.autopilot]
model                  = "gpt-5"
model_reasoning_effort = "high"
sandbox_mode           = "workspace-write"

[profiles.fast-track]
model                  = "gpt-5"
model_reasoning_effort = "medium"
sandbox_mode           = "workspace-write"

[profiles.read-only]
model                  = "gpt-5-haiku"
model_reasoning_effort = "low"
sandbox_mode           = "read-only"
`;

  const cdir = path.join(destDir, '.codex');
  fs.mkdirSync(cdir, { recursive: true });
  fs.writeFileSync(path.join(cdir, 'config.toml'), content, 'utf8');
  return { path: '.codex/config.toml' };
}

// ── env-detect.sh emit ──────────────────────────────────────────────────────
function emitEnvDetect({ coreDir, destDir }) {
  const src = path.join(coreDir, 'lib', 'env-detect.sh');
  if (!fs.existsSync(src)) return { copied: false };

  const libDir = path.join(destDir, '.codex', 'lib');
  fs.mkdirSync(libDir, { recursive: true });
  const dest = path.join(libDir, 'env-detect.sh');
  fs.copyFileSync(src, dest);
  fs.chmodSync(dest, 0o755);
  return { copied: true, path: '.codex/lib/env-detect.sh' };
}

// ── hooks.json emit ─────────────────────────────────────────────────────────
function emitHooksJson({ coreDir, destDir }) {
  // Map ShipKit's setup-claude hook templates to Codex hook events.
  const hooksSrcDir = path.join(
    coreDir, 'skills', 'sk:setup-claude', 'templates', 'hooks'
  );

  const eventMap = [
    { event: 'SessionStart',     file: 'session-start.sh',     matcher: 'startup' },
    { event: 'PreToolUse',       file: 'validate-commit.sh',   matcher: 'Bash' },
    { event: 'PreToolUse',       file: 'validate-push.sh',     matcher: 'Bash' },
    { event: 'PreToolUse',       file: 'safety-guard.sh',      matcher: 'Bash|apply_patch' },
    { event: 'PreToolUse',       file: 'config-protection.sh', matcher: 'apply_patch' },
    { event: 'PreToolUse',       file: 'scan-secrets.sh',      matcher: 'apply_patch' },
    { event: 'PostToolUse',      file: 'post-edit-format.sh',  matcher: 'apply_patch' },
    { event: 'PostToolUse',      file: 'auto-progress.sh',     matcher: 'apply_patch|Bash' },
    { event: 'PostToolUse',      file: 'log-agent.sh',         matcher: 'mcp__.*' },
    { event: 'UserPromptSubmit', file: 'keyword-router.sh',    matcher: '.*' },
    { event: 'Stop',             file: 'session-stop.sh',      matcher: '.*' },
  ];

  const hooks = {};
  for (const { event, file, matcher } of eventMap) {
    const src = path.join(hooksSrcDir, file);
    if (!fs.existsSync(src)) continue;
    hooks[event] = hooks[event] || [];
    hooks[event].push({
      matcher,
      hooks: [{
        type: 'command',
        command: `bash $CODEX_PROJECT_ROOT/.codex/hooks/${file}`,
        timeout: 30,
      }],
    });
  }

  const cdir = path.join(destDir, '.codex');
  const hooksDir = path.join(cdir, 'hooks');
  fs.mkdirSync(hooksDir, { recursive: true });

  // Copy the actual hook scripts so they exist on disk
  let copied = 0;
  for (const { file } of eventMap) {
    const src = path.join(hooksSrcDir, file);
    if (!fs.existsSync(src)) continue;
    const dest = path.join(hooksDir, file);
    fs.copyFileSync(src, dest);
    fs.chmodSync(dest, 0o755);
    copied++;
  }

  fs.writeFileSync(
    path.join(cdir, 'hooks.json'),
    JSON.stringify({ hooks }, null, 2) + '\n',
    'utf8'
  );

  return { copied, events: Object.keys(hooks).length };
}

// ── Top-level emit/uninstall ────────────────────────────────────────────────
function emit({ coreDir, destDir, repoRoot }) {
  if (!repoRoot) repoRoot = path.join(coreDir, '..');

  const skillsSrc      = path.join(coreDir, 'skills');
  const commandsSrc    = path.join(coreDir, 'commands', 'sk');
  const destSkillsDir  = path.join(destDir, '.agents', 'skills');
  fs.mkdirSync(destSkillsDir, { recursive: true });

  const result = {
    skills: 0,
    commandsAsSkills: 0,
    transforms: 0,
    skipped: [],
    failed: [],
  };

  // Skills
  if (fs.existsSync(skillsSrc)) {
    for (const entry of fs.readdirSync(skillsSrc, { withFileTypes: true })) {
      if (!entry.isDirectory()) continue;
      // Skip non-sk-prefixed directories (e.g. stray .claude/ subdir, find-skills/, etc.)
      if (!entry.name.startsWith('sk:')) continue;
      try {
        const r = emitSkill({
          srcDir: path.join(skillsSrc, entry.name),
          skillName: entry.name,
          destSkillsDir,
        });
        if (r.skipped) {
          result.skipped.push({ name: entry.name, reason: r.reason });
        } else {
          result.skills++;
          result.transforms += r.transforms || 0;
        }
      } catch (err) {
        result.failed.push({ name: entry.name, error: err.message });
      }
    }
  }

  // Commands without a backing skill — promote to Codex skills
  if (fs.existsSync(commandsSrc)) {
    for (const entry of fs.readdirSync(commandsSrc, { withFileTypes: true })) {
      if (!entry.isFile() || !entry.name.endsWith('.md')) continue;
      const skillCounterpart = 'sk:' + entry.name.replace(/\.md$/, '');
      if (fs.existsSync(path.join(skillsSrc, skillCounterpart))) {
        continue; // skill already covers this
      }
      try {
        emitCommand({
          srcFile: path.join(commandsSrc, entry.name),
          destSkillsDir,
        });
        result.commandsAsSkills++;
      } catch (err) {
        result.failed.push({ name: entry.name, error: err.message });
      }
    }
  }

  // Sub-agents (must precede config.toml so we can list them in the file)
  result.subAgents = emitSubAgents({ coreDir, destDir });
  const subAgentNames = []; // collect emitted names by reading dest dir
  const agentsDestDir = path.join(destDir, '.codex', 'agents');
  if (fs.existsSync(agentsDestDir)) {
    for (const e of fs.readdirSync(agentsDestDir, { withFileTypes: true })) {
      if (e.isFile() && e.name.endsWith('.toml')) {
        subAgentNames.push(e.name.replace(/\.toml$/, ''));
      }
    }
  }

  // Side artifacts
  result.envDetect = emitEnvDetect({ coreDir, destDir });
  result.config = emitConfigToml({ destDir, subAgentNames });
  result.hooks  = emitHooksJson({ coreDir, destDir });
  result.agentsMd = emitAgentsMd({ destDir, repoRoot });

  return result;
}

function uninstall({ destDir }) {
  const result = { agentsMd: false, codexDir: false, skillsRemoved: 0 };

  const agentsMd = path.join(destDir, 'AGENTS.md');
  if (fs.existsSync(agentsMd)) {
    fs.rmSync(agentsMd);
    result.agentsMd = true;
  }

  const skillsDir = path.join(destDir, '.agents', 'skills');
  if (fs.existsSync(skillsDir)) {
    const removed = fs.readdirSync(skillsDir, { withFileTypes: true })
      .filter(e => e.isDirectory() && e.name.startsWith('sk-'));
    for (const e of removed) {
      fs.rmSync(path.join(skillsDir, e.name), { recursive: true, force: true });
    }
    result.skillsRemoved = removed.length;
  }

  const codexDir = path.join(destDir, '.codex');
  if (fs.existsSync(codexDir)) {
    fs.rmSync(codexDir, { recursive: true, force: true });
    result.codexDir = true;
  }

  return result;
}

module.exports = { emit, uninstall, parseFrontmatter, toCodexName };

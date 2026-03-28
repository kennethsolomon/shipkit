---
name: sk:plugin
description: "Package your project's custom skills, agents, hooks, and MCP servers as a distributable Claude Code plugin with a plugin.json manifest. Helps teams share Claude Code customizations."
disable-model-invocation: true
argument-hint: "[--name <plugin-name>] [--output <dir>]"
---

# /sk:plugin

Package your custom Claude Code skills, agents, hooks, and MCP servers as a distributable plugin.

> **Note for ShipKit users:** ShipKit itself is distributed via npm (`npx @kennethsolomon/shipkit`), not as a plugin — that gives you shorter `/sk:*` command names and global installation. This skill is for packaging YOUR OWN project-specific customizations to share with your team.

## When to Use This

Use `/sk:plugin` when you have:
- Custom skills in `.claude/skills/` that your team wrote for your project
- Custom agents in `.claude/agents/` you want to share
- Hooks in `settings.json` you want to distribute
- MCP server configs in `.mcp.json` you want to bundle

**Don't use this** to re-package ShipKit itself — it's already on npm.

## Step 1 — Discover What to Package

Scan the project for custom Claude Code assets:

```bash
# Check for custom skills (not ShipKit skills)
ls ~/.claude/skills/ 2>/dev/null
ls .claude/skills/ 2>/dev/null

# Check for custom agents
ls .claude/agents/ 2>/dev/null

# Check for hooks in settings.json
cat .claude/settings.json 2>/dev/null | grep -A 20 '"hooks"'

# Check for MCP config
cat .mcp.json 2>/dev/null
cat .claude/mcp.json 2>/dev/null
```

Report what was found. Ask the user:
> "I found: [N skills], [N agents], [N hooks], [N MCP servers]. Which should be included in the plugin?"

## Step 2 — Gather Plugin Info

Ask:

```
Plugin name (kebab-case, e.g. "my-team-tools"):
Plugin version (default: 1.0.0):
Plugin description (1 sentence):
Author (name or org):
```

## Step 3 — Create Plugin Structure

Create the plugin directory structure:

```
<plugin-name>/
├── plugin.json              # manifest
├── skills/                  # selected skills
│   └── <skill-name>/
│       └── SKILL.md
├── agents/                  # selected agents
│   └── <agent-name>.md
├── hooks/
│   └── hooks.json           # selected hooks
├── .mcp.json                # MCP server configs (if any)
└── README.md                # auto-generated install instructions
```

### plugin.json manifest

```json
{
  "name": "<plugin-name>",
  "version": "1.0.0",
  "description": "<description>",
  "author": "<author>",
  "skills": [
    { "name": "<skill-name>", "path": "skills/<skill-name>/SKILL.md" }
  ],
  "agents": [
    { "name": "<agent-name>", "path": "agents/<agent-name>.md" }
  ],
  "hooks": "hooks/hooks.json",
  "mcp": ".mcp.json"
}
```

### hooks/hooks.json format

Convert from `settings.json` format:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          { "type": "command", "command": "your-hook-command" }
        ]
      }
    ]
  }
}
```

## Step 4 — Copy Selected Assets

For each selected skill:
1. Copy the skill directory to `<plugin-name>/skills/<skill-name>/`
2. Update any hardcoded paths to use `${CLAUDE_SKILL_DIR}` for portability

For each selected agent:
1. Copy the `.md` file to `<plugin-name>/agents/`
2. Review for hardcoded project-specific paths

For hooks:
1. Extract selected hooks from `settings.json`
2. Write to `<plugin-name>/hooks/hooks.json`

For MCP:
1. Copy relevant entries from `.mcp.json` to `<plugin-name>/.mcp.json`
2. Replace hardcoded paths with `${CLAUDE_PLUGIN_DIR}` placeholders

## Step 5 — Generate README.md

Create `<plugin-name>/README.md`:

```markdown
# <plugin-name>

<description>

## Install

### Option 1: Copy to project
```bash
cp -r <plugin-name>/.claude/skills/* .claude/skills/
cp -r <plugin-name>/.claude/agents/* .claude/agents/
```

### Option 2: Plugin install (when supported)
```bash
# In Claude Code terminal:
/plugin install ./<plugin-name>
```

### Option 3: npm (if published)
```bash
npx <plugin-name>
```

## Included

### Skills
<list skills with descriptions>

### Agents
<list agents with descriptions>

### Hooks
<list hooks with what they do>

## Configuration

<any required env vars or config>
```

## Step 6 — Validate

Check the plugin is well-formed:

```bash
# All referenced files exist
# plugin.json is valid JSON
# Skills have valid frontmatter (name, description)
# Agents have valid frontmatter (name, description, model, tools)
# hooks.json follows the correct event/matcher format
```

Report: "Plugin `<name>` created at `./<plugin-name>/` — N skills, N agents, N hooks."

## Step 7 — Distribution Options

Present options:

**Option A — Share within team (simplest):**
```bash
# Commit the plugin directory to your repo
git add <plugin-name>/
git commit -m "feat: add <plugin-name> Claude Code plugin"
# Team members run the setup script or copy manually
```

**Option B — npm package:**
```bash
# Add to package.json:
# "bin": { "<plugin-name>": "bin/install.js" }
# The install.js copies files to ~/.claude/skills/ and ~/.claude/agents/
npm publish
# Install: npx <plugin-name>
```

**Option C — Future: Plugin marketplace**
When Anthropic launches a plugin marketplace, you'll be able to submit via:
`https://claude.ai/settings/plugins/submit`

## Updating an Existing Plugin

If a `plugin.json` already exists in the target directory:
1. Show a diff of what changed since last packaging
2. Ask which changes to include
3. Bump the patch version automatically
4. Update README.md

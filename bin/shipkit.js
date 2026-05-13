#!/usr/bin/env node
'use strict';

const fs   = require('fs');
const path = require('path');
const os   = require('os');

const pkg = require('../package.json');

// ── ANSI ────────────────────────────────────────────────────────────────────
const cyan   = '\x1b[36m';
const green  = '\x1b[32m';
const yellow = '\x1b[33m';
const red    = '\x1b[31m';
const bold   = '\x1b[1m';
const dim    = '\x1b[2m';
const reset  = '\x1b[0m';

// ── Pirate ship ASCII art ────────────────────────────────────────────────────
const banner = `
${cyan}           ⚑${reset}
${cyan}           |${reset}
${cyan}          /|\\${reset}
${cyan}         / | \\${reset}
${cyan}        /  |  \\${reset}
${cyan}       /   |   \\${reset}
${cyan}      / ☠  |  ☠ \\${reset}
${cyan}     /     |     \\${reset}
${cyan}    /______|______\\${reset}
${cyan}  ▄████████████████▄${reset}
${cyan}  █  ◉          ◉  █${reset}
${cyan}   ▀██████████████▀${reset}
${cyan}     ≋  ≋  ≋  ≋  ≋${reset}

  ${bold}ShipKit${reset} ${dim}v${pkg.version}${reset}
  Quality-gated workflow toolkit for Claude Code + Codex.
  TDD · Lint · Security · Review · Ship.
  by Kenneth Solomon

`;

const USAGE = `
Usage: shipkit [options]

Options:
  --target <name>   Install for target: claude (default), codex, both
  -u, --uninstall   Remove installed ShipKit files for the selected target
  -h, --help        Show this help

Examples:
  shipkit                       Install for Claude Code (default)
  shipkit --target=codex        Install for Codex CLI / Cloud in current repo
  shipkit --target=both         Install for both targets
  shipkit --uninstall           Remove from Claude Code
`;

// ── Helpers ──────────────────────────────────────────────────────────────────
function getClaudeDir() {
  if (process.platform === 'win32') {
    return path.join(process.env.APPDATA || os.homedir(), 'Claude');
  }
  return path.join(os.homedir(), '.claude');
}

function getCodexProjectDir() {
  return process.cwd();
}

function getDestDir(target) {
  if (target === 'claude') return getClaudeDir();
  if (target === 'codex')  return getCodexProjectDir();
  throw new Error(`Unknown target: ${target}`);
}

function loadAdapter(target) {
  return require(path.join(__dirname, '..', 'adapters', target, 'emit.js'));
}

function parseArgs(argv) {
  const args = { target: 'claude', uninstall: false, help: false };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '-h' || a === '--help')        { args.help = true; continue; }
    if (a === '-u' || a === '--uninstall')   { args.uninstall = true; continue; }
    if (a.startsWith('--target=')) {
      args.target = a.slice('--target='.length);
      continue;
    }
    if (a === '--target') {
      args.target = argv[++i];
      continue;
    }
    console.error(`${yellow}Unknown argument: ${a}${reset}`);
  }
  return args;
}

function targetsFromFlag(flag) {
  if (flag === 'both') return ['claude', 'codex'];
  return [flag];
}

// ── Install / Uninstall ──────────────────────────────────────────────────────
function runInstall(targets) {
  process.stdout.write(banner);
  const pkgDir  = path.join(__dirname, '..');
  const coreDir = path.join(pkgDir, 'core');

  for (const target of targets) {
    console.log(`  ${bold}Target:${reset} ${cyan}${target}${reset}`);
    const destDir = getDestDir(target);
    if (!fs.existsSync(destDir)) fs.mkdirSync(destDir, { recursive: true });

    const adapter = loadAdapter(target);
    try {
      const r = adapter.emit({ coreDir, destDir, repoRoot: pkgDir });
      reportInstall(target, r);
    } catch (err) {
      console.log(`  ${red}✗${reset} ${target} adapter failed: ${err.message}`);
      process.exitCode = 1;
      continue;
    }
  }

  console.log(`\n  ${green}Done!${reset} Run ${cyan}/sk:help${reset} (Claude) or ask Codex to "use the sk-help skill" to get started.\n`);
}

function runUninstall(targets) {
  process.stdout.write(banner);

  for (const target of targets) {
    console.log(`  ${bold}Target:${reset} ${cyan}${target}${reset}`);
    const destDir = getDestDir(target);
    const adapter = loadAdapter(target);
    try {
      const r = adapter.uninstall({ destDir });
      reportUninstall(target, r);
    } catch (err) {
      console.log(`  ${red}✗${reset} ${target} adapter failed: ${err.message}`);
      process.exitCode = 1;
    }
  }

  console.log(`\n  ${green}Done!${reset} ShipKit uninstalled.\n`);
}

function reportInstall(target, r) {
  if (target === 'claude') {
    const skipNote = r.skippedCommands
      ? ` ${dim}(${r.skippedCommands} skipped — covered by skills)${reset}`
      : '';
    console.log(`  ${green}✓${reset} Installed commands/sk ${dim}(${r.commands} commands)${reset}${skipNote}`);
    if (r.failedSkills && r.failedSkills.length) {
      console.log(`  ${yellow}!${reset} ${r.failedSkills.length} skill(s) failed: ${dim}${r.failedSkills.join(', ')}${reset}`);
    }
    console.log(`  ${green}✓${reset} Installed skills ${dim}(${r.skills} skills)${reset}`);
    if (r.cleanedStale > 0) {
      console.log(`  ${green}✓${reset} Cleaned ${r.cleanedStale} stale command(s) superseded by skills`);
    }
    return;
  }

  if (target === 'codex') {
    const xform = r.transforms ? ` ${dim}(${r.transforms} path transforms applied)${reset}` : '';
    console.log(`  ${green}✓${reset} Emitted ${r.skills} skills ${dim}(.agents/skills/)${reset}${xform}`);
    if (r.commandsAsSkills > 0) {
      console.log(`  ${green}✓${reset} Promoted ${r.commandsAsSkills} command(s) to skills`);
    }
    if (r.skipped && r.skipped.length) {
      console.log(`  ${yellow}!${reset} Skipped ${r.skipped.length} skill(s): ${dim}${r.skipped.map(s => `${s.name}(${s.reason})`).join(', ')}${reset}`);
    }
    if (r.failed && r.failed.length) {
      console.log(`  ${red}✗${reset} ${r.failed.length} skill(s) failed: ${dim}${r.failed.map(f => `${f.name}(${f.error})`).join(', ')}${reset}`);
    }
    if (r.subAgents && r.subAgents.count > 0) {
      console.log(`  ${green}✓${reset} Emitted ${r.subAgents.count} sub-agent(s) ${dim}(.codex/agents/)${reset}`);
    }
    console.log(`  ${green}✓${reset} Wrote AGENTS.md ${dim}(${r.agentsMd.bytes} bytes${r.agentsMd.overLimit ? ', OVER 32 KiB limit — split into nested AGENTS.md recommended' : ''})${reset}`);
    console.log(`  ${green}✓${reset} Wrote .codex/config.toml`);
    console.log(`  ${green}✓${reset} Wrote .codex/hooks.json + ${r.hooks.copied} hook script(s) ${dim}(${r.hooks.events} event(s))${reset}`);
    return;
  }

  console.log(`  ${green}✓${reset} ${target} emit complete ${dim}(${JSON.stringify(r)})${reset}`);
}

function reportUninstall(target, r) {
  if (target === 'claude') {
    if (r.commandsRemoved) console.log(`  ${green}✓${reset} Removed commands/sk`);
    console.log(`  ${green}✓${reset} Removed ${r.skillsRemoved} skills`);
  } else {
    console.log(`  ${green}✓${reset} ${target} uninstall complete ${dim}(${JSON.stringify(r)})${reset}`);
  }
}

// ── Entry point ──────────────────────────────────────────────────────────────
const args = parseArgs(process.argv.slice(2));

if (args.help) {
  process.stdout.write(banner);
  console.log(USAGE);
  process.exit(0);
}

const targets = targetsFromFlag(args.target);
if (args.uninstall) {
  runUninstall(targets);
} else {
  runInstall(targets);
}

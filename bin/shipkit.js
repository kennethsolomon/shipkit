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
const bold   = '\x1b[1m';
const dim    = '\x1b[2m';
const reset  = '\x1b[0m';

// ── Pirate ship ASCII art ────────────────────────────────────────────────────
const banner = `
${cyan}                 ▄${reset}
${cyan}                 █${reset}
${cyan}                 █${reset}
${cyan}           ▄████████▄${reset}
${cyan}          ██░░░☠░░░░██${reset}
${cyan}          ██░░░░░░░░██${reset}
${cyan}           ▀████████▀${reset}
${cyan}       ▄███████████████▄${reset}
${cyan}      ██░░◉░░░░░░░░◉░░██${reset}
${cyan}       ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀${reset}
${cyan}        ≋  ≋  ≋  ≋  ≋  ≋${reset}

  ${bold}ShipKit${reset} ${dim}v${pkg.version}${reset}
  A structured workflow toolkit for Claude Code.
  by Kenneth Solomon

`;

// ── Helpers ──────────────────────────────────────────────────────────────────
function getClaudeDir() {
  if (process.platform === 'win32') {
    return path.join(process.env.APPDATA || os.homedir(), 'Claude');
  }
  return path.join(os.homedir(), '.claude');
}

function copyDir(src, dest) {
  fs.mkdirSync(dest, { recursive: true });
  for (const entry of fs.readdirSync(src, { withFileTypes: true })) {
    const srcPath  = path.join(src, entry.name);
    const destPath = path.join(dest, entry.name);
    if (entry.isDirectory()) {
      copyDir(srcPath, destPath);
    } else {
      fs.copyFileSync(srcPath, destPath);
    }
  }
}

function countFiles(dir, ext) {
  if (!fs.existsSync(dir)) return 0;
  return fs.readdirSync(dir).filter(f => f.endsWith(ext)).length;
}

// ── Uninstall ────────────────────────────────────────────────────────────────
function uninstall() {
  process.stdout.write(banner);
  const claudeDir   = getClaudeDir();
  const commandsDest = path.join(claudeDir, 'commands', 'sk');
  const skillsDest   = path.join(claudeDir, 'skills');

  if (fs.existsSync(commandsDest)) {
    fs.rmSync(commandsDest, { recursive: true, force: true });
    console.log(`  ${green}✓${reset} Removed commands/sk`);
  }

  // Remove only sk: prefixed skill dirs
  if (fs.existsSync(skillsDest)) {
    const removed = fs.readdirSync(skillsDest, { withFileTypes: true })
      .filter(e => e.isDirectory() && e.name.startsWith('sk:'))
      .map(e => {
        fs.rmSync(path.join(skillsDest, e.name), { recursive: true, force: true });
        return e.name;
      });
    console.log(`  ${green}✓${reset} Removed ${removed.length} skills`);
  }

  console.log(`\n  ${green}Done!${reset} ShipKit uninstalled.\n`);
}

// ── Install ──────────────────────────────────────────────────────────────────
function install() {
  process.stdout.write(banner);

  const claudeDir  = getClaudeDir();
  const pkgDir     = path.join(__dirname, '..');

  // Check Claude dir exists
  if (!fs.existsSync(claudeDir)) {
    fs.mkdirSync(claudeDir, { recursive: true });
  }

  // Install commands/sk/
  const commandsSrc  = path.join(pkgDir, 'commands', 'sk');
  const commandsDest = path.join(claudeDir, 'commands', 'sk');

  if (fs.existsSync(commandsSrc)) {
    copyDir(commandsSrc, commandsDest);
    const count = countFiles(commandsSrc, '.md');
    console.log(`  ${green}✓${reset} Installed commands/sk ${dim}(${count} commands)${reset}`);
  } else {
    console.log(`  ${yellow}!${reset} commands/sk not found — skipping`);
  }

  // Install skills/sk:*/
  const skillsSrc  = path.join(pkgDir, 'skills');
  const skillsDest = path.join(claudeDir, 'skills');
  let skillCount = 0;

  if (fs.existsSync(skillsSrc)) {
    const skillDirs = fs.readdirSync(skillsSrc, { withFileTypes: true })
      .filter(e => e.isDirectory());

    for (const entry of skillDirs) {
      const src  = path.join(skillsSrc, entry.name);
      const dest = path.join(skillsDest, entry.name);
      copyDir(src, dest);
      skillCount++;
    }
    console.log(`  ${green}✓${reset} Installed skills ${dim}(${skillCount} skills)${reset}`);
  } else {
    console.log(`  ${yellow}!${reset} skills/ not found — skipping`);
  }

  console.log(`\n  ${green}Done!${reset} Run ${cyan}/sk:help${reset} to get started.\n`);
}

// ── Entry point ──────────────────────────────────────────────────────────────
const args = process.argv.slice(2);

if (args.includes('--uninstall') || args.includes('-u')) {
  uninstall();
} else {
  install();
}

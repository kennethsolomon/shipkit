'use strict';

const fs   = require('fs');
const path = require('path');

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

function emit({ coreDir, destDir }) {
  const commandsSrc  = path.join(coreDir, 'commands', 'sk');
  const skillsSrc    = path.join(coreDir, 'skills');
  const commandsDest = path.join(destDir, 'commands', 'sk');
  const skillsDest   = path.join(destDir, 'skills');

  const result = { commands: 0, skills: 0, skippedCommands: 0, failedSkills: [], cleanedStale: 0 };

  if (fs.existsSync(commandsSrc)) {
    fs.mkdirSync(commandsDest, { recursive: true });
    for (const entry of fs.readdirSync(commandsSrc, { withFileTypes: true })) {
      const srcPath  = path.join(commandsSrc, entry.name);
      const destPath = path.join(commandsDest, entry.name);
      if (entry.isDirectory()) {
        copyDir(srcPath, destPath);
      } else if (entry.name.endsWith('.md')) {
        const skillName = 'sk:' + entry.name.replace(/\.md$/, '');
        if (fs.existsSync(path.join(skillsSrc, skillName))) {
          result.skippedCommands++;
          continue;
        }
        fs.copyFileSync(srcPath, destPath);
        result.commands++;
      } else {
        fs.copyFileSync(srcPath, destPath);
      }
    }
  }

  if (fs.existsSync(skillsSrc)) {
    const skillDirs = fs.readdirSync(skillsSrc, { withFileTypes: true })
      .filter(e => e.isDirectory());

    for (const entry of skillDirs) {
      const src  = path.join(skillsSrc, entry.name);
      const dest = path.join(skillsDest, entry.name);
      try {
        try {
          const lstat = fs.lstatSync(dest);
          if (lstat.isSymbolicLink()) fs.unlinkSync(dest);
        } catch (_) { /* dest doesn't exist — fine */ }
        copyDir(src, dest);
        result.skills++;
      } catch (err) {
        result.failedSkills.push(entry.name);
      }
    }
  }

  if (fs.existsSync(commandsDest) && fs.existsSync(skillsDest)) {
    for (const entry of fs.readdirSync(commandsDest, { withFileTypes: true })) {
      if (!entry.isFile() || !entry.name.endsWith('.md')) continue;
      const skillName = 'sk:' + entry.name.replace(/\.md$/, '');
      if (fs.existsSync(path.join(skillsDest, skillName))) {
        fs.rmSync(path.join(commandsDest, entry.name));
        result.cleanedStale++;
      }
    }
  }

  return result;
}

function uninstall({ destDir }) {
  const commandsDest = path.join(destDir, 'commands', 'sk');
  const skillsDest   = path.join(destDir, 'skills');
  const result = { commandsRemoved: false, skillsRemoved: 0 };

  if (fs.existsSync(commandsDest)) {
    fs.rmSync(commandsDest, { recursive: true, force: true });
    result.commandsRemoved = true;
  }

  if (fs.existsSync(skillsDest)) {
    const removed = fs.readdirSync(skillsDest, { withFileTypes: true })
      .filter(e => e.isDirectory() && e.name.startsWith('sk:'))
      .map(e => {
        fs.rmSync(path.join(skillsDest, e.name), { recursive: true, force: true });
        return e.name;
      });
    result.skillsRemoved = removed.length;
  }

  return result;
}

module.exports = { emit, uninstall };

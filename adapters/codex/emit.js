'use strict';

// Codex adapter — Phase 2 of the migration will fill this in.
// See tasks/codex-migration-plan.md for the full spec.
//
// Target output (planned):
//   <destDir>/AGENTS.md
//   <destDir>/.agents/skills/<name>/SKILL.md   (frontmatter: name, description only)
//   <destDir>/.codex/config.toml                (MCP servers, agents, profiles)
//   <destDir>/.codex/hooks.json                 (CLI-only)

function emit(_opts) {
  throw new Error(
    'Codex adapter is not yet implemented. ' +
    'See tasks/codex-migration-plan.md (Phase 2). ' +
    'Use --target=claude for now.'
  );
}

function uninstall(_opts) {
  throw new Error('Codex adapter uninstall is not yet implemented.');
}

module.exports = { emit, uninstall };

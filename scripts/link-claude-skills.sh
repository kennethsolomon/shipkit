#!/usr/bin/env bash
set -euo pipefail

agents_dir="${HOME}/.agents/skills"
claude_dir="${HOME}/.claude/skills"

mkdir -p "${claude_dir}"

shopt -s nullglob
for d in "${agents_dir}"/*; do
  [[ -d "${d}" ]] || continue
  [[ -f "${d}/SKILL.md" ]] || continue

  name="$(basename "${d}")"
  target="${claude_dir}/${name}"

  if [[ -e "${target}" && ! -L "${target}" ]]; then
    echo "skip (exists, not symlink): ${target}"
    continue
  fi

  ln -sfn "${d}" "${target}"
  echo "linked: ${target} -> ${d}"
done

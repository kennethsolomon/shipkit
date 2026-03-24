#!/usr/bin/env bash
# config-protection.sh — PreToolUse hook for Edit/Write
# Blocks modifications to linter/formatter configs.
# Override: SHIPKIT_ALLOW_CONFIG_EDIT=1

set -euo pipefail

if [[ "${SHIPKIT_ALLOW_CONFIG_EDIT:-0}" == "1" ]]; then
  exit 0
fi

# Read the tool input from stdin
INPUT=$(cat)

# Extract the file path from the tool input
FILE_PATH=$(echo "$INPUT" | grep -oE '"file_path"\s*:\s*"[^"]*"' | head -1 | sed 's/.*: *"//;s/"$//')

if [[ -z "$FILE_PATH" ]]; then
  exit 0
fi

BASENAME=$(basename "$FILE_PATH")

# Protected config patterns
PROTECTED_CONFIGS=(
  ".eslintrc"
  ".eslintrc.js"
  ".eslintrc.cjs"
  ".eslintrc.json"
  ".eslintrc.yml"
  ".eslintrc.yaml"
  "eslint.config.js"
  "eslint.config.mjs"
  "eslint.config.cjs"
  ".prettierrc"
  ".prettierrc.js"
  ".prettierrc.cjs"
  ".prettierrc.json"
  ".prettierrc.yml"
  ".prettierrc.yaml"
  "prettier.config.js"
  "prettier.config.mjs"
  "biome.json"
  "biome.jsonc"
  ".stylelintrc"
  ".stylelintrc.json"
  ".stylelintrc.js"
  "stylelint.config.js"
  "phpstan.neon"
  "phpstan.neon.dist"
  "pint.json"
  "rector.php"
  ".php-cs-fixer.php"
  ".php-cs-fixer.dist.php"
  ".rubocop.yml"
  ".golangci.yml"
  ".golangci.yaml"
  "rustfmt.toml"
  ".clang-format"
)

for config in "${PROTECTED_CONFIGS[@]}"; do
  if [[ "$BASENAME" == "$config" ]]; then
    echo "BLOCKED: Modifying linter/formatter config '$BASENAME'."
    echo "Fix the code instead of weakening the rules."
    echo "Override: set SHIPKIT_ALLOW_CONFIG_EDIT=1"
    exit 2
  fi
done

exit 0

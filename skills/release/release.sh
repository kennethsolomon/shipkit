#!/bin/bash

# Release automation script - generic for any project
# Usage: /release
# This script:
#   1. Auto-detects project info (name, version, GitHub URL)
#   2. Prompts for version number
#   3. Updates CHANGELOG.md with [Unreleased] → [Version]
#   4. Updates version in CLAUDE.md
#   5. Creates git tag
#   6. Pushes tag to GitHub

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'  # No Color

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

detect_project_name() {
    # Try multiple sources in order of preference

    # 1. Check CLAUDE.md for project name
    if [ -f "CLAUDE.md" ]; then
        local name=$(grep -E "^# " CLAUDE.md | head -1 | sed 's/^# //')
        if [ -n "$name" ] && [ "$name" != "CLAUDE.md" ]; then
            echo "$name"
            return 0
        fi
    fi

    # 2. Check package.json (Node projects)
    if [ -f "package.json" ]; then
        local name=$(grep '"name"' package.json | head -1 | sed 's/.*"name"\s*:\s*"\([^"]*\)".*/\1/')
        if [ -n "$name" ]; then
            echo "$name"
            return 0
        fi
    fi

    # 3. Check pyproject.toml (Python projects)
    if [ -f "pyproject.toml" ]; then
        local name=$(grep -E "^name\s*=" pyproject.toml | head -1 | sed 's/.*=\s*"\([^"]*\)".*/\1/')
        if [ -n "$name" ]; then
            echo "$name"
            return 0
        fi
    fi

    # 4. Check Cargo.toml (Rust projects)
    if [ -f "Cargo.toml" ]; then
        local name=$(grep -E "^name\s*=" Cargo.toml | head -1 | sed 's/.*=\s*"\([^"]*\)".*/\1/')
        if [ -n "$name" ]; then
            echo "$name"
            return 0
        fi
    fi

    # 5. Fall back to directory name
    basename "$(pwd)"
}

detect_github_url() {
    # Get GitHub URL from git remote origin
    if git remote -v 2>/dev/null | grep -q "origin"; then
        local url=$(git remote get-url origin 2>/dev/null || echo "")
        # Convert SSH to HTTPS if needed
        url=$(echo "$url" | sed 's/git@github.com:/https:\/\/github.com\//' | sed 's/\.git$//')
        if [ -n "$url" ]; then
            echo "$url"
            return 0
        fi
    fi
    echo ""
}

detect_current_version() {
    # Try to find version in CLAUDE.md
    if [ -f "CLAUDE.md" ]; then
        local version=$(grep -E "^Version:" CLAUDE.md | head -1 | awk '{print $NF}')
        if [ -n "$version" ]; then
            echo "$version"
            return 0
        fi
    fi
    echo ""
}

validate_version() {
    local version=$1
    # Validate semantic versioning format
    if [[ $version =~ ^v?[0-9]+\.[0-9]+\.[0-9]+(-[a-zA-Z0-9]+)?$ ]]; then
        return 0
    fi
    return 1
}

suggest_release_title() {
    # Analyze [Unreleased] section and suggest a title
    if ! [ -f "CHANGELOG.md" ]; then
        echo ""
        return 0
    fi

    local unreleased_content=$(sed -n '/## \[Unreleased\]/,/^---$/p' CHANGELOG.md 2>/dev/null || echo "")

    # Suggest based on keywords
    if echo "$unreleased_content" | grep -qi "security"; then
        echo "Security & Stability Improvements"
    elif echo "$unreleased_content" | grep -qi "performance\|optimize"; then
        echo "Performance Optimization & Enhancements"
    elif echo "$unreleased_content" | grep -qi "error\|fix\|bug\|stability"; then
        echo "Stability & Bug Fixes"
    elif echo "$unreleased_content" | grep -qi "breaking\|migration"; then
        echo "Major Release & Breaking Changes"
    else
        echo "Features & Improvements"
    fi
}

# ============================================================================
# MAIN SCRIPT
# ============================================================================

echo -e "${BLUE}📦 Release Automation${NC}"
echo ""

# Check if CHANGELOG.md exists
if [ ! -f "CHANGELOG.md" ]; then
    echo -e "${RED}❌ CHANGELOG.md not found in current directory${NC}"
    echo ""
    echo "This project needs a CHANGELOG.md file to use the release script."
    echo "See: https://keepachangelog.com/"
    exit 1
fi

# Check if CHANGELOG.md has [Unreleased] section
if ! grep -q "## \[Unreleased\]" CHANGELOG.md; then
    echo -e "${RED}❌ No [Unreleased] section found in CHANGELOG.md${NC}"
    exit 1
fi

# Auto-detect project info
PROJECT_NAME=$(detect_project_name)
CURRENT_VERSION=$(detect_current_version)
GITHUB_URL=$(detect_github_url)

echo -e "${YELLOW}Project: ${PROJECT_NAME}${NC}"
if [ -n "$CURRENT_VERSION" ]; then
    echo -e "${YELLOW}Current version: ${CURRENT_VERSION}${NC}"
fi
echo ""

# Prompt for new version
while true; do
    read -p "Enter new version (e.g., v0.2.0, 1.0.0-beta): " NEW_VERSION

    if [ -z "$NEW_VERSION" ]; then
        echo -e "${RED}❌ Version cannot be empty${NC}"
        continue
    fi

    if validate_version "$NEW_VERSION"; then
        break
    else
        echo -e "${RED}❌ Invalid version format. Use semantic versioning (e.g., v0.2.0, 1.0.0-beta)${NC}"
    fi
done

# Normalize version (ensure starts with 'v')
if [[ ! $NEW_VERSION =~ ^v ]]; then
    NEW_VERSION="v${NEW_VERSION}"
fi

echo -e "${GREEN}✅ Version: ${NEW_VERSION}${NC}"
echo ""

# Get today's date
TODAY=$(date +%Y-%m-%d)

# Suggest release title
echo -e "${BLUE}💭 Analyzing changes for title suggestion...${NC}"
SUGGESTED_TITLE=$(suggest_release_title)
echo -e "${YELLOW}Suggested title: ${SUGGESTED_TITLE}${NC}"

read -p "Use suggested title or enter your own (leave blank for suggestion): " RELEASE_TITLE
if [ -z "$RELEASE_TITLE" ]; then
    RELEASE_TITLE="$SUGGESTED_TITLE"
fi
echo -e "${GREEN}✅ Release title: ${RELEASE_TITLE}${NC}"
echo ""

# Update CHANGELOG.md
echo -e "${BLUE}📝 Updating CHANGELOG.md...${NC}"

export NEW_VERSION TODAY
python3 << 'PYTHON_SCRIPT'
import os
import sys

new_version = os.environ['NEW_VERSION']
today = os.environ['TODAY']

with open('CHANGELOG.md', 'r') as f:
    content = f.read()

# Find the unreleased section
unreleased_marker = "## [Unreleased]"
unreleased_index = content.find(unreleased_marker)

if unreleased_index == -1:
    print("ERROR: Could not find [Unreleased] section")
    sys.exit(1)

# Find the next section separator (---)
next_section = content.find("\n---\n", unreleased_index)
if next_section == -1:
    print("ERROR: Could not find section separator (---)")
    sys.exit(1)

# Extract the unreleased content (everything between marker and separator)
unreleased_content = content[unreleased_index + len(unreleased_marker):next_section]

# Create new changelog with fresh [Unreleased] section
header = """# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- _Upcoming features and improvements will be listed here_

### Changed
- _Behavioral changes will be listed here_

### Deprecated
- _Features being phased out will be listed here_

### Removed
- _Features being removed will be listed here_

### Fixed
- _Bug fixes will be listed here_

### Security
- _Security fixes will be listed here_

---

## [{new_version}] - {today}
{unreleased_content}

---

""".format(new_version=new_version, today=today, unreleased_content=unreleased_content)

# Get rest of content (everything after the first separator)
rest_content = content[next_section + len("\n---\n"):]

# Build final content
final_content = header + rest_content

with open('CHANGELOG.md', 'w') as f:
    f.write(final_content)

print("CHANGELOG.md updated successfully")
PYTHON_SCRIPT

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Failed to update CHANGELOG.md${NC}"
    exit 1
fi

echo -e "${GREEN}✅ CHANGELOG.md updated${NC}"

# Update version in CLAUDE.md (if it exists)
if [ -f "CLAUDE.md" ]; then
    echo -e "${BLUE}📝 Updating version in CLAUDE.md...${NC}"
    # Ensure version stored in CLAUDE.md always starts with exactly one 'v'
    CLEAN_VERSION="${NEW_VERSION#v}"  # strip leading 'v' if present

    # Use sed with in-place editing (compatible with macOS and Linux)
    if grep -q "^Version:" CLAUDE.md; then
        sed -i '' "s/^Version: .*/Version: v${CLEAN_VERSION}/" CLAUDE.md 2>/dev/null || sed -i "s/^Version: .*/Version: v${CLEAN_VERSION}/" CLAUDE.md
    else
        # Add Version line after title if it doesn't exist
        sed -i '' "2a\\
Version: v${CLEAN_VERSION}
" CLAUDE.md 2>/dev/null || sed -i "2a Version: v${CLEAN_VERSION}" CLAUDE.md
    fi
    echo -e "${GREEN}✅ CLAUDE.md version updated${NC}"
fi

# Stage changes
echo ""
echo -e "${BLUE}🔗 Staging changes...${NC}"
git add CHANGELOG.md 2>/dev/null
[ -f "CLAUDE.md" ] && git add CLAUDE.md 2>/dev/null

echo -e "${GREEN}✅ Changes staged${NC}"
git status 2>/dev/null || true

# Prompt before commit
echo ""
read -p "Commit these changes? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}⏭️  Skipped commit${NC}"
    exit 0
fi

# Create commit
echo -e "${BLUE}💬 Creating commit...${NC}"
git commit -m "chore: Release ${NEW_VERSION}

- Update CHANGELOG.md with release notes
- Update version in CLAUDE.md

Co-Authored-By: Release Automation <noreply@release.local>"

echo -e "${GREEN}✅ Commit created${NC}"

# Create and push tag
echo ""
echo -e "${BLUE}🏷️  Creating tag ${NEW_VERSION}...${NC}"
git tag -a "${NEW_VERSION}" -m "Release ${NEW_VERSION}"
echo -e "${GREEN}✅ Tag created${NC}"

# Prompt before push
echo ""
read -p "Push tag to GitHub? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}⏭️  Skipped push. You can push manually with: git push origin ${NEW_VERSION}${NC}"
    exit 0
fi

echo -e "${BLUE}🚀 Pushing to GitHub...${NC}"
if git push origin "${NEW_VERSION}" 2>/dev/null; then
    echo -e "${GREEN}✅ Tag pushed to GitHub${NC}"
else
    echo -e "${RED}❌ Failed to push tag to GitHub${NC}"
    echo "You can push manually with: git push origin ${NEW_VERSION}"
    exit 1
fi

echo ""
echo -e "${GREEN}✅ Release ${NEW_VERSION} completed!${NC}"
echo ""

# Show next steps
if [ -n "$GITHUB_URL" ]; then
    echo -e "${BLUE}📋 Next steps:${NC}"
    echo "1. Go to: ${GITHUB_URL}/releases/tag/${NEW_VERSION}"
    echo "2. Click 'Create release from tag'"
    echo "3. Use this as the release title:"
    echo -e "   ${YELLOW}${RELEASE_TITLE}${NC}"
    echo "4. Copy the [${NEW_VERSION}] section from CHANGELOG.md as release notes"
    echo "5. Publish!"
else
    echo -e "${BLUE}📋 Next steps:${NC}"
    echo "1. Go to your GitHub releases page"
    echo "2. Create a new release from tag: ${NEW_VERSION}"
    echo "3. Title: ${RELEASE_TITLE}"
    echo "4. Notes: Copy the [${NEW_VERSION}] section from CHANGELOG.md"
fi

echo ""

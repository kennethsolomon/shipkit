#!/usr/bin/env python3
"""
Detect architectural changes in git diff and generate arch log entry draft.

Analyzes git diff main..HEAD to identify:
- Control flow changes (skill interactions, execution order)
- Data flow changes (context threading, new files)
- Pattern changes (new design patterns)
- Integration changes (new connections between components)

Usage:
  python detect_arch_changes.py                    # Generate and save arch log
  python detect_arch_changes.py --dry-run          # Show what would be generated
  python detect_arch_changes.py --output FILE      # Save to specific file
"""

import sys
import subprocess
from pathlib import Path
from datetime import datetime


def get_git_diff():
    """Get git diff main..HEAD"""
    result = subprocess.run(
        ["git", "diff", "main..HEAD"],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        return None
    return result.stdout


def get_changed_files():
    """Get list of changed files"""
    result = subprocess.run(
        ["git", "diff", "--name-only", "main..HEAD"],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        return []
    return [f for f in result.stdout.strip().split("\n") if f]


def get_commit_message():
    """Get the commit message(s) from main..HEAD"""
    result = subprocess.run(
        ["git", "log", "--oneline", "main..HEAD"],
        capture_output=True,
        text=True
    )
    return result.stdout.strip()


def analyze_changes(diff, files):
    """Analyze diff to detect architectural patterns (universal for any project)"""

    analysis = {
        "has_schema_changes": False,
        "has_component_changes": False,
        "has_api_changes": False,
        "has_config_changes": False,
        "has_subsystem_changes": False,
        "has_dependency_changes": False,
        "has_context_threading": False,
        "has_documentation": False,
        "schema_files": [],
        "component_files": [],
        "api_files": [],
        "config_files": [],
        "new_directories": [],
        "context_reads": 0,
        "context_writes": 0,
        "lines_added": 0,
        "lines_removed": 0,
    }

    # Count added/removed lines
    for line in diff.split("\n"):
        if line.startswith("+") and not line.startswith("+++"):
            analysis["lines_added"] += 1
        elif line.startswith("-") and not line.startswith("---"):
            analysis["lines_removed"] += 1

    # Detect SCHEMA/DATABASE changes
    schema_patterns = [
        "schema.prisma",
        "migrations/",
        "alembic/",
        "models/",
        "db/",
        "database/",
        ".sql",
    ]
    schema_files = [
        f for f in files if any(pattern in f for pattern in schema_patterns)
    ]
    if schema_files:
        analysis["has_schema_changes"] = True
        analysis["schema_files"] = schema_files[:5]  # Limit to 5

    # Detect COMPONENT/MODULE structure changes
    component_patterns = [
        "src/components/",
        "src/pages/",
        "components/",
        "pages/",
        "lib/",
        "utils/",
        "hooks/",
    ]
    component_files = [
        f for f in files if any(pattern in f for pattern in component_patterns)
    ]
    if len(component_files) > 2:  # Multiple component changes
        analysis["has_component_changes"] = True
        analysis["component_files"] = component_files[:5]

    # Detect API/ROUTE structure changes
    api_patterns = [
        "routes/",
        "api/",
        "endpoints/",
        "controllers/",
        "handlers/",
        "middleware/",
        "/api/",
    ]
    api_files = [f for f in files if any(pattern in f for pattern in api_patterns)]
    if api_files:
        analysis["has_api_changes"] = True
        analysis["api_files"] = api_files[:5]

    # Detect CONFIG file changes
    config_patterns = [
        ".env",
        "config/",
        "settings/",
        ".yaml",
        ".yml",
        "tsconfig",
        "eslintrc",
        "pytest.ini",
        "setup.py",
    ]
    config_files = [
        f for f in files if any(pattern in f for pattern in config_patterns)
    ]
    if config_files:
        analysis["has_config_changes"] = True
        analysis["config_files"] = config_files[:5]

    # Detect NEW SUBSYSTEMS (new top-level directories)
    new_dirs = set()
    for f in files:
        if "/" in f:
            top_dir = f.split("/")[0]
            if top_dir not in ["src", "tests", "docs", "public", ".github", ".claude"]:
                new_dirs.add(top_dir)
    if len(new_dirs) >= 2:  # Multiple new top-level dirs
        analysis["has_subsystem_changes"] = True
        analysis["new_directories"] = sorted(list(new_dirs))[:5]

    # Detect DEPENDENCY changes
    if any(f in files for f in ["package.json", "requirements.txt", "Gemfile", "Cargo.toml", "go.mod"]):
        analysis["has_dependency_changes"] = True

    # Detect CONTEXT THREADING (findings.md, lessons.md)
    if "findings.md" in diff or "lessons.md" in diff:
        analysis["has_context_threading"] = True
        analysis["context_reads"] = diff.count("read")
        analysis["context_writes"] = diff.count("write")

    # Detect DOCUMENTATION changes
    if any(f in files for f in ["README.md", "CLAUDE.md", ".claude/docs/", "docs/"]):
        if analysis["lines_added"] > 50:
            analysis["has_documentation"] = True

    return analysis


def infer_topic(analysis, files):
    """Infer a good topic/filename from analysis"""
    if analysis["has_schema_changes"]:
        return "data-model-refactor"
    elif analysis["has_api_changes"]:
        return "api-structure-enhancement"
    elif analysis["has_component_changes"]:
        return "component-architecture-update"
    elif analysis["has_subsystem_changes"]:
        return "subsystem-refactor"
    elif analysis["has_context_threading"]:
        return "context-threading-enhancement"
    elif analysis["has_config_changes"]:
        return "configuration-restructuring"
    elif analysis["has_dependency_changes"]:
        return "dependency-upgrade"
    else:
        return "architecture-change"


def generate_arch_log_draft(analysis, files, topic):
    """Generate markdown content for arch log entry"""

    today = datetime.now()
    date_str = today.strftime("%Y-%m-%d")

    # Build summary based on analysis
    summary_parts = []
    if analysis["has_schema_changes"]:
        summary_parts.append("Modified data model/schema")
    if analysis["has_api_changes"]:
        summary_parts.append("Updated API/route structure")
    if analysis["has_component_changes"]:
        summary_parts.append("Refactored component architecture")
    if analysis["has_subsystem_changes"]:
        summary_parts.append("Added/refactored subsystems")
    if analysis["has_config_changes"]:
        summary_parts.append("Modified configuration affecting architecture")
    if analysis["has_context_threading"]:
        summary_parts.append("Enhanced context threading")
    if analysis["has_dependency_changes"]:
        summary_parts.append("Updated dependencies affecting system design")
    if analysis["has_documentation"]:
        summary_parts.append("Documented architectural changes")

    summary = (
        ". ".join(summary_parts) if summary_parts else "Architectural enhancement"
    )

    # Categorize change type
    change_type = []
    if analysis["has_schema_changes"]:
        change_type.append("Data Flow")
    if analysis["has_api_changes"]:
        change_type.append("Control Flow")
    if analysis["has_component_changes"]:
        change_type.append("Pattern")
    if analysis["has_subsystem_changes"]:
        change_type.append("Subsystem")
    if analysis["has_config_changes"]:
        change_type.append("Configuration")
    if analysis["has_context_threading"]:
        change_type.append("Integration")

    change_type_str = " + ".join(change_type) if change_type else "Architecture"

    # Build file listing sections
    sections = []

    if analysis["schema_files"]:
        sections.append(
            f"\n**Database/Schema Changes ({len(analysis['schema_files'])}):**\n"
            + "\n".join([f"- `{f}`" for f in analysis["schema_files"]])
        )

    if analysis["api_files"]:
        sections.append(
            f"\n**API/Route Changes ({len(analysis['api_files'])}):**\n"
            + "\n".join([f"- `{f}`" for f in analysis["api_files"]])
        )

    if analysis["component_files"]:
        sections.append(
            f"\n**Component/Module Changes ({len(analysis['component_files'])}):**\n"
            + "\n".join([f"- `{f}`" for f in analysis["component_files"]])
        )

    if analysis["config_files"]:
        sections.append(
            f"\n**Configuration Changes ({len(analysis['config_files'])}):**\n"
            + "\n".join([f"- `{f}`" for f in analysis["config_files"]])
        )

    if analysis["new_directories"]:
        sections.append(
            f"\n**New Subsystems/Directories:**\n"
            + "\n".join([f"- `{d}/`" for d in analysis["new_directories"]])
        )

    if analysis["has_dependency_changes"]:
        sections.append("\n**Dependency Changes:**\n- Check package.json/requirements.txt for details")

    file_sections = "".join(sections) if sections else "\n**Files Modified:**\n" + "\n".join(
        [f"- `{f}`" for f in sorted(files)[:10]]
    )

    # Build impact section
    impact_items = []
    if analysis["has_schema_changes"]:
        impact_items.append("Database/data model structure changed")
    if analysis["has_api_changes"]:
        impact_items.append("API contract or endpoint structure modified")
    if analysis["has_component_changes"]:
        impact_items.append("Component/module organization updated")
    if analysis["has_subsystem_changes"]:
        impact_items.append("New subsystems or major refactoring")
    if analysis["has_dependency_changes"]:
        impact_items.append("Dependencies changed (may affect system design)")
    if analysis["has_context_threading"]:
        impact_items.append(f"Context integration: +{analysis['context_reads']} reads, +{analysis['context_writes']} writes")

    impact_section = (
        "\n".join([f"- {item}" for item in impact_items])
        if impact_items
        else "- Enhanced system architecture"
    )

    content = f"""# {topic.replace("-", " ").title()} ({today.strftime("%B %d, %Y")})

## Summary

{summary}

## Type of Architectural Change

**{change_type_str}**

## What Changed
{file_sections}

**Statistics:**
- Lines added: {analysis['lines_added']}
- Lines removed: {analysis['lines_removed']}
- Files modified: {len(files)}

## Impact

{impact_section}

## Detailed Changes

[DESCRIBE: What specifically changed in the architecture? Why was this change necessary?]

## Before & After

**Before:**
[OLD DESIGN/STRUCTURE]

**After:**
[NEW DESIGN/STRUCTURE]

## Affected Components

[LIST: Which parts of the system are affected by this change?]

## Migration/Compatibility

[IF BREAKING CHANGE: How do users/developers need to adapt?]
[IF COMPATIBLE: Backward compatibility confirmed ✓]

## Verification

- [ ] All affected code paths tested
- [ ] Related documentation updated
- [ ] No breaking changes (or breaking changes documented)
- [ ] Dependent systems verified
"""

    return content


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Detect architectural changes and generate arch log draft"
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Show generated content without saving"
    )
    parser.add_argument(
        "--output", help="Output file (default: .claude/docs/architectural_change_log/)"
    )
    parser.add_argument(
        "--show-analysis",
        action="store_true",
        help="Show analysis details (debug mode)",
    )
    args = parser.parse_args()

    try:
        diff = get_git_diff()
        files = get_changed_files()

        if not diff or not files:
            print("ℹ No changes detected between main and HEAD", file=sys.stderr)
            return 1

        # Analyze changes
        analysis = analyze_changes(diff, files)

        if args.show_analysis:
            print("\n=== Analysis ===", file=sys.stderr)
            for key, value in analysis.items():
                print(f"{key}: {value}", file=sys.stderr)
            print()

        # Infer topic and generate draft
        topic = infer_topic(analysis, files)
        content = generate_arch_log_draft(analysis, files, topic)

        if args.dry_run:
            print(f"=== Would create: {topic} ===\n", file=sys.stderr)
            print(content)
            return 0

        # Determine output path
        if args.output:
            output_path = Path(args.output)
        else:
            today = datetime.now()
            date_str = today.strftime("%Y-%m-%d")
            filename = f"{date_str}-{topic}.md"
            arch_dir = Path(".claude/docs/architectural_change_log")
            arch_dir.mkdir(parents=True, exist_ok=True)
            output_path = arch_dir / filename

        # Create parent directories if needed
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Write file
        output_path.write_text(content)
        print(f"✓ Created draft: {output_path}", file=sys.stderr)
        print(str(output_path))  # stdout for capture by shell

        return 0

    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())

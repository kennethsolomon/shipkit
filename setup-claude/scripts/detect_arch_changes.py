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
    """Analyze diff to detect architectural patterns"""

    analysis = {
        "has_context_threading": False,
        "has_skill_changes": False,
        "has_template_changes": False,
        "has_documentation": False,
        "has_workflow_changes": False,
        "skill_files": [],
        "template_files": [],
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

    # Detect context threading
    if "findings.md" in diff or "lessons.md" in diff:
        analysis["has_context_threading"] = True
        analysis["context_reads"] = diff.count("read")
        analysis["context_writes"] = diff.count("write")

    # Identify changed skill files
    skill_files = [f for f in files if f.endswith("SKILL.md")]
    if skill_files:
        analysis["has_skill_changes"] = True
        analysis["skill_files"] = skill_files

    # Identify template changes
    template_files = [f for f in files if ".template" in f]
    if template_files:
        analysis["has_template_changes"] = True
        analysis["template_files"] = template_files

    # Identify documentation changes
    if any(f in files for f in ["README.md", "CLAUDE.md"]) and analysis["lines_added"] > 50:
        analysis["has_documentation"] = True

    # Detect workflow pattern changes
    if analysis["has_context_threading"] or analysis["has_skill_changes"]:
        analysis["has_workflow_changes"] = True

    return analysis


def infer_topic(analysis, files):
    """Infer a good topic/filename from analysis"""
    if analysis["has_context_threading"]:
        return "context-threading-enhancement"
    elif "frontend-design" in str(files):
        return "frontend-design-enhancement"
    elif "brainstorming" in str(files):
        return "brainstorming-enhancement"
    elif analysis["has_workflow_changes"]:
        return "workflow-enhancement"
    elif analysis["has_skill_changes"]:
        return "skill-enhancement"
    else:
        return "architecture-change"


def generate_arch_log_draft(analysis, files, topic):
    """Generate markdown content for arch log entry"""

    today = datetime.now()
    date_str = today.strftime("%Y-%m-%d")

    # Build summary based on analysis
    summary_parts = []
    if analysis["has_context_threading"]:
        summary_parts.append("Enhanced context threading (findings.md/lessons.md)")
    if analysis["has_workflow_changes"]:
        summary_parts.append("Changed skill interaction patterns")
    if analysis["has_documentation"]:
        summary_parts.append("Significantly updated documentation")

    summary = ". ".join(summary_parts) if summary_parts else "Architectural enhancement"

    # Categorize change type
    change_type = []
    if analysis["has_context_threading"]:
        change_type.append("Data Flow")
    if analysis["has_skill_changes"]:
        change_type.append("Control Flow")
    if analysis["has_template_changes"]:
        change_type.append("Pattern")
    if analysis["has_documentation"]:
        change_type.append("Documentation")

    change_type_str = " + ".join(change_type) if change_type else "Architecture"

    # Build file listing with counts
    skill_section = ""
    if analysis["skill_files"]:
        skill_section = f"\n**Skill Files ({len(analysis['skill_files'])}):**\n"
        for f in sorted(analysis["skill_files"]):
            skill_section += f"- `{f}`\n"

    template_section = ""
    if analysis["template_files"]:
        template_section = f"\n**Templates ({len(analysis['template_files'])}):**\n"
        for f in sorted(analysis["template_files"]):
            template_section += f"- `{f}`\n"

    other_section = ""
    other_files = [
        f
        for f in sorted(files)
        if f not in analysis["skill_files"]
        and f not in analysis["template_files"]
        and not f.startswith(".")
    ]
    if other_files:
        other_section = f"\n**Other Files ({len(other_files)}):**\n"
        for f in other_files:
            other_section += f"- `{f}`\n"

    # Build impact section
    impact_items = []
    if analysis["has_context_threading"]:
        impact_items.append(f"Context reads: +{analysis['context_reads']}")
        impact_items.append(f"Context writes: +{analysis['context_writes']}")
    if analysis["has_skill_changes"]:
        impact_items.append(f"{len(analysis['skill_files'])} skills modified")
    if analysis["has_template_changes"]:
        impact_items.append(f"{len(analysis['template_files'])} templates updated")

    impact_section = "\n".join([f"- {item}" for item in impact_items]) if impact_items else "- Enhanced system architecture"

    content = f"""# {topic.replace("-", " ").title()} ({today.strftime("%B %d, %Y")})

## Summary

{summary}

## Type of Architectural Change

**{change_type_str}**

## What Changed

**Files Modified ({len(files)} files):**
{skill_section}{template_section}{other_section}

**Statistics:**
- Lines added: {analysis['lines_added']}
- Lines removed: {analysis['lines_removed']}

## Impact

{impact_section}

## Detailed Changes

[DESCRIBE: What specifically changed in the architecture? How do skills/components interact differently now?]

## Before & After

**Before:**
[OLD PATTERN/FLOW]

**After:**
[NEW PATTERN/FLOW]

## Verification

- [ ] All affected skills tested
- [ ] Related documentation updated
- [ ] No breaking changes to existing workflows
- [ ] Workflow scenarios tested
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

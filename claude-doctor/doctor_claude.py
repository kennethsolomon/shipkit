#!/usr/bin/env python3
"""Diagnose and suggest improvements for existing CLAUDE.md."""

import json
import sys
from pathlib import Path

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from lib.detect import detect_project
from lib.sidecar import get_target_file, add_marker, count_lines, extract_sections


def diagnose_claude_md(file_path: Path = None) -> dict:
    """Diagnose an existing CLAUDE.md file.

    Args:
        file_path: Path to CLAUDE.md (defaults to ./CLAUDE.md)

    Returns:
        Dictionary with diagnosis report
    """
    if file_path is None:
        file_path = Path("CLAUDE.md")

    if not file_path.exists():
        return {
            "status": "error",
            "message": f"CLAUDE.md not found at {file_path}",
            "issues": [],
        }

    content = file_path.read_text()
    line_count = count_lines(content)
    sections = extract_sections(content)

    issues = []
    suggestions = []

    # Check line count
    if line_count > 150:
        issues.append(
            f"File is too long: {line_count} lines (target: < 150)"
        )
        suggestions.append(
            "Run `/optimize-claude` to trim unnecessary sections"
        )

    # Check for essential sections
    essential_sections = ["Stack", "Quick Start", "Development"]
    missing = [s for s in essential_sections if s not in sections]
    if missing:
        issues.append(f"Missing essential sections: {', '.join(missing)}")

    # Check for outdated patterns
    if "npm run" in content and not (Path.cwd() / "package.json").exists():
        issues.append("File mentions npm but no package.json found")

    # Check for generic placeholders
    if "[" in content and "]" in content:
        issues.append("File contains unreplaced template placeholders")

    # Suggestions for improvement
    if len(sections) < 5:
        suggestions.append("Consider adding more detailed sections (e.g., Dependencies, Contributing)")

    if "Environment" not in sections:
        suggestions.append("Add an 'Environment Variables' section for setup instructions")

    # Generate improved version
    improved = _generate_improved_claude(file_path)

    return {
        "status": "success",
        "file": str(file_path),
        "line_count": line_count,
        "sections": sections,
        "issues": issues,
        "suggestions": suggestions,
        "improved_line_count": count_lines(improved),
    }


def _generate_improved_claude(file_path: Path) -> str:
    """Generate an improved version of CLAUDE.md."""
    # Detect project to get fresh context
    project_root = file_path.parent
    config = detect_project(project_root)

    # Get template
    template_path = Path(__file__).parent.parent / "templates" / "CLAUDE.md.template"
    if not template_path.exists():
        return file_path.read_text()

    template = template_path.read_text()

    # Render with detected values
    build_system = {
        "JavaScript/TypeScript": "npm/Node.js",
        "Python": "pip/Poetry",
        "Go": "Go modules",
        "Rust": "Cargo",
    }.get(config.language, "Custom")

    framework = config.framework if config.framework and config.framework != "None" else "None"
    database = config.database if config.database and config.database != "None" else "None"
    ui = config.ui if config.ui and config.ui != "None" else "None"
    testing = config.testing if config.testing and config.testing != "None" else "None"

    replacements = {
        "[PROJECT_NAME]": config.project_name or "My Project",
        "[DESCRIPTION]": config.description or file_path.parent.name,
        "[LANGUAGE]": config.language,
        "[FRAMEWORK]": framework,
        "[DATABASE]": database,
        "[UI]": ui,
        "[TESTING]": testing,
        "[DEV_COMMAND]": config.dev_command,
        "[BUILD_COMMAND]": config.build_command,
        "[TEST_COMMAND]": config.test_command,
        "[LINT_COMMAND]": config.lint_command,
        "[BUILD_SYSTEM]": build_system,
    }

    result = template
    for key, value in replacements.items():
        result = result.replace(key, value)

    return result


def main():
    """Main entry point."""
    # Check if CLAUDE.md exists
    claude_path = Path("CLAUDE.md")
    report = diagnose_claude_md(claude_path)

    # Print report
    if report["status"] == "error":
        print(f"❌ {report['message']}")
        print("\nTo create a new CLAUDE.md, run: `/setup-starter`")
        return

    print(f"📋 Diagnosis Report for {report['file']}\n")
    print(f"📊 Lines: {report['line_count']}/150")
    print(f"📑 Sections: {', '.join(report['sections'])}\n")

    if report["issues"]:
        print("⚠️  Issues found:")
        for i, issue in enumerate(report["issues"], 1):
            print(f"   {i}. {issue}")
    else:
        print("✅ No major issues found!\n")

    if report["suggestions"]:
        print("\n💡 Suggestions:")
        for i, suggestion in enumerate(report["suggestions"], 1):
            print(f"   {i}. {suggestion}")

    # Offer sidecar with improved version
    if report["issues"] or report["suggestions"]:
        improved = _generate_improved_claude(claude_path)
        target_path, _ = get_target_file("CLAUDE.md")
        improved_with_marker = add_marker(improved)

        try:
            sidecar_path = Path(f"CLAUDE.md.setup-claude.md")
            sidecar_path.write_text(improved_with_marker)
            print(f"\n📝 Improved version saved to: {sidecar_path}")
            print(f"   Lines: {report['improved_line_count']}/150")
            print(f"   Review and merge manually if desired")
        except Exception as e:
            print(f"\n❌ Error creating suggestion: {e}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Create CLAUDE.md for new projects via auto-detection."""

import sys
from pathlib import Path

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from lib.detect import detect_project
from lib.sidecar import get_target_file, add_marker, format_output, count_lines, extract_sections


def render_template(template_path: Path, config) -> str:
    """Render the CLAUDE.md template with detected values."""
    template = template_path.read_text()

    # Determine build system
    build_system = {
        "JavaScript/TypeScript": "npm/Node.js",
        "Python": "pip/Poetry",
        "Go": "Go modules",
        "Rust": "Cargo",
    }.get(config.language, "Custom")

    # Handle None/empty values
    framework = config.framework if config.framework and config.framework != "None" else "None"
    database = config.database if config.database and config.database != "None" else "None"
    ui = config.ui if config.ui and config.ui != "None" else "None"
    testing = config.testing if config.testing and config.testing != "None" else "None"

    replacements = {
        "[PROJECT_NAME]": config.project_name or "My Project",
        "[DESCRIPTION]": config.description or "A new project.",
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


def create_claude_md(project_root: Path = None) -> None:
    """Create CLAUDE.md for a project.

    Args:
        project_root: Root directory of project (defaults to current directory)
    """
    if project_root is None:
        project_root = Path.cwd()

    # Detect project configuration
    config = detect_project(project_root)

    # Get template
    template_path = Path(__file__).parent.parent / "templates" / "CLAUDE.md.template"
    if not template_path.exists():
        print(f"❌ Template not found: {template_path}")
        return

    # Render template
    content = render_template(template_path, config)
    content_with_marker = add_marker(content)

    # Determine target file
    target_path, is_sidecar = get_target_file("CLAUDE.md")

    # Write file
    try:
        target_path.write_text(content_with_marker)
        line_count = count_lines(content_with_marker)
        sections = extract_sections(content_with_marker)

        # Format and print output
        output = format_output(target_path, is_sidecar, line_count, sections)
        print(output)

        if is_sidecar:
            print("📖 To use this file, review the suggestions and merge into CLAUDE.md manually.")
            print(f"📍 View suggestion: cat {target_path}")
        else:
            print(f"✅ CLAUDE.md created successfully!")

    except Exception as e:
        print(f"❌ Error writing file: {e}")
        sys.exit(1)


if __name__ == "__main__":
    create_claude_md()

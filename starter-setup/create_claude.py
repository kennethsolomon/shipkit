#!/usr/bin/env python3
"""Create CLAUDE.md for new projects via auto-detection."""

import sys
from pathlib import Path

# Add lib to path for local imports
sys.path.insert(0, str(Path(__file__).parent))

# Add setup-optimizer lib to path for shared discovery modules
sys.path.insert(0, str(Path(__file__).parent.parent / "setup-optimizer" / "lib"))

from lib.detect import detect_project
from lib.sidecar import get_target_file, add_marker, format_output, count_lines, extract_sections

# Import discovery modules from setup-optimizer
try:
    from discover import discover_directories, discover_documentation, discover_workflows
    from enrich import generate_directories_section, generate_documentation_section, generate_workflows_section
    DISCOVERY_AVAILABLE = True
except ImportError:
    DISCOVERY_AVAILABLE = False


def _insert_discovered_sections(content: str, discovered_sections: dict) -> str:
    """Insert discovered sections into the content before the marker.

    Args:
        content: Base CLAUDE.md content
        discovered_sections: Dict of discovered sections to insert

    Returns:
        Content with discovered sections inserted
    """
    lines = content.split('\n')
    insert_index = len(lines)

    # Find where to insert (before any marker comment)
    for i, line in enumerate(lines):
        if '<!-- Generated' in line or '<!-- Setup' in line:
            insert_index = i
            break

    # Build sections to insert
    new_sections = []
    for key in ['directories', 'documentation', 'workflows']:
        if key in discovered_sections:
            section = discovered_sections[key]
            new_sections.append(f"## {section['title']}\n")
            new_sections.append(section['content'])
            new_sections.append('')

    # Insert sections
    if new_sections:
        inserted_content = '\n'.join(lines[:insert_index])
        inserted_content += '\n\n' + '\n\n'.join(new_sections).rstrip()
        inserted_content += '\n\n' + '\n'.join(lines[insert_index:])
        return inserted_content

    return content


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
    template_path = Path(__file__).parent / "templates" / "CLAUDE.md.template"
    if not template_path.exists():
        print(f"❌ Template not found: {template_path}")
        return

    # Render template
    content = render_template(template_path, config)

    # Discover and enrich with project structure
    discovered_sections = {}
    discovery_worked = False
    if DISCOVERY_AVAILABLE:
        try:
            # Discover project structure
            directories = discover_directories(project_root)
            documentation = discover_documentation(project_root)
            workflows = discover_workflows(project_root)

            # Generate sections from discoveries
            if directories:
                discovered_sections['directories'] = {
                    'title': 'Key Directories',
                    'content': generate_directories_section(directories),
                }

            if documentation:
                discovered_sections['documentation'] = {
                    'title': 'Documentation & Resources',
                    'content': generate_documentation_section(documentation),
                }

            if workflows:
                discovered_sections['workflows'] = {
                    'title': 'Common Workflows',
                    'content': generate_workflows_section(workflows),
                }

            discovery_worked = True
        except Exception as e:
            # If discovery fails, continue without it
            print(f"⚠️  Warning: Discovery failed ({e}), using basic template")

    # Append discovered sections before marker
    if discovered_sections:
        content = _insert_discovered_sections(content, discovered_sections)

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

        # Enhanced output showing discoveries
        if discovery_worked and discovered_sections:
            print("\n📁 Discoveries from project structure:")
            for key, section in discovered_sections.items():
                if key == 'directories':
                    dirs = section['content'].count('\n') + 1
                    print(f"   📂 {dirs} directories found")
                elif key == 'documentation':
                    docs = section['content'].count('\n') + 1
                    print(f"   📚 {docs} documentation files")
                elif key == 'workflows':
                    print(f"   🔧 Workflows discovered and documented")

        if is_sidecar:
            print("\n📖 To use this file, review the suggestions and merge into CLAUDE.md manually.")
            print(f"📍 View suggestion: cat {target_path}")
        else:
            print(f"\n✅ CLAUDE.md created successfully!")

    except Exception as e:
        print(f"❌ Error writing file: {e}")
        sys.exit(1)


if __name__ == "__main__":
    create_claude_md()

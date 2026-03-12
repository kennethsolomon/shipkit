#!/usr/bin/env python3
"""Diagnose and suggest improvements for existing CLAUDE.md."""

import json
import sys
from pathlib import Path

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent))

# Add setup-optimizer lib to path for shared discovery modules
sys.path.insert(0, str(Path(__file__).parent.parent / "setup-optimizer" / "lib"))

from lib.detect import detect_project
from lib.sidecar import get_target_file, add_marker, count_lines, extract_sections

# Import discovery modules from setup-optimizer
try:
    from discover import discover_directories, discover_documentation, discover_workflows
    from enrich import generate_directories_section, generate_documentation_section, generate_workflows_section
    DISCOVERY_AVAILABLE = True
except ImportError:
    DISCOVERY_AVAILABLE = False


def _parse_claude_sections(content: str) -> dict:
    """Parse CLAUDE.md content into sections.

    Returns:
        Dict mapping section name to section content
    """
    sections = {}
    current_section = None
    section_content = []

    for line in content.split('\n'):
        if line.startswith('## '):
            # New section
            if current_section:
                sections[current_section] = '\n'.join(section_content).strip()
            current_section = line[3:].strip()
            section_content = []
        elif line.startswith('<!-- Generated'):
            # End of content
            if current_section:
                sections[current_section] = '\n'.join(section_content).strip()
            break
        elif current_section:
            section_content.append(line)

    return sections


def _extract_items_from_section(content: str, bullet_type='bullet') -> list:
    """Extract bulleted or inline items from section content.

    Returns:
        List of items
    """
    items = []
    for line in content.split('\n'):
        line = line.strip()
        if bullet_type == 'bullet' and line.startswith('-'):
            item = line[1:].strip()
            # Extract just the key part (before dash or colon)
            if ' - ' in item:
                item = item.split(' - ')[0].strip()
            if ' - ' in item:
                item = item.split('`')[1] if '`' in item else item
            items.append(item)
        elif bullet_type == 'code' and ('npm run' in line or 'make' in line):
            items.append(line)

    return items


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
    parsed_sections = _parse_claude_sections(content)

    issues = []
    suggestions = []
    discoveries = {}

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

    # Discovery-based diagnostics
    if DISCOVERY_AVAILABLE:
        try:
            project_root = file_path.parent
            config = detect_project(project_root)

            # Discover actual project structure
            discovered_dirs = discover_directories(project_root)
            discovered_docs = discover_documentation(project_root)
            discovered_workflows = discover_workflows(project_root)

            discoveries['directories'] = discovered_dirs
            discoveries['documentation'] = discovered_docs
            discoveries['workflows'] = discovered_workflows

            # Compare documented vs discovered directories
            documented_dirs = set()
            if "Key Directories" in sections or "Project Structure" in sections:
                section_name = "Key Directories" if "Key Directories" in sections else "Project Structure"
                section_content = parsed_sections.get(section_name, "")
                # Extract directory names from section
                for line in section_content.split('\n'):
                    if '/' in line:
                        # Extract directory name (e.g., "src/" or "src -")
                        parts = line.split('/')
                        if len(parts) > 0:
                            dir_name = parts[0].strip().split()[-1] if parts[0].strip() else ''
                            if dir_name and dir_name not in ['', '-', '|']:
                                documented_dirs.add(dir_name)

            # Check for undocumented directories
            undocumented = set(discovered_dirs.keys()) - documented_dirs
            if undocumented and len(undocumented) > 0:
                # Only flag significant directories
                significant = [d for d in undocumented if d not in ['.github', 'config']]
                if significant:
                    issues.append(f"Project has undocumented directories: {', '.join(significant)}")
                    suggestions.append(f"Add documentation for: {', '.join(significant)}")

            # Check for undocumented documentation
            if discovered_docs:
                doc_count = len(discovered_docs)
                doc_section_exists = "Documentation" in sections or "Resources" in sections
                if not doc_section_exists and doc_count > 0:
                    issues.append(f"Found {doc_count} documentation files but no documentation section")
                    suggestions.append("Add a 'Documentation & Resources' section linking to docs")

            # Check for workflow documentation
            if discovered_workflows and "Development" in sections:
                dev_section = parsed_sections.get("Development", "")
                npm_scripts = discovered_workflows.get('npm', [])
                if npm_scripts:
                    # Check if custom scripts are documented
                    custom_scripts = [s for s in npm_scripts if s not in ['test', 'build']]
                    undocumented_scripts = [s for s in custom_scripts if s not in dev_section]
                    if undocumented_scripts:
                        suggestions.append(f"Document additional npm scripts: {', '.join(undocumented_scripts)}")

            # Stack-specific suggestions
            if config.framework:
                framework_lower = config.framework.lower()
                if 'react' in framework_lower and 'component' not in content.lower():
                    suggestions.append("Consider adding a 'Components & Architecture' section for React projects")
                elif 'django' in framework_lower and 'model' not in content.lower():
                    suggestions.append("Consider adding a 'Models & Database' section for Django projects")
                elif 'fastapi' in framework_lower and 'endpoint' not in content.lower():
                    suggestions.append("Consider adding an 'API Endpoints' section for API projects")

        except Exception:
            # If discovery fails, continue with basic checks
            pass

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
        "discoveries": discoveries,
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

    # Show discovered project structure
    discoveries = report.get("discoveries", {})
    if discoveries:
        print("🔍 Project Structure Detected:")
        if discoveries.get('directories'):
            dirs = len(discoveries['directories'])
            print(f"   📂 {dirs} directories: {', '.join(discoveries['directories'].keys())}")
        if discoveries.get('documentation'):
            docs = len(discoveries['documentation'])
            print(f"   📚 {docs} documentation files")
        if discoveries.get('workflows'):
            workflows = discoveries['workflows']
            workflow_desc = []
            if 'npm' in workflows:
                workflow_desc.append(f"npm ({len(workflows['npm'])} scripts)")
            if 'make' in workflows:
                workflow_desc.append(f"Makefile ({len(workflows['make'])} targets)")
            if workflows:
                print(f"   🔧 Workflows: {', '.join(workflow_desc)}")
        print()

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

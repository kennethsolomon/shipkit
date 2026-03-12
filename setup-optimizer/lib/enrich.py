"""Enrich CLAUDE.md with comprehensive project context sections."""

from typing import Dict, List


def generate_directories_section(discovered: Dict[str, str]) -> str:
    """Generate Key Directories section from discovered structure.

    Args:
        discovered: Dict of directory_name -> description

    Returns:
        Formatted section content
    """
    if not discovered:
        return ''

    lines = []
    for dir_name in sorted(discovered.keys()):
        description = discovered[dir_name]
        lines.append(f'- **{dir_name}/** - {description}')

    return '\n'.join(lines)


def generate_documentation_section(docs: Dict[str, str]) -> str:
    """Generate Documentation & Resources section from discovered files.

    Args:
        docs: Dict of file_path -> description

    Returns:
        Formatted section content
    """
    if not docs:
        return ''

    lines = []

    # Prioritize certain docs
    priority_order = [
        'README.md', 'CONTRIBUTING.md', 'docs/API.md', 'docs/api.md',
        'docs/ARCHITECTURE.md', 'docs/architecture.md',
    ]

    added = set()

    # Add priority docs first
    for pattern in priority_order:
        if pattern in docs:
            lines.append(f'- **{pattern}** - {docs[pattern]}')
            added.add(pattern)

    # Add remaining docs
    for doc_path in sorted(docs.keys()):
        if doc_path not in added:
            description = docs[doc_path]
            lines.append(f'- **{doc_path}** - {description}')

    return '\n'.join(lines)


def generate_workflows_section(workflows: Dict[str, List[str]]) -> str:
    """Generate Common Workflows section from discovered commands.

    Args:
        workflows: Dict of workflow_type -> list of commands

    Returns:
        Formatted section content
    """
    if not workflows:
        return ''

    lines = []

    # npm/yarn scripts
    if 'npm' in workflows:
        lines.append('**Common npm scripts:**')
        for script in workflows['npm'][:5]:
            lines.append(f'- `npm run {script}`')
        lines.append('')

    # Makefile targets
    if 'make' in workflows:
        lines.append('**Makefile targets:**')
        for target in workflows['make'][:5]:
            lines.append(f'- `make {target}`')
        lines.append('')

    # GitHub workflows
    if 'workflows' in workflows:
        lines.append('**GitHub Actions workflows:**')
        for workflow in workflows['workflows'][:3]:
            lines.append(f'- `.github/workflows/{workflow}.yml`')
        lines.append('')

    return '\n'.join(lines).strip()


def generate_directories_section_compact(discovered: Dict[str, str]) -> str:
    """Generate a compact version of Key Directories section.

    Args:
        discovered: Dict of directory_name -> description

    Returns:
        Compact formatted section
    """
    if not discovered:
        return ''

    # For compact mode, use inline format
    lines = []
    items = []

    for dir_name in sorted(discovered.keys()):
        items.append(f'`{dir_name}/`')

    if items:
        lines.append('Project structure:')
        lines.append(', '.join(items))

    return '\n'.join(lines)


def merge_into_development_section(
    base_content: str,
    discovered_workflows: Dict[str, List[str]],
) -> str:
    """Merge discovered workflows into Development section.

    Args:
        base_content: Base development section content
        discovered_workflows: Discovered workflows

    Returns:
        Enhanced development section
    """
    lines = [base_content.rstrip()]

    # Add discovered workflows if any
    if discovered_workflows:
        lines.append('')
        lines.append('### Discovered Workflows')
        lines.append(generate_workflows_section(discovered_workflows))

    return '\n'.join(lines)


def estimate_content_lines(section_dict: Dict[str, str]) -> int:
    """Estimate total lines for section content.

    Args:
        section_dict: Dict of sections

    Returns:
        Approximate total line count
    """
    total = 0
    for content in section_dict.values():
        total += len(content.split('\n'))
    return total

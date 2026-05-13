"""Intelligent project structure, documentation, and workflow discovery."""

import json
from pathlib import Path
from typing import Dict, List


# Directories to exclude from discovery
EXCLUDE_DIRS = {
    'node_modules', '.next', 'dist', 'build', 'out',
    '.venv', 'venv', 'env', '__pycache__',
    '.git', '.github/actions', 'vendor',
    '.pytest_cache', '.mypy_cache', '.tox',
    'coverage', '.coverage', 'htmlcov',
    'egg-info', '.eggs', '*.egg-info',
}

# Documentation patterns to look for
DOC_PATTERNS = {
    'README.md': 'Project overview',
    'CONTRIBUTING.md': 'How to contribute',
    'CODE_OF_CONDUCT.md': 'Code of conduct',
    'CHANGELOG.md': 'Version history',
    'LICENSE': 'License information',
}


def discover_directories(root_path: Path) -> Dict[str, str]:
    """Auto-discover key project directories and their purposes.

    Args:
        root_path: Project root directory

    Returns:
        Dict mapping directory names to descriptions
    """
    found_dirs = {}

    # Define directory patterns and their descriptions
    dir_patterns = {
        'src': 'Application source code',
        'lib': 'Library utilities and helpers',
        'app': 'Application code',
        'source': 'Source code',
        'tests': 'Test suite',
        'test': 'Test suite',
        '__tests__': 'Test suite',
        'spec': 'Test specifications',
        'docs': 'Documentation',
        'public': 'Static assets and public files',
        'static': 'Static assets',
        'assets': 'Project assets',
        'scripts': 'Utility and build scripts',
        'config': 'Configuration files',
        'migrations': 'Database migrations',
        'prisma': 'Prisma database schema',
        'alembic': 'SQLAlchemy migrations',
        '.github': 'GitHub configuration and workflows',
        'infra': 'Infrastructure as code',
        'terraform': 'Terraform configuration',
        'docker': 'Docker configuration',
    }

    for dir_name, description in dir_patterns.items():
        dir_path = root_path / dir_name
        if dir_path.exists() and dir_path.is_dir():
            # Skip if in exclude list
            if dir_name not in EXCLUDE_DIRS:
                found_dirs[dir_name] = description

    return found_dirs


def discover_documentation(root_path: Path) -> Dict[str, str]:
    """Find documentation files and link them.

    Args:
        root_path: Project root directory

    Returns:
        Dict mapping doc file paths to descriptions
    """
    found_docs = {}

    # Check root level documentation
    for pattern, description in DOC_PATTERNS.items():
        doc_path = root_path / pattern
        if doc_path.exists() and doc_path.is_file():
            found_docs[pattern] = description

    # Check docs/ directory for additional documentation
    docs_dir = root_path / 'docs'
    if docs_dir.exists() and docs_dir.is_dir():
        # Look for common subdirectories and files
        doc_files = {
            'API.md': 'API documentation',
            'api.md': 'API documentation',
            'ARCHITECTURE.md': 'Architecture overview',
            'architecture.md': 'Architecture overview',
            'DEPLOYMENT.md': 'Deployment guide',
            'deployment.md': 'Deployment guide',
            'SETUP.md': 'Setup instructions',
            'setup.md': 'Setup instructions',
            'TROUBLESHOOTING.md': 'Troubleshooting guide',
            'troubleshooting.md': 'Troubleshooting guide',
        }

        for filename, description in doc_files.items():
            doc_file = docs_dir / filename
            if doc_file.exists() and doc_file.is_file():
                found_docs[f'docs/{filename}'] = description

        # Check for subdirectories
        try:
            for item in docs_dir.iterdir():
                if item.is_dir() and item.name not in EXCLUDE_DIRS:
                    found_docs[f'docs/{item.name}/'] = f'{item.name.capitalize()} documentation'
        except PermissionError:
            pass

    # Check .github for documentation
    github_dir = root_path / '.github'
    if github_dir.exists() and github_dir.is_dir():
        contributing = github_dir / 'CONTRIBUTING.md'
        if contributing.exists():
            found_docs['.github/CONTRIBUTING.md'] = 'GitHub contribution guidelines'

    return found_docs


def discover_workflows(root_path: Path) -> Dict[str, List[str]]:
    """Discover build workflows, scripts, and common commands.

    Args:
        root_path: Project root directory

    Returns:
        Dict mapping workflow type to list of commands/targets
    """
    workflows = {}

    # Check Makefile for targets
    makefile_targets = _extract_makefile_targets(root_path)
    if makefile_targets:
        workflows['make'] = makefile_targets

    # Check package.json for npm/yarn scripts
    npm_scripts = _extract_npm_scripts(root_path)
    if npm_scripts:
        workflows['npm'] = npm_scripts

    # Check for GitHub Actions workflows
    github_workflows = _find_github_workflows(root_path)
    if github_workflows:
        workflows['workflows'] = github_workflows

    return workflows


def _extract_makefile_targets(root_path: Path) -> List[str]:
    """Extract targets from Makefile."""
    makefile = root_path / 'Makefile'
    if not makefile.exists():
        return []

    targets = []
    try:
        content = makefile.read_text()
        for line in content.split('\n'):
            if line.startswith('.PHONY'):
                # Extract targets from .PHONY line
                targets_str = line.split(':')[1].strip()
                targets.extend(targets_str.split())
            elif ':' in line and not line.startswith('\t') and not line.startswith(' '):
                target = line.split(':')[0].strip()
                if target and not target.startswith('.'):
                    targets.append(target)
    except (OSError, UnicodeDecodeError) as e:
        print(f"Warning: Could not parse Makefile: {e}")

    return list(set(targets))[:10]  # Limit to 10 targets


def _extract_npm_scripts(root_path: Path) -> List[str]:
    """Extract scripts from package.json."""
    package_json = root_path / 'package.json'
    if not package_json.exists():
        return []

    scripts = []
    try:
        content = json.loads(package_json.read_text())
        if isinstance(content, dict) and 'scripts' in content:
            # Include common scripts, exclude default ones
            exclude = {'test', 'start', 'dev', 'build'}
            for script_name in content['scripts'].keys():
                if script_name not in exclude:
                    scripts.append(script_name)
    except (OSError, json.JSONDecodeError, UnicodeDecodeError) as e:
        print(f"Warning: Could not parse package.json scripts: {e}")

    return scripts[:8]  # Limit to 8 scripts


def _find_github_workflows(root_path: Path) -> List[str]:
    """Find GitHub Actions workflows."""
    workflows_dir = root_path / '.github' / 'workflows'
    if not workflows_dir.exists():
        return []

    workflows = []
    try:
        for workflow_file in workflows_dir.glob('*.yml'):
            workflows.append(workflow_file.stem)
        for workflow_file in workflows_dir.glob('*.yaml'):
            workflows.append(workflow_file.stem)
    except OSError as e:
        print(f"Warning: Could not read GitHub workflows: {e}")

    return workflows[:5]  # Limit to 5 workflows

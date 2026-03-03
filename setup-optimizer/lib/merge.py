"""Smart merging of CLAUDE.md sections with user customization preservation."""

import re
from typing import Dict, Tuple


def parse_claude_md(content: str) -> Dict[str, str]:
    """Parse CLAUDE.md into sections.

    Args:
        content: CLAUDE.md content

    Returns:
        Dict mapping section names to their content
    """
    sections = {}
    current_section = None
    current_content = []

    lines = content.split('\n')
    in_code_block = False

    for line in lines:
        # Track code blocks to avoid treating ``` as section markers
        if line.strip().startswith('```'):
            in_code_block = not in_code_block

        # Check for section headers (## level)
        if line.startswith('## ') and not in_code_block:
            # Save previous section
            if current_section:
                sections[current_section] = '\n'.join(current_content).strip()

            # Start new section
            current_section = line[3:].strip()
            current_content = []
        elif current_section:
            current_content.append(line)

    # Save last section
    if current_section:
        sections[current_section] = '\n'.join(current_content).strip()

    return sections


def detect_user_edits(current: str, generated: str) -> bool:
    """Detect if a section has been user-customized.

    Uses dual detection: content comparison + marker detection.

    Args:
        current: Current section content from file
        generated: What we would generate from template

    Returns:
        True if section appears to be user-edited
    """
    current = current.strip()
    generated = generated.strip()

    # Check for user edit marker
    if '<!-- EDITED -->' in current:
        return True

    # Check if content differs significantly from generated version
    if current == generated:
        return False

    # If content is substantially different, mark as user-edited
    current_len = len(current)
    generated_len = len(generated)

    # Allow small variations (formatting), but flag major differences
    if current_len == 0 and generated_len == 0:
        return False

    if current_len == 0 or generated_len == 0:
        return True

    # Check if content matches at least 50% (allowing for additions)
    matching_ratio = len(set(current) & set(generated)) / max(current_len, generated_len)
    if matching_ratio < 0.5:
        return True

    return False


def should_lock_section(section_name: str, current_content: str) -> bool:
    """Determine if a section should be locked from regeneration.

    Sections are locked if:
    1. They have <!-- LOCK --> marker
    2. They're in the smart default lock list AND have user content
    3. They're marked as edited

    Args:
        section_name: Name of the section
        current_content: Current content of the section

    Returns:
        True if section should be locked
    """
    # Explicit lock marker
    if '<!-- LOCK -->' in current_content:
        return True

    # Smart defaults - auto-lock these if they have user content
    auto_lock_sections = {
        'Important Context': True,
        'Known Issues': True,
        'Notes': True,
        'Custom Configuration': True,
    }

    if section_name in auto_lock_sections and current_content.strip():
        # Check if it looks like user content (not template boilerplate)
        if not current_content.startswith('[') and len(current_content) > 20:
            return True

    return False


def merge_sections(
    existing: Dict[str, str],
    generated: Dict[str, str],
) -> Tuple[Dict[str, str], Dict[str, str]]:
    """Merge existing and generated sections smartly.

    Strategy:
    - Keep generated sections as base
    - Override with existing sections if user-edited
    - Lock sections if needed
    - Return (merged_sections, preservation_report)

    Args:
        existing: Current sections from file
        generated: Newly generated sections from template

    Returns:
        Tuple of (merged sections dict, report dict of what was preserved)
    """
    merged = {}
    preserved = {}

    # Process all sections (both existing and generated)
    all_sections = set(list(existing.keys()) + list(generated.keys()))

    for section_name in all_sections:
        existing_content = existing.get(section_name, '').strip()
        generated_content = generated.get(section_name, '').strip()

        # Determine if user customized this section
        is_user_edited = (
            existing_content and
            detect_user_edits(existing_content, generated_content)
        )

        # Determine if section should be locked
        is_locked = should_lock_section(section_name, existing_content)

        if is_locked or is_user_edited:
            # Preserve user content
            merged[section_name] = existing_content
            preserved[section_name] = 'user-edited' if is_user_edited else 'locked'
        elif existing_content and generated_content:
            # Both exist - prefer generated but keep structure
            merged[section_name] = generated_content
        elif existing_content:
            # Only exists in current
            merged[section_name] = existing_content
            preserved[section_name] = 'preserved'
        else:
            # Only in generated or both same
            merged[section_name] = generated_content

    return merged, preserved


def reconstruct_claude_md(
    sections: Dict[str, str],
    include_marker: bool = True,
) -> str:
    """Reconstruct CLAUDE.md from sections.

    Args:
        sections: Dict of section_name -> content
        include_marker: Whether to add generation marker

    Returns:
        Reconstructed CLAUDE.md content
    """
    # Define standard section order
    section_order = [
        'Project Header',  # Placeholder for title/description
        'Stack',
        'Quick Start',
        'Key Directories',
        'Documentation & Resources',
        'Development',
        'Common Workflows',
        'Build & Deploy',
        'Important Context',
        'Environment Variables',
        'Common Tasks',
    ]

    lines = []

    # Add sections in order (putting unordered sections at end)
    added_sections = set()
    for section_name in section_order:
        if section_name in sections and section_name not in added_sections:
            content = sections[section_name].strip()
            if content:
                lines.append(f'## {section_name}')
                lines.append('')
                lines.append(content)
                lines.append('')
                added_sections.add(section_name)

    # Add any remaining sections
    for section_name in sorted(sections.keys()):
        if section_name not in added_sections:
            content = sections[section_name].strip()
            if content:
                lines.append(f'## {section_name}')
                lines.append('')
                lines.append(content)
                lines.append('')

    # Add marker
    if include_marker:
        lines.append('<!-- Generated by /setup-claude-tools -->')

    result = '\n'.join(lines).strip()
    return result + '\n'


def extract_preservation_report(preserved: Dict[str, str]) -> str:
    """Format a human-readable report of preserved content.

    Args:
        preserved: Dict of section_name -> preservation_reason

    Returns:
        Formatted report string
    """
    if not preserved:
        return ''

    report_lines = ['📝 Preservation Report:', '']

    user_edited = [s for s, r in preserved.items() if r == 'user-edited']
    locked = [s for s, r in preserved.items() if r == 'locked']
    kept = [s for s, r in preserved.items() if r == 'preserved']

    if user_edited:
        report_lines.append('✅ Preserved (user-edited):')
        for section in user_edited:
            report_lines.append(f'   - {section}')
        report_lines.append('')

    if locked:
        report_lines.append('🔒 Preserved (locked):')
        for section in locked:
            report_lines.append(f'   - {section}')
        report_lines.append('')

    if kept:
        report_lines.append('📌 Preserved (as-is):')
        for section in kept:
            report_lines.append(f'   - {section}')

    return '\n'.join(report_lines)

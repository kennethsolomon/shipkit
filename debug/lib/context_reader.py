"""Read and parse project context files (CLAUDE.md, lessons, findings, progress)."""

from pathlib import Path
from typing import Dict, List
import re


class ContextReader:
    """Safe reader for CLAUDE.md, lessons.md, findings.md, progress.md."""

    def __init__(self, project_root: Path = None):
        self.root = project_root or Path.cwd()

    def read_all(self) -> Dict:
        """Read all context files and return structured data."""
        return {
            'claude_md': self._read_claude_md(),
            'lessons': self._read_lessons(),
            'findings': self._read_findings(),
            'progress': self._read_progress(),
        }

    def _read_claude_md(self) -> Dict:
        """Parse CLAUDE.md for tech stack and conventions."""
        claude_path = self.root / 'CLAUDE.md'
        if not claude_path.exists():
            return {'exists': False}

        content = claude_path.read_text()
        return {
            'exists': True,
            'has_content': len(content) > 100,
        }

    def _read_lessons(self) -> List[Dict]:
        """Parse tasks/lessons.md and extract active lessons."""
        lessons_path = self.root / 'tasks' / 'lessons.md'
        if not lessons_path.exists():
            return []

        content = lessons_path.read_text()
        lessons = []

        # Parse markdown format:
        # ### [YYYY-MM-DD] Brief title
        # **Bug:** ...
        # **Root cause:** ...
        # **Prevention:** ...

        # Split by ### headers
        sections = re.split(r'### ', content)

        for section in sections[1:]:  # Skip header
            lines = section.strip().split('\n')
            if not lines:
                continue

            # First line: [YYYY-MM-DD] Title
            first = lines[0]
            match = re.match(r'\[(\d{4}-\d{2}-\d{2})\]\s*(.*)', first)
            if not match:
                continue

            date, title = match.groups()

            # Extract fields
            full_text = '\n'.join(lines)
            bug = self._extract_field(full_text, 'Bug')
            root_cause = self._extract_field(full_text, 'Root cause')
            prevention = self._extract_field(full_text, 'Prevention')

            lesson = {
                'date': date,
                'title': title,
                'bug': bug,
                'root_cause': root_cause,
                'prevention': prevention,
            }
            lessons.append(lesson)

        return lessons

    def _read_findings(self) -> List[Dict]:
        """Parse tasks/findings.md and extract past investigations."""
        findings_path = self.root / 'tasks' / 'findings.md'
        if not findings_path.exists():
            return []

        content = findings_path.read_text()
        findings = []

        # Parse markdown format:
        # ## YYYY-MM-DD HH:MM — Bug: Description
        # **Symptom:** ...
        # **Root cause:** ...

        sections = re.split(r'## (\d{4}-\d{2}-\d{2})', content)

        for i in range(1, len(sections), 2):
            date = sections[i]
            text = sections[i + 1] if i + 1 < len(sections) else ''

            # Extract description from "— Bug: ..."
            desc_match = re.search(r'—\s*Bug:\s*(.+)', text)
            description = desc_match.group(1).strip() if desc_match else ''

            symptom = self._extract_field(text, 'Symptom')
            root_cause = self._extract_field(text, 'Root cause')
            status = self._extract_field(text, 'Status')

            findings.append({
                'date': date,
                'description': description,
                'symptom': symptom,
                'root_cause': root_cause,
                'status': status,
            })

        return findings

    def _read_progress(self) -> Dict:
        """Parse tasks/progress.md for recent errors."""
        progress_path = self.root / 'tasks' / 'progress.md'
        if not progress_path.exists():
            return {'exists': False}

        content = progress_path.read_text()
        return {
            'exists': True,
            'has_error_log': '## Error Log' in content or '### Error' in content,
        }

    def _extract_field(self, text: str, field_name: str) -> str:
        """Extract field from markdown (e.g., **Bug:** content)."""
        pattern = rf'\*\*{field_name}:\*\*\s*(.+?)(?=\n\*\*|\n###|$)'
        match = re.search(pattern, text, re.DOTALL)
        if match:
            return match.group(1).strip()
        return ''

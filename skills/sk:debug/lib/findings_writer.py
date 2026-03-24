"""Safe writer for tasks/findings.md - appends findings without overwriting."""

from pathlib import Path
from datetime import datetime
from typing import Dict


class FindingsWriter:
    """Append findings to tasks/findings.md without overwriting."""

    def __init__(self, root: Path = None):
        self.root = root or Path.cwd()
        self.findings_path = self.root / 'tasks' / 'findings.md'

    def write_findings(self, state: Dict) -> bool:
        """Write findings entry from debug state."""
        bug_info = state.get('bug_info', {})
        hypotheses = state.get('hypotheses', [])
        root_cause = state.get('root_cause_confirmed', '')

        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        bug_summary = bug_info.get('description', 'Unknown')

        # Build the entry
        entry = f"\n## {now} — Bug: {bug_summary}\n\n"
        entry += f"**Symptom:** {bug_info.get('actual_behavior', 'Unknown')}\n\n"
        entry += f"**Root cause:** {root_cause}\n\n"

        # Add hypotheses tested
        if hypotheses:
            entry += "**Hypotheses tested:**\n"
            for h in hypotheses:
                status = h.get('status', 'UNKNOWN')
                entry += f"- H{h['rank']}: {h['description']} → **{status}**\n"
                if h.get('test_results'):
                    entry += f"  Result: {h['test_results']}\n"
            entry += "\n"

        entry += f"**Status:** Investigation complete\n"

        # Write to file
        try:
            self._ensure_file_exists()
            self._append_entry(entry)
            print(f"\n✅ Findings written to {self.findings_path}")
            return True
        except OSError as e:
            print(f"\n❌ Error writing findings to {self.findings_path}: {e}")
            return False

    def _ensure_file_exists(self):
        """Create tasks/findings.md if missing with template."""
        if not self.findings_path.exists():
            self.findings_path.parent.mkdir(parents=True, exist_ok=True)
            template = """# Bug Findings

Investigations of bugs found during development.

## Entry Format

Each entry includes:
- **Date and summary** — When and what
- **Symptom** — What the user reported
- **Root cause** — What was actually wrong
- **Hypotheses tested** — What we checked
- **Status** — Investigation stage

---

"""
            self.findings_path.write_text(template)

    def _append_entry(self, entry: str):
        """Append entry to findings.md without overwriting."""
        current = self.findings_path.read_text()
        self.findings_path.write_text(current + entry + "\n")

"""Safe writer for tasks/lessons.md - appends lessons only when pattern detected."""

from pathlib import Path
from datetime import datetime
from typing import Dict


class LessonsWriter:
    """Append lessons to tasks/lessons.md only when recurrence risk detected."""

    def __init__(self, root: Path = None):
        self.root = root or Path.cwd()
        self.lessons_path = self.root / 'tasks' / 'lessons.md'

    def should_create_lesson(self, state: Dict) -> bool:
        """Determine if this bug warrants a lesson (recurrence risk)."""
        root_cause = state.get('root_cause_confirmed', '')

        if not root_cause:
            return False

        # Skip lessons for one-off issues:
        skip_patterns = [
            'typo', 'spelling', 'copy-paste',
            'environment variable not set',
            'hardware failure', 'network timeout',
            'race condition (timing)',
            'one-off',
        ]

        for pattern in skip_patterns:
            if pattern.lower() in root_cause.lower():
                return False

        # Create lesson for systematic issues that could recur:
        # - Logic errors
        # - Missing validation
        # - Architectural oversights
        # - Performance issues
        # - Missing error handling

        return True

    def write_lesson(self, state: Dict) -> bool:
        """Write lesson entry from debug state."""
        if not self.should_create_lesson(state):
            print("\n⏭️  Skipping lesson (one-off issue, pattern unlikely to recur)")
            return False

        bug_info = state.get('bug_info', {})
        root_cause = state.get('root_cause_confirmed', '')

        date = datetime.now().strftime("%Y-%m-%d")
        bug_symptom = bug_info.get('description', 'Unknown')
        prevention = self._derive_prevention(state)

        # Build the lesson entry
        entry = f"\n### [{date}] {self._generate_title(root_cause)}\n\n"
        entry += f"**Bug:** {bug_symptom}\n\n"
        entry += f"**Root cause:** {root_cause}\n\n"
        entry += f"**Prevention:** {prevention}\n"

        # Write to file
        try:
            self._ensure_file_exists()
            self._append_lesson(entry)
            print(f"\n✅ New lesson added to {self.lessons_path}")
            return True
        except OSError as e:
            print(f"\n❌ Error writing lesson to {self.lessons_path}: {e}")
            return False

    def _ensure_file_exists(self):
        """Create tasks/lessons.md if missing with template."""
        if not self.lessons_path.exists():
            self.lessons_path.parent.mkdir(parents=True, exist_ok=True)
            template = """# Lessons Learned

Patterns that caused bugs and prevention rules to avoid them in the future.

## Entry Format

Each lesson includes:
- **[Date] Title** — When and what we learned
- **Bug** — What went wrong
- **Root cause** — Why it happened
- **Prevention** — How to avoid it next time

Lessons are applied as standing constraints by:
- `/brainstorm` — Applies to requirement exploration
- `/write-plan` — Applies to plan creation
- `/execute-plan` — Applies as implementation constraints
- `/write-tests` — Applies to test patterns
- `/review` — Applies to code review checks
- `/finish-feature` — Applies as merge gate checks

---

## Active Lessons

"""
            self.lessons_path.write_text(template)

    def _append_lesson(self, entry: str):
        """Append lesson to lessons.md in the Active Lessons section."""
        content = self.lessons_path.read_text()

        # Find "## Active Lessons" marker
        marker = "## Active Lessons\n"
        if marker in content:
            # Insert after the marker
            parts = content.split(marker)
            self.lessons_path.write_text(
                parts[0] + marker + "\n" + entry + "\n" + parts[1]
            )
        else:
            # Fallback: append at end
            self.lessons_path.write_text(content + entry + "\n")

    def _derive_prevention(self, state: Dict) -> str:
        """Suggest prevention rule from root cause."""
        root_cause = state.get('root_cause_confirmed', '').lower()

        # Simple heuristics to suggest prevention
        if 'validation' in root_cause:
            return "Always validate input at system boundaries (user input, API calls, file uploads) before processing. Check type, range, format, and size."

        elif 'race condition' in root_cause:
            return "Use locks or atomic operations for concurrent access to shared state. Add tests for concurrent scenarios."

        elif 'type' in root_cause or 'coercion' in root_cause:
            return "Enable and enforce strict type checking. Avoid implicit type coercion. Use type hints/annotations."

        elif 'error handling' in root_cause or 'exception' in root_cause:
            return "Always handle exceptions explicitly. Don't silently catch and ignore errors. Log unexpected conditions."

        elif 'null' in root_cause or 'undefined' in root_cause:
            return "Check for null/undefined values before accessing properties. Use optional chaining or default values."

        elif 'memory' in root_cause or 'resource' in root_cause:
            return "Always clean up resources (close files, connections, listeners). Use try-finally or context managers."

        elif 'performance' in root_cause or 'slow' in root_cause:
            return "Profile before optimizing. Add monitoring and alerts for performance regressions. Include performance tests."

        elif 'security' in root_cause or 'injection' in root_cause:
            return "Apply input validation and output encoding. Use parameterized queries. Never trust user input. Review OWASP top 10."

        else:
            # Generic prevention
            return f"Pattern identified: {root_cause[:60]}... Review root cause and implement safeguard in code review checklist."

    def _generate_title(self, root_cause: str) -> str:
        """Generate lesson title from root cause."""
        # Try to create a concise title
        title = root_cause

        # Limit length
        if len(title) > 60:
            title = title[:57] + "..."

        # Capitalize first letter
        title = title[0].upper() + title[1:] if title else "Bug Lesson"

        return title

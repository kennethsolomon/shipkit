"""Gather bug information from user input."""

from typing import Dict


class BugGatherer:
    """Interactive bug information gathering."""

    def gather_from_user(self) -> Dict:
        """Prompt user for bug details."""
        print("\nLet's gather information about the bug.\n")

        bug_info = {
            'description': self._prompt("Brief description of what's wrong"),
            'error_message': self._prompt("Exact error message (if any)", optional=True),
            'stack_trace': self._prompt_multiline("Stack trace or logs (if any)", optional=True),
            'expected_behavior': self._prompt("What SHOULD happen"),
            'actual_behavior': self._prompt("What ACTUALLY happens"),
            'trigger_conditions': self._prompt("When/how does it happen? (Always, sometimes, specific conditions?)"),
            'recent_changes': self._prompt("Did this work before? What changed?", optional=True),
            'environment': self._prompt("Environment (local, staging, prod)?"),
        }

        return bug_info

    def _prompt(self, question: str, optional: bool = False) -> str:
        """Prompt user for input."""
        marker = " (optional)" if optional else " (required)"
        print(f"❓ {question}{marker}:")
        answer = input("> ").strip()

        if not answer and not optional:
            print("   ⚠️  This is required. Please try again.")
            return self._prompt(question, optional)

        return answer

    def _prompt_multiline(self, question: str, optional: bool = False) -> str:
        """Prompt for multiline input (ends with empty line)."""
        marker = " (optional, blank line to end)" if optional else " (blank line to end)"
        print(f"❓ {question}{marker}:")

        lines = []
        while True:
            line = input("> ")
            if not line:
                break
            lines.append(line)

        result = '\n'.join(lines)
        if not result and not optional:
            print("   ⚠️  This is required. Please try again.")
            return self._prompt_multiline(question, optional)

        return result

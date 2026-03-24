#!/usr/bin/env python3
"""Main conductor for /debug skill: 11-step structured debugging."""

import sys
from pathlib import Path
from enum import Enum
from datetime import datetime

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent / "lib"))

from context_reader import ContextReader
from bug_gatherer import BugGatherer
from step_runner import StepRunner
from findings_writer import FindingsWriter
from lessons_writer import LessonsWriter


class DebugStep(Enum):
    GATHER_INFO = 1
    READ_CONTEXT = 2
    CHECK_CHANGES = 3
    REPRODUCE = 4
    ISOLATE = 5
    FORM_HYPOTHESES = 6
    TEST_HYPOTHESES = 7
    UPDATE_FINDINGS = 8
    PROPOSE_FIX = 9
    VERIFY_FIX = 10
    DOCUMENT = 11


class DebugConductor:
    """Manages the 11-step debugging workflow with gating."""

    def __init__(self):
        self.context_reader = ContextReader()
        self.bug_gatherer = BugGatherer()
        self.step_runner = StepRunner()
        self.findings_writer = FindingsWriter()
        self.lessons_writer = LessonsWriter()
        self.current_step = DebugStep.GATHER_INFO
        self.state = {}  # Accumulate findings across steps

    def run(self):
        """Execute debugging workflow from step 1 to 11."""
        print("\n" + "="*70)
        print("🐛 DEBUG: Structured Bug Investigation")
        print("="*70)

        # Step 1: Gather user input
        print("\n[STEP 1] Gathering Information")
        bug_info = self.bug_gatherer.gather_from_user()
        self.state['bug_info'] = bug_info

        # Step 2: Read context files
        print("\n[STEP 2] Reading Project Context")
        context = self.context_reader.read_all()
        self.state['context'] = context
        self.state['active_lessons'] = context['lessons']

        # Apply lessons as constraints
        self._apply_lessons_as_constraints(context['lessons'])

        # Steps 3-11: Run sequentially with gating
        for step_num in range(3, 12):
            step = DebugStep(step_num)
            self.current_step = step

            print(f"\n{'='*70}")
            print(f"[STEP {step_num}] {step.name.replace('_', ' ').title()}")
            print(f"{'='*70}\n")

            # Check if we can proceed
            if not self._can_proceed(step):
                print(f"\n⛔ BLOCKED: {self._gate_reason(step)}")
                print("\nRun /debug again to continue from this step.")
                return

            # Run step and update state
            result = self.step_runner.execute(step, self.state)
            self.state.update(result)

            # Step 8: Write findings
            if step_num == 8:
                self.findings_writer.write_findings(self.state)

            # Step 11: Write lesson (conditional)
            if step_num == 11:
                self.lessons_writer.write_lesson(self.state)

            if step_num < 11:
                proceed = input(f"\n✅ Step {step_num} complete. Continue to step {step_num + 1}? (y/n): ").strip().lower()
                if proceed not in ['y', 'yes', '']:
                    print(f"Pausing after step {step_num}. Run /debug again to continue.")
                    return

        print("\n" + "="*70)
        print("🎉 DEBUGGING WORKFLOW COMPLETE")
        print("="*70)
        print(f"\n✅ Findings written to: tasks/findings.md")
        if self.state.get('lesson_created'):
            print(f"✅ New lesson written to: tasks/lessons.md")
        print("\n📝 Next: Run /commit to create a fix commit")
        print("   Or:  Run /write-tests to add test coverage")

    def _apply_lessons_as_constraints(self, lessons: list):
        """Apply all active lessons as standing constraints during investigation."""
        if not lessons:
            return

        print("\n📚 APPLYING STANDING LESSONS:")
        for lesson in lessons:
            print(f"   - [{lesson.get('date', '?')}] {lesson.get('title', 'Unknown')}")
            print(f"     Prevention: {lesson.get('prevention', 'N/A')}")
        print()

    def _can_proceed(self, step: DebugStep) -> bool:
        """Check if we can proceed to/through this step."""
        # Step 4: Must eventually reproduce to proceed
        if step == DebugStep.REPRODUCE:
            return True  # Can always try to reproduce

        # Step 5+: Must have reproduced
        if step.value > 4:
            return self.state.get('reproduced', False)

        # Step 6: Can form hypotheses
        if step == DebugStep.FORM_HYPOTHESES:
            return True

        # Step 7+: Must have hypotheses
        if step.value > 6:
            return len(self.state.get('hypotheses', [])) > 0

        # Step 8+: Must have tested at least one
        if step.value > 7:
            hypotheses = self.state.get('hypotheses', [])
            return any(h.get('status') in ['CONFIRMED', 'REJECTED', 'PARTIAL']
                      for h in hypotheses)

        # Step 9+: Must have confirmed hypothesis
        if step.value > 8:
            hypotheses = self.state.get('hypotheses', [])
            return any(h.get('status') == 'CONFIRMED' for h in hypotheses)

        return True

    def _gate_reason(self, step: DebugStep) -> str:
        """Explain why we can't proceed."""
        if step.value > 4 and not self.state.get('reproduced'):
            return "Cannot proceed without reproducing the bug first."
        if step.value > 7 and not self.state.get('hypotheses'):
            return "No hypotheses formed yet."
        if step.value > 8 and not any(
            h.get('status') == 'CONFIRMED'
            for h in self.state.get('hypotheses', [])
        ):
            return "No confirmed hypothesis yet—cannot propose fix."
        return "Precondition not met for this step."

def main():
    """Entry point for /debug skill."""
    conductor = DebugConductor()
    conductor.run()


if __name__ == '__main__':
    main()

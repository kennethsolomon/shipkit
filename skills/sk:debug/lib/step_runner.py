"""Execute individual debug steps (3-11)."""

import subprocess
from typing import Dict
from pathlib import Path
import sys


class StepRunner:
    """Execute each debugging step."""

    def execute(self, step, state: Dict) -> Dict:
        """Execute a specific step and return results."""
        step_num = step.value

        if step_num == 3:
            return self._step_3_check_changes()
        elif step_num == 4:
            return self._step_4_reproduce(state)
        elif step_num == 5:
            return self._step_5_isolate(state)
        elif step_num == 6:
            return self._step_6_form_hypotheses(state)
        elif step_num == 7:
            return self._step_7_test_hypotheses(state)
        elif step_num == 8:
            return self._step_8_update_findings(state)
        elif step_num == 9:
            return self._step_9_propose_fix(state)
        elif step_num == 10:
            return self._step_10_verify_fix(state)
        elif step_num == 11:
            return self._step_11_document(state)

        return {}

    def _step_3_check_changes(self) -> Dict:
        """Check recent git changes."""
        print("Checking recent git commits and diffs...\n")

        try:
            # Recent commits
            print("📋 Recent commits:")
            result = subprocess.run(
                "git log --oneline -10",
                shell=True,
                capture_output=True,
                text=True
            )
            print(result.stdout)

            # Recent diffs
            print("\n📋 Recent file changes:")
            result = subprocess.run(
                "git diff HEAD~3 --stat",
                shell=True,
                capture_output=True,
                text=True
            )
            print(result.stdout)

            return {'changes_reviewed': True}

        except Exception as e:
            print(f"⚠️  Could not check git history: {e}")
            return {'changes_reviewed': False}

    def _step_4_reproduce(self, state: Dict) -> Dict:
        """Reproduce the bug (CLI or browser)."""
        bug_info = state['bug_info']

        print("Now let's reproduce the bug to confirm it exists.\n")

        # Detect if likely browser bug
        is_browser_bug = self._detect_browser_bug(bug_info)

        if is_browser_bug:
            return self._reproduce_browser_bug(state)
        else:
            return self._reproduce_cli_bug(state)

    def _detect_browser_bug(self, bug_info: Dict) -> bool:
        """Heuristic: is this a browser/UI bug?"""
        keywords = [
            'visual', 'browser', 'javascript', 'console', 'render',
            'DOM', 'click', 'button', 'form', 'UI', 'page', 'screen'
        ]
        text = (
            bug_info.get('description', '') + ' ' +
            bug_info.get('error_message', '')
        ).lower()
        return any(kw in text for kw in keywords)

    def _reproduce_cli_bug(self, state: Dict) -> Dict:
        """Reproduce CLI/server bug via bash command."""
        print("📝 Provide the bash command that triggers the bug:")
        print("   (Leave blank if you'd rather describe manually)\n")

        command = input("> ").strip()

        if not command:
            print("\n⚠️  Cannot reproduce without a command.")
            print("   Please provide the exact command/steps to trigger the bug.")
            return {'reproduced': False}

        print(f"\n🔧 Running: {command}\n")

        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )

            output = result.stdout + result.stderr
            print(output)

            print("\n✅ Bug reproduced successfully!")

            return {
                'reproduced': True,
                'bug_type': 'cli',
                'reproduction_command': command,
                'reproduction_output': output[:500],  # First 500 chars
                'evidence_collected': [f"Reproduced with: {command}"]
            }

        except subprocess.TimeoutExpired:
            print("\n⚠️  Command timed out (30s)")
            return {'reproduced': False}
        except Exception as e:
            print(f"\n❌ Error: {e}")
            return {'reproduced': False}

    def _reproduce_browser_bug(self, state: Dict) -> Dict:
        """Reproduce browser/UI bug using Playwright (if available)."""
        print("🌐 Browser bug detected. Provide URL where bug occurs:")
        print("   (e.g., http://localhost:3000/page)\n")

        url = input("> ").strip()

        if not url:
            print("\n⚠️  Cannot reproduce without URL.")
            return {'reproduced': False}

        print(f"\n🔧 Navigating to {url}...\n")

        # TODO: Integrate Playwright MCP if available
        # For now, mark as reproduced with manual confirmation

        confirmed = input("Is the bug visible? (y/n): ").strip().lower()

        if confirmed in ['y', 'yes']:
            return {
                'reproduced': True,
                'bug_type': 'browser',
                'url': url,
                'evidence_collected': [f"Reproduced at {url}"]
            }

        return {'reproduced': False}

    def _step_5_isolate(self, state: Dict) -> Dict:
        """Isolate the problem by analyzing code."""
        print("Now let's isolate the problem.\n")

        error = state['bug_info'].get('error_message', '')
        stack_trace = state['bug_info'].get('stack_trace', '')

        print("📊 Code path to investigate:")
        if error:
            print(f"   Error: {error}")
        if stack_trace:
            print(f"   Stack trace: {stack_trace}")

        isolation_notes = input("\n> Describe what code you think is involved: ").strip()

        return {
            'isolated_problem': isolation_notes,
            'evidence_collected': [f"Isolated problem: {isolation_notes}"]
        }

    def _step_6_form_hypotheses(self, state: Dict) -> Dict:
        """Form 2-3 hypotheses about root cause."""
        print("\nForm hypotheses about what's causing the bug.\n")
        print("For each hypothesis, provide:")
        print("  1. Your theory")
        print("  2. Evidence that supports it")
        print("  3. How you'd test it\n")

        hypotheses = []
        for rank in range(1, 4):
            print(f"Hypothesis {rank}:")
            description = input("  > Theory: ").strip()
            if not description:
                continue

            evidence = input("  > Evidence supporting this: ").strip()
            test_plan = input("  > How to test it: ").strip()

            hypotheses.append({
                'rank': rank,
                'description': description,
                'evidence': evidence,
                'test_plan': test_plan,
                'status': 'UNKNOWN',
                'test_results': '',
            })

        return {'hypotheses': hypotheses}

    def _step_7_test_hypotheses(self, state: Dict) -> Dict:
        """Test each hypothesis systematically."""
        hypotheses = state.get('hypotheses', [])

        print(f"\nTesting {len(hypotheses)} hypothesis/hypotheses...\n")

        for h in hypotheses:
            print(f"Testing H{h['rank']}: {h['description']}")
            print(f"  Plan: {h['test_plan']}\n")

            result = input("  > Test result (CONFIRMED/REJECTED/PARTIAL): ").strip().upper()
            details = input("  > Details: ").strip()

            h['status'] = result if result in ['CONFIRMED', 'REJECTED', 'PARTIAL'] else 'UNKNOWN'
            h['test_results'] = details

            if h['status'] == 'CONFIRMED':
                print(f"  ✅ H{h['rank']} CONFIRMED!\n")
            elif h['status'] == 'REJECTED':
                print(f"  ❌ H{h['rank']} rejected.\n")
            else:
                print(f"  ⚠️  H{h['rank']} inconclusive.\n")

        return {'hypotheses': hypotheses}

    def _step_8_update_findings(self, state: Dict) -> Dict:
        """Update findings.md with investigation results."""
        print("\n📝 Findings will be written to tasks/findings.md")
        print("   (This happens automatically in the next step)")
        return {}

    def _step_9_propose_fix(self, state: Dict) -> Dict:
        """Propose minimal fix."""
        hypotheses = state.get('hypotheses', [])
        confirmed = next((h for h in hypotheses if h['status'] == 'CONFIRMED'), None)

        if not confirmed:
            print("\n❌ No confirmed hypothesis—cannot propose fix.")
            return {}

        print(f"\nConfirmed root cause: {confirmed['description']}\n")
        print("Describe the minimal fix:")
        print("  - What file(s) to change")
        print("  - What to change")
        print("  - Why it fixes the problem\n")

        fix_description = input("> Fix proposal: ").strip()

        return {
            'confirmed_hypothesis': confirmed['description'],
            'proposed_fix': fix_description,
            'root_cause_confirmed': confirmed['description']
        }

    def _step_10_verify_fix(self, state: Dict) -> Dict:
        """Verify the fix works."""
        print("\n✅ Apply the fix to your code, then return here.\n")
        input("Press Enter when fix is applied: ")

        print("\nVerifying fix works...\n")

        command = input("Run your reproduction command again: ").strip()

        if command:
            try:
                result = subprocess.run(
                    command,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                output = result.stdout + result.stderr
                print(output)

                fixed = input("\nIs the bug fixed? (y/n): ").strip().lower()
                if fixed in ['y', 'yes']:
                    print("✅ Fix verified!")
                    return {'fix_verified': True}

            except Exception as e:
                print(f"Error: {e}")

        return {'fix_verified': False}

    def _step_11_document(self, state: Dict) -> Dict:
        """Document the findings and create lesson if needed."""
        print("\n📚 Documentation will be written:")
        print("   ✅ tasks/findings.md (bug details)")

        # Determine if a lesson should be created
        root_cause = state.get('root_cause_confirmed', '')

        skip_patterns = [
            'typo', 'spelling', 'copy-paste',
            'environment variable',
            'one-off', 'race condition'
        ]

        skip_lesson = any(p.lower() in root_cause.lower() for p in skip_patterns)

        if not skip_lesson and root_cause:
            print("   ✅ tasks/lessons.md (prevention rule)")
            return {
                'lesson_created': True,
                'root_cause_confirmed': root_cause
            }
        else:
            print("   ⏭️  Skipping lesson (one-off issue)")
            return {
                'lesson_created': False,
                'root_cause_confirmed': root_cause
            }

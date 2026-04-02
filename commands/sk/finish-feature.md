---
description: "Finalize a feature/bug-fix: changelog, arch log, verification, and PR creation."
disable-model-invocation: true
---

# /sk:finish-feature

Finalize a feature/bug-fix branch and create a pull request.

Finalize a feature/bug-fix branch: changelog, arch log, security gate, verification, and PR creation.

This is the **last step before `/sk:release`**. It auto-commits documentation changes (changelog, arch log) so you don't need to loop back to `/sk:smart-commit` for docs-only work.

## Before You Start

**ShipKit structural change check:** Count SKILL.md files changed on this branch:
```bash
git diff main..HEAD --name-only | grep -c 'SKILL\.md' || true
```
If the count is **≥ 3**, `/sk:review` must be run before proceeding. If it has not been run this session, stop and run it now. This prevents cross-cutting skill regressions from shipping unreviewed.

If `tasks/lessons.md` exists, read it in full. For each active lesson, scan the
final diff (`git diff main..HEAD`) for the **Bug** pattern described in that lesson
before marking the feature done. This is the last gate before merge — catch recurring
mistakes here rather than in review.

If `tasks/security-findings.md` exists, read it. Check that any Critical or High
severity findings from the most recent `/sk:security-check` audit have been addressed.
If unresolved Critical/High findings remain, warn the user before proceeding.

## Steps

1. **Check Git Branch**
   - Verify you are not on `main`
   - Create a branch if needed: `feature/<desc>`, `fix/<desc>`, or `chore/<desc>`

2. **Show Branch Summary**
   - `git status --short`
   - `git log main..HEAD --oneline`

3. **Verify `CHANGELOG.md` Updated**
   - Ensure an entry exists under `[Unreleased]`
   - Follow `.claude/docs/changelog-guide.md`
   - If CHANGELOG.md needs updating, make the edit and auto-commit:
     ```bash
     git add CHANGELOG.md
     git commit -m "docs: update CHANGELOG.md for unreleased changes"
     ```

4. **Check for Architectural Changes**

   The auto-detector scans for architecture-relevant changes:
   - Schema/database changes (migrations, models, databases)
   - API/route structure changes (endpoints, controllers)
   - Component/module organization changes
   - Configuration changes affecting architecture
   - New subsystems or major refactors
   - Dependency changes

   Run to see what would be detected:
   ```bash
   python3 $HOME/.claude/skills/sk:setup-claude/scripts/detect_arch_changes.py --dry-run
   ```

   If architectural changes detected:
   a) **Auto-generate the draft:**
      ```bash
      python3 $HOME/.claude/skills/sk:setup-claude/scripts/detect_arch_changes.py
      ```
      This creates a markdown draft in `.claude/docs/architectural_change_log/`

   b) **Review and edit the draft:**
      - Open the generated file
      - Fill in [TODO] sections:
        - Detailed Changes: What specifically changed?
        - Before & After: Show the comparison
        - Affected Components: What parts of system are impacted?
        - Migration/Compatibility: Any breaking changes?
      - Verify the auto-filled sections (Summary, Type, What Changed, Impact)

   c) **Auto-commit the arch log** (no need to go back to `/sk:smart-commit`):
      ```bash
      git add .claude/docs/architectural_change_log/
      git commit -m "docs: add architectural changelog entry"
      ```

   If no architectural changes detected: skip to step 5.

5. **Verification** (with Test Checklist for Reviewers)

   Tests should have been created during `/sk:execute-plan`. Verify:

   Detect the project stack from `CLAUDE.md`, `package.json`, `composer.json`, etc. before running checks.

   a) **Automated Tests**
      - Execute the detected test runner (e.g. `npm test`, `./vendor/bin/pest`, `python -m pytest`)
      - Verify all tests pass with no failures
      - Check test coverage (target: >80% for new code)
      - No skipped tests (`test.skip`, `it.skip`, `@skip`, etc.)
      - Run other CI checks: lint and build using project-detected commands

   b) **Manual Testing**
      - For frontend (if detected): Render the component/page in browser, verify state updates work correctly, test all user interactions (clicks, form inputs, navigation), verify conditional rendering, check edge cases and error states
      - For backend/API (if detected): Test HTTP status codes and responses, verify request/response bodies match spec, test error cases and input validation, check database transactions/state, verify authentication/authorization if applicable
      - For CLI/desktop (if detected): Test command-line arguments and flags, verify output format and readability, test error messages and help text, check file I/O operations
      - Verify test structure matches project conventions, assertions are clear and specific, setup/teardown is properly handled

   c) **Regression Testing**
      - Test related existing functionality to ensure no breakage
      - Check related components/endpoints/commands work correctly
      - Verify no new console errors, warnings, or debug statements
      - Confirm existing tests still pass

   d) **Code Quality Checks**
      - No hardcoded test data, credentials, or environment-specific values in production code
      - Proper error handling and validation
      - No debugging code (`console.log`, `debugger`, `pdb`, `print` statements, etc.)
      - Comments explain *why*, not *what*
      - Follows project conventions and style guide (see `CLAUDE.md`)

6. **Security Gate**
   - If `/sk:security-check` has not been run on this branch, recommend: "Run `/sk:security-check` before creating a PR."
   - If `tasks/security-findings.md` has unresolved Critical or High findings, list them and ask the user to confirm they've been addressed.

7. **Create Pull Request**

   a) **Check remote status:**
   ```bash
   git remote -v
   git rev-parse --abbrev-ref --symbolic-full-name @{u} 2>/dev/null || echo "no upstream"
   ```

   b) **Push branch if needed:**
   ```bash
   git push -u origin HEAD
   ```

   c) **Generate PR title and body:**
      - Title: Short, imperative, under 70 characters
      - Body: Summary of changes, review findings (if any from `/sk:review`), test status

   d) **Create PR:**
   ```bash
   gh pr create --title "title here" --body "$(cat <<'EOF'
   ## Summary
   - bullet points of key changes

   ## Review Notes
   - Any findings from /sk:review (or "Clean review — no issues found")

   ## Security
   - Security check status (passed / N findings addressed)

   ## Test Plan
   - How to verify the changes

   Generated with [Claude Code](https://claude.com/claude-code)
   EOF
   )"
   ```

   e) Report the PR URL to the user.

7.5. **CI Monitor Loop** (mandatory — do not skip)

After the PR is created, monitor CI and respond to all auto-reviewer comments before calling the feature done.

   a) **Wait for auto-reviewers** — wait 3 minutes after PR creation. Auto-reviewers (Copilot, CodeRabbit, Gemini, etc.) need time to post their first round.

   b) **Poll CI status:**
   ```bash
   gh run list --branch "$(git rev-parse --abbrev-ref HEAD)" --limit 1 --json status,conclusion,name
   ```
   Re-poll every 60 seconds until status is `completed`. If `conclusion` is `failure`: read the failed run logs (`gh run view --log-failed`), fix the issue, push, and restart the loop.

   c) **Read all PR comments:**
   ```bash
   gh pr view --comments
   ```
   Address **every comment** — no exceptions, no "minor" exemptions. For each:
   - Apply the suggested change or push back with a reply explaining why not
   - Mark threads resolved after addressing

   d) **Iterate** until both conditions are true:
   - CI conclusion: `success`
   - Zero unresolved comment threads

   e) **Output verification line:**
   ```
   [VERIFIED] CI: ✓ success | Unresolved comments: 0 | Iterations: N
   ```

   **Forbidden:** checking CI once and proceeding, ignoring "nit" comments, merging with unresolved threads.

8. **Capture Patterns** (`/sk:learn`)

   After the PR is created, run `/sk:learn` to extract reusable patterns from this session.
   Present extracted patterns and ask: "Save patterns? (all / 1,3 / none)"

9. **Retrospective** (`/sk:retro`)

   Run `/sk:retro` to capture a brief post-ship retrospective:
   - What went well
   - What slowed things down
   - Top action items for next time

   Output is appended to `tasks/progress.md`.

## When Done

> "Feature finalized and PR created! Run `/sk:release` when ready to tag and publish."

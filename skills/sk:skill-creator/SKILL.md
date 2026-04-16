---
name: sk:skill-creator
description: Create new skills, modify and improve existing skills, and measure skill performance. Use when users want to create a skill from scratch, update or optimize an existing skill, run evals to test a skill, benchmark skill performance with variance analysis, or optimize a skill's description for better triggering accuracy.
---

# Skill Creator

Create and iteratively improve skills via: draft → test → evaluate → improve → repeat.

Assess where the user is in this loop and jump in accordingly. If they already have a draft, skip to eval. If they want to skip evals entirely, that's fine too. After the skill is done, offer to run description optimization.

Adapt communication to user familiarity — briefly define "JSON", "assertion", etc. if context suggests unfamiliarity.

> **ShipKit structural changes:** If this skill creation or modification touches ShipKit's own structure (adding/removing a skill, gate, command, agent, or community plugin), read `.claude/docs/maintenance-guide.md` BEFORE writing any files. The guide lists every derived file that must stay in sync — missing even one causes a second-pass cleanup. This is a lesson learned from experience.

---

## Creating a skill

### Capture Intent

If the current conversation already contains a workflow to capture, extract tools, steps, corrections, and I/O formats from history first. User confirms before proceeding.

1. What should this skill enable Claude to do?
2. When should it trigger? (phrases/contexts)
3. What's the expected output format?
4. Do we need test cases? Suggest based on skill type: objectively verifiable outputs (transforms, extraction, codegen, fixed workflows) → yes. Subjective outputs (writing style, art) → usually no.

### Interview and Research

Ask about edge cases, I/O formats, example files, success criteria, and dependencies before writing test prompts. Check available MCPs for research; run parallel subagents if available.

### Write the SKILL.md

Fill in:
- **name**: Skill identifier
- **description**: When to trigger + what it does. Primary triggering mechanism — include both function and contexts. All "when to use" info goes here, not in the body. Make descriptions slightly "pushy" to counter undertriggering: e.g., "Use this whenever the user mentions dashboards, data visualization, or wants to display any company data, even if they don't explicitly ask for a 'dashboard.'"
- **compatibility**: Required tools/dependencies (optional, rarely needed)
- **body**: Instructions

### Skill Writing Guide

#### Anatomy of a Skill

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter (name, description required)
│   └── Markdown instructions
└── Bundled Resources (optional)
    ├── scripts/    - Executable code for deterministic/repetitive tasks
    ├── references/ - Docs loaded into context as needed
    └── assets/     - Files used in output (templates, icons, fonts)
```

#### Progressive Disclosure

Three-level loading:
1. **Metadata** (name + description) — always in context (~100 words)
2. **SKILL.md body** — in context when skill triggers (<500 lines ideal)
3. **Bundled resources** — loaded as needed (unlimited; scripts can execute without loading)

- Keep SKILL.md under 500 lines; if approaching limit, add hierarchy with clear pointers to follow-up files
- Reference bundled files clearly with guidance on when to read them
- For large reference files (>300 lines), include a table of contents

**Domain organization**: When a skill supports multiple domains/frameworks:
```
cloud-deploy/
├── SKILL.md (workflow + selection)
└── references/
    ├── aws.md
    ├── gcp.md
    └── azure.md
```

#### Security

Skills must not contain malware, exploit code, or anything that could compromise system security. Don't create misleading skills or skills designed for unauthorized access, data exfiltration, or other malicious purposes.

#### Anti-Patterns Section (recommended)

Every skill should define what it must NEVER do — not just what it does. This prevents subtle failure modes where the skill technically follows instructions but produces wrong results.

Add a `## Anti-Patterns (NEVER do these)` section listing 3–5 concrete failure modes. Use specific examples, not abstract rules.

```markdown
## Anti-Patterns (NEVER do these)

- [Concrete bad behavior + why it fails]
- [Another failure mode + what happens]
- [Edge case that looks correct but isn't]
```

Good anti-patterns are:
- **Specific** — "Stating the answer then asking 'do you understand?'" not "Don't give answers"
- **Observable** — someone reading the output can tell if it happened
- **Non-obvious** — things the LLM might do that look right but are wrong

Adapted from the [Socrates skill](https://github.com/RoundTable02/socrates-skill) pattern.

#### Agent Persona Skills (when the skill embodies a specialist role)

When a skill positions Claude as a specialist agent (analyst, reviewer, architect, coach, etc.), it needs more than instructions — it needs identity. Generic "act as X" skills produce generic output. Apply these five components:

| Component | What it means | Example |
|-----------|--------------|---------|
| **Strong personality** | Character and voice, not just a job title | "Direct, no-hedging, calls out weak reasoning immediately" |
| **Clear deliverables** | Concrete output format, not vague guidance | "Returns: risk table + 3 recommended actions + one-line verdict" |
| **Success metrics** | Measurable quality bar | "Every finding cites file:line and explains production impact" |
| **Proven workflow** | Step-by-step process to follow | "1. Read blast radius 2. Check changed symbols 3. Classify by severity" |
| **Explicit failure modes** | What this agent must never do | "Never mark a finding verified without reading the file" |

These map directly to the anti-patterns section — personality prevents generic output, deliverables prevent vague output, success metrics make grading possible.

#### Auto-Clarity Escape Hatch (recommended)

Skills that modify output style (compression, formatting, tone) should define when to temporarily disable themselves. Without this, the skill may compress a security warning into an ambiguous fragment.

Add a `## Auto-Clarity` section listing conditions where the skill should revert to normal output:

```markdown
## Auto-Clarity

Drop [modified behavior] for:
- Security warnings and irreversible action confirmations
- Multi-step sequences where modified output risks misreading
- When user is confused or asking for clarification

Resume [modified behavior] after the clear section is complete.
```

This is a safety valve — the skill self-governs when its style becomes dangerous. Adapted from the [Caveman skill](https://github.com/JuliusBrussee/caveman) pattern.

#### Writing Patterns

Use imperative form. Explain *why* behind instructions rather than heavy-handed MUSTs — LLMs perform better with reasoning than rote commands.

**Output format:**
```markdown
## Report structure
ALWAYS use this exact template:
# [Title]
## Executive summary
## Key findings
## Recommendations
```

**Examples:**
```markdown
## Commit message format
**Example 1:**
Input: Added user authentication with JWT tokens
Output: feat(auth): implement JWT-based authentication
```

### Test Cases

After the skill draft, write 2-3 realistic test prompts. Share with user for confirmation, then run them.

Save to `evals/evals.json` (no assertions yet — draft those while runs are in progress):

```json
{
  "skill_name": "example-skill",
  "evals": [
    {
      "id": 1,
      "prompt": "User's task prompt",
      "expected_output": "Description of expected result",
      "files": []
    }
  ]
}
```

See `references/schemas.md` for the full schema including the `assertions` field.

---

## Running and evaluating test cases

One continuous sequence — do not stop partway. Do NOT use `/skill-test` or any other testing skill.

Organize results in `<skill-name>-workspace/` as a sibling to the skill directory, by iteration (`iteration-1/`, `iteration-2/`, etc.) and test case (`eval-0/`, `eval-1/`, etc.). Create directories as you go.

### Step 1: Spawn all runs in the same turn

For each test case, spawn two subagents simultaneously — one with the skill, one without. Launch everything at once.

**With-skill run:**
```
Execute this task:
- Skill path: <path-to-skill>
- Task: <eval prompt>
- Input files: <eval files if any, or "none">
- Save outputs to: <workspace>/iteration-<N>/eval-<ID>/with_skill/outputs/
- Outputs to save: <what the user cares about>
```

**Baseline run** (context-dependent):
- **New skill**: no skill at all — same prompt, no skill path, save to `without_skill/outputs/`
- **Improving existing skill**: old version — snapshot first (`cp -r <skill-path> <workspace>/skill-snapshot/`), point baseline at snapshot, save to `old_skill/outputs/`

Write `eval_metadata.json` per test case (assertions empty for now). Use descriptive names for directories — not just "eval-0":

```json
{
  "eval_id": 0,
  "eval_name": "descriptive-name-here",
  "prompt": "The user's task prompt",
  "assertions": []
}
```

### Step 2: Draft assertions while runs are in progress

Don't wait — draft quantitative assertions and explain them to the user. Good assertions are objectively verifiable and have descriptive names. For subjective skills, don't force assertions — use qualitative review.

Update `eval_metadata.json` and `evals/evals.json` with assertions once drafted. Explain what the user will see in the viewer.

### Step 3: Capture timing data as runs complete

When each subagent completes, save timing data immediately to `timing.json` in the run directory — this data is only available in the task notification:

```json
{
  "total_tokens": 84852,
  "duration_ms": 23332,
  "total_duration_seconds": 23.3
}
```

### Step 4: Grade, aggregate, and launch the viewer

1. **Grade** — spawn a grader subagent reading `agents/grader.md`. Save `grading.json` per run directory. Required fields: `text`, `passed`, `evidence` (not `name`/`met`/`details`). Use scripts for programmatic assertions.

2. **Aggregate** — run from the skill-creator directory:
   ```bash
   python -m scripts.aggregate_benchmark <workspace>/iteration-N --skill-name <name>
   ```
   Produces `benchmark.json` and `benchmark.md`. Put each `with_skill` version before its baseline counterpart. See `references/schemas.md` for manual schema.

3. **Analyst pass** — read `agents/analyzer.md` ("Analyzing Benchmark Results") to surface non-discriminating assertions, high-variance evals, and time/token tradeoffs.

4. **Launch the viewer:**
   ```bash
   nohup python <skill-creator-path>/eval-viewer/generate_review.py \
     <workspace>/iteration-N \
     --skill-name "my-skill" \
     --benchmark <workspace>/iteration-N/benchmark.json \
     > /dev/null 2>&1 &
   VIEWER_PID=$!
   ```
   For iteration 2+, also pass `--previous-workspace <workspace>/iteration-<N-1>`.

   **Cowork / headless environments:** Use `--static <output_path>` for a standalone HTML file. Feedback downloads as `feedback.json` when user clicks "Submit All Reviews" — copy it into the workspace for the next iteration.

   Use `generate_review.py` — do not write custom HTML.

5. Tell the user: "I've opened the results in your browser. 'Outputs' tab lets you review each test case and leave feedback; 'Benchmark' shows quantitative comparison. Come back when done."

**Viewer layout:**
- **Outputs tab**: Prompt, Output, Previous Output (iter 2+, collapsed), Formal Grades (collapsed), Feedback textbox, Previous Feedback (iter 2+)
- **Benchmark tab**: Pass rates, timing, token usage per configuration, per-eval breakdowns, analyst observations
- Navigation: prev/next or arrow keys; "Submit All Reviews" saves `feedback.json`

### Step 5: Read feedback

```json
{
  "reviews": [
    {"run_id": "eval-0-with_skill", "feedback": "the chart is missing axis labels", "timestamp": "..."},
    {"run_id": "eval-1-with_skill", "feedback": "", "timestamp": "..."}
  ],
  "status": "complete"
}
```

Empty feedback = the user thought it was fine. Focus on test cases with specific complaints.

Kill the viewer when done:
```bash
kill $VIEWER_PID 2>/dev/null
```

---

## Improving the skill

### Improvement principles

1. **Generalize, don't overfit.** Skills run across millions of diverse prompts. Avoid fiddly or over-constrictive changes. If a stubborn issue persists, try different metaphors or working patterns.

2. **Keep the prompt lean.** Remove instructions that aren't pulling their weight. Read transcripts — if the model wastes time on unproductive steps, remove the instructions causing it.

3. **Explain the why.** Write *why* something matters, not just *what* to do. Avoid all-caps ALWAYS/NEVER; reframe with reasoning instead. LLMs respond better to rationale than rigid commands.

4. **Bundle repeated work.** If all test cases resulted in subagents writing similar helper scripts, bundle the script in `scripts/` and reference it from the skill.

### Iteration loop

1. Apply improvements to the skill
2. Rerun all test cases into `iteration-<N+1>/`, including baselines (new skill → `without_skill`; improving → use judgment on whether baseline is original or previous iteration)
3. Launch viewer with `--previous-workspace` pointing at previous iteration
4. Wait for user review, read feedback, improve again

Stop when:
- User is satisfied
- All feedback is empty
- No meaningful progress is being made

---

## Advanced: Blind comparison

For rigorous A/B comparison between two skill versions, read `agents/comparator.md` and `agents/analyzer.md`. An independent agent judges outputs without knowing which version produced them. Optional, requires subagents — human review is usually sufficient.

---

## Description Optimization

The `description` field is the primary triggering mechanism. After creating or improving a skill, offer to optimize it.

### Step 1: Generate trigger eval queries

Create 20 eval queries — mix of should-trigger and should-not-trigger. Save as JSON:

```json
[
  {"query": "the user prompt", "should_trigger": true},
  {"query": "another prompt", "should_trigger": false}
]
```

Queries must be realistic and specific — include file paths, personal context, column names, company names, URLs, backstory, typos, casual speech, varying lengths. Focus on edge cases over clear-cut examples.

**Bad:** `"Format this data"`, `"Extract text from PDF"`, `"Create a chart"`

**Good:** `"ok so my boss just sent me this xlsx file (its in my downloads, called something like 'Q4 sales final FINAL v2.xlsx') and she wants me to add a column that shows the profit margin as a percentage. The revenue is in column C and costs are in column D i think"`

- **Should-trigger (8-10)**: varied phrasings of same intent — formal and casual; cases where user doesn't name the skill but clearly needs it; uncommon use cases; cases where this skill competes with another but should win
- **Should-not-trigger (8-10)**: near-misses that share keywords but need something different; adjacent domains; ambiguous phrasing where naive keyword match would trigger but shouldn't. Do NOT make these obviously irrelevant.

### Step 2: Review with user

1. Read `assets/eval_review.html`
2. Replace placeholders: `__EVAL_DATA_PLACEHOLDER__` → JSON array (no quotes, it's a JS variable), `__SKILL_NAME_PLACEHOLDER__`, `__SKILL_DESCRIPTION_PLACEHOLDER__`
3. Write to `/tmp/eval_review_<skill-name>.html` and open it
4. User edits queries, toggles should-trigger, adds/removes entries, clicks "Export Eval Set"
5. File downloads to `~/Downloads/eval_set.json` — check for most recent version if duplicates exist (e.g., `eval_set (1).json`)

### Step 3: Run the optimization loop

Tell the user: "This will take some time — I'll run the optimization loop in the background and check periodically."

Save eval set to workspace, then run in background:

```bash
python -m scripts.run_loop \
  --eval-set <path-to-trigger-eval.json> \
  --skill-path <path-to-skill> \
  --model <model-id-powering-this-session> \
  --max-iterations 5 \
  --verbose
```

Use the model ID from your system prompt so the triggering test matches what the user actually experiences. Periodically tail output to give iteration/score updates.

The loop: splits eval 60% train / 40% held-out test → evaluates current description (3 runs per query for reliability) → calls Claude with extended thinking to propose improvements → re-evaluates on train + test → iterates up to 5 times → returns `best_description` selected by test score (not train, to avoid overfitting).

**How triggering works:** Claude sees skills in `available_skills` with name + description and decides whether to consult one. Claude only consults skills for tasks it can't handle alone — simple one-step queries won't trigger skills even with a perfect description match. Eval queries must be substantive enough that Claude would genuinely benefit from a skill.

### Step 4: Apply the result

Take `best_description` from JSON output, update the skill's frontmatter. Show before/after and report scores.

---

### Package and Present (only if `present_files` tool is available)

```bash
python -m scripts.package_skill <path/to/skill-folder>
```

Direct user to the resulting `.skill` file path for installation.

---

## Claude.ai-specific instructions

Core workflow is the same (draft → test → review → improve → repeat), but adapt mechanics:

| Feature | Claude.ai behavior |
|---|---|
| Test case runs | No subagents — run sequentially, following SKILL.md yourself. Skip baselines. |
| Results review | No browser — present results inline in conversation. Share file paths for downloadable outputs. Ask for feedback inline. |
| Benchmarking | Skip — no meaningful baselines without subagents |
| Iteration loop | Same — improve, rerun, ask for feedback. Organize results into iteration directories if filesystem available. |
| Description optimization | Skip — requires `claude -p` CLI, only available in Claude Code |
| Blind comparison | Skip — requires subagents |
| Packaging | Works anywhere with Python + filesystem |

---

## Cowork-specific instructions

| Feature | Cowork behavior |
|---|---|
| Subagents | Available — main workflow works. Fall back to serial if timeouts are severe. |
| Viewer | No display — use `--static <output_path>`. Provide a link for user to open HTML in browser. |
| Feedback | No running server — "Submit All Reviews" downloads `feedback.json`. Read from Downloads (may need to request access). |
| Eval viewer timing | ALWAYS generate the eval viewer BEFORE evaluating inputs yourself — get outputs in front of the user first. Add "Create evals JSON and run `eval-viewer/generate_review.py`" to TodoList. |
| Description optimization | Works — `run_loop.py` uses `claude -p` via subprocess. Run only after skill is finalized and user agrees it's in good shape. |
| Packaging | Works |

---

## Reference files

- `agents/grader.md` — Evaluate assertions against outputs
- `agents/comparator.md` — Blind A/B comparison between outputs
- `agents/analyzer.md` — Analyze why one version beat another
- `references/schemas.md` — JSON structures for evals.json, grading.json, benchmark.json, etc.

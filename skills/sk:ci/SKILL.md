---
name: sk:ci
description: "Set up Claude Code GitHub Actions or GitLab CI integration. Generates workflow files for PR review, issue triage, nightly audits, and release automation. Supports direct API, AWS Bedrock, and Google Vertex AI."
disable-model-invocation: true
argument-hint: "[github|gitlab] [--bedrock|--vertex]"
---

# /sk:ci

Set up Claude Code CI/CD integration: GitHub Actions or GitLab CI.

## Before You Start

1. Read `CLAUDE.md` to understand the project stack and repository type
2. Check if `.github/workflows/` or `.gitlab-ci.yml` already exists
3. Detect provider: `git remote -v` — github.com → GitHub Actions, gitlab.com → GitLab CI

## Step 1 — Choose Provider

**GitHub Actions** (default):
- Quick setup: Run `/install-github-app` in Claude Code terminal
- Manual setup: follow the instructions below

**GitLab CI**: generate `.gitlab-ci.yml` with inline Claude Code runner

If user doesn't specify, ask: "GitHub Actions or GitLab CI?"

## Step 2 — Choose Authentication

For GitHub Actions, ask:

> "Which API provider? (1) Anthropic direct API — simplest, (2) AWS Bedrock — enterprise/data residency, (3) Google Vertex AI — enterprise/GCP"

For option 1 (direct API), proceed to Step 3.
For options 2 or 3, follow the Enterprise Setup section below.

## Step 3 — Choose Workflows

Present a checklist. Ask the user which they want:

```
Which workflows do you want to set up? (select all that apply)

[1] @claude trigger — respond to @claude mentions in PR/issue comments
[2] Auto PR review — review every PR automatically on open/sync
[3] Issue triage — auto-label and respond to new issues
[4] Nightly audit — daily code quality / security / SEO review
[5] Release automation — auto-generate changelog on tag push
```

Generate only the selected workflows.

## GitHub Actions — Workflow Templates

### [1] @claude Trigger (responds to @claude mentions)

Create `.github/workflows/claude.yml`:

```yaml
name: Claude Code
on:
  issue_comment:
    types: [created]
  pull_request_review_comment:
    types: [created]
  issues:
    types: [opened, assigned]

permissions:
  contents: write
  pull-requests: write
  issues: write

jobs:
  claude:
    if: |
      (github.event_name == 'issue_comment' && contains(github.event.comment.body, '@claude')) ||
      (github.event_name == 'pull_request_review_comment' && contains(github.event.comment.body, '@claude')) ||
      (github.event_name == 'issues' && contains(github.event.issue.body, '@claude'))
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
```

### [2] Auto PR Review

Create `.github/workflows/claude-review.yml`:

```yaml
name: Claude PR Review
on:
  pull_request:
    types: [opened, synchronize]

permissions:
  contents: read
  pull-requests: write

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          prompt: |
            Review this pull request for:
            1. Correctness — logic errors, edge cases, off-by-one errors
            2. Security — OWASP Top 10, injection, auth issues
            3. Performance — N+1 queries, unnecessary allocations
            4. Test coverage — missing tests for new code paths

            Post findings as inline review comments on the diff.
            If the PR is clean, post a single approval comment.
          claude_args: "--max-turns 5"
```

### [3] Issue Triage

Create `.github/workflows/claude-triage.yml`:

```yaml
name: Claude Issue Triage
on:
  issues:
    types: [opened]

permissions:
  contents: read
  issues: write

jobs:
  triage:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          prompt: |
            Triage this new issue:
            1. Add appropriate labels (bug, enhancement, question, documentation)
            2. Ask for missing information (reproduction steps, OS, version)
            3. Check if a similar issue already exists — if so, link it
            4. Estimate complexity: trivial / small / medium / large

            Post a single helpful comment. Be concise.
          claude_args: "--max-turns 3"
```

### [4] Nightly Audit

Create `.github/workflows/claude-nightly.yml`:

```yaml
name: Claude Nightly Audit
on:
  schedule:
    - cron: "0 2 * * *"   # 2 AM UTC daily
  workflow_dispatch:        # allow manual trigger

permissions:
  contents: write
  issues: write
  pull-requests: write

jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          prompt: |
            Run a nightly audit of this repository:
            1. Security: Check for new vulnerabilities, outdated dependencies
            2. Code quality: Identify patterns that should be refactored
            3. Documentation gaps: Find public APIs or components with no docs
            4. Dead code: Identify unused exports, orphaned files

            If critical findings exist, create a GitHub issue titled
            "Nightly Audit [date] — N critical findings" with a full report.
            If clean, no action needed.
          claude_args: "--max-turns 10 --model claude-sonnet-4-6"
```

### [5] Release Automation

Create `.github/workflows/claude-release.yml`:

```yaml
name: Claude Release Notes
on:
  push:
    tags:
      - 'v*'

permissions:
  contents: write

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          prompt: |
            Generate release notes for this tag based on commits since the last tag.
            Group by: Features, Bug Fixes, Performance, Breaking Changes.
            Keep it concise — 3-5 bullet points per section maximum.
            Create a GitHub Release with these notes.
          claude_args: "--max-turns 5"
```

## Enterprise Setup — AWS Bedrock

For Bedrock, update each workflow's `steps` to add:

```yaml
# After actions/checkout, before claude-code-action:
- name: Configure AWS Credentials
  uses: aws-actions/configure-aws-credentials@v4
  with:
    role-to-assume: ${{ secrets.AWS_ROLE_TO_ASSUME }}
    aws-region: us-west-2

# In claude-code-action:
- uses: anthropics/claude-code-action@v1
  with:
    use_bedrock: "true"
    claude_args: "--model us.anthropic.claude-sonnet-4-6 --max-turns 10"
    # No anthropic_api_key needed — uses AWS credentials
```

**Required secrets:** `AWS_ROLE_TO_ASSUME`

**Required AWS setup:**
1. Configure GitHub OIDC identity provider in AWS IAM
2. Create IAM role with `AmazonBedrockFullAccess` that trusts GitHub Actions
3. Enable Claude model access in AWS Bedrock console

## Enterprise Setup — Google Vertex AI

```yaml
# After actions/checkout, before claude-code-action:
- name: Authenticate to Google Cloud
  id: auth
  uses: google-github-actions/auth@v2
  with:
    workload_identity_provider: ${{ secrets.GCP_WORKLOAD_IDENTITY_PROVIDER }}
    service_account: ${{ secrets.GCP_SERVICE_ACCOUNT }}

- uses: anthropics/claude-code-action@v1
  with:
    use_vertex: "true"
    claude_args: "--model claude-sonnet-4@20250514 --max-turns 10"
  env:
    ANTHROPIC_VERTEX_PROJECT_ID: ${{ steps.auth.outputs.project_id }}
    CLOUD_ML_REGION: us-east5
```

**Required secrets:** `GCP_WORKLOAD_IDENTITY_PROVIDER`, `GCP_SERVICE_ACCOUNT`

## Custom GitHub App (Optional)

For branded bot usernames or enterprise requirements:

1. Create GitHub App at https://github.com/settings/apps/new
   - Permissions: Contents (R+W), Issues (R+W), Pull Requests (R+W)
2. Generate a private key and save it
3. Add secrets: `APP_ID`, `APP_PRIVATE_KEY`
4. Add to workflow before `claude-code-action`:

```yaml
- name: Generate GitHub App token
  id: app-token
  uses: actions/create-github-app-token@v2
  with:
    app-id: ${{ secrets.APP_ID }}
    private-key: ${{ secrets.APP_PRIVATE_KEY }}

- uses: anthropics/claude-code-action@v1
  with:
    github_token: ${{ steps.app-token.outputs.token }}
    anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
```

## GitLab CI

Create `.gitlab-ci.yml` (or append to existing):

```yaml
claude-review:
  stage: review
  image: node:20-alpine
  only:
    - merge_requests
  script:
    - npm install -g @anthropic-ai/claude-code
    - git diff origin/$CI_MERGE_REQUEST_TARGET_BRANCH_NAME..HEAD > /tmp/diff.patch
    - claude --print --max-turns 5 \
        "Review this diff for security, correctness, and test coverage: $(cat /tmp/diff.patch). Post findings as a structured report."
  variables:
    ANTHROPIC_API_KEY: $ANTHROPIC_API_KEY
```

**Required:** Add `ANTHROPIC_API_KEY` to GitLab CI/CD Variables (Settings → CI/CD → Variables).

## After Setup

1. Commit the generated workflow files
2. Add `ANTHROPIC_API_KEY` to repository secrets (Settings → Secrets → Actions → New secret)
3. For quick setup, run `/install-github-app` in Claude Code to install the GitHub App automatically
4. Test by tagging `@claude` in a PR or issue comment

## Customizing Claude's Behavior

Claude reads `CLAUDE.md` in your repository root during CI runs. Add CI-specific rules there:

```markdown
## CI/CD Rules
- In PR reviews: focus on correctness and security — skip style comments
- In issue triage: always ask for reproduction steps for bug reports
- Maximum PR review length: 10 bullet points total
```

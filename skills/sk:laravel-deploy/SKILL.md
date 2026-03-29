---
name: sk:laravel-deploy
description: "Deploy a Laravel application to Laravel Cloud via the `cloud` CLI. Requires /sk:gates to pass before deploying."
---

# /sk:laravel-deploy

Deploy the current Laravel application to Laravel Cloud.

## Pre-Deploy Gate Check

**Gates must pass before any deploy.** If `/sk:gates` has not been run since the last code change, run it first:

```
/sk:gates
```

All quality checks (lint, tests, security, review) must be green before deploying to any environment.

## Setup (First Time)

Install the Laravel Cloud CLI if missing:
```bash
composer global require laravel/cloud-cli
```

Authenticate:
```bash
cloud auth -n
```

## CLI Rules

Never hardcode command signatures — always run `cloud <command> -h` to discover options at runtime.

| Operation | Flags |
|-----------|-------|
| Read | `--json -n` |
| Create | `--json -n` |
| Update | `--json -n --force` |
| Delete | `-n --force` (no `--json`) |
| Deploy | `-n` with all options explicitly |

## Deployment Workflow

### First Deploy
```bash
cloud ship -n
```

### Existing App
```bash
cloud repo:config
cloud deploy {app} {env} -n --open
cloud deploy:monitor -n
```

### Environment Variables
```bash
cloud environment:variables -n --force
```

### Infrastructure

**Database:**
```bash
cloud database-cluster:create --json -n
cloud database:create --json -n
```

**Cache:**
```bash
cloud cache:create --json -n
```

**Custom Domain:**
```bash
cloud domain:create --json -n
cloud domain:verify -n
```

## Sub-Agent Delegation

Delegate to background agents (non-blocking):
- `deploy:monitor` — watch deployment progress
- `deployment:get` — fetch deployment status
- `resource:list` — list infrastructure resources

Keep in main context:
- `cloud deploy` (need deployment ID immediately)
- Short status commands

## Troubleshooting

Inspect current infrastructure state:
```bash
cloud <resource>:list --json -n
```

Check deployment logs:
```bash
cloud deployment:get {id} --json -n
```

## Official Plugin

For richer guidance with checklists for complex multi-step infrastructure operations, install the official plugin:
```
/plugin install laravel-cloud@laravel
```

Docs: https://cloud.laravel.com/docs

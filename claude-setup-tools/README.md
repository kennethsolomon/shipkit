# claude-setup-tools 🛠️

**A comprehensive toolkit for creating, diagnosing, and optimizing CLAUDE.md files for Claude Code projects.**

Create perfect project documentation in seconds. No more manual setup or outdated project files.

## ⚙️ Installation & Availability

After cloning the repo and running the installation:

```bash
git clone git@github.com:kennethsolomon/claude-skills.git ~/.agents/skills
~/.agents/skills/scripts/link-claude-skills.sh
```

The three skills will be **automatically available** as `/` commands:
- ✅ `/setup-starter` — Create CLAUDE.md
- ✅ `/doctor-claude` — Diagnose issues
- ✅ `/optimize-claude` — Optimize and trim

**You can use them immediately** in any Claude Code session! The `link-claude-skills.sh` script automatically symlinks all skills (folders with `SKILL.md`) into `~/.claude/skills/`, making them discoverable.

---

## 🤔 What is CLAUDE.md?

Think of CLAUDE.md as a project "cheat sheet" for Claude Code. It tells Claude:
- **What you're building**: Project name and description
- **What tools you're using**: Language, framework, database, UI library
- **How to run it**: The exact commands to start, test, and build
- **Where things are**: Project structure and key files
- **What's special**: Important architectural decisions and setup requirements

**Example**: Instead of Claude guessing that your project uses React, Next.js, Prisma, and Jest, CLAUDE.md tells Claude directly. This means:
- ✅ Better code suggestions (uses patterns that match your stack)
- ✅ Faster responses (Claude understands your project instantly)
- ✅ Fewer mistakes (knows your exact build commands)
- ✅ Better onboarding (new team members know how to start)

---

## ⚡ Quick Start (30 seconds)

### I want to create CLAUDE.md for my project

```bash
/setup-starter
```

**What happens**:
1. Tool scans your project (checks package.json, Cargo.toml, etc.)
2. Auto-detects your tech stack (React? Django? Go?)
3. Generates a complete, optimized CLAUDE.md file
4. Shows you what was created

**Example output**:
```
✓ CLAUDE.md created: CLAUDE.md
  Lines: 94/150
  Sections: Stack, Quick Start, Project Structure, ...
✅ CLAUDE.md created successfully!
```

### I want to check if my CLAUDE.md is good

```bash
/doctor-claude
```

**What happens**:
1. Analyzes your existing CLAUDE.md
2. Checks for common issues (file too long, missing sections, outdated info)
3. Suggests specific improvements
4. Shows you a better version to review

**Example output**:
```
⚠️ Issues found:
   1. File is too long: 180 lines (target: < 150)
   2. Missing essential sections: Development

💡 Suggestions:
   1. Run `/optimize-claude` to trim unnecessary sections
   2. Add a 'Development' section with setup instructions
```

### My CLAUDE.md is too long, make it shorter

```bash
/optimize-claude
```

**What happens**:
1. Reads your CLAUDE.md
2. Removes redundancy and verbose descriptions
3. Keeps all important information
4. Makes file shorter and cleaner

**Example output**:
```
✨ CLAUDE.md optimized!
   Before: 180 lines
   After:  142 lines
   Saved:  38 lines
```

---

## 📚 Understanding the Three Skills

All skills are accessible with `/` commands in Claude Code.

## 🎯 The Three Skills Explained

### 1️⃣ `/setup-starter` - Create Your CLAUDE.md

**Use this when**: You're starting a new project or your project doesn't have a CLAUDE.md yet.

**What it does**:
- 🔍 **Scans your project** automatically (reads package.json, pyproject.toml, Cargo.toml, etc.)
- 🤖 **Auto-detects everything**: language, framework, database, testing setup
- 📄 **Generates CLAUDE.md** with all essential sections
- ✅ **Keeps it short** (optimized for ~100-150 lines)

**Example: What it detects**

For a Node.js project with React, Prisma, and Jest:
```
Language: JavaScript/TypeScript ✓
Framework: React ✓
Database: Prisma ✓
UI: (auto-detected from dependencies) ✓
Testing: Jest ✓
Dev command: npm run dev ✓
Build command: npm run build ✓
Test command: npm test ✓
```

**Result**: Generates a complete CLAUDE.md in seconds that would take 15+ minutes to write manually.

**Triggers**: `/setup-starter`, `/create-claude`, `/new-claude`

---

### 2️⃣ `/doctor-claude` - Check Your CLAUDE.md Health

**Use this when**: You already have a CLAUDE.md and want to verify it's good.

**What it does**:
- 📊 **Checks line count** (warns if > 150 lines)
- ✓ **Verifies essential sections** (Stack, Quick Start, Development, etc.)
- 🔍 **Detects issues**: outdated commands, unreplaced placeholders, missing info
- 💡 **Suggests improvements** with specific recommendations
- 📝 **Shows you a better version** to review and merge

**Issues it can find**:
```
⚠️  File is too long (180 lines, target: < 150)
⚠️  Missing sections: Development workflow
⚠️  File mentions npm but no package.json found
⚠️  Has unreplaced placeholders like [PROJECT]
```

**Example workflow**:
```
1. Run /doctor-claude
2. Read the suggestions (doesn't force changes)
3. Decide what to apply
4. Review the suggested version in .setup-claude.md
5. Update your CLAUDE.md manually with the good parts
```

**Triggers**: `/doctor-claude`, `/check-claude`, `/diagnose-claude`

---

### 3️⃣ `/optimize-claude` - Enrich & Maintain Your CLAUDE.md (ENHANCED)

**Use this when**: You want to discover and document your project structure, or maintain CLAUDE.md during development.

**What it does (NEW)**:
- 🔍 **Auto-discovers** actual project directories (src/, tests/, docs/, etc.)
- 📚 **Finds documentation** files and links them (README, CONTRIBUTING, docs/)
- 🔧 **Detects workflows** (Makefile targets, npm scripts, GitHub Actions)
- 🔄 **Safely re-runs** during development without losing your customizations
- 🔒 **Preserves edits** with smart detection of user customizations
- 📊 **Reports findings** so you know what was added

**Smart Features**:
- ✅ **Auto-discovers real structure** - No hardcoded templates, uses actual filesystem
- ✅ **Dual edit detection** - Compares content + looks for markers to detect user edits
- ✅ **Auto-locking** - "Important Context" section is auto-locked if it has content
- ✅ **Flexible line count** - Grows to ~200 lines if content is valuable
- ✅ **Safe to run multiple times** - Preserves all your customizations

**Example Usage**:
```bash
# After adding tests/ directory
mkdir tests
/optimize-claude
# CLAUDE.md now documents tests/ automatically!

# After adding docs
touch docs/DEPLOYMENT.md
/optimize-claude
# New doc is automatically linked!

# Edit Important Context
vim CLAUDE.md  # Add custom notes
/optimize-claude
# ✅ Your notes are preserved!
```

**Expected Output**:
```
🔍 Analyzing project structure...

📊 Analysis Complete:
   📁 Directories discovered: 5
   📚 Documentation files: 3
   🔧 Workflows found: 4

✅ Key Directories Found:
   - src/
   - tests/
   - docs/

📖 Documentation Found:
   - README.md
   - CONTRIBUTING.md
   - docs/API.md

✅ Preserved (user-edited):
   - Important Context

✨ CLAUDE.md enriched and saved!
   Before: 95 lines
   After: 145 lines
   Added: 50 lines (comprehensive context)
```

**Triggers**: `/optimize-claude`, `/optimize-setup`, `/enrich-claude`, `/maintain-claude`

---

## 📖 The Three Guides (Quick Reference)

### 1️⃣ `/explain-claude` - Learn CLAUDE.md Structure

**What it explains**:
- What each section of CLAUDE.md is for
- Why each section matters to Claude Code
- What should go in each section
- Common mistakes to avoid
- Best practices for keeping it current

**Read this to understand**:
- Why CLAUDE.md has 10 specific sections
- What information belongs where
- Why 150 lines is a good target
- How to keep CLAUDE.md up-to-date

---

### 2️⃣ `/implement-claude` - Step-by-Step Workflow

**A complete workflow for creating perfect CLAUDE.md**:

**Step 1** (30 sec): Run `/setup-starter` to generate initial file
**Step 2** (5 min): Review and customize with your project details
**Step 3** (10 sec): Run `/doctor-claude` to check for issues
**Step 4** (10 sec): Run `/optimize-claude` if file is too long
**Step 5** (10 sec): Final review and commit

**Total time**: ~6 minutes for a perfect CLAUDE.md

**Use this guide when**:
- Creating CLAUDE.md for the first time
- Updating an existing CLAUDE.md
- Unsure about the right workflow
- Want to do things in the right order

---

### 3️⃣ `/review-claude` - Quality Checklist

**A checklist to verify your CLAUDE.md is ready**:

**Quick checks** (5 min):
- [ ] File exists and is readable
- [ ] No syntax errors (valid Markdown)
- [ ] Line count under 150
- [ ] No unreplaced placeholders

**Content accuracy** (10 min):
- [ ] Project name matches your project
- [ ] Technology stack is correct
- [ ] All commands actually work
- [ ] No outdated information

**Structure validation** (5 min):
- [ ] All essential sections present
- [ ] Clear and specific instructions
- [ ] Real file paths (not placeholders)
- [ ] Documentation links verified

**Use this when**:
- Before committing CLAUDE.md to version control
- After updating your tech stack
- Before sharing project with team
- Monthly maintenance checks

## 📝 What Your CLAUDE.md Will Look Like

Here's an example of a generated CLAUDE.md (around 100-150 lines):

```markdown
# my-awesome-app

A beautiful web application for managing tasks and collaborating with your team.

## Stack

| Layer | Tech |
|-------|------|
| Language | JavaScript/TypeScript |
| Framework | React |
| Database | PostgreSQL (Prisma) |
| UI | Tailwind CSS |
| Testing | Jest |

## Quick Start

```bash
npm run dev
```

## Project Structure

```
my-awesome-app/
├── src/
│   ├── components/    # React components
│   ├── pages/         # Next.js pages
│   └── styles/        # Global styles
├── tests/             # Test suite
├── docs/              # Documentation
└── package.json       # Dependencies
```

## Key Files

- **src/components/** - Reusable React components
- **src/pages/** - Application pages
- **prisma/schema.prisma** - Database schema
- **package.json** - Dependencies and scripts

## Development

### Setup
```bash
npm install
npm run migrate  # Create database
```

### Run
```bash
npm run dev
```

### Test
```bash
npm test
```

### Lint
```bash
npm run lint
```

## Build & Deploy

- **Development**: `npm run dev`
- **Production**: `npm run build && npm start`
- **Tests**: `npm test`
- **Linting**: `npm run lint`

## Important Context

- Uses React with TypeScript for type safety
- Database: PostgreSQL with Prisma ORM
- Authentication: JWT tokens (see docs/auth.md)
- API: RESTful design with error handling

## Environment Variables

Create `.env.local` with:
```
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
API_KEY=your_api_key_here
NEXT_PUBLIC_API_URL=http://localhost:3000
```

## Common Tasks

### Add a new component
```bash
# Create in src/components/MyComponent.tsx
# Then import and use in pages
```

### Run migrations
```bash
npx prisma migrate dev
```

### Deploy to production
```bash
npm run build
npm start
```

<!-- Generated by /setup-claude-tools -->
```

**That's it!** Everything Claude needs to understand your project. 100-150 lines. No fluff.

---

## 🔄 Common Workflows

### Workflow 1: Starting a New Project

```bash
# Step 1: Create CLAUDE.md automatically
/setup-starter

# Step 2: Review what was created
# (Opens CLAUDE.md in your editor)

# Step 3: Customize with your project details
# Edit the file, keep the structure

# Step 4: Check for issues
/doctor-claude

# Step 5: Commit to git
git add CLAUDE.md
git commit -m "docs: add CLAUDE.md with project setup"
```

**Time**: ~6 minutes | **Effort**: Minimal ✅

---

### Workflow 2: Improving an Existing CLAUDE.md

```bash
# Step 1: Check current state
/doctor-claude

# Step 2: See what could be improved
# (Doctor shows issues and suggestions)

# Step 3: If file is too long
/optimize-claude

# Step 4: Review the suggestions
# (Check CLAUDE.md.setup-claude.md)

# Step 5: Apply good ideas to your file
# Manually update CLAUDE.md

# Step 6: Final verification
/doctor-claude

# Step 7: Commit improvements
git add CLAUDE.md
git commit -m "docs: improve CLAUDE.md with latest tech stack"
```

**Time**: ~5 minutes | **Effort**: Manual review

---

### Workflow 3: Keeping CLAUDE.md Updated

**Do this monthly or when tech stack changes**:

```bash
# Check if file still matches reality
/doctor-claude

# If file is too long
/optimize-claude

# Manually update outdated information
# (Change command versions, add new dependencies, etc.)

# Verify final result
/doctor-claude

# Commit updates
git add CLAUDE.md
git commit -m "docs: update CLAUDE.md with current stack"
```

---

## 🚀 What Gets Auto-Detected

### JavaScript/Node.js Projects

Detects from `package.json`:
- ✅ React, Vue, Angular, Svelte (frameworks)
- ✅ Next.js, Nuxt, Remix (meta-frameworks)
- ✅ Prisma, Drizzle, TypeORM, Sequelize, Mongoose (databases)
- ✅ Tailwind, styled-components, Sass (styling)
- ✅ Jest, Vitest, Mocha (testing)
- ✅ npm scripts (dev, build, test, lint commands)

### Python Projects

Detects from `pyproject.toml` or `setup.py`:
- ✅ Django, FastAPI, Flask, Starlette (frameworks)
- ✅ SQLAlchemy, Django ORM (databases)
- ✅ pytest (testing framework)
- ✅ Default commands (python -m, pytest, etc.)

### Go Projects

- ✅ Language: Go
- ✅ Commands: go run, go build, go test, golangci-lint

### Rust Projects

- ✅ Language: Rust
- ✅ Commands: cargo run, cargo build, cargo test

**Not detected?** No problem! Edit the generated CLAUDE.md manually. Just keep the structure.

---

## 🛡️ Safety Features (Don't Worry!)

### Your Custom Files Are Protected

If you already have a CLAUDE.md that YOU wrote:

```bash
/setup-starter    # Doesn't overwrite!
```

Instead:
1. ✅ Original file stays untouched
2. ✅ New suggestion saved as `CLAUDE.md.setup-claude.md`
3. ✅ You review and merge manually
4. ✅ You're always in control

### How It Works

- **Generated files** have a marker: `<!-- Generated by /setup-claude-tools -->`
- **Generated files** can be updated directly (safe!)
- **Custom files** (without marker) get suggestions in `.setup-claude.md`
- **You decide** which changes to apply

**Result**: Your work is never lost or overwritten. ✨

---

## ❓ FAQ

### Q: Can I customize the generated CLAUDE.md?

**A**: Absolutely! After generation, edit it like any other Markdown file:
- Change descriptions to match your project
- Add specific details about your setup
- Remove sections that don't apply
- Add custom sections if needed

If you edit a generated file, it keeps the marker and can still be regenerated later.

---

### Q: What if my project uses technologies not listed?

**A**: The tool detects common stacks. For others:
1. Run `/setup-starter` to get the basic structure
2. Edit the "Stack" section manually
3. Update commands that are specific to your tools
4. Everything else stays the same!

The structure is the important part, not the detection. You can customize completely.

---

### Q: How often should I run `/doctor-claude`?

**A**:
- **After big changes**: New framework, database, testing setup
- **Monthly**: Just to verify everything is still accurate
- **Before sharing**: With new team members or public repos
- **Before committing**: Before pushing to version control

Regular checks keep your documentation fresh and accurate.

---

### Q: Why is the target line count 150 lines?

**A**:
- **150 lines is scannable**: You can read it in 2-3 minutes
- **Good for Claude**: Provides essential info without noise
- **Fits context**: Doesn't take up valuable token space
- **Practical**: Enough for all critical information

You can go higher if needed—it's a guideline, not a law!

---

### Q: What if my CLAUDE.md gets out of date?

**A**:
1. Run `/doctor-claude` to find stale info
2. Manually update outdated commands/tech
3. Run `/doctor-claude` again to verify

Regular maintenance (monthly) prevents drift. Or just update when your tech stack changes.

---

### Q: Can I version control my CLAUDE.md?

**A**: Yes, please!
- ✅ Commit it to git like any other file
- ✅ Track changes over time
- ✅ Share with your team
- ✅ Update when dependencies change

CLAUDE.md should be part of your repository!

---

### Q: Do I need to worry about the `.setup-claude.md` file?

**A**: Nope!
- It's just a temporary suggestion file
- Review it, take what you want
- Delete it after you're done merging
- It won't be generated again unless needed

## Core Features

### 1. Auto-Detection

Automatically discovers your project's technology stack:

```bash
$ /setup-starter
✓ CLAUDE.md created: CLAUDE.md
  Lines: 94/150
  Sections: Stack, Quick Start, Project Structure, Key Files, Development, ...
```

**Detected automatically:**
- Language from build config files
- Framework from dependencies
- Database ORM from package management
- Testing framework from imports
- Build/test/lint commands from package.json scripts

### 2. Optimization

Keeps files under 150 lines for efficiency:

```bash
$ /optimize-claude
✨ CLAUDE.md optimized!
   Before: 180 lines
   After:  142 lines
   Saved:  38 lines
```

**Optimization strategies:**
- Remove redundant descriptions
- Collapse verbose sections
- Consolidate related information
- Preserve all essential content

### 3. Diagnosis

Finds issues and suggests improvements:

```bash
$ /doctor-claude
⚠️  Issues found:
   1. File is too long: 180 lines (target: < 150)
   2. Missing essential sections: Development

💡 Suggestions:
   1. Run `/optimize-claude` to trim unnecessary sections
   2. Add a 'Development' section with setup instructions
```

### 4. Comprehensive Documentation

Three guides explain everything:
- **explain-claude**: Detailed guide to each section and why it matters
- **implement-claude**: Step-by-step workflow (5 steps, ~6 minutes)
- **review-claude**: Quality checklist before finalizing

## Typical Workflow

### For New Projects

```bash
1. /setup-starter          # Generate initial CLAUDE.md
2. [Edit file manually]    # Customize with project details
3. /doctor-claude          # Check for issues
4. /optimize-claude        # Trim if needed
5. [Commit to repo]        # Save to version control
```

**Timeline**: ~6 minutes

### For Existing Projects

```bash
1. /doctor-claude          # Assess current state
2. /optimize-claude        # Trim if too long
3. [Review suggestions]    # Check CLAUDE.md.setup-claude.md
4. [Manual merge]          # Integrate good ideas
5. [Commit updates]        # Save improvements
```

**Timeline**: ~5 minutes

## Generated CLAUDE.md Structure

Each generated file includes:

```markdown
# [Project Name]
[Description]

## Stack
| Layer | Tech |
| Language | ... |
| Framework | ... |
...

## Quick Start
```bash
[working command]
```

## Project Structure
...

## Key Files
...

## Development
### Setup
...

### Run
...

### Test
...

### Lint
...

## Build & Deploy
...

## Important Context
...

## Environment Variables
...

## Common Tasks
...

## Documentation
...

<!-- Generated by /setup-claude-tools -->
```

**Total**: ~140 lines (optimized)

## Key Patterns Leveraged

This toolkit follows patterns established by `setup-claude`:

1. **Marker-based Updates**: Safe regeneration without overwriting custom work
2. **Sidecar Files**: `.setup-claude.md` suggestions when custom files exist
3. **Template-driven**: Consistent output with variable substitution
4. **Detection Logic**: Infer project structure from configuration files
5. **Idempotency**: Safe to run multiple times

## File Structure

```
claude-setup-tools/
├── README.md                          # This file
├── skills/
│   ├── starter-setup/
│   │   └── SKILL.md                   # Create new CLAUDE.md
│   ├── claude-doctor/
│   │   └── SKILL.md                   # Diagnose issues
│   └── setup-optimizer/
│       └── SKILL.md                   # Optimize file
├── commands/
│   ├── explain.md                     # Guide to CLAUDE.md sections
│   ├── implement.md                   # Step-by-step workflow
│   └── review.md                      # Quality checklist
├── lib/
│   ├── __init__.py                    # Library exports
│   ├── detect.py                      # Auto-detection logic
│   └── sidecar.py                     # File handling & markers
├── templates/
│   └── CLAUDE.md.template             # Optimized template
└── scripts/
    ├── create_claude.py               # Create skill implementation
    ├── doctor_claude.py               # Doctor skill implementation
    └── optimize_claude.py             # Optimizer skill implementation
```

## Library Components

### detect.py

Auto-detection module for project configuration:

```python
from lib.detect import detect_project, ProjectConfig

config = detect_project(Path.cwd())
# Returns: ProjectConfig with language, framework, database, etc.
```

**Supports:**
- Node.js/JavaScript/TypeScript
- Python (FastAPI, Django, Flask)
- Go
- Rust

### sidecar.py

File handling and marker detection:

```python
from lib.sidecar import (
    has_marker,        # Check if file was generated
    is_custom_file,    # Check if file is user-created
    get_target_file,   # Determine write location
    add_marker,        # Add generation marker
    format_output,     # User-friendly messages
)
```

## Testing

### Test Scenarios

1. **New Project**: Create CLAUDE.md from scratch
2. **Existing Project**: Suggest improvements via sidecar
3. **Generated File**: Update directly via marker
4. **Custom File**: Protect and suggest alternatives
5. **Optimization**: Trim to < 150 lines

### Running Tests

```bash
# Check detection on current project
python3 scripts/create_claude.py

# Run doctor on CLAUDE.md
python3 scripts/doctor_claude.py

# Optimize existing file
python3 scripts/optimize_claude.py
```

## Integration

### With setup-claude

Both `setup-claude` and `claude-setup-tools` work independently:

```bash
/setup-claude              # Create project scaffolding
/setup-starter             # Create CLAUDE.md
```

Both are discoverable and can be used in any order.

### With Claude Code

The generated CLAUDE.md is automatically used by Claude Code to:
- Understand your project context
- Suggest appropriate patterns and solutions
- Provide language-specific recommendations
- Know your build and test commands

## Best Practices

### Keep CLAUDE.md Current

Update when:
- Adding/removing major dependencies
- Changing project structure
- Updating build process
- Changing deployment strategy

### Run Regular Checks

```bash
# Monthly or when making structural changes
/doctor-claude

# Before committing major changes
/review-claude
```

### Document Important Decisions

Add to "Important Context" section:
- Why you chose certain technologies
- Architectural decisions
- Known limitations or constraints
- Performance considerations

## Troubleshooting

### Issue: CLAUDE.md is custom (no marker)

**Why**: File exists without our generation marker.

**Solution**: Commands write to `.setup-claude.md` instead.

**Action**: Review the suggestion and manually merge good ideas.

### Issue: Commands not detected correctly

**Why**: Your project may use non-standard configuration.

**Solution**: Edit CLAUDE.md manually after generation.

**Action**: Update command sections with correct values.

### Issue: File keeps growing

**Why**: You're adding more sections and details.

**Solution**: Run `/optimize-claude` to trim.

**Action**: Be selective about what's essential vs. nice-to-have.

## 🔧 Troubleshooting

### Issue: "I ran `/setup-starter` but it created a `.setup-claude.md` file instead of updating CLAUDE.md"

**Why?** Your existing CLAUDE.md doesn't have the generation marker.

**Solution**:
1. Review the suggestion in `CLAUDE.md.setup-claude.md`
2. Copy the good ideas into your `CLAUDE.md`
3. Delete `CLAUDE.md.setup-claude.md` when done

**Next time**: Once you manually merge everything, your new file will be recognized in the future.

---

### Issue: "/doctor-claude says my CLAUDE.md mentions npm but no package.json found"

**Why?** The tool is running from a directory that doesn't have package.json.

**Solution**:
- Run the commands from your project root directory (where package.json is)
- Or ignore the warning if you're in a monorepo or special setup

**Example**:
```bash
cd my-project      # Go to project root
/doctor-claude     # Now it finds package.json
```

---

### Issue: "The generated CLAUDE.md doesn't have the exact tech I use"

**Why?** The tool detects common stacks. Your stack might be uncommon.

**Solution**:
1. Run `/setup-starter` to get the structure
2. Edit the "Stack" section to your actual tech
3. Update the commands to match your setup
4. Everything else can stay the same!

The structure matters more than perfect detection. You're in full control.

---

### Issue: "I want to regenerate CLAUDE.md from scratch"

**Solution**:
```bash
# Save your current file as backup (just in case)
cp CLAUDE.md CLAUDE.md.backup

# Delete the original
rm CLAUDE.md

# Generate fresh
/setup-starter
```

The new file will be auto-detected fresh from your project.

---

### Issue: "My team has a custom CLAUDE.md and doesn't want auto-detection"

**Solution**:
- Don't add the generation marker `<!-- Generated by /setup-claude-tools -->`
- The tools will never overwrite it
- The tools will create `.setup-claude.md` suggestions instead
- Your team can review and manually apply changes

**Result**: Full control! The file stays 100% yours.

---

## 💡 Pro Tips

### Tip 1: Add CLAUDE.md to Your Project Template

If you create a template or starter project:
1. Run `/setup-starter` to generate CLAUDE.md
2. Customize it for your typical stack
3. Add it to your template
4. New projects start with solid documentation!

---

### Tip 2: Use CLAUDE.md for Better Claude Responses

Make Claude even smarter by referencing CLAUDE.md:

**Bad**: "Fix the bug in my app"
**Better**: "Fix the bug in my app (see CLAUDE.md for stack info)"

Claude will read CLAUDE.md and understand your exact setup.

---

### Tip 3: Share CLAUDE.md with Your Team

When onboarding new developers:
1. Point them to CLAUDE.md
2. They learn your stack in 2 minutes
3. They know exact commands to run
4. They understand project structure
5. Fewer "How do I...?" questions!

---

### Tip 4: Update CLAUDE.md When You Update Dependencies

Make it a habit:
- Updated to React 18? Update CLAUDE.md
- Switched to PostgreSQL? Update CLAUDE.md
- Added TypeScript? Update CLAUDE.md
- Then run `/doctor-claude` to verify

Keep it fresh = accurate documentation!

---

## 📊 Understanding the Generated Structure

Here's what each section of CLAUDE.md does:

| Section | Purpose | Contains |
|---------|---------|----------|
| **Header** | Project identity | Name, 1-line description |
| **Stack** | Technology overview | Language, framework, database, UI, testing |
| **Quick Start** | Get running fast | Single command: npm run dev (or equivalent) |
| **Project Structure** | File organization | Directory layout with comments |
| **Key Files** | Important files | What each directory/file does |
| **Development** | How to work locally | Setup, run, test, lint commands |
| **Build & Deploy** | Production process | Build and deployment commands |
| **Important Context** | Key decisions | Why you chose what you chose |
| **Environment Variables** | Config needed | What .env values are required |
| **Documentation** | Reference links | Links to detailed docs |

---

## 🎓 Learning Path

### For First-Time Users

1. **Read this README** (you're doing it! ✓)
2. **Run `/setup-starter`** in your project
3. **Review the generated file**
4. **Run `/doctor-claude`** to verify it's good
5. **Done!** You now have perfect documentation

### For Advanced Users

1. **Read `/explain-claude`** to understand sections deeply
2. **Read `/implement-claude`** for optimal workflows
3. **Read `/review-claude`** for quality checkpoints
4. **Customize CLAUDE.md** for your unique needs
5. **Integrate into your process** (commit, track, maintain)

---

## 🌍 Supported Project Types

### Definitely Supported ✅

- **Node.js/JavaScript** projects (npm, yarn)
- **Python** projects (FastAPI, Django, Flask)
- **Go** projects
- **Rust** projects (Cargo)
- **TypeScript** projects
- **React** projects (CRA, Next.js, Remix)
- **Monorepos** (run in sub-project root)

### Partially Supported (manual editing needed) ⚠️

- **Custom stacks** (Python + Go mixed, etc.)
- **Uncommon frameworks** (detection may be basic)
- **Containerized projects** (Docker setup recommended)

### Workaround

For any project type:
1. Run `/setup-starter` to get structure
2. Edit manually to match your stack
3. The tool provides the template, you customize!

---

## 🔗 How CLAUDE.md Integrates with Claude Code

When you have a good CLAUDE.md:

```
Your Project + CLAUDE.md
        ↓
Claude Code reads CLAUDE.md
        ↓
Claude understands:
  - Your exact tech stack
  - How to build/test your code
  - Your project structure
  - Important conventions
        ↓
Claude gives better suggestions:
  ✅ Uses patterns from your stack
  ✅ Writes code in your style
  ✅ Knows your build process
  ✅ Understands your structure
```

**Result**: Claude works like it already knows your project! 🚀

---

## ❓ FAQ

### Q: Can I customize the generated CLAUDE.md?

**A**: Absolutely! After generation, edit it like any other Markdown file:
- Change descriptions to match your project
- Add specific details about your setup
- Remove sections that don't apply
- Add custom sections if needed

If you edit a generated file, it keeps the marker and can still be regenerated later.

---

### Q: What if my project uses technologies not listed?

**A**: The tool detects common stacks. For others:
1. Run `/setup-starter` to get the basic structure
2. Edit the "Stack" section manually
3. Update commands that are specific to your tools
4. Everything else stays the same!

The structure is the important part, not the detection. You can customize completely.

---

### Q: How often should I run `/doctor-claude`?

**A**:
- **After big changes**: New framework, database, testing setup
- **Monthly**: Just to verify everything is still accurate
- **Before sharing**: With new team members or public repos
- **Before committing**: Before pushing to version control

Regular checks keep your documentation fresh and accurate.

---

### Q: Why is the target line count 150 lines?

**A**:
- **150 lines is scannable**: You can read it in 2-3 minutes
- **Good for Claude**: Provides essential info without noise
- **Fits context**: Doesn't take up valuable token space
- **Practical**: Enough for all critical information

You can go higher if needed—it's a guideline, not a law!

---

### Q: What if my CLAUDE.md gets out of date?

**A**:
1. Run `/doctor-claude` to find stale info
2. Manually update outdated commands/tech
3. Run `/doctor-claude` again to verify

Regular maintenance (monthly) prevents drift. Or just update when your tech stack changes.

---

### Q: Can I version control my CLAUDE.md?

**A**: Yes, please!
- ✅ Commit it to git like any other file
- ✅ Track changes over time
- ✅ Share with your team
- ✅ Update when dependencies change

CLAUDE.md should be part of your repository!

---

### Q: Do I need to worry about the `.setup-claude.md` file?

**A**: Nope!
- It's just a temporary suggestion file
- Review it, take what you want
- Delete it after you're done merging
- It won't be generated again unless needed

---

## 📚 Quick Reference Card

**Save this and share with your friends!**

```
CLAUDE.md Toolkit - Quick Reference

CREATE:        /setup-starter
DIAGNOSE:      /doctor-claude
OPTIMIZE:      /optimize-claude

LEARN:         /explain-claude
WORKFLOW:      /implement-claude
CHECKLIST:     /review-claude

TARGET: < 150 lines
ESSENTIALS: Stack, Quick Start, Development
TIME: ~6 min per project
RESULT: Perfect Claude context!
```

---

## 🎯 About This Toolkit

### What This Is

- ✅ A tool to create and maintain CLAUDE.md files
- ✅ Auto-detection for common project stacks
- ✅ Safety features to protect your customizations
- ✅ Guides and checklists for best practices
- ✅ A time-saver (saves 15+ minutes per project)

### What This Is NOT

- ❌ A replacement for good code documentation
- ❌ A substitute for README.md
- ❌ Project scaffolding (see `/setup-claude` for that)
- ❌ A format enforcer (you can customize everything)

### Philosophy

**Simple principle**: *Small, focused documentation that's actually useful.*

Not 500-line guides. Not autogenerated API docs. Just the essentials that Claude needs to help you better.

---

## 🚀 Ready to Get Started?

### Your Next Steps

1. **Navigate to your project**:
   ```bash
   cd your-project
   ```

2. **Create CLAUDE.md**:
   ```bash
   /setup-starter
   ```

3. **Review the result** (opens in your editor)

4. **Check for issues**:
   ```bash
   /doctor-claude
   ```

5. **Commit to git**:
   ```bash
   git add CLAUDE.md
   git commit -m "docs: add CLAUDE.md"
   ```

That's it! You now have professional project documentation in under 10 minutes.

---

## 📞 Need Help?

- **Learning**: Read `/explain-claude`
- **Workflow**: Follow `/implement-claude`
- **Quality**: Use `/review-claude`
- **Issues**: Check troubleshooting above
- **Questions**: Ask about specific sections in the guides

---

## 🎁 Share This With Your Friends

Use this README to introduce colleagues to the toolkit:

> "We can now create perfect project documentation in seconds. Check this out..."
>
> Run `/setup-starter` in any project and let it auto-detect your entire tech stack.

Share the quick reference card above! ☝️

---

**Made with ❤️ for Claude Code projects**

Last updated: March 2026
Version: 1.0

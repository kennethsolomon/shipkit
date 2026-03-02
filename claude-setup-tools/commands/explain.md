# Understanding CLAUDE.md

This guide explains each section of CLAUDE.md and why it matters for working with Claude Code.

## What is CLAUDE.md?

CLAUDE.md is a configuration file for Claude Code that provides context about your project. It helps Claude understand:
- Your project structure and conventions
- How to run, test, and deploy your code
- What tools and technologies you're using
- Important workflows and patterns

## CLAUDE.md Structure

### 1. **Project Header**
```markdown
# [PROJECT_NAME]
[DESCRIPTION]
```
- Clear name and one-line description
- Helps Claude quickly understand the project
- Used in prompts and context

**Why it matters**: Claude uses this to provide relevant suggestions

### 2. **Stack Table**
```markdown
## Stack

| Layer | Tech |
|-------|------|
| Language | JavaScript |
| Framework | React |
| Database | PostgreSQL |
| UI | Tailwind CSS |
| Testing | Jest |
```
- Lists the key technologies used
- Organized by layer (language, framework, database, etc.)
- Quick reference for Claude to understand capabilities

**Why it matters**: Claude suggests patterns and libraries that match your stack

### 3. **Quick Start**
```markdown
## Quick Start

\`\`\`bash
npm run dev
\`\`\`
```
- Single command to get the project running
- New contributors or Claude can start immediately
- Assumes dependencies are installed

**Why it matters**: Claude can suggest how to test and verify changes

### 4. **Project Structure**
```markdown
## Project Structure

\`\`\`
src/          # Source code
tests/        # Tests
docs/         # Documentation
\`\`\`
```
- Directory layout and organization
- What each folder contains
- Helps Claude navigate the codebase

**Why it matters**: Claude suggests files in the right locations

### 5. **Key Files**
```markdown
## Key Files

- **src/** - Application code
- **tests/** - Test suite
- **.env.example** - Environment template
```
- Important files and their purposes
- Conventions for project organization
- Quick reference for documentation

**Why it matters**: Claude can find relevant files faster

### 6. **Development Commands**
```markdown
## Development

### Setup
\`\`\`bash
npm install
\`\`\`

### Run
\`\`\`bash
npm run dev
\`\`\`

### Test
\`\`\`bash
npm test
\`\`\`

### Lint
\`\`\`bash
npm run lint
\`\`\`
```
- Complete workflow for development
- How to set up, run, test, and lint
- Build and production commands

**Why it matters**: Claude includes these commands in suggestions

### 7. **Important Context**
```markdown
## Important Context

- Uses TypeScript with React
- Database: PostgreSQL with Prisma ORM
- Testing framework: Jest with React Testing Library
- Build tool: Next.js with TypeScript
```
- Key architectural decisions
- Important constraints or conventions
- Patterns Claude should follow

**Why it matters**: Claude considers these constraints in suggestions

### 8. **Environment Variables**
```markdown
## Environment Variables

Create a \`.env\` file based on \`.env.example\` with:
- DATABASE_URL: PostgreSQL connection string
- API_KEY: External service key
```
- What environment variables are needed
- How to obtain them
- Example values

**Why it matters**: Claude suggests proper configuration

### 9. **Common Tasks**
```markdown
## Common Tasks

### Add a dependency
\`\`\`bash
npm install package-name
\`\`\`

### Run tests
\`\`\`bash
npm test
\`\`\`
```
- Frequent operations and commands
- How to accomplish common goals
- Reference for Claude

**Why it matters**: Claude uses these as templates for similar tasks

### 10. **Documentation Links**
```markdown
## Documentation

- **Architecture**: See docs/architecture.md
- **API**: See docs/api.md
- **Contributing**: See CONTRIBUTING.md
```
- Links to deeper documentation
- Where to find detailed information
- Guides for specific areas

**Why it matters**: Claude knows where to point users for details

## Best Practices

### Keep It Concise
- Target 100-150 lines
- One idea per section
- Remove redundancy
- Use tables and lists

### Be Specific
- Actual command examples, not generic placeholders
- Real file names and paths
- Specific technology names
- Link to actual documentation

### Stay Current
- Update when tech stack changes
- Verify commands still work
- Remove outdated information
- Fix broken documentation links

### Prioritize Essential Information
- Your exact tech stack
- How to run the project
- Important conventions
- Critical setup steps

## Examples

### Minimal CLAUDE.md (50 lines)
Perfect for small projects:
- Project name and description
- Stack table
- Quick start command
- Key files
- Build commands

### Comprehensive CLAUDE.md (150 lines)
For medium/complex projects:
- All sections above
- Plus: Environment setup, common tasks
- Deployment instructions
- Architecture notes
- Contributing guidelines

## Common Mistakes to Avoid

1. **Generic placeholders**: Replace [PROJECT] with actual values
2. **Outdated commands**: Verify all commands work
3. **Missing stack info**: Include all major technologies
4. **Unclear instructions**: Be specific and complete
5. **Too verbose**: Remove unnecessary details

## Maintenance Tips

- Review CLAUDE.md when onboarding new people
- Update when project structure changes
- Run `/doctor-claude` to check for issues
- Run `/optimize-claude` if file grows too large
- Keep a CLAUDE.md template for new projects

---

Use `/setup-starter` to auto-generate CLAUDE.md, or `/doctor-claude` to improve an existing one.

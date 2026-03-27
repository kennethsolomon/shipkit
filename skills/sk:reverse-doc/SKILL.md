---
name: sk:reverse-doc
description: Generate architecture and design documentation from existing code by analyzing patterns and asking clarifying questions
allowed_tools: Read, Glob, Grep, Write, Agent
---

# Reverse Document

Generate documentation from existing code — work backwards from implementation to create missing design or architecture docs.

## When to Use

- Onboarding to an existing codebase that lacks documentation
- Formalizing a prototype into a documented design
- Capturing the "why" behind existing code before refactoring
- Creating architecture docs for a codebase you inherited

## Arguments

```
/sk:reverse-doc <type> <path>
```

| Type | Output | Location |
|------|--------|----------|
| `architecture` | Architecture Decision Record | `docs/architecture/` |
| `design` | Design document (GDD-style) | `docs/design/` |
| `api` | API specification | `docs/api/` |

If no type specified, infer from the path:
- `src/core/`, `src/lib/`, `app/Services/` → architecture
- `src/components/`, `resources/views/` → design
- `routes/`, `app/Http/Controllers/` → api

## Steps

### Phase 1: Analyze

Launch Explore agents to analyze the target path:

1. **Structure agent**: Map the file tree, identify entry points, trace dependency chains
2. **Patterns agent**: Identify design patterns, abstractions, conventions used
3. **Data flow agent**: Trace data through the system — inputs, transformations, outputs

Synthesize findings into:
- **What it does** (mechanics, behavior)
- **How it's built** (patterns, architecture, dependencies)
- **What's unclear** (inconsistencies, undocumented decisions)

### Phase 2: Clarify

Ask the user 3-5 clarifying questions to distinguish intentional design from accidental implementation:

- "Is [pattern X] intentional, or would you change it in a refactor?"
- "What was the motivation for [architectural decision Y]?"
- "Are [components A and B] coupled by design, or is that tech debt?"

**Critical principle: Never assume intent. Always ask before documenting "why."**

The distinction between "what the code does" and "what the developer intended" is the entire value of this skill. Do not skip this phase.

### Phase 3: Draft

Based on analysis + user answers, generate the document:

**Architecture docs include:**
- System overview and purpose
- Component diagram (text-based)
- Data flow description
- Key design decisions with rationale (from user answers)
- Dependencies and interfaces
- Trade-offs and known limitations

**Design docs include:**
- Feature overview and user-facing behavior
- Component breakdown
- State management approach
- Interaction patterns
- Edge cases and error handling

**API docs include:**
- Endpoint inventory
- Request/response schemas
- Authentication requirements
- Error codes and formats
- Rate limits and constraints

### Phase 4: Approve

Present the draft to the user:
- Show key sections
- Highlight areas marked as "inferred" (not confirmed by user)
- Ask for corrections or additions

**Do not write the file until the user approves.**

### Phase 5: Write

Save the approved document to the appropriate location.

Flag follow-up work:
- Related areas that also need documentation
- Inconsistencies discovered during analysis
- Suggested refactoring based on documented architecture

**Do not auto-execute follow-up work.** Present it as a list for the user to decide.

## Model Routing

| Profile | Model |
|---------|-------|
| `full-sail` | opus (inherit) |
| `quality` | opus (inherit) |
| `balanced` | sonnet |
| `budget` | sonnet |

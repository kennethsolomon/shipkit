---
name: sk:explain
description: "Explain any code — file, function, module, or concept — with a structured format: one-sentence summary, mental model, visual diagram, key details, and modification guide. Use when the user asks to explain, understand, or break down code."
argument-hint: "[file, function, or concept]"
---

# Explain Code

Explain the target using this exact 5-section format. Scale depth to complexity — a 10-line utility gets a compact answer, a core module gets the full treatment.

## Determine Target

Parse the argument:
- **File path** → Read the file
- **Function/class name** → Grep to locate, then read the surrounding context
- **Concept** ("how does auth work here") → Explore relevant files with Grep/Glob, read the key ones
- **No argument** → Ask what to explain

## Format

### 1. One-sentence summary
What does it do and why does it exist? One sentence.

### 2. Mental model
The simplest analogy or abstraction that makes it click. Frame it as "Think of it like..." or "This is basically a..." — something a senior dev would use to onboard someone.

### 3. Visual diagram
ASCII diagram showing the key relationships. Pick the right type:

- **Data flow**: `Input → Process → Output`
- **Architecture**: boxes and arrows showing component relationships
- **Sequence**: numbered steps for request/response flows
- **Tree**: for hierarchies or decision trees

```
┌─────────┐    request    ┌──────────┐    query    ┌────────┐
│  Client  │─────────────▶│  Handler │────────────▶│   DB   │
└─────────┘               └──────────┘             └────────┘
                               │
                               ▼ validate
                          ┌──────────┐
                          │  Schema  │
                          └──────────┘
```

Keep it focused — show the part that matters, not every box in the system.

### 4. Key details
The non-obvious things someone reading this code would miss or misunderstand:
- Edge cases handled (or not handled)
- Performance characteristics
- Important dependencies or coupling
- Configuration that changes behavior
- Error paths

Use bullet points. No filler — only things that would surprise or save someone time.

### 5. How to modify it
What would someone need to know to safely change this code?
- Where are the entry points?
- What invariants must be preserved?
- What would break if changed carelessly?
- Are there tests covering this? Where?

### 6. Suggested questions
4-5 questions this analysis is uniquely positioned to answer — things the code surfaces that aren't obvious from reading it linearly. Frame each as a question worth investigating.

## Intensity

Read `.shipkit/config.json` for intensity settings. Resolution: `intensity_overrides["sk:explain"]` → global `intensity` → `full`.

| Level | Explain behavior |
|-------|-----------------|
| **lite** | Section 1 (one-sentence summary) + Section 4 (key details) only. Skip diagram, modification guide, and suggested questions. |
| **full** | All 6 sections. Scale depth to complexity. Default. |
| **deep** | All 6 sections with expanded detail. Include alternative approaches, historical context, and cross-references to related code. |

## Rules

- Read the actual code before explaining — never guess from file names
- Match depth to complexity — don't write 5 paragraphs about a one-liner
- Use the project's actual names, not generic placeholders
- If the code is confusing or poorly written, say so (tactfully)
- Skip sections that don't apply (a pure function doesn't need an architecture diagram)

---
paths:
  - "**/*.tsx"
  - "**/*.jsx"
  - "src/**/*.ts"
  - "resources/js/**"
---

# React / TypeScript Rules

- Function components + hooks only — no class components
- Always type props with interfaces, not inline object literals
- Local state: `useState`; shared state: Zustand/Jotai; server state: React Query/SWR
- Never mutate state directly — always return new objects/arrays
- `useEffect` dependencies: list all of them — no empty `[]` unless truly mount-only
- Event handler naming: `handleClick`, `handleSubmit`, `handleChange`
- Async in effects: create inner async function, never make the effect itself async
- List keys: use stable IDs — never array index
- `React.memo` only when profiling confirms unnecessary re-renders — not preemptively
- Imports: absolute paths for anything more than 1 level up from current file
- No inline styles — use the project's established pattern (Tailwind, CSS modules, etc.)
- Forms with validation: React Hook Form
- Never store derived state — compute it in render or `useMemo`

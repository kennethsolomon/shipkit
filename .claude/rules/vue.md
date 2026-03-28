---
paths:
  - "**/*.vue"
  - "resources/js/**/*.ts"
---

# Vue 3 / Composition API Rules

- Composition API only — no Options API in new code
- Prefer `<script setup>` syntax for SFCs
- `defineProps` with TypeScript types — always validate prop types
- Always declare emits with typed `defineEmits` interface
- Composables: prefix with `use` (`useAuth`, `useCart`) — one concern per composable
- `ref` for primitives, `reactive` for objects — be consistent within a file
- `computed`: no side effects — read-only getters only
- Prefer `watchEffect` when dependencies are obvious from usage; use `watch` for explicit control
- All `v-for` must have `:key` — stable IDs, never array index
- No logic in templates beyond simple ternaries — extract complex conditions to computed
- Pinia stores: one store per domain; actions for mutations, getters for derived state
- `nextTick`: use sparingly — frequent use usually indicates a design issue

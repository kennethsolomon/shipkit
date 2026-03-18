# Nuxt + Tailwind — Stack Reference

## Scaffold

```bash
npx nuxi@latest init {project-name}
cd {project-name}
npm install
npx nuxi module add @nuxtjs/tailwindcss
npx nuxi module add @nuxtjs/google-fonts
```

## Directory Structure

```
{project-name}/
├── pages/
│   ├── index.vue               ← landing page
│   ├── dashboard.vue           ← dashboard
│   ├── {feature-1}.vue
│   ├── {feature-2}.vue
│   └── settings.vue
├── components/
│   ├── landing/
│   │   ├── Navbar.vue
│   │   ├── Hero.vue
│   │   ├── Features.vue
│   │   ├── HowItWorks.vue
│   │   ├── Pricing.vue
│   │   ├── Testimonials.vue
│   │   ├── WaitlistForm.vue
│   │   └── Footer.vue
│   ├── app/
│   │   ├── Sidebar.vue
│   │   ├── DashboardCards.vue
│   │   └── {feature components}
│   └── ui/
│       ├── UButton.vue
│       ├── UInput.vue
│       ├── UCard.vue
│       ├── UModal.vue
│       └── UToast.vue
├── layouts/
│   ├── default.vue             ← app layout (sidebar + header)
│   └── landing.vue             ← landing page layout (no sidebar)
├── server/
│   └── api/
│       └── waitlist.post.ts    ← waitlist API handler
├── public/
│   └── {static assets}
├── waitlist.json               ← email storage (auto-created by API)
├── tailwind.config.ts
├── nuxt.config.ts
└── package.json
```

## Nuxt Config

`nuxt.config.ts`:

```ts
export default defineNuxtConfig({
  modules: [
    '@nuxtjs/tailwindcss',
    '@nuxtjs/google-fonts',
  ],
  googleFonts: {
    families: {
      '{DisplayFont}': [400, 600, 700, 800],
      '{BodyFont}': [400, 500, 600],
    },
  },
  app: {
    head: {
      title: '{Product Name}',
      meta: [
        { name: 'description', content: '{product description}' },
      ],
    },
  },
})
```

## Tailwind Config

`tailwind.config.ts`:

```ts
export default {
  theme: {
    extend: {
      colors: {
        bg: 'var(--color-bg)',
        fg: 'var(--color-fg)',
        accent: 'var(--color-accent)',
        muted: 'var(--color-muted)',
      },
      fontFamily: {
        display: ['{DisplayFont}', 'serif'],
        body: ['{BodyFont}', 'sans-serif'],
      },
    },
  },
}
```

CSS variables in `assets/css/main.css` (referenced in nuxt.config):

```css
:root {
  --color-bg: #xxxxxx;
  --color-fg: #xxxxxx;
  --color-accent: #xxxxxx;
  --color-muted: #xxxxxx;
}

body {
  font-family: '{BodyFont}', sans-serif;
}
```

## Layouts

### Landing Layout (`layouts/landing.vue`)

```vue
<template>
  <div class="min-h-screen bg-bg text-fg">
    <slot />
  </div>
</template>
```

Landing page uses this layout via `definePageMeta({ layout: 'landing' })`.

### App Layout (`layouts/default.vue`)

```vue
<template>
  <div class="flex min-h-screen bg-bg text-fg">
    <AppSidebar />
    <main class="flex-1 p-6 lg:p-8">
      <slot />
    </main>
  </div>
</template>
```

All app pages use this layout by default.

## Waitlist API Route

`server/api/waitlist.post.ts`:

```ts
import { readFile, writeFile } from 'fs/promises'
import { join } from 'path'

const WAITLIST_PATH = join(process.cwd(), 'waitlist.json')

export default defineEventHandler(async (event) => {
  const { email } = await readBody(event)

  // Validate
  if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    throw createError({ statusCode: 400, message: 'Please enter a valid email.' })
  }

  // Read or create
  let data: { entries: Array<{ email: string; timestamp: string; source: string }> } = { entries: [] }
  try {
    const raw = await readFile(WAITLIST_PATH, 'utf-8')
    data = JSON.parse(raw)
  } catch {
    // File doesn't exist yet
  }

  // Check duplicate
  if (data.entries.some(e => e.email === email)) {
    return { success: true, message: "You're already on the list!" }
  }

  // Append
  data.entries.push({ email, timestamp: new Date().toISOString(), source: 'landing-page' })
  await writeFile(WAITLIST_PATH, JSON.stringify(data, null, 2))

  return { success: true, message: "You're on the list!" }
})
```

## Component Patterns

- Use Vue 3 Composition API with `<script setup lang="ts">`.
- Components are auto-imported by Nuxt (no manual imports needed).
- Use `ref()` and `reactive()` for state management.
- Navigation: `<NuxtLink to="/dashboard">`.
- Pages set layout via `definePageMeta({ layout: 'landing' })`.

### Page Example

```vue
<script setup lang="ts">
definePageMeta({ layout: 'landing' })
</script>

<template>
  <div>
    <LandingNavbar />
    <LandingHero />
    <LandingFeatures />
    <LandingHowItWorks />
    <LandingPricing />
    <LandingTestimonials />
    <LandingWaitlistForm />
    <LandingFooter />
  </div>
</template>
```

### WaitlistForm Component

```vue
<script setup lang="ts">
const email = ref('')
const status = ref<'idle' | 'loading' | 'success' | 'error'>('idle')
const message = ref('')

async function submit() {
  status.value = 'loading'
  try {
    const res = await $fetch('/api/waitlist', {
      method: 'POST',
      body: { email: email.value },
    })
    status.value = 'success'
    message.value = res.message
  } catch (err: any) {
    status.value = 'error'
    message.value = err.data?.message || 'Something went wrong.'
  }
}
</script>
```

## Dev Server

```bash
npm run dev
# Runs on http://localhost:3000
```

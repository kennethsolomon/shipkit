# Nuxt 3 + Tailwind — Client Website Stack Reference

Stack for building multi-page client marketing sites with Vue 3. NOT a prototype — real copy, real SEO, no fake data.

## Scaffold

```bash
npx nuxi@latest init {project-name}
cd {project-name}
npm install
npx nuxi module add @nuxtjs/tailwindcss
npx nuxi module add @nuxtjs/google-fonts
npx nuxi module add @nuxtjs/sitemap
```

## Directory Structure

```
{project-name}/
├── pages/
│   ├── index.vue               ← Home page
│   ├── about.vue               ← About page
│   ├── services.vue            ← Services / Menu page
│   ├── contact.vue             ← Contact page
│   └── [additional].vue        ← niche-specific pages
├── components/
│   ├── layout/
│   │   ├── TheNavbar.vue
│   │   └── TheFooter.vue
│   ├── home/
│   │   ├── HomeHero.vue
│   │   ├── HomeServices.vue
│   │   └── HomeTestimonials.vue
│   ├── contact/
│   │   └── ContactForm.vue     ← reactive form with validation
│   ├── WhatsAppButton.vue      ← floating CTA
│   └── MessengerButton.vue     ← alternative CTA (Philippines)
├── layouts/
│   └── default.vue             ← site layout (Navbar + Footer + WhatsApp CTA)
├── server/
│   └── api/
│       └── contact.post.ts     ← contact form handler
├── content/
│   └── site.ts                 ← typed site config: copy, pages, metadata
├── assets/
│   └── css/
│       └── main.css            ← Tailwind directives + CSS custom properties
├── public/
│   ├── images/
│   └── favicon.ico
├── tailwind.config.ts
└── nuxt.config.ts
```

## Site Config

`content/site.ts`:

```ts
export const site = {
  name: '{Business Name}',
  tagline: '{Tagline}',
  description: '{Meta description — used for SEO}',
  url: 'https://{domain}',
  phone: '{639171234567}',          // E.164 without +
  email: '{contact@example.com}',
  address: '{Full address}',
  hours: '{Mon–Fri 9am–6pm}',
  social: {
    facebook: '{https://facebook.com/page}',
    instagram: '{https://instagram.com/handle}',
  },
  pages: {
    home: {
      title: '{Business Name} — {Primary benefit}',
      description: '{Page-specific meta description}',
      hero: {
        headline: '{Real headline — no Lorem ipsum}',
        subheadline: '{Supporting line}',
        cta: '{Primary CTA text}',
        ctaHref: '/contact',
      },
    },
    about: {
      title: 'About — {Business Name}',
      description: '{About page meta description}',
    },
    services: {
      title: 'Services — {Business Name}',
      description: '{Services page meta description}',
      items: [
        { name: '{Service 1}', description: '{Real description}', price: '{optional}' },
      ],
    },
    contact: {
      title: 'Contact — {Business Name}',
      description: '{Contact page meta description}',
    },
  },
}
```

## Nuxt Config

`nuxt.config.ts`:

```ts
import { site } from './content/site'

export default defineNuxtConfig({
  modules: [
    '@nuxtjs/tailwindcss',
    '@nuxtjs/google-fonts',
    '@nuxtjs/sitemap',
  ],
  googleFonts: {
    families: {
      '{DisplayFont}': [400, 600, 700, 800],
      '{BodyFont}': [400, 500, 600],
    },
  },
  css: ['~/assets/css/main.css'],
  app: {
    head: {
      htmlAttrs: { lang: 'en' },
      meta: [
        { name: 'description', content: site.description },
        { property: 'og:site_name', content: site.name },
      ],
      link: [
        { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' },
      ],
    },
  },
  sitemap: {
    hostname: site.url,
  },
  nitro: {
    preset: 'vercel',               // or 'netlify', 'node-server'
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
        surface: 'var(--color-surface)',
      },
      fontFamily: {
        display: ['{DisplayFont}', 'serif'],
        body: ['{BodyFont}', 'sans-serif'],
      },
    },
  },
}
```

`assets/css/main.css`:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

:root {
  --color-bg: #xxxxxx;        /* from art direction spec */
  --color-fg: #xxxxxx;
  --color-accent: #xxxxxx;
  --color-muted: #xxxxxx;
  --color-surface: #xxxxxx;
}

body {
  font-family: '{BodyFont}', sans-serif;
}
```

## Default Layout

`layouts/default.vue`:

```vue
<template>
  <div class="min-h-screen bg-bg text-fg font-body antialiased">
    <LayoutTheNavbar />
    <main>
      <slot />
    </main>
    <LayoutTheFooter />
    <!-- Remove if not a local PH/SEA business -->
    <WhatsAppButton :phone="site.phone" message="Hi! I found you on your website." />
  </div>
</template>

<script setup lang="ts">
import { site } from '~/content/site'
</script>
```

## Per-Page SEO

Use `useSeoMeta` (recommended) or `useHead` in each page:

```vue
<!-- pages/about.vue -->
<script setup lang="ts">
import { site } from '~/content/site'

useSeoMeta({
  title: site.pages.about.title,
  description: site.pages.about.description,
  ogTitle: site.pages.about.title,
  ogDescription: site.pages.about.description,
  ogUrl: `${site.url}/about`,
  ogSiteName: site.name,
  ogType: 'website',
})
</script>

<template>
  <div>
    <h1>About {{ site.name }}</h1>
    <!-- real content -->
  </div>
</template>
```

## Contact Form API

`server/api/contact.post.ts`:

```ts
export default defineEventHandler(async (event) => {
  const { name, email, phone, message } = await readBody(event)

  if (!name || !email || !message) {
    throw createError({ statusCode: 400, message: 'Name, email, and message are required.' })
  }

  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    throw createError({ statusCode: 400, message: 'Invalid email address.' })
  }

  // TODO: wire to email service (Resend, Nodemailer, etc.)
  console.log('Contact submission:', { name, email, phone, message, timestamp: new Date().toISOString() })

  return { success: true, message: "Message received. We'll be in touch soon." }
})
```

## Contact Form Component

`components/contact/ContactForm.vue`:

```vue
<script setup lang="ts">
const form = reactive({ name: '', email: '', phone: '', message: '' })
const status = ref<'idle' | 'loading' | 'success' | 'error'>('idle')
const feedback = ref('')

async function submit() {
  status.value = 'loading'
  try {
    const res = await $fetch('/api/contact', { method: 'POST', body: form })
    status.value = 'success'
    feedback.value = (res as any).message
  } catch (err: any) {
    status.value = 'error'
    feedback.value = err.data?.message || 'Something went wrong. Please try again.'
  }
}
</script>

<template>
  <form @submit.prevent="submit" class="space-y-4">
    <input v-model="form.name" type="text" placeholder="Your name" required class="w-full px-4 py-3 border rounded-lg" />
    <input v-model="form.email" type="email" placeholder="Email address" required class="w-full px-4 py-3 border rounded-lg" />
    <input v-model="form.phone" type="tel" placeholder="Phone (optional)" class="w-full px-4 py-3 border rounded-lg" />
    <textarea v-model="form.message" placeholder="Your message" required rows="4" class="w-full px-4 py-3 border rounded-lg resize-none"></textarea>
    <button type="submit" :disabled="status === 'loading'" class="w-full px-6 py-3 bg-accent text-white rounded-lg font-medium transition hover:opacity-90">
      {{ status === 'loading' ? 'Sending...' : 'Send Message' }}
    </button>
    <p v-if="status === 'success'" class="text-green-600 font-medium">{{ feedback }}</p>
    <p v-if="status === 'error'" class="text-red-500 text-sm">{{ feedback }}</p>
  </form>
</template>
```

## WhatsApp Component

`components/WhatsAppButton.vue`:

```vue
<script setup lang="ts">
const props = defineProps<{
  phone: string    // E.164 without +: e.g., "639171234567"
  message?: string
}>()

const url = computed(() =>
  props.message
    ? `https://wa.me/${props.phone}?text=${encodeURIComponent(props.message)}`
    : `https://wa.me/${props.phone}`
)
</script>

<template>
  <a
    :href="url"
    target="_blank"
    rel="noopener noreferrer"
    aria-label="Chat on WhatsApp"
    class="fixed bottom-6 right-6 z-50 flex h-14 w-14 items-center justify-center rounded-full bg-[#25D366] shadow-lg transition-transform hover:scale-110 focus:outline-none focus:ring-2 focus:ring-[#25D366] focus:ring-offset-2"
  >
    <!-- WhatsApp SVG icon — see whatsapp-cta.md for full SVG path -->
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="white" class="h-7 w-7" aria-hidden="true">
      <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/>
    </svg>
  </a>
</template>
```

## Structured Data

In each page or layout, add LocalBusiness structured data:

```vue
<script setup lang="ts">
import { site } from '~/content/site'

useHead({
  script: [{
    type: 'application/ld+json',
    children: JSON.stringify({
      '@context': 'https://schema.org',
      '@type': 'LocalBusiness',
      name: site.name,
      description: site.description,
      url: site.url,
      telephone: `+${site.phone}`,
      address: { '@type': 'PostalAddress', streetAddress: site.address },
    }),
  }],
})
</script>
```

## Dev + Build Commands

```bash
npm run dev           # http://localhost:3000
npm run build         # production build (outputs .output/)
npm run preview       # preview production build locally
npm run generate      # static site generation (SSG)
```

## Vercel Deploy

```bash
npm install -g vercel
vercel --prod
```

Or: set `nitro.preset = 'vercel'` in `nuxt.config.ts` and connect GitHub to Vercel dashboard.

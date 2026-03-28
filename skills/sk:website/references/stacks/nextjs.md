# Next.js + Tailwind — Client Website Stack Reference

Stack for building multi-page client marketing sites. NOT a prototype — real copy, real SEO, no fake data.

## Scaffold

```bash
npx create-next-app@latest {project-name} --typescript --tailwind --eslint --app --src-dir --no-import-alias
cd {project-name} && npm install
```

## Directory Structure

```
{project-name}/
├── src/
│   ├── app/
│   │   ├── layout.tsx                  ← root layout (fonts, WhatsApp CTA, global nav)
│   │   ├── page.tsx                    ← Home page
│   │   ├── globals.css                 ← Tailwind directives + CSS custom properties
│   │   ├── sitemap.ts                  ← auto-generated sitemap.xml
│   │   ├── robots.ts                   ← robots.txt
│   │   ├── about/
│   │   │   └── page.tsx                ← About page
│   │   ├── services/
│   │   │   └── page.tsx                ← Services / Menu page
│   │   ├── contact/
│   │   │   └── page.tsx                ← Contact page
│   │   ├── [additional-pages]/
│   │   │   └── page.tsx
│   │   └── api/
│   │       └── contact/
│   │           └── route.ts            ← contact form handler
│   └── components/
│       ├── layout/
│       │   ├── Navbar.tsx
│       │   └── Footer.tsx
│       ├── home/
│       │   ├── Hero.tsx
│       │   ├── Services.tsx
│       │   ├── About.tsx               ← brief About preview on Home
│       │   └── Testimonials.tsx
│       ├── contact/
│       │   └── ContactForm.tsx         ← "use client" — form with validation
│       ├── WhatsAppButton.tsx          ← floating CTA
│       └── MessengerButton.tsx         ← alternative CTA (Philippines)
├── content/
│   └── site.ts                         ← typed site config: copy, pages, metadata
├── public/
│   ├── images/
│   └── favicon.ico
├── tailwind.config.ts
├── next.config.ts
└── package.json
```

## Site Config Pattern

`content/site.ts` — single source of truth for all copy and metadata:

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

## Root Layout

`src/app/layout.tsx`:

```tsx
import type { Metadata } from 'next'
import { {DisplayFont}, {BodyFont} } from 'next/font/google'
import './globals.css'
import { Navbar } from '@/components/layout/Navbar'
import { Footer } from '@/components/layout/Footer'
import { WhatsAppButton } from '@/components/WhatsAppButton'
import { site } from '@/content/site'

const display = {DisplayFont}({ subsets: ['latin'], variable: '--font-display' })
const body = {BodyFont}({ subsets: ['latin'], variable: '--font-body' })

export const metadata: Metadata = {
  metadataBase: new URL(site.url),
  title: { default: site.name, template: `%s — ${site.name}` },
  description: site.description,
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={`${display.variable} ${body.variable}`}>
      <body className="font-body antialiased bg-bg text-fg">
        <Navbar />
        <main>{children}</main>
        <Footer />
        {/* Remove WhatsAppButton if not a local PH/SEA business */}
        <WhatsAppButton phone={site.phone} message="Hi! I found you on your website." />
      </body>
    </html>
  )
}
```

## Per-Page SEO Metadata

Each page exports a `generateMetadata` function or a `metadata` object:

```tsx
// src/app/about/page.tsx
import type { Metadata } from 'next'
import { site } from '@/content/site'

export const metadata: Metadata = {
  title: site.pages.about.title,
  description: site.pages.about.description,
  openGraph: {
    title: site.pages.about.title,
    description: site.pages.about.description,
    url: `${site.url}/about`,
    siteName: site.name,
    type: 'website',
  },
}

export default function AboutPage() {
  return (
    <div>
      <h1>About {site.name}</h1>
      {/* real content */}
    </div>
  )
}
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
        display: ['var(--font-display)', 'serif'],
        body: ['var(--font-body)', 'sans-serif'],
      },
    },
  },
}
```

`src/app/globals.css`:

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
```

## Contact Form API Route

`src/app/api/contact/route.ts`:

```ts
import { NextResponse } from 'next/server'

export async function POST(request: Request) {
  const body = await request.json()
  const { name, email, phone, message } = body

  if (!name || !email || !message) {
    return NextResponse.json({ success: false, message: 'Name, email, and message are required.' }, { status: 400 })
  }

  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    return NextResponse.json({ success: false, message: 'Invalid email address.' }, { status: 400 })
  }

  // TODO: wire to email service (Resend, Nodemailer, SendGrid)
  // For now: log to console and return success
  console.log('Contact form submission:', { name, email, phone, message, timestamp: new Date().toISOString() })

  return NextResponse.json({ success: true, message: "Message received. We'll be in touch soon." })
}
```

## Sitemap + Robots

`src/app/sitemap.ts`:

```ts
import { MetadataRoute } from 'next'
import { site } from '@/content/site'

export default function sitemap(): MetadataRoute.Sitemap {
  return [
    { url: site.url, lastModified: new Date(), changeFrequency: 'monthly', priority: 1 },
    { url: `${site.url}/about`, lastModified: new Date(), changeFrequency: 'monthly', priority: 0.8 },
    { url: `${site.url}/services`, lastModified: new Date(), changeFrequency: 'monthly', priority: 0.8 },
    { url: `${site.url}/contact`, lastModified: new Date(), changeFrequency: 'yearly', priority: 0.5 },
  ]
}
```

`src/app/robots.ts`:

```ts
import { MetadataRoute } from 'next'
import { site } from '@/content/site'

export default function robots(): MetadataRoute.Robots {
  return {
    rules: { userAgent: '*', allow: '/' },
    sitemap: `${site.url}/sitemap.xml`,
  }
}
```

## WhatsApp Component

`src/components/WhatsAppButton.tsx` — see `references/whatsapp-cta.md` for full implementation.

```tsx
'use client'

interface WhatsAppButtonProps {
  phone: string   // E.164 without +: e.g., "639171234567"
  message?: string
}

export function WhatsAppButton({ phone, message }: WhatsAppButtonProps) {
  const url = message
    ? `https://wa.me/${phone}?text=${encodeURIComponent(message)}`
    : `https://wa.me/${phone}`

  return (
    <a
      href={url}
      target="_blank"
      rel="noopener noreferrer"
      aria-label="Chat on WhatsApp"
      className="fixed bottom-6 right-6 z-50 flex h-14 w-14 items-center justify-center rounded-full bg-[#25D366] shadow-lg transition-transform hover:scale-110"
    >
      {/* SVG icon — see whatsapp-cta.md */}
    </a>
  )
}
```

## Structured Data

Add to each page's `<head>` via Next.js metadata or a script tag:

```tsx
// For local businesses — in layout.tsx or per-page
const structuredData = {
  '@context': 'https://schema.org',
  '@type': 'LocalBusiness',        // or Restaurant, Dentist, LawFirm, etc.
  name: site.name,
  description: site.description,
  url: site.url,
  telephone: `+${site.phone}`,
  address: {
    '@type': 'PostalAddress',
    streetAddress: site.address,
  },
}

// In page component:
<script
  type="application/ld+json"
  dangerouslySetInnerHTML={{ __html: JSON.stringify(structuredData) }}
/>
```

## Dev + Build Commands

```bash
npm run dev        # http://localhost:3000
npm run build      # production build — must pass before handoff
npm run start      # preview production build locally
npm run lint       # ESLint check
```

## Vercel Deploy

```bash
npm install -g vercel
vercel --prod      # deploy to production
```

Or: connect GitHub repo to Vercel dashboard for automatic deployments on push.

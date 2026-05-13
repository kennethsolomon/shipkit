# Next.js + Tailwind — Stack Reference

## Scaffold

```bash
npx create-next-app@latest {project-name} --typescript --tailwind --eslint --app --src-dir --no-import-alias
```

Then `cd {project-name} && npm install`.

## Directory Structure

```
{project-name}/
├── src/
│   ├── app/
│   │   ├── layout.tsx          ← root layout (fonts, global styles)
│   │   ├── page.tsx            ← landing page
│   │   ├── globals.css         ← Tailwind directives + custom CSS
│   │   ├── api/
│   │   │   └── waitlist/
│   │   │       └── route.ts    ← waitlist API handler
│   │   ├── dashboard/
│   │   │   └── page.tsx        ← dashboard page
│   │   ├── {feature-1}/
│   │   │   └── page.tsx
│   │   ├── {feature-2}/
│   │   │   └── page.tsx
│   │   └── settings/
│   │       └── page.tsx
│   └── components/
│       ├── landing/
│       │   ├── Navbar.tsx
│       │   ├── Hero.tsx
│       │   ├── Features.tsx
│       │   ├── HowItWorks.tsx
│       │   ├── Pricing.tsx
│       │   ├── Testimonials.tsx
│       │   ├── WaitlistForm.tsx
│       │   └── Footer.tsx
│       ├── app/
│       │   ├── Sidebar.tsx
│       │   ├── DashboardCards.tsx
│       │   └── {feature components}
│       └── ui/
│           ├── Button.tsx
│           ├── Input.tsx
│           ├── Card.tsx
│           ├── Modal.tsx
│           └── Toast.tsx
├── public/
│   └── {static assets}
├── waitlist.json               ← email storage (auto-created by API)
├── tailwind.config.ts
├── next.config.ts
└── package.json
```

## Root Layout Pattern

`src/app/layout.tsx`:
- Import Google Fonts via `next/font/google`.
- Apply font CSS variables to `<html>` element.
- Include global nav only for app pages (not landing page — it has its own navbar).

```tsx
import { {DisplayFont}, {BodyFont} } from 'next/font/google'

const display = {DisplayFont}({ subsets: ['latin'], variable: '--font-display' })
const body = {BodyFont}({ subsets: ['latin'], variable: '--font-body' })

export default function RootLayout({ children }) {
  return (
    <html className={`${display.variable} ${body.variable}`}>
      <body className="font-body antialiased">{children}</body>
    </html>
  )
}
```

## Tailwind Config

`tailwind.config.ts` — extend with custom palette and fonts:

```ts
export default {
  theme: {
    extend: {
      colors: {
        bg: 'var(--color-bg)',
        fg: 'var(--color-fg)',
        accent: 'var(--color-accent)',
        muted: 'var(--color-muted)',
        // add more as needed
      },
      fontFamily: {
        display: ['var(--font-display)', 'serif'],
        body: ['var(--font-body)', 'sans-serif'],
      },
    },
  },
}
```

Define CSS variables in `globals.css`:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

:root {
  --color-bg: #xxxxxx;
  --color-fg: #xxxxxx;
  --color-accent: #xxxxxx;
  --color-muted: #xxxxxx;
}
```

## Waitlist API Route

`src/app/api/waitlist/route.ts`:

```ts
import { NextResponse } from 'next/server'
import { readFile, writeFile } from 'fs/promises'
import { join } from 'path'

const WAITLIST_PATH = join(process.cwd(), 'waitlist.json')

export async function POST(request: Request) {
  const { email } = await request.json()

  // Validate
  if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    return NextResponse.json({ success: false, message: 'Please enter a valid email.' }, { status: 400 })
  }

  // Read or create
  let data = { entries: [] as Array<{ email: string; timestamp: string; source: string }> }
  try {
    const raw = await readFile(WAITLIST_PATH, 'utf-8')
    data = JSON.parse(raw)
  } catch {
    // File doesn't exist yet — use empty default
  }

  // Check duplicate
  if (data.entries.some(e => e.email === email)) {
    return NextResponse.json({ success: true, message: "You're already on the list!" })
  }

  // Append
  data.entries.push({ email, timestamp: new Date().toISOString(), source: 'landing-page' })
  await writeFile(WAITLIST_PATH, JSON.stringify(data, null, 2))

  return NextResponse.json({ success: true, message: "You're on the list!" })
}
```

## Component Patterns

- Landing page components are **server components** by default (no `"use client"`).
- Interactive components (WaitlistForm, modals, toasts) need `"use client"` directive.
- Use `useState` for local UI state (form values, modal open/close).
- Navigation between app pages: use `<Link>` from `next/link`.
- App pages can share a layout: `src/app/(app)/layout.tsx` with sidebar.

### App Layout (grouped routes)

```
src/app/
├── page.tsx                    ← landing page (no app layout)
├── (app)/
│   ├── layout.tsx              ← shared sidebar + header
│   ├── dashboard/page.tsx
│   ├── {feature-1}/page.tsx
│   ├── {feature-2}/page.tsx
│   └── settings/page.tsx
```

`(app)/layout.tsx` wraps app pages with sidebar navigation without affecting the landing page.

## Dev Server

```bash
npm run dev
# Runs on http://localhost:3000
```

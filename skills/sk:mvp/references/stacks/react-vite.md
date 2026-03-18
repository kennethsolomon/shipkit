# React + Vite + Tailwind — Stack Reference

## Scaffold

```bash
npm create vite@latest {project-name} -- --template react-ts
cd {project-name}
npm install
npm install -D tailwindcss @tailwindcss/vite
npm install react-router-dom
```

## Directory Structure

```
{project-name}/
├── src/
│   ├── main.tsx                ← entry point (router setup)
│   ├── App.tsx                 ← route definitions
│   ├── index.css               ← Tailwind directives + custom CSS
│   ├── pages/
│   │   ├── Landing.tsx         ← landing page
│   │   ├── Dashboard.tsx       ← dashboard
│   │   ├── {Feature1}.tsx
│   │   ├── {Feature2}.tsx
│   │   └── Settings.tsx
│   ├── components/
│   │   ├── landing/
│   │   │   ├── Navbar.tsx
│   │   │   ├── Hero.tsx
│   │   │   ├── Features.tsx
│   │   │   ├── HowItWorks.tsx
│   │   │   ├── Pricing.tsx
│   │   │   ├── Testimonials.tsx
│   │   │   ├── WaitlistForm.tsx
│   │   │   └── Footer.tsx
│   │   ├── app/
│   │   │   ├── Sidebar.tsx
│   │   │   ├── AppLayout.tsx
│   │   │   ├── DashboardCards.tsx
│   │   │   └── {feature components}
│   │   └── ui/
│   │       ├── Button.tsx
│   │       ├── Input.tsx
│   │       ├── Card.tsx
│   │       ├── Modal.tsx
│   │       └── Toast.tsx
│   ├── data/
│   │   └── mock.ts             ← all fake data centralized
│   └── lib/
│       └── utils.ts            ← shared helpers (cn, etc.)
├── public/
│   └── {static assets}
├── index.html
├── vite.config.ts
├── tailwind.config.ts
└── package.json
```

## Vite Config

`vite.config.ts`:

```ts
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [react(), tailwindcss()],
})
```

## Tailwind Config

`tailwind.config.ts`:

```ts
export default {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        bg: 'var(--color-bg)',
        fg: 'var(--color-fg)',
        accent: 'var(--color-accent)',
        muted: 'var(--color-muted)',
      },
      fontFamily: {
        display: ['var(--font-display)', 'serif'],
        body: ['var(--font-body)', 'sans-serif'],
      },
    },
  },
}
```

CSS variables and font imports in `src/index.css`:

```css
@import url('https://fonts.googleapis.com/css2?family={DisplayFont}:wght@400;600;700;800&family={BodyFont}:wght@400;500;600&display=swap');

@tailwind base;
@tailwind components;
@tailwind utilities;

:root {
  --color-bg: #xxxxxx;
  --color-fg: #xxxxxx;
  --color-accent: #xxxxxx;
  --color-muted: #xxxxxx;
  --font-display: '{DisplayFont}', serif;
  --font-body: '{BodyFont}', sans-serif;
}

body {
  font-family: var(--font-body);
}
```

## Router Setup

`src/App.tsx`:

```tsx
import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import Landing from './pages/Landing'
import AppLayout from './components/app/AppLayout'
import Dashboard from './pages/Dashboard'
import Feature1 from './pages/{Feature1}'
import Feature2 from './pages/{Feature2}'
import Settings from './pages/Settings'

const router = createBrowserRouter([
  { path: '/', element: <Landing /> },
  {
    element: <AppLayout />,
    children: [
      { path: '/dashboard', element: <Dashboard /> },
      { path: '/{feature-1}', element: <Feature1 /> },
      { path: '/{feature-2}', element: <Feature2 /> },
      { path: '/settings', element: <Settings /> },
    ],
  },
])

export default function App() {
  return <RouterProvider router={router} />
}
```

## App Layout

`src/components/app/AppLayout.tsx`:

```tsx
import { Outlet } from 'react-router-dom'
import Sidebar from './Sidebar'

export default function AppLayout() {
  return (
    <div className="flex min-h-screen bg-bg text-fg">
      <Sidebar />
      <main className="flex-1 p-6 lg:p-8">
        <Outlet />
      </main>
    </div>
  )
}
```

## Waitlist — Formspree Integration

Since React + Vite has no backend, use Formspree for email collection.

`src/components/landing/WaitlistForm.tsx`:

```tsx
import { useState, FormEvent } from 'react'

// Replace YOUR_FORM_ID with your Formspree form ID
// Create one free at https://formspree.io
const FORMSPREE_URL = 'https://formspree.io/f/YOUR_FORM_ID'

export default function WaitlistForm() {
  const [email, setEmail] = useState('')
  const [status, setStatus] = useState<'idle' | 'loading' | 'success' | 'error'>('idle')
  const [message, setMessage] = useState('')

  async function handleSubmit(e: FormEvent) {
    e.preventDefault()
    setStatus('loading')

    try {
      const res = await fetch(FORMSPREE_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
        body: JSON.stringify({ email }),
      })

      if (res.ok) {
        setStatus('success')
        setMessage("You're on the list! We'll notify you when we launch.")
      } else {
        throw new Error()
      }
    } catch {
      setStatus('error')
      setMessage('Something went wrong. Please try again.')
    }
  }

  if (status === 'success') {
    return <p className="text-green-600 font-medium text-lg">{message}</p>
  }

  return (
    <form onSubmit={handleSubmit} className="flex flex-col sm:flex-row gap-3 max-w-md">
      <input
        type="email"
        value={email}
        onChange={e => setEmail(e.target.value)}
        placeholder="you@example.com"
        required
        className="flex-1 px-4 py-3 rounded-lg border border-muted/30 bg-bg focus:ring-2 focus:ring-accent focus:outline-none"
      />
      <button
        type="submit"
        disabled={status === 'loading'}
        className="px-6 py-3 bg-accent text-white rounded-xl font-medium hover:opacity-90 transition-all disabled:opacity-50"
      >
        {status === 'loading' ? 'Joining...' : 'Join Waitlist'}
      </button>
      {status === 'error' && <p className="text-red-500 text-sm">{message}</p>}
    </form>
  )
}
```

## Mock Data

Centralize all fake data in `src/data/mock.ts`:

```ts
export const features = [
  { icon: '🎯', title: 'Feature One', description: 'Short benefit-driven description.' },
  { icon: '⚡', title: 'Feature Two', description: 'Short benefit-driven description.' },
  { icon: '🔒', title: 'Feature Three', description: 'Short benefit-driven description.' },
]

export const testimonials = [
  { quote: 'Realistic testimonial here.', name: 'Jane Smith', role: 'CTO, TechCo' },
  // ...
]

export const pricingPlans = [
  { name: 'Free', price: '$0', features: ['Feature A', 'Feature B'], cta: 'Get Started' },
  { name: 'Pro', price: '$29/mo', features: ['Everything in Free', 'Feature C'], cta: 'Get Pro', popular: true },
  { name: 'Enterprise', price: 'Custom', features: ['Everything in Pro', 'Priority support'], cta: 'Contact Us' },
]

// Dashboard mock data
export const dashboardStats = [
  { label: 'Total Users', value: '2,847', change: '+12%' },
  // ...
]

export const recentActivity = [
  { user: 'Jane Smith', action: 'created a new project', time: '2 hours ago' },
  // ...
]
```

## Component Patterns

- Use functional components with TypeScript.
- Use `useState` for local state, no state management library needed.
- Navigation: `<Link to="/dashboard">` from react-router-dom.
- Keep components focused — one file per component.
- Props typed with interfaces or inline.

## Dev Server

```bash
npm run dev
# Runs on http://localhost:5173
```

# WhatsApp CTA Implementation Guide

Inject a floating WhatsApp button for local businesses in PH/SEA. WhatsApp is the primary contact channel for local businesses across Southeast Asia — not email.

## When to inject

See the SEA Location Detection table in SKILL.md. Default to injecting for any local business when location is unknown.

---

## Component — Next.js + Tailwind

Create `components/whatsapp-button.tsx`:

```tsx
'use client'

interface WhatsAppButtonProps {
  phone: string // E.164 format without +: e.g., "639171234567"
  message?: string // Pre-filled message (URL-encoded)
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
      className="fixed bottom-6 right-6 z-50 flex h-14 w-14 items-center justify-center rounded-full bg-[#25D366] shadow-lg transition-transform hover:scale-110 focus:outline-none focus:ring-2 focus:ring-[#25D366] focus:ring-offset-2"
    >
      {/* WhatsApp SVG icon */}
      <svg
        xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 24 24"
        fill="white"
        className="h-7 w-7"
        aria-hidden="true"
      >
        <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/>
      </svg>
    </a>
  )
}
```

---

## Usage in layout

Add to `app/layout.tsx` (or the root layout):

```tsx
import { WhatsAppButton } from '@/components/whatsapp-button'

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        {children}
        <WhatsAppButton
          phone="639171234567"
          message="Hi! I found you on your website."
        />
      </body>
    </html>
  )
}
```

---

## Phone number format

WhatsApp uses E.164 format **without the `+`**:
- Philippines: `63` + 10-digit mobile number → `639171234567`
- Singapore: `65` + 8-digit number → `6591234567`
- Malaysia: `60` + mobile number → `60121234567`
- Indonesia: `62` + mobile number → `628111234567`

If phone number is unknown, use `+[PHONE]` as placeholder in the config and document it clearly in `HANDOFF.md`:
```tsx
<WhatsAppButton phone="[REPLACE_WITH_PHONE_WITHOUT_PLUS]" />
```

---

## Pre-filled message by business type

Set a context-aware default message so the client knows where the inquiry came from:

| Business type | Pre-filled message |
|---|---|
| Cafe / restaurant | "Hi! I found you on your website. I'd like to inquire about a reservation." |
| Service business | "Hi! I found you on your website. I'd like to get a quote." |
| Medical / dental | "Hi! I found you on your website. I'd like to book an appointment." |
| Fitness / gym | "Hi! I found you on your website. I'd like to know more about your classes." |
| Generic | "Hi! I found you on your website." |

---

## Messenger alternative (Philippines-heavy markets)

For Philippine businesses where Facebook Messenger is more common than WhatsApp:

```tsx
// Messenger variant — use when brief mentions Facebook or when user prefers Messenger
'use client'

export function MessengerButton({ pageId }: { pageId: string }) {
  return (
    <a
      href={`https://m.me/${pageId}`}
      target="_blank"
      rel="noopener noreferrer"
      aria-label="Message us on Messenger"
      className="fixed bottom-6 right-6 z-50 flex h-14 w-14 items-center justify-center rounded-full bg-[#0084FF] shadow-lg transition-transform hover:scale-110 focus:outline-none focus:ring-2 focus:ring-[#0084FF] focus:ring-offset-2"
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 24 24"
        fill="white"
        className="h-7 w-7"
        aria-hidden="true"
      >
        <path d="M12 0C5.373 0 0 4.974 0 11.111c0 3.498 1.744 6.614 4.469 8.654V24l4.088-2.242c1.092.3 2.246.464 3.443.464 6.627 0 12-4.975 12-11.111S18.627 0 12 0zm1.191 14.963l-3.055-3.26-5.963 3.26L10.732 8l3.131 3.26L19.752 8l-6.561 6.963z"/>
      </svg>
    </a>
  )
}
```

---

## Both WhatsApp + Messenger (stacked)

If the client wants both options:

```tsx
// Stack them vertically with a gap
<div className="fixed bottom-6 right-6 z-50 flex flex-col gap-3">
  <MessengerButton pageId="your.page.name" />
  <WhatsAppButton phone="639171234567" />
</div>
```

Adjust `bottom-6` / `right-6` to match the site's spacing.

---

## Accessibility notes

- Always include `aria-label` on the button
- The SVG should have `aria-hidden="true"` (label is on the link)
- Ensure the button passes 3:1 contrast against the page background
- Fixed position — verify it doesn't cover critical page content on mobile (375px)

# Handoff Template

Use this to generate the 3 client deliverable files after the site is built. Populate using real project details — replace all `[PLACEHOLDER]` values.

---

## HANDOFF.md template

```markdown
# [Business Name] — Website Handoff

Built with Next.js + Tailwind CSS. Hosted on [Vercel/Netlify].

---

## What was built

| Page | URL | Purpose |
|---|---|---|
| Home | `/` | Main landing + primary CTA |
| About | `/about` | Brand story + trust signals |
| [Services/Menu] | `/[path]` | [Purpose] |
| Contact | `/contact` | Inquiry form + location |
| [Additional pages] | | |

**Features included:**
- [ ] WhatsApp floating button — wired to [phone number / ⚠️ REPLACE: see below]
- [ ] Contact form with spam protection
- [ ] SEO metadata on all pages
- [ ] Sitemap + robots.txt
- [ ] [Other features]

---

## What still needs replacing

Before going live, update these:

| Item | File | What to change |
|---|---|---|
| WhatsApp number | `app/layout.tsx` line ~[N] | Replace `+[PHONE]` with your WhatsApp number |
| Hero photo | `public/images/hero.jpg` | Replace with your actual photo |
| Google Analytics ID | `.env.local` | Add `NEXT_PUBLIC_GA_ID=G-XXXXXXXXXX` |
| [Other placeholder] | [file] | [instruction] |

---

## Editing content

Most content lives in one file: `content/site.ts`

**To change your business name or tagline:**
Open `content/site.ts`, find `name:` and `tagline:` near the top.

**To change opening hours:**
Open `content/site.ts`, find `hours:` and update the values.

**To change services/menu items:**
Open `content/site.ts`, find `services:` (or `menu:`) and edit the list.

**To change contact info (phone, email, address):**
Open `content/site.ts`, find `contact:` and update.

**To change social media links:**
Open `content/site.ts`, find `social:` and update the URLs.

---

## Need help?

For technical changes beyond content editing, contact your developer or post in the project repo.

---

## Developer notes

- Stack: Next.js [version] + Tailwind CSS
- Node version: 18+
- Deploy: Vercel (see DEPLOY.md)
- Local dev: `npm install && npm run dev`
```

---

## DEPLOY.md template

```markdown
# Deploying [Business Name] Website

Step-by-step guide to go live. Total time: ~10 minutes.

---

## Option 1: Vercel (recommended — free tier available)

### One-click deploy

1. Push the project to a GitHub repository (create one at github.com if needed)
2. Go to vercel.com and sign in with GitHub
3. Click "Add New Project" → select your repository
4. Set environment variables (see below)
5. Click "Deploy"
6. Your site is live at `[project].vercel.app`

### Custom domain (recommended)

1. In Vercel dashboard → your project → Settings → Domains
2. Add your domain (e.g., `cornerbrew.ph`)
3. Follow the DNS instructions (add CNAME or A record in your domain registrar)
4. Takes 5–30 minutes to propagate

### Via CLI

```bash
npm install -g vercel
vercel login
vercel --prod
```

---

## Option 2: Netlify (alternative)

1. Go to netlify.com → "Add new site" → "Import from Git"
2. Connect GitHub and select the repository
3. Build command: `npm run build`
4. Publish directory: `.next`
5. Set environment variables
6. Deploy

---

## Environment variables

Set these in Vercel dashboard → Settings → Environment Variables (or in `.env.local` for local development):

| Variable | Required | Description | Example |
|---|---|---|---|
| `NEXT_PUBLIC_SITE_URL` | Yes | Your full site URL (no trailing slash) | `https://cornerbrew.ph` |
| `NEXT_PUBLIC_GA_ID` | Optional | Google Analytics 4 Measurement ID | `G-XXXXXXXXXX` |
| `NEXT_PUBLIC_PLAUSIBLE_DOMAIN` | Optional | Plausible domain (alternative to GA4) | `cornerbrew.ph` |
| `CONTACT_EMAIL` | If using contact form | Email to receive form submissions | `hello@cornerbrew.ph` |
| `RESEND_API_KEY` | If using Resend | API key for email sending | `re_xxxxxxxxx` |

---

## Estimated monthly costs

| Service | Cost | Notes |
|---|---|---|
| Vercel hosting | Free | Hobby plan — sufficient for most small business sites |
| Domain name | ~$12–20/year | Buy from Namecheap, GoDaddy, or Cloudflare Registrar |
| Google Analytics | Free | Optional — Plausible is $9/mo for privacy-friendly alternative |
| Custom email | ~$6/mo | Google Workspace or Zoho for @yourdomain.com email |
| **Total** | ~$18–26/year minimum | Domain + free hosting |

---

## After going live

- [ ] Test all pages on mobile and desktop
- [ ] Test the contact form by submitting it yourself
- [ ] Test the WhatsApp button
- [ ] Submit sitemap to Google Search Console: `yourdomain.com/sitemap.xml`
- [ ] Set up Google My Business if not already done (helps local SEO)
```

---

## CONTENT-GUIDE.md template

```markdown
# Content Editing Guide — [Business Name]

This guide is for updating your website content without a developer.

---

## Where content lives

Most of your site content is in one file:

**`content/site.ts`** — open this file to edit most things

---

## Editing your content

### Business name and tagline
File: `content/site.ts`
```
name: "[Your Business Name]",
tagline: "[Your Tagline]",
```
Change the text inside the quotes.

### Contact details
File: `content/site.ts`
```
contact: {
  phone: "[Your Phone]",
  email: "[Your Email]",
  address: "[Your Address]",
}
```

### Opening hours
File: `content/site.ts`
```
hours: [
  { day: "Monday–Friday", time: "8:00 AM – 6:00 PM" },
  { day: "Saturday", time: "9:00 AM – 5:00 PM" },
  { day: "Sunday", time: "Closed" },
]
```

### Services / Menu items
File: `content/site.ts`
```
services: [
  { name: "[Service Name]", description: "[Short description]" },
  ...
]
```
Add or remove items by copying/pasting a line.

### Social media links
File: `content/site.ts`
```
social: {
  facebook: "https://facebook.com/yourpage",
  instagram: "https://instagram.com/yourhandle",
}
```

---

## Adding a photo

1. Save your photo as a `.jpg` or `.webp` file
2. Copy it to the `public/images/` folder
3. In the relevant page file, change the image filename to match

---

## After editing

Save the file, then run the site locally with:
```bash
npm run dev
```
Visit `http://localhost:3000` to preview your changes before deploying.

To deploy changes live: push to GitHub — Vercel will automatically redeploy.

---

## Need more help?

For changes beyond this guide (new pages, new features, design changes), contact your developer.
```

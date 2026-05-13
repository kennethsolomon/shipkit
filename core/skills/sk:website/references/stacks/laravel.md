# Laravel 11 + Blade + Tailwind — Client Website Stack Reference

Stack for building multi-page client marketing sites with PHP/Laravel. NOT a prototype — real copy, real SEO, no fake data.

## Scaffold

```bash
composer create-project laravel/laravel {project-name}
cd {project-name}
npm install
```

Laravel 11 ships with Tailwind CSS configured via Vite out of the box.

## Directory Structure

```
{project-name}/
├── resources/
│   ├── views/
│   │   ├── layouts/
│   │   │   └── site.blade.php          ← site layout (head, nav, footer, WhatsApp)
│   │   ├── components/
│   │   │   ├── layout/
│   │   │   │   ├── navbar.blade.php
│   │   │   │   └── footer.blade.php
│   │   │   ├── home/
│   │   │   │   ├── hero.blade.php
│   │   │   │   ├── services.blade.php
│   │   │   │   └── testimonials.blade.php
│   │   │   ├── contact/
│   │   │   │   └── form.blade.php
│   │   │   └── whatsapp-button.blade.php  ← floating CTA partial
│   │   ├── home.blade.php               ← Home page
│   │   ├── about.blade.php              ← About page
│   │   ├── services.blade.php           ← Services / Menu page
│   │   └── contact.blade.php            ← Contact page
│   ├── css/
│   │   └── app.css                      ← Tailwind directives + CSS custom properties
│   └── js/
│       └── app.js                       ← Vite entry + Alpine.js for interactivity
├── routes/
│   └── web.php                          ← page routes + contact POST route
├── app/
│   ├── Http/
│   │   └── Controllers/
│   │       └── ContactController.php    ← contact form handler
│   └── Data/
│       └── SiteData.php                 ← typed site config: copy, pages, metadata
├── config/
│   └── site.php                         ← site-wide config values
├── public/
│   ├── images/
│   └── favicon.ico
├── tailwind.config.js
└── vite.config.js
```

## Site Config

`config/site.php` — single source of truth for all copy and metadata:

```php
<?php

return [
    'name'        => '{Business Name}',
    'tagline'     => '{Tagline}',
    'description' => '{Meta description — used for SEO}',
    'url'         => env('APP_URL', 'https://{domain}'),
    'phone'       => '{639171234567}',   // E.164 without +
    'email'       => '{contact@example.com}',
    'address'     => '{Full address}',
    'hours'       => '{Mon–Fri 9am–6pm}',
    'social' => [
        'facebook'  => '{https://facebook.com/page}',
        'instagram' => '{https://instagram.com/handle}',
    ],
    'pages' => [
        'home' => [
            'title'       => '{Business Name} — {Primary benefit}',
            'description' => '{Page-specific meta description}',
            'hero' => [
                'headline'    => '{Real headline — no Lorem ipsum}',
                'subheadline' => '{Supporting line}',
                'cta'         => '{Primary CTA text}',
                'cta_href'    => '/contact',
            ],
        ],
        'about' => [
            'title'       => 'About — {Business Name}',
            'description' => '{About page meta description}',
        ],
        'services' => [
            'title'       => 'Services — {Business Name}',
            'description' => '{Services page meta description}',
            'items' => [
                ['name' => '{Service 1}', 'description' => '{Real description}', 'price' => '{optional}'],
            ],
        ],
        'contact' => [
            'title'       => 'Contact — {Business Name}',
            'description' => '{Contact page meta description}',
        ],
    ],
];
```

## Site Layout

`resources/views/layouts/site.blade.php`:

```blade
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ $title ?? config('site.name') }}</title>
    <meta name="description" content="{{ $description ?? config('site.description') }}">

    {{-- Open Graph --}}
    <meta property="og:title" content="{{ $title ?? config('site.name') }}">
    <meta property="og:description" content="{{ $description ?? config('site.description') }}">
    <meta property="og:url" content="{{ $canonical ?? url()->current() }}">
    <meta property="og:site_name" content="{{ config('site.name') }}">
    <meta property="og:type" content="website">

    {{-- Canonical --}}
    <link rel="canonical" href="{{ $canonical ?? url()->current() }}">
    <link rel="icon" href="/favicon.ico">

    {{-- Fonts: replace with art-direction spec fonts --}}
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family={DisplayFont}:wght@400;600;700;800&family={BodyFont}:wght@400;500;600&display=swap" rel="stylesheet">

    @vite(['resources/css/app.css', 'resources/js/app.js'])
</head>
<body class="bg-bg text-fg font-body antialiased">
    <x-layout.navbar />
    <main>
        {{ $slot }}
    </main>
    <x-layout.footer />

    {{-- Remove if not a local PH/SEA business --}}
    <x-whatsapp-button :phone="config('site.phone')" message="Hi! I found you on your website." />

    {{-- LocalBusiness structured data --}}
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "LocalBusiness",
      "name": "{{ config('site.name') }}",
      "description": "{{ config('site.description') }}",
      "url": "{{ config('site.url') }}",
      "telephone": "+{{ config('site.phone') }}",
      "address": {
        "@type": "PostalAddress",
        "streetAddress": "{{ config('site.address') }}"
      }
    }
    </script>
</body>
</html>
```

## Page Views

`resources/views/home.blade.php`:

```blade
<x-layouts.site
    title="{{ config('site.pages.home.title') }}"
    description="{{ config('site.pages.home.description') }}"
>
    <x-home.hero />
    <x-home.services />
    <x-home.testimonials />
</x-layouts.site>
```

`resources/views/contact.blade.php`:

```blade
<x-layouts.site
    title="{{ config('site.pages.contact.title') }}"
    description="{{ config('site.pages.contact.description') }}"
>
    <section class="py-24 px-4 max-w-2xl mx-auto">
        <h1 class="font-display text-4xl font-bold mb-8">Contact Us</h1>
        <x-contact.form />
    </section>
</x-layouts.site>
```

## Routes

`routes/web.php`:

```php
<?php

use App\Http\Controllers\ContactController;

Route::view('/', 'home')->name('home');
Route::view('/about', 'about')->name('about');
Route::view('/services', 'services')->name('services');
Route::view('/contact', 'contact')->name('contact');

Route::post('/contact', [ContactController::class, 'store'])->name('contact.store');

// Sitemap
Route::get('/sitemap.xml', function () {
    $sitemap = simplexml_load_string('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"></urlset>');
    foreach (['/', '/about', '/services', '/contact'] as $path) {
        $url = $sitemap->addChild('url');
        $url->addChild('loc', config('site.url') . $path);
        $url->addChild('changefreq', 'monthly');
        $url->addChild('priority', $path === '/' ? '1.0' : '0.8');
    }
    return response($sitemap->asXML(), 200)->header('Content-Type', 'application/xml');
})->name('sitemap');

// Robots.txt
Route::get('/robots.txt', function () {
    return response("User-agent: *\nAllow: /\nSitemap: " . config('site.url') . "/sitemap.xml", 200)
        ->header('Content-Type', 'text/plain');
});
```

## Contact Controller

`app/Http/Controllers/ContactController.php`:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

class ContactController extends Controller
{
    public function store(Request $request)
    {
        $validated = $request->validate([
            'name'    => 'required|string|max:255',
            'email'   => 'required|email',
            'phone'   => 'nullable|string|max:50',
            'message' => 'required|string|max:5000',
        ]);

        // Honeypot check (add a hidden "website" field to the form)
        if ($request->filled('website')) {
            return back()->with('success', "Message received. We'll be in touch soon.");
        }

        // TODO: wire to mail (Mail::to(...)->send(new ContactMail($validated)))
        // For now: log submission
        logger()->info('Contact form submission', $validated);

        return back()->with('success', "Message received. We'll be in touch soon.");
    }
}
```

## Contact Form Component

`resources/views/components/contact/form.blade.php`:

```blade
<form
    action="{{ route('contact.store') }}"
    method="POST"
    x-data="{ loading: false }"
    @submit="loading = true"
    class="space-y-4"
>
    @csrf

    {{-- Honeypot --}}
    <input type="text" name="website" class="hidden" autocomplete="off" tabindex="-1">

    @if (session('success'))
        <p class="text-green-600 font-medium">{{ session('success') }}</p>
    @endif

    <input type="text" name="name" value="{{ old('name') }}" placeholder="Your name" required
           class="w-full px-4 py-3 border rounded-lg @error('name') border-red-500 @enderror">
    @error('name') <p class="text-red-500 text-sm">{{ $message }}</p> @enderror

    <input type="email" name="email" value="{{ old('email') }}" placeholder="Email address" required
           class="w-full px-4 py-3 border rounded-lg @error('email') border-red-500 @enderror">
    @error('email') <p class="text-red-500 text-sm">{{ $message }}</p> @enderror

    <input type="tel" name="phone" value="{{ old('phone') }}" placeholder="Phone (optional)"
           class="w-full px-4 py-3 border rounded-lg">

    <textarea name="message" placeholder="Your message" required rows="4"
              class="w-full px-4 py-3 border rounded-lg resize-none @error('message') border-red-500 @enderror">{{ old('message') }}</textarea>
    @error('message') <p class="text-red-500 text-sm">{{ $message }}</p> @enderror

    <button type="submit" :disabled="loading"
            class="w-full px-6 py-3 bg-accent text-white rounded-lg font-medium transition hover:opacity-90 disabled:opacity-60">
        <span x-show="!loading">Send Message</span>
        <span x-show="loading">Sending...</span>
    </button>
</form>
```

## WhatsApp Blade Component

`resources/views/components/whatsapp-button.blade.php`:

```blade
@props([
    'phone',           // E.164 without +: e.g., "639171234567"
    'message' => null,
])

@php
$url = $message
    ? 'https://wa.me/' . $phone . '?text=' . urlencode($message)
    : 'https://wa.me/' . $phone;
@endphp

<a
    href="{{ $url }}"
    target="_blank"
    rel="noopener noreferrer"
    aria-label="Chat on WhatsApp"
    class="fixed bottom-6 right-6 z-50 flex h-14 w-14 items-center justify-center rounded-full bg-[#25D366] shadow-lg transition-transform hover:scale-110 focus:outline-none focus:ring-2 focus:ring-[#25D366] focus:ring-offset-2"
>
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="white" class="h-7 w-7" aria-hidden="true">
        <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/>
    </svg>
</a>
```

## Tailwind Config

`tailwind.config.js`:

```js
export default {
  content: [
    './resources/**/*.blade.php',
    './resources/**/*.js',
  ],
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

`resources/css/app.css`:

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

## Alpine.js for Interactivity

`resources/js/app.js`:

```js
import Alpine from 'alpinejs'
window.Alpine = Alpine
Alpine.start()
```

Install:

```bash
npm install alpinejs
```

## Dev + Build Commands

```bash
# Run both in separate terminals
php artisan serve          # http://localhost:8000
npm run dev                # Vite HMR for assets

# Or use Laravel Herd (auto-serves at {project-name}.test)

npm run build              # compile assets for production
php artisan optimize       # cache config, routes, views for production
```

## Vercel / Netlify Deploy

Laravel requires a PHP host — Vercel and Netlify do not support PHP natively. Options:

| Host | Notes |
|---|---|
| **Laravel Cloud** | First-party — simplest, scalable |
| **Forge + DigitalOcean** | Full control, $6–12/mo droplet |
| **Railway** | Docker-based, easy setup |
| **Render** | Free tier available for small sites |

Add deploy steps to `DEPLOY.md` based on chosen host. The default guide should recommend Laravel Cloud or Forge.

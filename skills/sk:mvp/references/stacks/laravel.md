# Laravel + Blade + Tailwind — Stack Reference

## Scaffold

```bash
composer create-project laravel/laravel {project-name}
cd {project-name}
npm install
```

Laravel ships with Tailwind and Vite out of the box (Laravel 11+).

## Directory Structure

```
{project-name}/
├── resources/
│   ├── views/
│   │   ├── layouts/
│   │   │   ├── landing.blade.php      ← landing page layout
│   │   │   └── app.blade.php          ← app layout (sidebar)
│   │   ├── components/
│   │   │   ├── landing/
│   │   │   │   ├── navbar.blade.php
│   │   │   │   ├── hero.blade.php
│   │   │   │   ├── features.blade.php
│   │   │   │   ├── how-it-works.blade.php
│   │   │   │   ├── pricing.blade.php
│   │   │   │   ├── testimonials.blade.php
│   │   │   │   ├── waitlist-form.blade.php
│   │   │   │   └── footer.blade.php
│   │   │   ├── app/
│   │   │   │   ├── sidebar.blade.php
│   │   │   │   └── {feature components}
│   │   │   └── ui/
│   │   │       ├── button.blade.php
│   │   │       ├── input.blade.php
│   │   │       ├── card.blade.php
│   │   │       └── modal.blade.php
│   │   ├── landing.blade.php          ← landing page
│   │   ├── dashboard.blade.php        ← dashboard
│   │   ├── {feature-1}.blade.php
│   │   ├── {feature-2}.blade.php
│   │   └── settings.blade.php
│   ├── css/
│   │   └── app.css                    ← Tailwind directives + custom vars
│   └── js/
│       └── app.js                     ← Vite entry + Alpine.js for interactivity
├── routes/
│   └── web.php                        ← all routes
├── app/
│   └── Http/
│       └── Controllers/
│           └── WaitlistController.php
├── storage/
│   └── app/
│       └── waitlist.json              ← email storage (auto-created)
├── public/
│   └── {compiled assets}
├── tailwind.config.js
├── vite.config.js
└── package.json
```

## Routes

`routes/web.php`:

```php
use App\Http\Controllers\WaitlistController;

// Landing page
Route::view('/', 'landing');

// App pages
Route::view('/dashboard', 'dashboard');
Route::view('/{feature-1}', '{feature-1}');
Route::view('/{feature-2}', '{feature-2}');
Route::view('/settings', 'settings');

// Waitlist API
Route::post('/api/waitlist', [WaitlistController::class, 'store']);
```

## Layouts

### Landing Layout (`resources/views/layouts/landing.blade.php`)

```blade
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ $title ?? '{Product Name}' }}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family={DisplayFont}:wght@400;600;700;800&family={BodyFont}:wght@400;500;600&display=swap" rel="stylesheet">
    @vite(['resources/css/app.css', 'resources/js/app.js'])
</head>
<body class="bg-bg text-fg font-body antialiased">
    {{ $slot }}
</body>
</html>
```

### App Layout (`resources/views/layouts/app.blade.php`)

```blade
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ $title ?? '{Product Name}' }}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family={DisplayFont}:wght@400;600;700;800&family={BodyFont}:wght@400;500;600&display=swap" rel="stylesheet">
    @vite(['resources/css/app.css', 'resources/js/app.js'])
</head>
<body class="bg-bg text-fg font-body antialiased">
    <div class="flex min-h-screen">
        <x-app.sidebar />
        <main class="flex-1 p-6 lg:p-8">
            {{ $slot }}
        </main>
    </div>
</body>
</html>
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
      },
      fontFamily: {
        display: ['{DisplayFont}', 'serif'],
        body: ['{BodyFont}', 'sans-serif'],
      },
    },
  },
}
```

CSS variables in `resources/css/app.css`:

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

## Interactivity with Alpine.js

Install Alpine.js for lightweight interactivity (modals, toasts, form states):

```bash
npm install alpinejs
```

`resources/js/app.js`:

```js
import Alpine from 'alpinejs'
window.Alpine = Alpine
Alpine.start()
```

## Waitlist Controller

`app/Http/Controllers/WaitlistController.php`:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Storage;

class WaitlistController extends Controller
{
    public function store(Request $request)
    {
        $request->validate([
            'email' => 'required|email',
        ]);

        $email = $request->input('email');
        $path = 'waitlist.json';

        // Read or create
        $data = Storage::exists($path)
            ? json_decode(Storage::get($path), true)
            : ['entries' => []];

        // Check duplicate
        $exists = collect($data['entries'])->contains('email', $email);
        if ($exists) {
            return response()->json(['success' => true, 'message' => "You're already on the list!"]);
        }

        // Append
        $data['entries'][] = [
            'email' => $email,
            'timestamp' => now()->toISOString(),
            'source' => 'landing-page',
        ];

        Storage::put($path, json_encode($data, JSON_PRETTY_PRINT));

        return response()->json(['success' => true, 'message' => "You're on the list!"]);
    }
}
```

## Blade Component Patterns

### Anonymous Components (preferred for UI)

`resources/views/components/ui/button.blade.php`:

```blade
@props(['variant' => 'primary', 'size' => 'md'])

@php
$classes = match($variant) {
    'primary' => 'bg-accent text-white hover:opacity-90',
    'secondary' => 'border border-accent text-accent hover:bg-accent/10',
    'ghost' => 'text-fg hover:bg-muted/20',
};
$sizes = match($size) {
    'sm' => 'px-4 py-2 text-sm',
    'md' => 'px-6 py-3 text-base',
    'lg' => 'px-8 py-4 text-lg',
};
@endphp

<button {{ $attributes->merge(['class' => "$classes $sizes rounded-xl font-medium transition-all duration-200"]) }}>
    {{ $slot }}
</button>
```

Usage: `<x-ui.button variant="primary">Join Waitlist</x-ui.button>`

### Landing Page

`resources/views/landing.blade.php`:

```blade
<x-layouts.landing>
    <x-landing.navbar />
    <x-landing.hero />
    <x-landing.features />
    <x-landing.how-it-works />
    <x-landing.pricing />
    <x-landing.testimonials />
    <x-landing.waitlist-form />
    <x-landing.footer />
</x-layouts.landing>
```

### Waitlist Form with Alpine.js

```blade
<div x-data="{ email: '', status: 'idle', message: '' }">
    <form @submit.prevent="
        status = 'loading';
        fetch('/api/waitlist', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'X-CSRF-TOKEN': '{{ csrf_token() }}' },
            body: JSON.stringify({ email })
        })
        .then(r => r.json())
        .then(d => { status = 'success'; message = d.message; })
        .catch(() => { status = 'error'; message = 'Something went wrong.'; })
    ">
        <template x-if="status !== 'success'">
            <div class="flex gap-3">
                <input x-model="email" type="email" placeholder="you@example.com" required
                       class="flex-1 px-4 py-3 rounded-lg border focus:ring-2 focus:ring-accent" />
                <x-ui.button type="submit" x-bind:disabled="status === 'loading'">
                    <span x-show="status !== 'loading'">Join Waitlist</span>
                    <span x-show="status === 'loading'">Joining...</span>
                </x-ui.button>
            </div>
        </template>
        <p x-show="status === 'success'" x-text="message" class="text-green-600 font-medium"></p>
        <p x-show="status === 'error'" x-text="message" class="text-red-500 text-sm mt-2"></p>
    </form>
</div>
```

## Dev Server

```bash
# Run both in separate terminals (or use Concurrently)
php artisan serve          # http://localhost:8000
npm run dev                # Vite dev server for assets
```

Or use Laravel Herd if available (auto-serves at `{project-name}.test`).

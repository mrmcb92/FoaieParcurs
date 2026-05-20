const CACHE = 'foaie-parcurs-v1';

// Fișiere care se cachează la instalare (app shell)
const SHELL = [
  '/',
  '/static/manifest.json',
];

// Instalare: cache app shell
self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE).then(c => c.addAll(SHELL))
  );
  self.skipWaiting();
});

// Activare: șterge cache-urile vechi
self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))
    )
  );
  self.clients.claim();
});

// Fetch: network-first pentru API, cache-first pentru app shell
self.addEventListener('fetch', e => {
  const url = new URL(e.request.url);

  // API: mereu din rețea, fără cache
  if (url.pathname.startsWith('/api/')) {
    e.respondWith(fetch(e.request));
    return;
  }

  // Fonturi Google: cache-first
  if (url.hostname === 'fonts.googleapis.com' || url.hostname === 'fonts.gstatic.com') {
    e.respondWith(
      caches.match(e.request).then(cached => {
        if (cached) return cached;
        return fetch(e.request).then(res => {
          const copy = res.clone();
          caches.open(CACHE).then(c => c.put(e.request, copy));
          return res;
        });
      })
    );
    return;
  }

  // App shell: network-first cu fallback pe cache
  e.respondWith(
    fetch(e.request)
      .then(res => {
        const copy = res.clone();
        caches.open(CACHE).then(c => c.put(e.request, copy));
        return res;
      })
      .catch(() => caches.match(e.request).then(cached => cached || caches.match('/')))
  );
});

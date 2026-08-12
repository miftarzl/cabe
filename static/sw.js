// ============================================================
// Service Worker — Klinik Daun Cabai PWA
// Versi: 1.0.0
// Strategi: Cache-First untuk aset statis, Network-First untuk API
// ============================================================

const CACHE_NAME = 'klinik-daun-cabai-v1';
const OFFLINE_URL = '/offline';

// Aset yang langsung di-cache saat install (pre-cache)
const PRECACHE_ASSETS = [
  '/',
  '/static/style.css',
  '/static/script.js',
  '/static/icons/icon-192.png',
  '/static/icons/icon-512.png',
  '/manifest.json',
];

// ── INSTALL ──────────────────────────────────────────────────
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      console.log('[SW] Pre-caching aset utama');
      return cache.addAll(PRECACHE_ASSETS);
    })
  );
  // Aktifkan service worker baru langsung tanpa menunggu tab lama ditutup
  self.skipWaiting();
});

// ── ACTIVATE ─────────────────────────────────────────────────
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames
          .filter((name) => name !== CACHE_NAME)
          .map((name) => {
            console.log('[SW] Menghapus cache lama:', name);
            return caches.delete(name);
          })
      );
    })
  );
  // Ambil kendali semua tab yang terbuka segera
  self.clients.claim();
});

// ── FETCH ─────────────────────────────────────────────────────
self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);

  // Hanya tangani request dari origin yang sama
  if (url.origin !== self.location.origin) return;

  // ── API /predict: Network-First (butuh koneksi, tidak di-cache) ──
  if (url.pathname.startsWith('/predict')) {
    event.respondWith(
      fetch(request).catch(() => {
        return new Response(
          JSON.stringify({
            success: false,
            error: 'Tidak ada koneksi internet. Diagnosis memerlukan koneksi aktif untuk menjalankan model AI.',
          }),
          {
            status: 503,
            headers: { 'Content-Type': 'application/json' },
          }
        );
      })
    );
    return;
  }

  // ── Aset statis: Cache-First ──────────────────────────────
  if (
    url.pathname.startsWith('/static/') ||
    url.pathname === '/manifest.json'
  ) {
    event.respondWith(
      caches.match(request).then((cached) => {
        if (cached) return cached;
        return fetch(request).then((response) => {
          if (!response || response.status !== 200) return response;
          const clone = response.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(request, clone));
          return response;
        });
      })
    );
    return;
  }

  // ── Halaman HTML: Network-First + fallback cache ──────────
  if (request.mode === 'navigate') {
    event.respondWith(
      fetch(request)
        .then((response) => {
          if (!response || response.status !== 200) return response;
          const clone = response.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(request, clone));
          return response;
        })
        .catch(() => {
          return caches.match('/').then((cached) => {
            if (cached) return cached;
            // Fallback offline minimal
            return new Response(
              `<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>Offline — Klinik Daun Cabai</title>
  <style>
    *{margin:0;padding:0;box-sizing:border-box}
    body{background:#0d0d0d;color:#fff;font-family:Inter,sans-serif;
         display:flex;align-items:center;justify-content:center;
         min-height:100vh;text-align:center;padding:2rem}
    .icon{font-size:4rem;margin-bottom:1rem}
    h1{font-size:1.5rem;color:#c0392b;margin-bottom:.5rem}
    p{color:#aaa;line-height:1.6;max-width:360px}
    button{margin-top:1.5rem;padding:.75rem 2rem;background:#c0392b;
           color:#fff;border:none;border-radius:8px;cursor:pointer;
           font-size:1rem}
  </style>
</head>
<body>
  <div>
    <div class="icon">🌶️</div>
    <h1>Tidak Ada Koneksi</h1>
    <p>Aplikasi Klinik Daun Cabai memerlukan koneksi internet untuk menjalankan diagnosis AI. Periksa koneksimu dan coba lagi.</p>
    <button onclick="location.reload()">Coba Lagi</button>
  </div>
</body>
</html>`,
              { headers: { 'Content-Type': 'text/html; charset=utf-8' } }
            );
          });
        })
    );
    return;
  }
});

// ── BACKGROUND SYNC (opsional, untuk retry jika offline) ─────
self.addEventListener('sync', (event) => {
  if (event.tag === 'retry-predict') {
    console.log('[SW] Background sync: retry-predict');
  }
});

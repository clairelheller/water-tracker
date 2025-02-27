self.addEventListener('install', event => {
    event.waitUntil(
        caches.open('water-tracker-cache').then(cache => {
            return cache.addAll([
                '/',
                '/static/style.css',
                '/static/script.js',
                'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css'
            ]);
        })
    );
});

self.addEventListener('fetch', event => {
    event.respondWith(
        caches.match(event.request).then(response => {
            return response || fetch(event.request);
        })
    );
});

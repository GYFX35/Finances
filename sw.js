const CACHE_NAME = 'my-sfn-cache-v1';
const URLS_TO_CACHE = [
    '/', // Home page
    '/offline', // The offline fallback page
    '/static/style.css', // Main stylesheet
    // Add other essential static assets or core app shell URLs if desired
    // For example, if you have a main JS file: '/static/main.js'
    // Manifest should be fetched by browser, not usually cached by SW itself.
];

// Install event: Caches core assets
self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then((cache) => {
                console.log('Opened cache and caching core assets');
                return cache.addAll(URLS_TO_CACHE);
            })
            .catch((err) => {
                console.error('Failed to cache core assets:', err);
            })
    );
    self.skipWaiting(); // Force the waiting service worker to become the active service worker
});

// Activate event: Cleans up old caches
self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((cacheName) => {
                    if (cacheName !== CACHE_NAME) {
                        console.log('Deleting old cache:', cacheName);
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
    return self.clients.claim(); // Take control of all open clients once activated
});

// Fetch event: Serves assets from cache or network, with offline fallback
self.addEventListener('fetch', (event) => {
    event.respondWith(
        // Try to find the response in the cache first
        caches.match(event.request)
            .then((cachedResponse) => {
                // Return cached response if found
                if (cachedResponse) {
                    // console.log('Serving from cache:', event.request.url);
                    return cachedResponse;
                }

                // If not in cache, try to fetch from the network
                // console.log('Fetching from network:', event.request.url);
                return fetch(event.request).then((networkResponse) => {
                    // If fetch is successful, clone it and store in cache
                    if (networkResponse && networkResponse.status === 200) {
                        const responseToCache = networkResponse.clone();
                        caches.open(CACHE_NAME)
                            .then((cache) => {
                                // console.log('Caching new resource:', event.request.url);
                                cache.put(event.request, responseToCache);
                            });
                    }
                    return networkResponse;
                }).catch(() => {
                    // If network fetch fails (e.g., offline)
                    console.log('Network request failed. Serving offline page for navigation or if asset not cached.');
                    // For navigation requests, serve the offline page.
                    if (event.request.mode === 'navigate') {
                        return caches.match('/offline');
                    }
                    // For other requests (e.g. images, non-critical scripts),
                    // they will fail if not already in cache and network is down.
                    // You could return a placeholder for images here if needed.
                    return new Response("Network error occurred", {
                        status: 408,
                        headers: { "Content-Type": "text/plain" },
                    });
                });
            })
    );
});

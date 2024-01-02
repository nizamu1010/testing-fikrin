const staticCacheName = 'site-static-1';
const dynamicCacheName = 'site-dynamic-1';
const assets = [
    '/',
    '/static/css/bootstrap.min.css',
    '/static/css/comment-styles.css',
    '/static/css/index-styles.css',
    '/static/css/login-styles.css',
    '/static/css/profile-styles.css',
    '/static/css/styles.css',
    '/static/js/app.js',
    '/static/js/bootstrap.bundle.min.js',
    '/static/js/cropper.js',
    '/static/js/index.js',
    '/static/js/ui.js',
];

// Limit cache size
const cacheLimit = 50;

// Cache static assets on install
self.addEventListener('install', evt => {
    evt.waitUntil(
        caches.open(staticCacheName).then(cache => {
            console.log('Caching shell assets');
            return cache.addAll(assets);
        })
    );
});

// Clear old caches on activate
self.addEventListener('activate', evt => {  
    evt.waitUntil(
        caches.keys().then(keys => {
            return Promise.all(keys
                .filter(key => key !== staticCacheName && key !== dynamicCacheName)
                .map(key => caches.delete(key))
            );
        })
    );
});

// Cache then network strategy
const cacheThenNetwork = async (request) => {
    const cachedResponse = await caches.match(request);
    if (cachedResponse) {
        return cachedResponse;
    }

    try {
        const networkResponse = await fetch(request);
        const cache = await caches.open(dynamicCacheName);
        cache.put(request, networkResponse.clone());
        return networkResponse;
    } catch (err) {
        // Handle fetch errors (offline)
        console.error('Error fetching data:', err);
    }
};

// Fetch event with caching strategies
self.addEventListener('fetch', evt => {
    if (evt.request.url.includes('/api/')) {
        // Network-first strategy for API requests
        evt.respondWith(cacheThenNetwork(evt.request));
    } else {
        // Cache-first strategy for other requests
        evt.respondWith(
            caches.match(evt.request).then(cacheRes => {
                return cacheRes || cacheThenNetwork(evt.request);
            })
        );
    }
});

// Limit the cache size by removing old items
const limitCacheSize = async (cacheName, size) => {
    const cache = await caches.open(cacheName);
    const keys = await cache.keys();
    if (keys.length > size) {
        cache.delete(keys[0]).then(limitCacheSize(cacheName, size)); // Recursively check and delete until size is met
    }
};

// Listen for message from client
self.addEventListener('message', evt => {
    if (evt.data.action === 'cleanCache') {
        // Clean up the dynamic cache on demand
        caches.open(dynamicCacheName).then(cache => {
            cache.keys().then(keys => {
                keys.forEach(key => {
                    cache.delete(key);
                });
            });
        });
    }
});

// Run cache size check on dynamic cache after each fetch
self.addEventListener('fetch', evt => {
    if (evt.request.url.includes('/static/')) {
        // Only check cache size for static assets
        evt.waitUntil(limitCacheSize(staticCacheName, cacheLimit));
    }
});


// cloud messaging 

import { initializeApp } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-app.js";
import { getAnalytics } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-analytics.js";


const firebaseConfig = {
apiKey: "AIzaSyDkyNO4aWT4qVCVJwkcb354_Rtc-TdFybk",
authDomain: "fknpj-9c7bb.firebaseapp.com",
projectId: "fknpj-9c7bb",
storageBucket: "fknpj-9c7bb.appspot.com",
messagingSenderId: "624374608791",
appId: "1:624374608791:web:143bdac26d9762dcbb0ad2",
measurementId: "G-93ZXLVMBCF"
};

const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);


const staticCacheName = 'site-static-1';
const assets = [
    '/',
    '/static/css/bootstrap.min.css', '/static/css/comment-styles.css', '/static/css/index-styles.css', '/static/css/login-styles.css',  '/static/css/profile-styles.css',  '/static/css/styles.css',
    '/static/js/app.js','/static/js/bootstrap.bundle.min.js',  '/static/js/cropper.js',  '/static/js/index.js', '/static/js/ui.js',
];

// install service worker
self.addEventListener('install', evt => {
    evt.waitUntil(
        caches.open(staticCacheName).then(cache => {
        console.log('caching shell assets');
        cache.addAll(assets);
        })
    );
});
    
// activate event
self.addEventListener('activate', evt => {  
    evt.waitUntil(
        caches.keys().then(keys => {
        return Promise.all(keys
            .filter(key => key !== staticCacheName)
            .map(key => caches.delete(key))
            )
        })
    );
});


// fetch event
self.addEventListener('fetch', evt => {
    //console.log('fetch event', evt);
    evt.respondwith(
        caches.match(evt.request).then(cacheRes => {
            return cacheRes || fetch(evt.request);
        })
    );
});





var CACHE_NAME = 'my-site-cache-v1';
var urlsToCache = [
  '/',
  
];

self.addEventListener('install', function(event) {
  event.waitUntil(
    caches.open(CACHE_NAME).then(function(cache) {
      console.log('Opened cache');
      return cache.addAll(urlsToCache);
    })
  );
});

self.addEventListener('fetch', function(event) {
  event.respondWith(
    fetch(event.request)
      .then(function(result) {
        return caches.open(CACHE_NAME).then(function(c) {
          c.put(event.request.url, result.clone());
          return result;
        });
      })
      .catch(function(e) {
        return caches.match(event.request);
      })
  );
});

// Check for updates
self.addEventListener('activate', function(event) {
  event.waitUntil(
    caches.keys().then(function(cacheNames) {
      return Promise.all(
        cacheNames.map(function(cacheName) {
          if (cacheName !== CACHE_NAME) {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});

// Automatic updates
self.addEventListener('message', function(event) {
  if (event.data === 'skipWaiting') {
    self.skipWaiting();
  }
});

// codigo para notificaciones push

importScripts("https://www.gstatic.com/firebasejs/8.10.0/firebase-app.js") ;
importScripts("https://www.gstatic.com/firebasejs/8.10.0/firebase-analytics.js") ;
importScripts("https://www.gstatic.com/firebasejs/8.10.0/firebase-messaging.js") ; 

var firebaseConfig = {
  apiKey: "AIzaSyDkyNO4aWT4qVCVJwkcb354_Rtc-TdFybk",
  authDomain: "fknpj-9c7bb.firebaseapp.com",
  projectId: "fknpj-9c7bb",
  storageBucket: "fknpj-9c7bb.appspot.com",
  messagingSenderId: "624374608791",
  appId: "1:624374608791:web:143bdac26d9762dcbb0ad2",
  measurementId: "G-93ZXLVMBCF"
};

// Initialize Firebase
firebase.initializeApp(firebaseConfig);

// Get Firebase Messaging instance
let messaging = firebase.messaging();


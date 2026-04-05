importScripts('https://storage.googleapis.com/workbox-cdn/releases/6.0.2/workbox-sw.js');

self.__WB_MANIFEST = [];

const CACHE_NAME = 'staking-dashboard-pwa';

const { precacheAndRoute } = self.workbox.precaching;
const { registerRoute } = self.workbox.routing;
const { CacheFirst, StaleWhileRevalidate } = self.workbox.strategies;
const { ExpirationPlugin } = self.workbox.expiration;
const { CacheableResponse } = self.workbox.cacheableResponse;

self.workbox.precaching.precacheAndRoute(self.__WB_MANIFEST);

// Cache first for static assets
registerRoute(
  new RegExp('/static/.*'),
  new CacheFirst({
    cacheName: 'static-resources',
    plugins: [
      new CacheableResponse({ statuses: [200] })
    ]
  })
);

// Cache first for images
registerRoute(
  new RegExp('/img/.*'),
  new CacheFirst({
    cacheName: 'image-cache',
    plugins: [
      new CacheableResponse({ statuses: [200] }),
      new ExpirationPlugin({
        maxEntries: 50,
        maxAgeSeconds: 30 * 24 * 60 * 60
      })
    ]
  })
);

// Network first for API requests
registerRoute(
  new RegExp('/api/.*'),
  new StaleWhileRevalidate({
    cacheName: 'api-cache',
    plugins: [
      new CacheableResponse({ statuses: [200] })
    ]
  })
);

// Cache first for the main document
registerRoute(
  new RegExp('/$'),
  new CacheFirst({
    cacheName: 'main-page',
    plugins: [
      new CacheableResponse({ statuses: [200] })
    ]
  })
);
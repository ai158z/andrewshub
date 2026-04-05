importScripts('https://storage.googleapis.com/workbox-cdn/releases/6.0.2/workbox-sw.js');

self.__WB_MANIFEST = [];

const CACHE_NAME = 'staking-dashboard-pwa';

const { precacheAndRoute } = self.workbox.precaching;
const { registerRoute } = self.workbox.routing;
const { CacheFirst, StaleWhileRevalidate } = self.workbox.strategies;
const { ExpirationPlugin } = self.workbox.expiration;
const { CacheableResponse } = self.workbox.cacheableResponse;

const { precache } = self.workbox.precaching;
const { cacheNames } = self.workbox.core;

// Precache the assets
precache(self.__WB_MANIFEST);
precacheAndRoute(self.____WB_MANIFEST);

// Cache strategies
registerRoute(
  new RegExp('/static/.*'),
  new CacheFirst({
    cacheName: 'static-resources',
    plugins: [
      new CacheableResponse({
        statuses: [200]
      })
    ]
  })
);

registerRoute(
  new RegExp('/api/.*'),
  new StaleWhileRevalidate({
    cacheName: 'api-cache',
    plugins: [
      new CacheableResponse({
        statuses: [200]
      })
    ]
  })
);

registerRoute(
  new RegExp('/'),
  new CacheFirst({
    cacheName: 'static-resources',
    plugins: [
      new CacheableResponse({
        statuses: [200]
      })
    ]
  })
);

registerRoute(
  new RegExp('/img/.*'),
  new CacheFirst({
    cacheName: 'image-cache',
    plugins: [
      new CacheableResponse({
        statuses: [200]
      })
    ]
  })
);

// Fallback route
registerRoute(
  new RegExp('.*'),
  new CacheFirst({
    cacheName: 'static-resources',
    plugins: [
      new CacheableResponse({
        statuses: [200]
      })
    ]
  })
);
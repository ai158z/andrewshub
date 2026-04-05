import { Workbox } from 'workbox-window';

const isLocalhost = Boolean(
  window.location.hostname === 'localhost' ||
  window.location.hostname === '[::1]' ||
  window.location.hostname.match(
    /^127(?:\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9]{3})){3}$/
  )
);

export function register(config) {
  if (typeof process.env.PUBLIC_URL === 'undefined' || process.env.PUBLIC_URL === null) {
    process.env.PUBLIC_URL = '';
  }
  
  if ('serviceWorker' in navigator) {
    const publicUrl = new URL(process.env.PUBLIC_URL, window.location);
    if (publicUrl.origin !== window.location.origin) {
      return;
    }

    const swUrl = `${process.env.PUBLIC_URL}/service-worker.js`;
    
    if (isLocalhost) {
      checkValidServiceWorker(swUrl);
    } else {
      registerValidSW(swUrl);
    }
  }
}

function registerValidSW(swUrl) {
  const wb = new Workbox(swUrl);
  
  wb.addEventListener('waiting', (event) => {
    if (window.confirm('New content is available and ready to be installed. Would you like to update?')) {
      wb.messageSkipWaiting();
    }
  });

  wb.addEventListener('controlling', () => {
    window.location.reload();
  });

  wb.register();
}

function checkValidServiceWorker(swUrl) {
  fetch(swUrl, {
    headers: { 'Service-Worker': 'script' }
  })
    .then(response => {
      const contentType = response.headers.get('content-type');
      if (response.status === 404 || (contentType && !contentType.includes('javascript'))) {
        navigator.serviceWorker.ready.then(registration => {
          registration.unregister().then(() => {
            window.location.reload();
          });
        });
      } else {
        registerValidSW(swUrl);
      }
    })
    .catch(() => {
      console.log('No internet connection found. App is running in offline mode.');
    });
}
import React, { useState, useEffect } from 'react';
import { get, set, del } from 'idb-keyval';
import NotificationBanner from './NotificationBanner';

const NOTIFICATION_PERMISSION_KEY = 'notification-perms';
const SUBSCRIPTION_KEY = 'push-subscription';
const NOTIFICATION_QUEUE_KEY = 'notification-queue';

const NotificationManager = () => {
  const [isSupported, setIsSupported] = useState(false);
  const [permission, setPermission] = useState(Notification.permission);
  const [registration, setRegistration] = useState(null);
  const [notifications, setNotifications] = useState([]);
  const [isOnline, setIsOnline] = useState(navigator.onLine);

  // Check if service worker and notifications are supported
  useEffect(() => {
    if ('serviceWorker' in navigator && 'PushManager' in window) {
      setIsSupported(true);
      navigator.serviceWorker.ready.then(reg => {
        setRegistration(reg);
      });
    }
  }, []);

  // Update online status
  useEffect(() => {
    const handleOnline = () => setIsOnline(true);
    const handleOffline = () => setIsOnline(false);
    
    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);
    
    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);

  const requestNotificationPermission = async () => {
    if (!isSupported) return;
    
    try {
      const perm = await Notification.requestPermission();
      setPermission(perm);
      await set(NOTIFICATION_PERMISSION_KEY, perm);
      return perm;
    } catch (error) {
      console.error('Failed to request notification permission:', error);
      return 'denied';
    }
  };

  const subscribeToPush = async () => {
    if (!registration || !isSupported) return null;
    
    try {
      const subscription = await registration.pushManager.subscribe({
        userVisibleOnly: true,
        applicationServerKey: process.env.VAPID_PUBLIC_KEY
      });
      
      await set(SUBSCRIPTION_KEY, subscription.toJSON());
      return subscription;
    } catch (error) {
      console.error('Push subscription failed:', error);
      return null;
    }
  };

  const unsubscribeFromPush = async () => {
    if (!registration) return;
    
    try {
      const subscription = await registration.pushManager.getSubscription();
      if (subscription) {
        await subscription.unsubscribe();
        await del(SUBSCRIPTION_KEY);
      }
    } catch (error) {
      console.error('Unsubscribe failed:', error);
    }
  };

  const showNotification = async (title, options = {}) => {
    if (permission !== 'granted') {
      console.warn('Notifications not permitted');
      return;
    }

    if (isOnline) {
      new Notification(title, {
        body: options.body || '',
        icon: options.icon,
        ...options
      });
    } else {
      const newNotifications = [...notifications, { title, ...options }];
      setNotifications(newNotifications);
      await set(NOTIFICATION_QUEUE_KEY, newNotifications);
    }
  };

  const processQueuedNotifications = async () => {
    const queued = await get(NOTIFICATION_QUEUE_KEY);
    if (queued && queued.length > 0) {
      queued.forEach(notification => {
        new Notification(notification.title, notification);
      });
      await del(NOTIFICATION_QUEUE_KEY);
    }
  };

  const sendNotificationToServer = async (payload) => {
    if (!isSupported) return;

    try {
      const subscription = await get(SUBSCRIPTION_KEY);
      if (!subscription) return;

      await fetch('/api/notifications', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ...payload, subscription })
      });
    } catch (error) {
      console.error('Failed to send notification:', error);
    }
  };

  const registerBackgroundSync = async () => {
    if (!registration) return;
    
    if ('sync' in registration) {
      try {
        await registration.sync.register('sync-notifications');
      } catch (error) {
        console.error('Background sync registration failed:', error);
      }
    }
  };

  const initialize = async () => {
    if (!isSupported) return;

    try {
      const reg = await navigator.serviceWorker.register('/service-worker.js');
      setRegistration(reg);
      
      if (Notification.permission === 'default') {
        await requestNotificationPermission();
      }
      
      await subscribeToPush();
    } catch (error) {
      console.error('Service worker registration failed:', error);
    }
  };

  return (
    <div>
      <NotificationBanner 
        message={isOnline ? '' : 'You are currently offline. Notifications will be displayed when you come back online.'}
        type={isOnline ? 'info' : 'warning'}
        visible={!isOnline}
      />
    </div>
  );
};

export default NotificationManager;
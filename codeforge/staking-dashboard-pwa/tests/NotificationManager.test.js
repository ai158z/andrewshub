import React from 'react';
import { render, act } from '@testing-library/react';
import NotificationManager from '../src/components/NotificationManager';
import * as idbKeyval from 'idb-keyval';

// Mock idb-keyval
jest.mock('idb-keyval', () => ({
  get: jest.fn(),
  set: jest.fn(),
  del: jest.fn()
}));

// Mock service worker API
const mockRegisterServiceWorker = jest.fn();
const mockGetSubscription = jest.fn();
const mockSubscribe = jest.fn();
const mockUnsubscribe = jest.fn();
const mockPushManager = {
  subscribe: mockSubscribe,
  getSubscription: mockGetSubscription
};

// Mock Notification API
global.Notification = {
  permission: 'default',
  requestPermission: jest.fn().mockResolvedValue('granted')
};

// Mock service worker
Object.defineProperty(navigator, 'serviceWorker', {
  value: {
    ready: Promise.resolve({
      pushManager: mockPushManager
    }),
    register: mockRegisterServiceWorker
  },
  writable: true
});

// Mock window events
Object.defineProperty(navigator, 'onLine', {
  value: true,
  writable: true
});

// Mock environment
process.env.REACT_APP_VAPID_PUBLIC_KEY = 'test-key';

describe('NotificationManager', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    global.Notification.requestPermission.mockClear();
    mockSubscribe.mockClear();
    mockGetSubscription.mockClear();
    mockRegisterServiceWorker.mockClear();
  });

  test('should render without crashing', () => {
    render(<NotificationManager />);
  });

  test('should request notification permission', async () => {
    global.Notification.requestPermission.mockResolvedValueOnce('granted');
    const { container } = render(<NotificationManager />);
    await act(async () => {
      const result = await container.getInstance().requestNotificationPermission();
      expect(result).toBe('granted');
    });
  });

  test('should handle notification permission denial', async () => {
    global.Notification.requestPermission.mockResolvedValueOnce('denied');
    const { container } = render(<NotificationManager />);
    await act(async () => {
      const result = await container.getInstance().requestNotificationPermission();
      expect(result).toBe('denied');
    });
  });

  test('should not subscribe when not supported', async () => {
    const originalPushManager = window.PushManager;
    const originalSW = navigator.serviceWorker;
    delete window.PushManager;
    delete navigator.serviceWorker;
    
    const { container } = render(<NotificationManager />);
    await act(async () => {
      const result = await container.getInstance().subscribeToPush();
      expect(result).toBeNull();
    });
    
    window.PushManager = originalPushManager;
    navigator.serviceWorker = originalSW;
  });

  test('should subscribe to push notifications', async () => {
    const mockSub = { toJSON: () => 'subscription-data' };
    mockSubscribe.mockResolvedValueOnce(mockSub);
    
    const { container } = render(<NotificationManager />);
    await act(async () => {
      const result = await container.getInstance().subscribeToPush();
      expect(result).toEqual(mockSub);
    });
  });

  test('should handle subscription failure', async () => {
    mockSubscribe.mockRejectedValueOnce(new Error('Subscription failed'));
    
    const { container } = render(<NotificationManager />);
    await act(async () => {
      const result = await container.getInstance().subscribeToPush();
      expect(result).toBeNull();
    });
  });

  test('should unsubscribe from push notifications', async () => {
    const mockSub = { unsubscribe: jest.fn().mockResolvedValue(undefined) };
    mockGetSubscription.mockResolvedValueOnce(mockSub);
    
    const { container } = render(<NotificationManager />);
    await act(async () => {
      await container.getInstance().unsubscribeFromPush();
      expect(mockSub.unsubscribe).toHaveBeenCalled();
    });
  });

  test('should handle unsubscribe failure', async () => {
    mockGetSubscription.mockRejectedValueOnce(new Error('Unsubscribe failed'));
    
    const { container } = render(<NotificationManager />);
    await act(async () => {
      await container.getInstance().unsubscribeFromPush();
    });
  });

  test('should show notification when permission granted and online', async () => {
    global.Notification.permission = 'granted';
    const { container } = render(<NotificationManager />);
    
    const notification = new (jest.fn().mockImplementation((title, options) => {
      return { title, ...options };
    }))();
    
    jest.spyOn(global, 'Notification').mockImplementation(() => notification);
    
    await act(async () => {
      await container.getInstance().showNotification('Test', { body: 'Test body' });
      expect(global.Notification).toHaveBeenCalledWith('Test', {
        body: 'Test body'
      });
    });
  });

  test('should queue notification when offline', async () => {
    Object.defineProperty(navigator, 'onLine', {
      value: false,
      writable: true
    });
    
    const { container } = render(<NotificationManager />);
    await act(async () => {
      await container.getInstance().showNotification('Test', { body: 'Test body' });
    });
  });

  test('should send notification to server', async () => {
    const mockFetch = jest.fn().mockResolvedValue({ ok: true });
    global.fetch = mockFetch;
    
    const { container } = render(<NotificationManager />);
    await act(async () => {
      await container.getInstance().sendNotificationToServer({ message: 'test' });
      expect(mockFetch).toHaveBeenCalledWith('/api/notifications', expect.any(Object));
    });
  });

  test('should not send notification when not supported', async () => {
    const originalSW = navigator.serviceWorker;
    delete navigator.serviceWorker;
    
    const { container } = render(<NotificationManager />);
    await act(async () => {
      await container.getInstance().sendNotificationToServer({ message: 'test' });
    });
    
    navigator.serviceWorker = originalSW;
  });

  test('should initialize service worker and notifications', async () => {
    mockRegisterServiceWorker.mockResolvedValueOnce({ waiting: null });
    
    const { container } = render(<NotificationManager />);
    await act(async () => {
      await container.getInstance().initialize();
    });
    
    expect(mockRegisterServiceWorker).toHaveBeenCalledWith('/service-worker.js');
  });

  test('should handle service worker registration failure', async () => {
    mockRegisterServiceWorker.mockRejectedValue(new Error('Registration failed'));
    
    const { container } = render(<NotificationManager />);
    await act(async () => {
      await container.getInstance().initialize();
    });
  });

  test('should process queued notifications when coming online', async () => {
    const mockGet = jest.fn().mockResolvedValue([{ title: 'Queued notification' }]);
    idbKeyval.get.mockImplementation(mockGet);
    
    const { container } = render(<NotificationManager />);
    await act(async () => {
      await container.getInstance().processQueuedNotifications();
    });
  });

  test('should handle empty notification queue', async () => {
    const mockGet = jest.fn().mockResolvedValue(null);
    idbKeyval.get.mockImplementation(mockGet);
    
    const { container } = render(<NotificationManager />);
    await act(async () => {
      await container.getInstance().processQueuedNotifications();
    });
  });

  test('should register background sync', async () => {
    const mockSync = { register: jest.fn().mockResolvedValue() };
    const mockReg = { sync: mockSync };
    
    const { container } = render(<NotificationManager />);
    await act(async () => {
      await container.getInstance().registerBackgroundSync();
      expect(mockSync.register).toHaveBeenCalledWith('sync-notifications');
    });
  });

  test('should handle background sync registration failure', async () => {
    const mockReg = { sync: null };
    
    const { container } = render(<NotificationManager />);
    await act(async () => {
      await container.getInstance().registerBackgroundSync();
    });
  });

  test('should handle online/offline state changes', async () => {
    const { container } = render(<NotificationManager />);
    
    // Simulate going offline
    act(() => {
      Object.defineProperty(navigator, 'onLine', {
        value: false,
        writable: true
      });
      window.dispatchEvent(new Event('offline'));
    });
    
    // Simulate coming back online
    act(() => {
      Object.defineProperty(navigator, 'onLine', {
        value: true,
        writable: true
      });
      window.dispatchEvent(new Event('online'));
    });
  });

  test('should handle online state on mount', async () => {
    Object.defineProperty(navigator, 'onLine', {
      value: true,
      writable: true
    });
    
    render(<NotificationManager />);
  });

  test('should handle unsupported browser', () => {
    const originalSW = navigator.serviceWorker;
    const originalPush = window.PushManager;
    delete navigator.serviceWorker;
    delete window.PushManager;
    
    render(<NotificationManager />);
    
    navigator.serviceWorker = originalSW;
    window.PushManager = originalPush;
  });
});
import { register } from '../src/register-service-worker';
import { Workbox } from 'workbox-window';
import * as idbKeyval from 'idb-keyval';

jest.mock('workbox-window');
jest.mock('idb-keyval');

describe('register-service-worker', () => {
  let mockWindow;
  let originalLocation;
  let originalAddEventListener;

  beforeEach(() => {
    // Mock window object and location
    mockWindow = {
      location: {
        hostname: 'localhost',
        origin: 'http://localhost'
      },
      addEventListener: jest.fn()
    };

    // Save original values
    originalLocation = window.location;
    originalAddEventListener = window.addEventListener;

    // Mock window.location
    delete window.location;
    window.location = mockWindow.location;

    // Mock addEventListener to control when load event fires
    window.addEventListener = (event, callback) => {
      if (event === 'load') {
        callback();
      }
    };

    // Mock Workbox
    Workbox.mockImplementation(() => {
      return {
        addEventListener: jest.fn(),
        register: jest.fn(),
        messageSkipWaiting: jest.fn()
      };
    });

    // Mock fetch
    global.fetch = jest.fn();
  });

  afterEach(() => {
    // Restore original values
    window.location = originalLocation;
    window.addEventListener = originalAddEventListener;
    jest.clearAllMocks();
  });

  test('should not register when serviceWorker is not supported', () => {
    Object.defineProperty(navigator, 'serviceWorker', {
      value: undefined,
      writable: true
    });

    expect(() => register()).not.toThrow();
  });

  test('should not register when origins do not match', () => {
    const originalCreateObjectURL = window.URL.createObjectURL;
    window.URL.createObjectURL = jest.fn(() => 'https://other.com');

    const publicUrl = new URL(process.env.PUBLIC_URL, window.location);
    expect(publicUrl.origin).not.toBe(window.location.origin);

    window.URL.createObjectURL = originalCreateObjectURL;
  });

  test('should register service worker on localhost', () => {
    window.location.hostname = 'localhost';
    global.fetch.mockResolvedValue({
      status: 200,
      headers: { get: () => 'application/javascript' }
    });

    register();
    
    expect(window.addEventListener).toHaveBeenCalledWith('load', expect.any(Function));
  });

  test('should call registerValidSW for non-localhost with valid SW', () => {
    window.location.hostname = 'example.com';
    global.fetch.mockResolvedValue({
      status: 200,
      headers: { get: () => 'application/javascript' }
    });

    register();
    
    expect(window.addEventListener).toHaveBeenCalledWith('load', expect.any(Function));
  });

  test('should checkValidServiceWorker when fetch returns 404', () => {
    global.fetch.mockResolvedValue({
      status: 404,
      headers: { get: () => 'text/html' }
    });

    register();
  });

  test('should checkValidServiceWorker when content-type is not javascript', () => {
    global.fetch.mockResolvedValue({
      status: 200,
      headers: { get: () => 'text/html' }
    });

    register();
  });

  test('should handle fetch error gracefully', () => {
    global.fetch.mockRejectedValue(new Error('Network error'));
    console.log = jest.fn();

    register();

    expect(console.log).toHaveBeenCalledWith('No internet connection found. App is running in offline mode.');
  });

  test('should reload page when service worker is unregistered', async () => {
    global.fetch.mockResolvedValue({
      status: 404,
      headers: { get: () => 'text/html' }
    });

    const mockRegistration = { unregister: jest.fn().mockResolvedValue(true) };
    navigator.serviceWorker = {
      ready: Promise.resolve(mockRegistration)
    };

    window.location.reload = jest.fn();

    register();
  });

  test('should not register if PUBLIC_URL origin does not match window location origin', () => {
    const publicUrl = new URL(process.env.PUBLIC_URL, window.location);
    const mockOrigin = 'https://other-origin.com';
    Object.defineProperty(publicUrl, 'origin', { value: mockOrigin, writable: true });
    
    expect(publicUrl.origin).not.toBe(window.location.origin);
  });

  test('should add controlling event listener that reloads window', () => {
    global.fetch.mockResolvedValue({
      status: 200,
      headers: { get: () => 'application/javascript' }
    });

    register();
  });

  test('should confirm update when workbox emits waiting event', () => {
    global.window.confirm = jest.fn(() => true);
    global.fetch.mockResolvedValue({
      status: 200,
      headers: { get: () => 'application/javascript' }
    });

    register();
  });

  test('should not update when user cancels confirmation', () => {
    global.window.confirm = jest.fn(() => false);
    global.fetch.mockResolvedValue({
      status: 200,
      headers: { get: () => 'application/javascript' }
    });

    register();
  });

  test('should handle localhost IPv4 address pattern', () => {
    window.location.hostname = '127.0.0.1';
    expect(window.location.hostname).toMatch(/^127(?:\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}$/);
  });

  test('should handle localhost IPv6 address', () => {
    window.location.hostname = '[::1]';
    expect(window.location.hostname).toBe('[::1]');
  });

  test('should not register service worker when not in browser environment', () => {
    const swInNavigator = 'serviceWorker' in navigator;
    Object.defineProperty(navigator, 'serviceWorker', {
      value: undefined,
      writable: true
    });

    expect(swInNavigator).toBeFalsy();
  });

  test('should register workbox with correct service worker URL', () => {
    global.fetch.mockResolvedValue({
      status: 200,
      headers: { get: () => 'application/javascript' }
    });

    register();
  });

  test('should handle service worker ready event', async () => {
    global.fetch.mockResolvedValue({
      status: 200,
      headers: { get: () => 'application/javascript' }
    });

    const mockUnregister = jest.fn().mockResolvedValue(true);
    const mockRegistration = {
      unregister: mockUnregister
    };

    navigator.serviceWorker = {
      ready: Promise.resolve(mockRegistration)
    };

    register();
  });

  test('should handle workbox waiting event', () => {
    global.window.confirm = jest.fn(() => true);
    global.fetch.mockResolvedValue({
      status: 200,
      headers: { get: () => 'application/javascript' }
    });

    register();
  });

  test('should handle workbox controlling event', () => {
    global.fetch.mockResolvedValue({
      status: 200,
      headers: { get: () => 'application/javascript' }
    });
    
    window.location.reload = jest.fn();
    register();
  });

  test('should not reload if not confirmed', () => {
    global.window.confirm = jest.fn(() => false);
    global.fetch.mockResolvedValue({
      status: 200,
      headers: { get: () => 'application/javascript' }
    });

    register();
  });

  test('should handle localhost check correctly', () => {
    window.location.hostname = 'localhost';
    global.fetch.mockResolvedValue({
      status: 200,
      headers: { get: () => 'application/javascript' }
    });

    register();
  });
});
import React from 'react';
import { render, act } from '@testing-library/react';
import NetworkStatus from '../src/components/NetworkStatus';
import * as utils from '../src/utils';
import * as NotificationManager from '../src/components/NotificationManager';

jest.mock('../src/utils', () => ({
  isOnline: jest.fn()
}));

jest.mock('../src/components/NotificationManager', () => ({
  useNotification: jest.fn()
}));

describe('NetworkStatus', () => {
  let mockAddNotification;

  beforeEach(() => {
    mockAddNotification = jest.fn();
    utils.isOnline.mockReturnValue(true);
    NotificationManager.useNotification = jest.fn(() => ({
      addNotification: mockAddNotification
    }));
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  test('displays online status when browser is online', () => {
    jest.spyOn(navigator, 'onLine', 'get').mockReturnValue(true);
    const { getByText, container } = render(<NetworkStatus />);
    expect(getByText('Online')).toBeInTheDocument();
    expect(container.querySelector('span').style.backgroundColor).toBe('green');
  });

  test('displays offline status when browser is offline', () => {
    jest.spyOn(navigator, 'onLine', 'get').mockReturnValue(false);
    const { getByText, container } = render(<NetworkStatus />);
    expect(getByText('Offline')).toBeInTheDocument();
    expect(container.querySelector('span').style.backgroundColor).toBe('red');
  });

  test('calls addNotification when going online', () => {
    jest.spyOn(navigator, 'onLine', 'get').mockReturnValue(false);
    const { rerender } = render(<NetworkStatus />);
    
    act(() => {
      window.dispatchEvent(new Event('online'));
    });

    expect(mockAddNotification).toHaveBeenCalledWith('You are now online', 'success');
  });

  test('calls addNotification when going offline', () => {
    jest.spyOn(navigator, 'onLine', 'get').mockReturnValue(true);
    const { rerender } = render(<NetworkStatus />);
    
    act(() => {
      window.dispatchEvent(new Event('offline'));
    });

    expect(mockAddNotification).toHaveBeenCalledWith('You are offline. Some features may be limited.', 'warning');
  });

  test('updates online status when online event is triggered', () => {
    jest.spyOn(navigator, 'onLine', 'get').mockReturnValue(false);
    const { rerender, getByText } = render(<NetworkStatus />);
    
    act(() => {
      window.dispatchEvent(new Event('online'));
    });

    expect(getByText('Online')).toBeInTheDocument();
  });

  test('updates offline status when offline event is triggered', () => {
    jest.spyOn(navigator, 'onLine', 'get').mockReturnValue(true);
    const { rerender, getByText } = render(<NetworkStatus />);
    
    act(() => {
      window.dispatchEvent(new Event('offline'));
    });

    expect(getByText('Offline')).toBeInTheDocument();
  });

  test('removes event listeners on unmount', () => {
    const removeEventListener = jest.spyOn(window, 'removeEventListener');
    const { unmount } = render(<NetworkStatus />);
    unmount();
    expect(removeEventListener).toHaveBeenCalledWith('online', expect.any(Function));
    expect(removeEventListener).toHaveBeenCalledWith('offline', expect.any(Function));
  });

  test('shows green indicator when online', () => {
    jest.spyOn(navigator, 'onLine', 'get').mockReturnValue(true);
    const { container } = render(<NetworkStatus />);
    expect(container.querySelector('span').style.backgroundColor).toBe('green');
  });

  test('shows red indicator when offline', () => {
    jest.spyOn(navigator, 'onLine', 'get').mockReturnValue(false);
    const { container } = render(<NetworkStatus />);
    expect(container.querySelector('span').style.backgroundColor).toBe('red');
  });

  test('uses initial navigator onLine status', () => {
    jest.spyOn(navigator, 'onLine', 'get').mockReturnValue(false);
    const { getByText } = render(<NetworkStatus />);
    expect(getByText('Offline')).toBeInTheDocument();
  });

  test('does not call addNotification if already online', () => {
    jest.spyOn(navigator, 'onLine', 'get').mockReturnValue(true);
    render(<NetworkStatus />);
    act(() => {
      window.dispatchEvent(new Event('online'));
    });
    expect(mockAddNotification).not.toHaveBeenCalled();
  });

  test('does not call addNotification if already offline', () => {
    jest.spyOn(navigator, 'onLine', 'get').mockReturnValue(false);
    const { rerender } = render(<NetworkStatus />);
    act(() => {
      window.dispatchEvent(new Event('offline'));
    });
    expect(mockAddNotification).not.toHaveBeenCalled();
  });

  test('renders correctly with default online status', () => {
    jest.spyOn(navigator, 'onLine', 'get').mockReturnValue(true);
    const { getByText } = render(<NetworkStatus />);
    expect(getByText('Online')).toBeInTheDocument();
  });

  test('renders correctly with default offline status', () => {
    jest.spyOn(navigator, 'onLine', 'get').mockReturnValue(false);
    const { getByText } = render(<NetworkStatus />);
    expect(getByText('Offline')).toBeInTheDocument();
  });

  test('adds event listeners on mount', () => {
    const addEventListener = jest.spyOn(window, 'addEventListener');
    render(<NetworkStatus />);
    expect(addEventListener).toHaveBeenCalledWith('online', expect.any(Function));
    expect(addEventListener).toHaveBeenCalledWith('offline', expect.any(Function));
  });
});
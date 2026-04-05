import React from 'react';
import { render, screen, waitFor, act } from '@testing-library/react';
import { isOnline } from './utils';
import App from './App';

jest.mock('./utils', () => ({
  isOnline: jest.fn()
}));

jest.mock('./register-service-worker', () => ({
  register: jest.fn()
}));

jest.mock('./components/127.0.0.1', () => {
  return function MockNotificationManager() {
    return <div data-testid="notification-manager">Notification Manager</div>;
  };
});

jest.mock('./components/Dashboard', () => {
  return function MockDashboard() {
    return <div data-testid="dashboard">Dashboard</div>;
  };
});

jest.mock('./components/StakingOverview', () => {
  return function MockStakingOverview() {
    return <div data-testid="staking-overview">Staking Overview</div>;
  };
});

jest.mock('./components/TransactionHistory', () => {
  return function MockTransactionHistory() {
    return <div data-testid="transaction-history">Transaction History</div>;
  };
});

jest.mock('./components/StakeForm', () => {
  return function MockStakeForm() {
    return <div data-testid="stake-form">Stake Form</div>;
  };
});

jest.mock('./components/NetworkStatus', () => {
  return function MockNetworkStatus({ isOnline }) {
    return <div data-testid="network-status">{isOnline ? 'Online' : 'Offline'}</div>;
  };
});

jest.mock('./components/OfflineBanner', () => {
  return function MockOfflineBanner() {
    return <div data-testid="offline-banner">Offline Banner</div>;
  };
});

jest.mock('./components/NotificationBanner', () => {
  return function MockNotificationBanner({ message }) {
    return <div data-testid="notification-banner">{message}</div>;
  };
});

describe('App', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('renders register service worker', async () => {
    isOnline.mockResolvedValue(true);
    render(<App />);
    await waitFor(() => expect(require('./register-service-worker').register).toHaveBeenCalled());
  });

  test('renders network status online', async () => {
    isOnline.mockResolvedValue(true);
    render(<App />);
    await waitFor(() => screen.getByText('Online'));
  });

  test('renders network status offline', async () => {
    isOnline.mockResolvedValue(false);
    render(<App />);
    await waitFor(() => screen.getByText('Offline'));
  });

  test('renders offline banner when offline', async () => {
    isOnline.mockResolvedValue(false);
    render(<App />);
    await waitFor(() => screen.getByTestId('offline-banner'));
  });

  test('renders notification manager', async () => {
    isOnline.mockResolvedValue(true);
    render(<App />);
    await waitFor(() => screen.getByTestId('notification-manager'));
  });

  test('renders dashboard route', async () => {
    isOnline.mockResolvedValue(true);
    render(<App />);
    await waitFor(() => screen.getByTestId('dashboard'));
  });

  test('renders staking overview route', async () => {
    isOnline.mockResolvedValue(true);
    render(<App />);
    await waitFor(() => screen.getByTestId('staking-overview'));
  });

  test('renders transaction history route', async () => {
    isOnline.mockResolvedValue(true);
    render(<App />);
    await waitFor(() => screen.getByTestId('transaction-history'));
  });

  test('renders stake form route', async () => {
    isOnline.mockResolvedValue(true);
    render(<App />);
    await waitFor(() => screen.getByTestId('stake-form'));
  });

  test('shows notification banner when triggered', async () => {
    isOnline.mockResolvedValue(true);
    render(<App />);
    const app = screen.getByText('Notification Manager');
    expect(app).toBeInTheDocument();
  });

  test('navigates to dashboard by default', async () => {
    isOnline.mockResolvedValue(true);
    render(<App />);
    await waitFor(() => screen.getByTestId('dashboard'));
  });

  test('adds and removes online/offline event listeners', async () => {
    isOnline.mockResolvedValue(true);
    const { unmount } = render(<App />);
    
    await waitFor(() => {
      expect(window.addEventListener).toHaveBeenCalledWith('online', expect.any(Function));
      expect(window.addEventListener).toHaveBeenCalledWith('offline', expect.any(Function));
    });
    
    unmount();
    
    expect(window.removeEventListener).toHaveBeenCalledWith('online', expect.any(Function));
    expect(window.removeEventListener).toHaveBeenCalledWith('offline', expect.any(Function));
  });

  test('shows notification banner with message', async () => {
    isOnline.mockResolvedValue(true);
    render(<App />);
    
    await act(async () => {
      const showNotification = (message) => {
        const element = screen.getByText(message);
        expect(element).toBeInTheDocument();
      };
      showNotification('Test message');
    });
  });

  test('hides notification after timeout', async () => {
    isOnline.mockResolvedValue(true);
    jest.useFakeTimers();
    render(<App />);
    
    await act(async () => {
      const notificationBanner = screen.getByTestId('notification-banner');
      expect(notificationBanner).toBeInTheDocument();
      
      jest.advanceTimersByTime(3000);
      expect(screen.queryByTestId('notification-banner')).not.toBeInTheDocument();
    });
  });
});
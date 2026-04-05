import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import { act } from 'react-dom/test-utils';
import Dashboard from '../src/components/Dashboard';
import * as dexieReactHooks from 'dexie-react-hooks';
import * as utils from '../src/utils';
import * as idbKeyval from 'idb-keyval';

jest.mock('../src/utils', () => ({
  fetchWithCache: jest.fn(),
  isOnline: jest.fn()
}));

jest.mock('dexie-react-hooks', () => ({
  useLiveQuery: jest.fn()
}));

jest.mock('idb-keyval', () => ({
  get: jest.fn()
}));

describe('Dashboard', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    jest.resetAllMocks();
    global.fetch = jest.fn();
  });

  test('shows loading state initially', async () => {
    utils.isOnline.mockReturnValue(true);
    utils.fetchWithCache.mockImplementation(() => Promise.reject(new Error('API Error')));
    dexieReactHooks.useLiveQuery.mockReturnValue(null);
    
    render(<Dashboard />);
    
    expect(screen.getByText('Loading dashboard...')).toBeInTheDocument();
  });

  test('displays staking overview when data loads', async () => {
    utils.isOnline.mockReturnValue(true);
    utils.fetchWithCache.mockResolvedValue({ staked: 1000, rewards: 50 });
    dexieReactHooks.useLiveQuery.mockReturnValue([]);
    
    render(<Dashboard />);
    
    await waitFor(() => {
      expect(screen.getByText('Staking Overview')).toBeInTheDocument();
    });
  });

  test('shows error message when staking data fails to load', async () => {
    utils.isOnline.mockReturnValue(true);
    utils.fetchWithCache.mockRejectedValue(new Error('API Error'));
    dexieReactHooks.useLiveQuery.mockReturnValue([]);
    
    render(<Dashboard />);
    
    await waitFor(() => {
      expect(screen.getByText('Failed to load staking data')).toBeInTheDocument();
    });
  });

  test('displays offline banner when offline', async () => {
    utils.isOnline.mockReturnValue(false);
    utils.fetchWithCache.mockResolvedValue({ staked: 1000, rewards: 50 });
    dexieReactHooks.useLiveQuery.mockReturnValue([]);
    
    render(<Dashboard />);
    
    await waitFor(() => {
      expect(screen.getByText('You are currently offline')).toBeInTheDocument();
    });
  });

  test('shows notification banner with error message', async () => {
    utils.isOnline.mockReturnValue(true);
    utils.fetchWithCache.mockRejectedValue(new Error('API Error'));
    dexieReactHooks.useLiveQuery.mockReturnValue([]);
    
    render(<Dashboard />);
    
    await waitFor(() => {
      expect(screen.getByText('Failed to load staking data. Please try again later.')).toBeInTheDocument();
    });
  });

  test('displays transaction history', async () => {
    utils.isOnline.mockReturnValue(true);
    utils.fetchWithCache.mockResolvedValue({ staked: 1000, rewards: 50 });
    dexieReactHooks.useLiveQuery.mockReturnValue([
      { id: 1, type: 'stake', amount: 100, timestamp: Date.now() }
    ]);
    
    render(<Dashboard />);
    
    await waitFor(() => {
      expect(screen.getByText('Transaction History')).toBeInTheDocument();
    });
  });

  test('shows success notification after staking', async () => {
    utils.isOnline.mockReturnValue(true);
    utils.fetchWithCache.mockResolvedValue({ staked: 1000, rewards: 50 });
    dexieReactHooks.useLiveQuery.mockReturnValue([]);
    
    render(<Dashboard />);
    
    await waitFor(() => {
      expect(screen.getByText('Stake transaction submitted successfully!')).toBeInTheDocument();
    });
  });

  test('syncs data when coming online', async () => {
    utils.isOnline.mockReturnValue(true);
    utils.fetchWithCache.mockResolvedValue({ staked: 1000, rewards: 50 });
    idbKeyval.get.mockResolvedValue(null);
    dexieReactHooks.useLiveQuery.mockReturnValue([]);
    
    const { rerender } = render(<Dashboard />);
    
    act(() => {
      window.dispatchEvent(new Event('online'));
    });
    
    await waitFor(() => {
      expect(utils.fetchWithCache).toHaveBeenCalledTimes(2);
    });
  });

  test('removes notification when dismissed', async () => {
    utils.isOnline.mockReturnValue(true);
    utils.fetchWithCache.mockRejectedValue(new Error('API Error'));
    dexieReactHooks.useLiveQuery.mockReturnValue([]);
    
    render(<Dashboard />);
    
    await waitFor(() => {
      const dismissButton = screen.getByRole('button', { name: /dismiss/i });
      if (dismissButton) {
        act(() => {
          dismissButton.click();
        });
      }
    });
    
    await waitFor(() => {
      expect(screen.queryByText('Failed to load staking data. Please try again later.')).not.toBeInTheDocument();
    });
  });

  test('loads staking data on mount', async () => {
    utils.isOnline.mockReturnValue(true);
    utils.fetchWithCache.mockResolvedValue({ staked: 1000, rewards: 50 });
    dexieReactHooks.useLiveQuery.mockReturnValue([]);
    
    render(<Dashboard />);
    
    await waitFor(() => {
      expect(utils.fetchWithCache).toHaveBeenCalledWith('/api/staking-info', { cache: 'force-cache' });
    });
  });

  test('handles online event', async () => {
    utils.isOnline.mockReturnValue(true);
    utils.fetchWithCache.mockResolvedValue({ staked: 1000, rewards: 50 });
    dexieReactHooks.useLiveQuery.mockReturnValue([]);
    
    render(<Dashboard />);
    
    act(() => {
      window.dispatchEvent(new Event('online'));
    });
    
    await waitFor(() => {
      expect(utils.fetchWithCache).toHaveBeenCalledTimes(2);
    });
  });

  test('handles offline event', () => {
    utils.isOnline.mockReturnValue(false);
    utils.fetchWithCache.mockResolvedValue({ staked: 1000, rewards: 50 });
    dexieReactHooks.useLiveQuery.mockReturnValue([]);
    
    render(<Dashboard />);
    
    act(() => {
      window.dispatchEvent(new Event('offline'));
    });
    
    expect(screen.getByText('You are currently offline')).toBeInTheDocument();
  });

  test('shows network status component', async () => {
    utils.isOnline.mockReturnValue(true);
    utils.fetchWithCache.mockResolvedValue({ staked: 1000, rewards: 50 });
    dexieReactHooks.useLiveQuery.mockReturnValue([]);
    
    render(<Dashboard />);
    
    await waitFor(() => {
      expect(screen.getByText('Network Status')).toBeInTheDocument();
    });
  });

  test('shows staking section', async () => {
    utils.isOnline.mockReturnValue(true);
    utils.fetchWithCache.mockResolvedValue({ staked: 1000, rewards: 50 });
    dexieReactHooks.useLiveQuery.mockReturnValue([]);
    
    render(<Dashboard />);
    
    await waitFor(() => {
      expect(screen.getByText('Staking Overview')).toBeInTheDocument();
    });
  });

  test('shows transaction section', async () => {
    utils.isOnline.mockReturnValue(true);
    utils.fetchWithCache.mockResolvedValue({ staked: 1000, rewards: 50 });
    dexieReactHooks.useLiveQuery.mockReturnValue([
      { id: 1, type: 'stake', amount: 100, timestamp: Date.now() }
    ]);
    
    render(<Dashboard />);
    
    await waitFor(() => {
      expect(screen.getByText('Transaction History')).toBeInTheDocument();
    });
  });

  test('shows stake form section', async () => {
    utils.isOnline.mockReturnValue(true);
    utils.fetchWithCache.mockResolvedValue({ staked: 1000, rewards: 50 });
    dexieReactHooks.useLiveQuery.mockReturnValue([]);
    
    render(<Dashboard />);
    
    await waitFor(() => {
      expect(screen.getByText('Stake Tokens')).toBeInTheDocument();
    });
  });

  test('shows dashboard header', async () => {
    utils.isOnline.mockReturnValue(true);
    utils.fetchWithCache.mockResolvedValue({ staked: 1000, rewards: 50 });
    dexieReactHooks.useLiveQuery.mockReturnValue([]);
    
    render(<Dashboard />);
    
    await waitFor(() => {
      expect(screen.getByText('Staking Dashboard')).toBeInTheDocument();
    });
  });

  test('shows error in dashboard content', async () => {
    utils.isOnline.mockReturnValue(true);
    utils.fetchWithCache.mockRejectedValue(new Error('API Error'));
    dexieReactHooks.useLiveQuery.mockReturnValue([]);
    
    render(<Dashboard />);
    
    await waitFor(() => {
      expect(screen.getByText('Failed to load staking data')).toBeInTheDocument();
    });
  });

  test('shows loading state in dashboard content', () => {
    utils.isOnline.mockReturnValue(true);
    utils.fetchWithCache.mockReturnValue(new Promise(() => {})); // Never resolving promise
    dexieReactHooks.useLiveQuery.mockReturnValue([]);
    
    render(<Dashboard />);
    
    expect(screen.getByText('Loading dashboard...')).toBeInTheDocument();
  });

  test('shows staking overview with data', async () => {
    utils.isOnline.mockReturnValue(true);
    utils.fetchWithCache.mockResolvedValue({ staked: 1000, rewards: 50 });
    dexieReactHooks.useLiveQuery.mockReturnValue([]);
    
    render(<Dashboard />);
    
    await waitFor(() => {
      expect(screen.getByText('Staking Overview')).toBeInTheDocument();
    });
  });

  test('shows transaction history with data', async () => {
    utils.isOnline.mockReturnValue(true);
    utils.fetchWithCache.mockResolvedValue({ staked: 1000, rewards: 50 });
    dexieReactHooks.useLiveQuery.mockReturnValue([
      { id: 1, type: 'stake', amount: 100, timestamp: Date.now() }
    ]);
    
    render(<Dashboard />);
    
    await waitFor(() => {
      expect(screen.getByText('Transaction History')).toBeInTheDocument();
    });
  });
});
import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import StakingOverview from '../src/components/StakingOverview';
import * as utils from '../src/utils';

jest.mock('../src/utils', () => ({
  fetchWithCache: jest.fn(),
  isOnline: jest.fn()
}));

describe('StakingOverview', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('renders staking overview with initial values', () => {
    render(<StakingOverview />);
    expect(screen.getByText('Staking Overview')).toBeInTheDocument();
    expect(screen.getByText('Total Staked: $0')).toBeInTheDocument();
    expect(screen.getByText('Total Rewards: $0')).toBeInTheDocument();
    expect(screen.getByText('Staker Count: $0')).toBeInTheDocument();
  });

  test('fetches staking data on mount', async () => {
    const mockData = {
      data: {
        total_stakers: 1000,
        total_staked: 50000,
        total_rewards: 2500,
        formatted_staker_count: 1000
      }
    };
    
    utils.fetchWithCache.mockResolvedValue(mockData);
    
    render(<StakingOverview />);
    
    await waitFor(() => {
      expect(screen.getByText('Staker Count: 1,000')).toBeInTheDocument();
    });
  });

  test('handles fetch error gracefully', async () => {
    utils.fetchWithCache.mockRejectedValue(new Error('API Error'));
    
    const consoleSpy = jest.spyOn(console, 'error').mockImplementation();
    
    render(<StakingOverview />);
    
    await waitFor(() => {
      expect(consoleSpy).toHaveBeenCalled();
    });
    
    consoleSpy.mockRestore();
  });

  test('formats staker count correctly', () => {
    const { formatStakerCount } = new StakingOverview();
    const formatted = formatStakerCount(1000);
    expect(formatted).toBe('$1,000');
  });

  test('formats total staked correctly', () => {
    const { formatTotalStaked } = new StakingOverview();
    const formatted = formatTotalStaked(50000);
    expect(formatted).toBe('$50,000');
  });

  test('displays formatted staking data', async () => {
    const mockData = {
      data: {
        total_stakers: 1500,
        total_staked: 75000,
        total_rewards: 3750,
        formatted_staker_count: 1500
      }
    };
    
    utils.fetchWithCache.mockResolvedValue(mockData);
    
    render(<StakingOverview />);
    
    await waitFor(() => {
      expect(screen.getByText('Staker Count: 1,500')).toBeInTheDocument();
    });
  });

  test('uses cached data when available', async () => {
    const mockData = {
      data: {
        total_stakers: 2000,
        total_staked: 100000,
        total_rewards: 5000,
        formatted_staker_count: 2000
      }
    };
    
    utils.fetchWithCache.mockResolvedValue(mockData);
    
    render(<StakingOverview />);
    
    await waitFor(() => {
      expect(screen.getByText('Total Staked: $100,000')).toBeInTheDocument();
    });
  });

  test('handles null response gracefully', async () => {
    utils.fetchWithCache.mockResolvedValue(null);
    
    render(<StakingOverview />);
    
    await waitFor(() => {
      // Should still show initial values
      expect(screen.getByText('Total Staked: $0')).toBeInTheDocument();
    });
  });

  test('handles network errors gracefully', async () => {
    utils.fetchWithCache.mockRejectedValue(new Error('Network error'));
    
    const consoleSpy = jest.spyOn(console, 'error').mockImplementation();
    
    render(<StakingOverview />);
    
    await waitFor(() => {
      expect(consoleSpy).toHaveBeenCalledWith(expect.stringContaining('Error fetching staking data'));
    });
    
    consoleSpy.mockRestore();
  });

  test('renders component with default values', () => {
    render(<StakingOverview />);
    
    expect(screen.getByText('Staking Overview')).toBeInTheDocument();
    expect(screen.getByText('Total Staked: $0')).toBeInTheDocument();
    expect(screen.getByText('Total Rewards: $0')).toBeInTheDocument();
  });

  test('handles empty data response', async () => {
    const mockData = { data: {} };
    utils.fetchWithCache.mockResolvedValue(mockData);
    
    render(<StakingOverview />);
    
    await waitFor(() => {
      // Should show default values when data is missing
      expect(screen.getByText('Total Staked: $0')).toBeInTheDocument();
    });
  });

  test('handles partial data response', async () => {
    const mockData = {
      data: {
        total_staked: 25000
        // Missing total_rewards and total_stakers
      }
    };
    
    utils.fetchWithCache.mockResolvedValue(mockData);
    
    render(<StakingOverview />);
    
    // Should handle missing fields gracefully
    await waitFor(() => {
      expect(screen.getByText('Total Staked: $25,000')).toBeInTheDocument();
    });
  });

  test('renders with network error', async () => {
    utils.fetchWithCache.mockRejectedValue(new Error('Network failure'));
    
    const consoleSpy = jest.spyOn(console, 'error').mockImplementation();
    
    render(<StakingOverview />);
    
    await waitFor(() => {
      expect(consoleSpy).toHaveBeenCalled();
    });
    
    consoleSpy.mockRestore();
  });

  test('handles zero values correctly', () => {
    const { formatStakerCount, formatTotalStaked } = new StakingOverview();
    
    expect(formatStakerCount(0)).toBe('$0');
    expect(formatTotalStaked(0)).toBe('$0');
  });

  test('handles large number formatting', () => {
    const { formatStakerCount, formatTotalStaked } = new StakingOverview();
    
    expect(formatStakerCount(1000000)).toBe('$1,000,000');
    expect(formatTotalStaked(1000000)).toBe('$1,000,000');
  });

  test('handles decimal values', () => {
    const { formatStakerCount, formatTotalStaked } = new StakingOverview();
    
    expect(formatStakerCount(1000.50)).toBe('$1,000.50');
    expect(formatTotalStaked(25000.75)).toBe('$25,000.75');
  });

  test('component handles unmount cleanup', () => {
    const { unmount } = render(<StakingOverview />);
    unmount();
    // Should not throw errors
  });

  test('handles repeated renders', () => {
    const { rerender } = render(<StakingOverview />);
    rerender(<StakingOverview />);
    // Should not throw errors
  });

  test('handles fast consecutive updates', async () => {
    const mockData1 = {
      data: { total_staked: 10000, total_rewards: 500, total_stakers: 100, formatted_staker_count: 100 }
    };
    
    const mockData2 = {
      data: { total_staked: 20000, total_rewards: 1000, total_stakers: 200, formatted_staker_count: 200 }
    };
    
    utils.fetchWithCache
      .mockResolvedValueOnce(mockData1)
      .mockResolvedValueOnce(mockData2);
    
    render(<StakingOverview />);
    
    await waitFor(() => {
      expect(screen.getByText('Total Staked: $20,000')).toBeInTheDocument();
    });
  });
});
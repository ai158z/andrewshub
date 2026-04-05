import React from 'react';
import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import '@testing'
import App from './App';

// Mock fetch globally
global.fetch = jest.fn();

// Mock components
jest.mock('./components/CalculatorForm', () => {
  return function MockCalculatorForm({ onCalculate, loading }) {
    return (
      <div data-testid="calculator-form-mock">
        <button 
          data-testid="calculate-button"
          onClick={() => onCalculate({ amount: 1000, apr: 5 })}
          disabled={loading}
        >
          Calculate
        </button>
      </div>
    );
  };
});

jest.mock('./components/ResultsDisplay', () => {
  return function MockResultsDisplay({ result }) {
    return <div data-testid="results-display-mock">{result?.totalReward}</div>;
  };
});

jest.mock('./components/NetworkData', () => {
  return function MockNetworkData({ data, loading }) {
    return (
      <div data-testid="network-data-mock">
        {loading ? 'Loading...' : data?.networks?.length ? 'Networks loaded' : 'No data'}
      </div>
    );
  };
});

describe('App', () => {
  beforeEach(() => {
    fetch.mockClear();
    // Reset default state
    render(<App />);
  });

  test('renders app header', () => {
    expect(screen.getByText('Staking Reward Calculator')).toBeInTheDocument();
  });

  test('displays network data on load', async () => {
    fetch.mockResolvedValueOnce({
      json: () => Promise.resolve({ networks: ['solana', 'ethereum'] })
    });

    render(<App />);
    
    await waitFor(() => {
      expect(screen.getByTestId('network-data-mock')).toHaveTextContent('Networks loaded');
    });
  });

  test('shows loading state during network fetch', async () => {
    render(<App />);
    
    expect(screen.getByTestId('network-data-mock')).toHaveTextContent('Loading...');
    
    await waitFor(() => {
      expect(screen.getByTestId('network-data-mock')).not.toHaveTextContent('Loading...');
    });
  });

  test('displays error when network fetch fails', async () => {
    fetch.mockRejectedValueOnce(new Error('Network error'));
    
    render(<App />);
    
    await waitFor(() => {
      expect(screen.getByText('Failed to fetch network data')).toBeInTheDocument();
    });
  });

  test('performs calculation successfully', async () => {
    fetch.mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve({ 
        totalReward: 125.5,
        interest: 50,
        fee: 2.5
      })
    });

    const calculateButton = screen.getByTestId('calculate-button');
    fireEvent.click(calculateButton);

    await waitFor(() => {
      expect(screen.getByText('125.5')).toBeInTheDocument();
    });
  });

  test('shows error when calculation fails', async () => {
    fetch.mockResolvedValueOnce({
      ok: false,
      status: 500
    });

    const calculateButton = screen.getByTestId('calculate-button');
    fireEvent.click(calculateButton);

    await waitFor(() => {
      expect(screen.getByText('Calculation failed')).toBeInTheDocument();
    });
  });

  test('displays error message component when error occurs', async () => {
    fetch.mockRejectedValueOnce(new Error('API Error'));
    
    render(<App />);
    
    await waitFor(() => {
      expect(screen.getByText('Failed to fetch network data')).toBeInTheDocument();
    });
  });

  test('does not show results display initially', () => {
    expect(screen.queryByTestId('results-display-mock')).not.toBeInTheDocument();
  });

  test('shows results after successful calculation', async () => {
    fetch.mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve({ totalReward: 1000 })
    });

    const calculateButton = screen.getByTestId('calculate-button');
    fireEvent.click(calculateButton);

    await waitFor(() => {
      expect(screen.getByTestId('results-display-mock')).toBeInTheDocument();
    });
  });

  test('passes loading state to calculator form during calculation', async () => {
    fetch.mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve({ totalReward: 100 })
    });

    const calculateButton = screen.getByTestId('calculate-button');
    fireEvent.click(calculateButton);

    await waitFor(() => {
      expect(screen.getByTestId('calculator-form-mock')).toHaveTextContent('Calculate');
    });
  });

  test('handles HTTP error in calculation', async () => {
    fetch.mockResolvedValueOnce({
      ok: false,
      status: 400
    });

    const calculateButton = screen.getByTestId('calculate-button');
    fireEvent.click(calculateButton);

    await waitFor(() => {
      expect(screen.getByText('Calculation failed')).toBeInTheDocument();
    });
  });

  test('makes initial network data fetch on mount', async () => {
    expect(fetch).toHaveBeenCalledWith('/api/networks');
  });

  test('shows loading state during calculation', async () => {
    render(<App />);
    
    // Initially shows loading for network data
    expect(screen.getByTestId('network-data-mock')).toHaveTextContent('Loading...');
    
    // After network data loads
    await waitFor(() => {
      expect(screen.getByTestId('network-data-mock')).not.toHaveTextContent('Loading...');
    });
  });

  test('makes calculation API call with correct data', async () => {
    const mockData = { amount: 1000, apr: 5 };
    fetch.mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve({ totalReward: 50 })
    });

    const calculateButton = screen.getByTestId('calculate-button');
    fireEvent.click(calculateButton);

    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith('/api/calculate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(mockData)
      });
    });
  });

  test('displays network data after successful fetch', async () => {
    fetch.mockResolvedValueOnce({
      json: () => Promise.resolve({ networks: ['solana', 'ethereum'] })
    });

    render(<App />);
    
    await waitFor(() => {
      expect(screen.getByTestId('network-data-mock')).toHaveTextContent('Networks loaded');
    });
  });

  test('shows error for failed network request', async () => {
    fetch.mockRejectedValueOnce(new Error('Failed'));
    
    render(<App />);
    
    await waitFor(() => {
      expect(screen.getByText('Failed to fetch network data')).toBeInTheDocument();
    });
  });

  test('disables calculate button during loading', () => {
    render(<App />);
    expect(screen.getByTestId('calculate-button')).toBeDisabled();
  });

  test('enables calculate button after loading', async () => {
    fetch.mockResolvedValueOnce({
      json: () => Promise.resolve({ networks: [] })
    });
    
    render(<App />);
    
    await waitFor(() => {
      expect(screen.getByTestId('calculate-button')).not.toBeDisabled();
    });
  });

  test('keeps results display hidden when no calculation result', () => {
    render(<App />);
    expect(screen.queryByTestId('results-display-mock')).not.toBeInTheDocument();
  });

  test('shows results display when calculation completes', async () => {
    fetch.mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve({ totalReward: 1000 })
    });

    const calculateButton = screen.getByTestId('calculate-button');
    fireEvent.click(calculateButton);

    await waitFor(() => {
      expect(screen.getByTestId('results-display-mock')).toBeInTheDocument();
    });
  });

  test('error message cleared after successful calculation', async () => {
    // First fail
    fetch.mockRejectedValueOnce(new Error('Network error'));
    render(<App />);
    
    await waitFor(() => {
      expect(screen.getByText('Failed to fetch network data')).toBeInTheDocument();
    });

    // Then succeed
    fetch.mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve({ totalReward: 100 })
    });

    const calculateButton = screen.getByTestId('calculate-button');
    fireEvent.click(calculateButton);

    await waitFor(() => {
      expect(screen.queryByText('Failed to fetch network data')).not.toBeInTheDocument();
    });
  });

  test('handles network data fetch error', async () => {
    fetch.mockRejectedValueOnce(new Error('Network error'));
    
    render(<App />);
    
    await waitFor(() => {
      expect(screen.getByText('Failed to fetch network data')).toBeInTheDocument();
    });
  });
});
import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import TransactionHistory from '../src/components/TransactionHistory';
import * as idb from 'idb-keyval';
import * as utils from '../src/utils';

jest.mock('idb-keyval', () => ({
  openDB: jest.fn()
}));

jest.mock('../src/utils', () => ({
  fetchWithCache: jest.fn()
}));

const mockTransactions = [
  { id: '1', type: 'stake', amount: 1.5, timestamp: '2023-01-01T10:00:00Z', status: 'completed' },
  { id: '2', type: 'unstake', amount: 0.5, timestamp: '2023-01-02T15:30:00Z', status: 'pending' }
];

const mockDB = {
  transaction: jest.fn().mockReturnThis(),
  objectStore: jest.fn().mockReturnThis(),
  getAll: jest.fn(),
  clear: jest.fn(),
  add: jest.fn(),
  done: Promise.resolve()
};

describe('TransactionHistory', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    idb.openDB.mockResolvedValue(mockDB);
    mockDB.getAll.mockResolvedValue([]);
  });

  test('displays loading state initially', () => {
    render(<TransactionHistory />);
    expect(screen.getByText('Loading transactions...')).toBeInTheDocument();
  });

  test('displays transactions when loaded successfully', async () => {
    utils.fetchWithCache.mockResolvedValue(mockTransactions);
    mockDB.getAll.mockResolvedValue(mockTransactions);

    render(<TransactionHistory />);

    await waitFor(() => {
      expect(screen.getByText('Transaction History')).toBeInTheDocument();
    });

    expect(screen.getByText('STAKE')).toBeInTheDocument();
    expect(screen.getByText('1.50 ETH')).toBeInTheDocument();
  });

  test('formats stake transaction amounts correctly', async () => {
    utils.fetchWithCache.mockResolvedValue(mockTransactions);
    mockDB.getAll.mockResolvedValue(mockTransactions);

    render(<TransactionHistory />);

    await waitFor(() => {
      expect(screen.getByText('-1.50 ETH')).toBeInTheDocument();
    });
  });

  test('formats unstake transaction amounts correctly', async () => {
    const unstakeTx = [{ ...mockTransactions[1], type: 'unstake' }];
    utils.fetchWithCache.mockResolvedValue(unstakeTx);
    mockDB.getAll.mockResolvedValue(unstakeTx);

    render(<TransactionHistory />);

    await waitFor(() => {
      expect(screen.getByText('+0.50 ETH')).toBeInTheDocument();
    });
  });

  test('displays error message when API fails', async () => {
    utils.fetchWithCache.mockRejectedValue(new Error('API Error'));
    mockDB.getAll.mockResolvedValue([]);

    render(<TransactionHistory />);

    await waitFor(() => {
      expect(screen.getByText(/Error loading transactions/)).toBeInTheDocument();
    });
  });

  test('falls back to IndexedDB when API fails', async () => {
    utils.fetchWithCache.mockRejectedValue(new Error('API Error'));
    mockDB.getAll.mockResolvedValue(mockTransactions);

    render(<TransactionHistory />);

    await waitFor(() => {
      expect(screen.getByText('STAKE')).toBeInTheDocument();
    });
  });

  test('shows no transactions message when empty', async () => {
    utils.fetchWithCache.mockResolvedValue([]);
    mockDB.getAll.mockResolvedValue([]);

    render(<TransactionHistory />);

    await waitFor(() => {
      expect(screen.getByText('No transactions found')).toBeInTheDocument();
    });
  });

  test('displays transaction date in local format', async () => {
    utils.fetchWithCache.mockResolvedValue([mockTransactions[0]]);
    mockDB.getAll.mockResolvedValue([mockTransactions[0]]);

    render(<TransactionHistory />);

    await waitFor(() => {
      // Check that date is formatted (exact date format depends on timezone)
      expect(screen.getByText(/2023/)).toBeInTheDocument();
    });
  });

  test('renders transaction status correctly', async () => {
    utils.fetchWithCache.mockResolvedValue([mockTransactions[0]]);
    mockDB.getAll.mockResolvedValue([mockTransactions[0]]);

    render(<TransactionHistory />);

    await waitFor(() => {
      expect(screen.getByText('completed')).toBeInTheDocument();
    });
  });

  test('renders transaction ID correctly', async () => {
    utils.fetchWithCache.mockResolvedValue([mockTransactions[0]]);
    mockDB.getAll.mockResolvedValue([mockTransactions[0]]);

    render(<TransactionHistory />);

    await waitFor(() => {
      expect(screen.getByText('ID: 1')).toBeInTheDocument();
    });
  });

  test('applies correct CSS class for stake transactions', async () => {
    utils.fetchWithCache.mockResolvedValue([mockTransactions[0]]);
    mockDB.getAll.mockResolvedValue([mockTransactions[0]]);

    render(<TransactionHistory />);

    await waitFor(() => {
      expect(screen.getByText('STAKE')).toHaveClass('transaction-type');
    });
  });

  test('applies correct CSS class for transaction items', async () => {
    utils.fetchWithCache.mockResolvedValue(mockTransactions);
    mockDB.getAll.mockResolvedValue(mockTransactions);

    render(<TransactionHistory />);

    await waitFor(() => {
      expect(screen.getByText('STAKE')).toBeInTheDocument();
    });
  });

  test('handles transaction with missing amount', async () => {
    const txWithMissingAmount = [{ id: '3', type: 'stake', timestamp: '2023-01-03T12:00:00Z', status: 'completed' }];
    utils.fetchWithCache.mockResolvedValue(txWithMissingAmount);
    mockDB.getAll.mockResolvedValue(txWithMissingAmount);

    render(<TransactionHistory />);

    await waitFor(() => {
      expect(screen.getByText('STAKE')).toBeInTheDocument();
    });
  });

  test('handles transaction with missing type', async () => {
    const txWithMissingType = [{ id: '4', amount: 1.0, timestamp: '2023-01-04T12:00:00Z', status: 'pending' }];
    utils.fetchWithCache.mockResolvedValue(txWithMissingType);
    mockDB.getAll.mockResolvedValue(txWithMissingType);

    render(<TransactionHistory />);

    await waitFor(() => {
      expect(screen.getByText('ID: 4')).toBeInTheDocument();
    });
  });

  test('handles transaction with missing timestamp', async () => {
    const txWithMissingTimestamp = [{ id: '5', type: 'stake', amount: 2.0, status: 'failed' }];
    utils.fetchWithCache.mockResolvedValue(txWithMissingTimestamp);
    mockDB.getAll.mockResolvedValue(txWithMissingTimestamp);

    render(<TransactionHistory />);

    await waitFor(() => {
      expect(screen.getByText('STAKE')).toBeInTheDocument();
    });
  });

  test('handles transaction with missing status', async () => {
    const txWithMissingStatus = [{ id: '6', type: 'stake', amount: 1.5, timestamp: '2023-01-05T10:00:00Z' }];
    utils.fetchWithCache.mockResolvedValue(txWithMissingStatus);
    mockDB.getAll.mockResolvedValue(txWithMissingStatus);

    render(<TransactionHistory />);

    await waitFor(() => {
      expect(screen.getByText('1.50 ETH')).toBeInTheDocument();
    });
  });

  test('handles empty transaction array from API', async () => {
    utils.fetchWithCache.mockResolvedValue([]);
    mockDB.getAll.mockResolvedValue([]);

    render(<TransactionHistory />);

    await waitFor(() => {
      expect(screen.getByText('No transactions found')).toBeInTheDocument();
    });
  });

  test('handles large transaction amounts', async () => {
    const largeAmountTx = [{ 
      id: '7', 
      type: 'stake', 
      amount: 1000000, 
      timestamp: '2023-01-06T10:00:00Z', 
      status: 'completed' 
    }];
    
    utils.fetchWithCache.mockResolvedValue(largeAmountTx);
    mockDB.getAll.mockResolvedValue(largeAmountTx);

    render(<TransactionHistory />);

    await waitFor(() => {
      expect(screen.getByText('1,000,000.00 ETH')).toBeInTheDocument();
    });
  });

  test('handles negative transaction amounts', async () => {
    const negativeAmountTx = [{ 
      id: '8', 
      type: 'stake', 
      amount: -1.5, 
      timestamp: '2023-01-07T10:00:00Z', 
      status: 'completed' 
    }];
    
    utils.fetchWithCache.mockResolvedValue(negativeAmountTx);
    mockDB.getAll.mockResolvedValue(negativeAmountTx);

    render(<TransactionHistory />);

    await waitFor(() => {
      expect(screen.getByText('-1.50 ETH')).toBeInTheDocument();
    });
  });
});
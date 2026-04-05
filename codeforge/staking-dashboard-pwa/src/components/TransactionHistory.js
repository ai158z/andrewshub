import React, { useState, useEffect, useCallback } from 'react';
import { openDB } from 'idb-keyval';
import { fetchWithCache } from '../utils';

const TRANSACTION_STORE_NAME = 'transactions';
const DB_NAME = 'StakingDashboardDB';
const DB_VERSION = 1;

const TransactionHistory = () => {
  const [transactions, setTransactions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const initDB = async () => {
    return openDB(DB_NAME, DB_VERSION, {
      upgrade(db) {
        if (!db.objectStoreNames.contains(TRANSACTION_STORE_NAME)) {
          db.createObjectStore(TRANSACTION_STORE_NAME, { keyPath: 'id' });
        }
      }
    });
  };

  const fetchTransactions = useCallback(async () => {
    try {
      setLoading(true);
      const db = await initDB();
      
      // Try to get from cache first
      const cachedTransactions = await fetchWithCache('transactions', async () => {
        const response = await fetch('/api/transactions');
        if (!response.ok) {
          throw new Error('Failed to fetch transactions');
        }
        const data = await response.json();
        return Array.isArray(data) ? data : [];
      });

      // Save to IndexedDB
      const tx = db.transaction(TRANSACTION_STORE_NAME, 'readwrite');
      const store = tx.objectStore(TRANSACTION_STORE_NAME);
      await store.clear();
      for (const transaction of cachedTransactions) {
        await store.add(transaction);
      }
      await tx.done;
      
      setTransactions(cachedTransactions);
      setError(null);
    } catch (err) {
      setError(err.message);
      // Fallback to IndexedDB if API fails
      try {
        const db = await initDB();
        const tx = db.transaction(TRANSACTION_STORE_NAME, 'readonly');
        const store = tx.objectStore(TRANSACTION_STORE_NAME);
        const allTransactions = await store.getAll();
        setTransactions(allTransactions);
        await tx.done;
      } catch (dbError) {
        setError(dbError.message);
      }
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchTransactions();
  }, [fetchTransactions]);

  const formatAmount = (amount) => {
    return new Intl.NumberFormat('en-US', {
      style: 'decimal',
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
    }).format(amount);
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleString();
  };

  if (loading) {
    return <div className="transaction-history">Loading transactions...</div>;
  }

  if (error) {
    return (
      <div className="transaction-history">
        <div className="error-message">
          Error loading transactions: {error}
        </div>
      </div>
    );
  }

  return (
    <div className="transaction-history">
      <h2>Transaction History</h2>
      {transactions.length === 0 ? (
        <p>No transactions found</p>
      ) : (
        <div className="transaction-list">
          {transactions.map((transaction) => (
            <div 
              key={transaction.id} 
              className={`transaction-item ${transaction.type}`}
            >
              <div className="transaction-details">
                <div className="transaction-header">
                  <span className="transaction-type">
                    {transaction.type.toUpperCase()}
                  </span>
                  <span className="transaction-date">
                    {formatDate(transaction.timestamp)}
                  </span>
                </div>
                <div className="transaction-amount">
                  {transaction.type === 'stake' ? '-' : '+'}
                  {formatAmount(transaction.amount)} ETH
                </div>
                <div className="transaction-id">
                  ID: {transaction.id}
                </div>
              </div>
              <div className="transaction-status">
                <span className={`status ${transaction.status}`}>
                  {transaction.status}
                </span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default TransactionHistory;
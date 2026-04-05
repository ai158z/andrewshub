import React, { useState, useEffect, useCallback } from 'react';
import { useLiveQuery } from 'dexie-react-hooks';
import { db } from '../utils/database';
import StakingOverview from './StakingOverview';
import TransactionHistory from './TransactionHistory';
import StakeForm from './StakeForm';
import NotificationBanner from './NotificationBanner';
import NetworkStatus from './NetworkStatus';
import OfflineBanner from './OfflineBanner';
import { fetchWithCache, isOnline } from '../utils';
import { get, set } from 'idb-keyval';

const Dashboard = () => {
  const [notifications, setNotifications] = useState([]);
  const [stakeData, setStakeData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isOffline, setIsOffline] = useState(!isOnline());

  const transactions = useLiveQuery(() => db.transactions.orderBy('timestamp').reverse().toArray());

  const addNotification = useCallback((notification) => {
    setNotifications(prev => [...prev, notification]);
  }, []);

  const removeNotification = useCallback((id) => {
    setNotifications(prev => prev.filter(notification => notification.id !== id));
  }, []);

  const loadStakingData = useCallback(async () => {
    try {
      setLoading(true);
      const data = await fetchWithCache('/api/staking-info', { cache: 'force-cache' });
      setStakeData(data);
      setError(null);
    } catch (err) {
      setError('Failed to load staking data');
      addNotification({
        id: Date.now(),
        type: 'error',
        message: 'Failed to load staking data. Please try again later.'
      });
    } finally {
      setLoading(false);
    }
  }, [addNotification]);

  useEffect(() => {
    loadStakingData();
    
    const handleOnline = () => {
      setIsOffline(false);
      loadStakingData();
    };

    const handleOffline = () => {
      setIsOffline(true);
    };

    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, [loadStakingData]);

  useEffect(() => {
    const syncOnOnline = async () => {
      if (isOnline() && !document.hidden) {
        const lastSync = await get('lastSync');
        if (!lastSync || Date.now() - lastSync > 300000) {
          await loadStakingData();
          await set('lastSync', Date.now());
        }
      }
    };

    const onlineHandler = () => {
      setIsOffline(false);
      syncOnOnline();
    };

    window.addEventListener('online', onlineHandler);
    return () => {
      window.removeEventListener('online', onlineHandler);
    };
  }, [loadStakingData]);

  const addNotificationRef = useCallback(addNotification, [addNotification]);

  if (loading && !stakeData) {
    return <div className="dashboard-loading">Loading dashboard...</div>;
  }

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <h1>Staking Dashboard</h1>
        <NetworkStatus isOffline={isOffline} />
      </header>

      {isOffline && <OfflineBanner />}
      
      <main className="dashboard-content">
        {error && (
          <div className="dashboard-error">
            {error}
          </div>
        )}

        <NotificationBanner 
          notifications={notifications} 
          onDismiss={removeNotification}
        />

        <section className="staking-section">
          <StakingOverview 
            data={stakeData}
            loading={loading}
            error={error}
          />
        </section>

        <section className="transaction-section">
          <h2>Transaction History</h2>
          <TransactionHistory transactions={transactions || []} />
        </section>

        <section className="stake-form-section">
          <h2>Stake Tokens</h2>
          <StakeForm 
            onStakeSuccess={() => {
              addNotificationRef({
                id: Date.now(),
                type: 'success',
                message: 'Stake transaction submitted successfully!'
              });
              loadStakingData();
            }}
          />
        </section>
      </main>
    </div>
  );
};

export default Dashboard;
import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import NotificationManager from './components/NotificationManager';
import Dashboard from './components/Dashboard';
import StakingOverview from './components/StakingOverview';
import TransactionHistory from './components/TransactionHistory';
import StakeForm from './components/StakeForm';
import NotificationBanner from './components/NotificationBanner';
import NetworkStatus from './components/NetworkStatus';
import OfflineBanner from './components/OfflineBanner';
import { isOnline } from './utils';
import './App.css';

function App() {
  const [onlineStatus, setOnlineStatus] = ('.onlineStatus);
  const [showNotification, setShowNotification] = useState(false);
  const [notificationMessage, setNotificationMessage] = useState('');
  const [notification, setNotification] = useState(false);
  const [notificationMessage, setNotificationMessage] = useState('');

  useEffect(() => {
    const checkNetworkStatus = async () => {
      const status = await isOnline();
      setOnlineStatus(status);
    };

    checkNetworkStatus();

    const handleOnline = () => setOnlineStatus(true);
    const handleOffline = () => setOnlineStatus(false);

    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);

  const showNotificationBanner = (message) => {
    setNotificationMessage(message);
    setShowNotification(true);
    setTimeout(() => setShowNotification(false), 3000);
  };

  return (
    <Router>
      <div className="App">
        {onlineStatus? (
          <NetworkStatus isOnline={true} />
        ) : (
          <OfflineBanner />
        )}
        
        {showNotification && (
          <NotificationBanner 
            message={notificationMessage} 
            onClose={() => setShowNotification(false)} 
          />
        )}
        
        <Routes>
          <Route path="/" element={<Navigate to="/dashboard" replace />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/stake" element={<StakingOverview />} />
          <Route 
            path="/transactions" 
            element={<TransactionHistory showNotification={showNotificationBanner} />}
          <Route 
            path="/stake/form" 
            element={<StakeForm showNotification={showNotificationBanner} />}
        </Routes>
      </div>
    </Router>
  );
}

export default App;
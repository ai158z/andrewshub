import React, { useState, useEffect } from 'react';
import { useNotification } from '../hooks/useNotification';
import './NotificationBanner.css';

const NotificationBanner = () => {
  const { notifications, removeNotification, clearNotifications } = useNotification();
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    if (notifications.length > 0) {
      setVisible(true);
    }
  }, [notifications]);

  const handleDismiss = (id) => {
    removeNotification(id);
  };

  const handleDismissAll = () => {
    clearNotifications();
    setVisible(false);
  };

  const hasNotifications = notifications.length > 0;

  useEffect(() => {
    if (!hasNotifications) {
      setVisible(false);
    }
  }, [hasNotifications]);

  if (!visible || !hasNotifications) {
    return null;
  }

  return (
    <div className="notification-banner">
      <div className="notification-banner-content">
        <div className="notification-banner-header">
          <h3>Notifications</h3>
          <button 
            className="notification-banner-dismiss-all"
            onClick={handleDismissAll}
            aria-label="Dismiss all notifications"
          >
            Dismiss All
          </button>
        </div>
        <ul className="notification-banner-list">
          {notifications.map((notification) => (
            <li 
              key={notification.id} 
              className={`notification-item notification-item--${notification.type}`}
            >
              <div className="notification-item-content">
                <span>{notification.message}</span>
                <button 
                  onClick={() => handleDismiss(notification.id)}
                  aria-label="Dismiss notification"
                  className="notification-item-dismiss"
                >
                  &times;
                </button>
              </div>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default NotificationBanner;
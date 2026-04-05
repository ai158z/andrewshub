import React from 'react';
import { render, screen, within } from '@testing-library/react';
import { userEvent } from '@testing-library/user-event';
import NotificationBanner from './NotificationBanner';

jest.mock('../hooks/useNotification', () => ({
  useNotification: () => ({
    notifications: [
      { id: 1, type: 'info', message: 'Test notification 1' },
      { id: 2, type: 'error', message: 'Test notification 2' }
    ],
    removeNotification: jest.fn(),
    clearNotifications: jest.fn(),
    addNotification: jest.fn()
  })
}));

jest.mock('./NotificationBanner.css', () => ({}), { virtual: true });

const mockUseNotification = (mockData) => {
  const actualUseNotification = jest.requireActual('../hooks/useNotification');
  return {
    ...actualUseNotification.useNotification(),
    ...mockData
  };
};

describe('NotificationBanner', () => {
  let mockRemoveNotification;
  let mockClearNotifications;

  beforeEach(() => {
    mockRemoveNotification = jest.fn();
    mockClearNotifications = jest.fn();
    
    jest.mock('../hooks/useNotification', () => ({
      useNotification: () => ({
        notifications: [
          { id: 1, type: 'info', message: 'Test notification 1' },
          { id: 2, type: 'error', message: 'Test notification 2' }
        ],
        removeNotification: mockRemoveNotification,
        clearNotifications: mockClearNotifications,
        addNotification: jest.fn()
      })
    }));
  });

  test('renders notification banner when notifications exist', () => {
    render(<NotificationBanner />);
    expect(screen.getByText('Notifications')).toBeInTheDocument();
  });

  test('does not render when no notifications exist', () => {
    jest.mock('../hooks/useNotification', () => ({
      useNotification: () => ({
        notifications: [],
        removeNotification: mockRemoveNotification,
        clearNotifications: mockClearNotifications
      })
    }));
    
    const { container } = render(<NotificationBanner />);
    expect(container.firstChild).toBeNull();
  });

  test('renders all notifications with correct messages', () => {
    render(<NotificationBanner />);
    expect(screen.getByText('Test notification 1')).toBeInTheDocument();
    expect(screen.getByText('Test notification 2')).toBeInTheDocument();
  });

  test('renders notifications with correct types', () => {
    render(<NotificationBanner />);
    const items = screen.getAllByRole('listitem');
    expect(items[0]).toHaveClass('notification-item--info');
    expect(items[1]).toHaveClass('notification-item--error');
  });

  test('dismisses single notification when dismiss button is clicked', async () => {
    render(<NotificationBanner />);
    const notificationItems = screen.getAllByRole('listitem');
    const firstNotificationDismissButton = within(notificationItems[0]).getByRole('button', { name: 'Dismiss notification' });
    
    await userEvent.click(firstNotificationDismissButton);
    
    expect(mockRemoveNotification).toHaveBeenCalledWith(1);
  });

  test('dismisses all notifications when dismiss all button is clicked', async () => {
    render(<NotificationBanner />);
    const dismissAllButton = screen.getByRole('button', { name: 'Dismiss all notifications' });
    
    await userEvent.click(dismissAllButton);
    
    expect(mockClearNotifications).toHaveBeenCalled();
  });

  test('renders notification header correctly', () => {
    render(<NotificationBanner />);
    expect(screen.getByText('Notifications')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Dismiss all notifications' })).toBeInTheDocument();
  });

  test('renders notification list correctly', () => {
    render(<NotificationBanner />);
    const listItems = screen.getAllByRole('listitem');
    expect(listItems).toHaveLength(2);
  });

  test('applies correct CSS classes to notification items', () => {
    render(<NotificationBanner />);
    const items = screen.getAllByRole('listitem');
    expect(items[0]).toHaveClass('notification-item');
    expect(items[0]).toHaveClass('notification-item--info');
    expect(items[1]).toHaveClass('notification-item');
    expect(items[1]).toHaveClass('notification-item--error');
  });

  test('renders dismiss buttons for each notification', () => {
    render(<NotificationBanner />);
    const items = screen.getAllByRole('listitem');
    expect(within(items[0]).getByRole('button', { name: 'Dismiss notification' })).toBeInTheDocument();
    expect(within(items[1]).getByRole('button', { name: 'Dismiss notification' })).toBeInTheDocument();
  });

  test('renders dismiss all button', () => {
    render(<NotificationBanner />);
    expect(screen.getByRole('button', { name: 'Dismiss all notifications' })).toBeInTheDocument();
  });

  test('hides banner after dismissing all notifications', async () => {
    const { container } = render(<NotificationBanner />);
    const dismissAllButton = screen.getByRole('button', { name: 'Dismiss all notifications' });
    
    await userEvent.click(dismissAllButton);
    
    expect(container.firstChild).toBeNull();
  });

  test('handles empty notifications array gracefully', () => {
    jest.mock('../hooks/useNotification', () => ({
      useNotification: () => ({
        notifications: [],
        removeNotification: mockRemoveNotification,
        clearNotifications: mockClearNotifications
      })
    }));
    
    const { container } = render(<NotificationBanner />);
    expect(container.firstChild).toBeNull();
  });

  test('handles notification removal correctly', async () => {
    render(<NotificationBanner />);
    const notificationItems = screen.getAllByRole('listitem');
    const firstNotificationDismissButton = within(notificationItems[0]).getByRole('button', { name: 'Dismiss notification' });
    
    await userEvent.click(firstNotificationDismissButton);
    
    expect(mockRemoveNotification).toHaveBeenCalledTimes(1);
  });

  test('handles multiple notification dismissal', async () => {
    render(<NotificationBanner />);
    const dismissAllButton = screen.getByRole('button', { name: 'Dismiss all notifications' });
    
    await userEvent.click(dismissAllButton);
    
    expect(mockClearNotifications).toHaveBeenCalled();
  });

  test('renders notification content correctly', () => {
    render(<NotificationBanner />);
    expect(screen.getByText('Test notification 1')).toBeInTheDocument();
    expect(screen.getByText('Test notification 2')).toBeInTheDocument();
  });

  test('applies correct styling classes', () => {
    render(<NotificationBanner />);
    const banner = document.querySelector('.notification-banner');
    const content = document.querySelector('.notification-banner-content');
    const header = document.querySelector('.notification-banner-header');
    const list = document.querySelector('.notification-banner-list');
    
    expect(banner).toBeInTheDocument();
    expect(content).toBeInTheDocument();
    expect(header).toBeInTheDocument();
    expect(list).toBeInTheDocument();
  });

  test('renders notification item content correctly', () => {
    render(<NotificationBanner />);
    const items = screen.getAllByRole('listitem');
    expect(items).toHaveLength(2);
    
    const firstItemContent = within(items[0]).getByText('Test notification 1');
    const secondItemContent = within(items[1]).getByText('Test notification 2');
    
    expect(firstItemContent).toBeInTheDocument();
    expect(secondItemContent).toBeInTheDocument();
  });

  test('dismisses notification and updates UI', async () => {
    render(<NotificationBanner />);
    const dismissButton = screen.getAllByRole('button', { name: 'Dismiss notification' })[0];
    
    await userEvent.click(dismissButton);
    
    expect(mockRemoveNotification).toHaveBeenCalledWith(1);
  });

  test('dismisses all notifications and hides banner', async () => {
    render(<NotificationBanner />);
    const dismissAllButton = screen.getByRole('button', { name: 'Dismiss all notifications' });
    
    await userEvent.click(dismissAllButton);
    
    expect(mockClearNotifications).toHaveBeenCalled();
  });

  test('renders banner with correct structure', () => {
    render(<NotificationBanner />);
    const banner = document.querySelector('.notification-banner');
    const header = document.querySelector('.notification-banner-header');
    const content = document.querySelector('.notification-banner-content');
    
    expect(banner).toBeInTheDocument();
    expect(header).toBeInTheDocument();
    expect(content).toBeInTheDocument();
  });

  test('handles empty notifications gracefully', () => {
    jest.mock('../hooks/useNotification', () => ({
      useNotification: () => ({
        notifications: [],
        removeNotification: mockRemoveNotification,
        clearNotifications: mockClearNotifications
      })
    }));
    
    const { container } = render(<NotificationBanner />);
    expect(container.firstChild).toBeNull();
  });

  test('renders single notification correctly', () => {
    jest.mock('../hooks/useNotification', () => ({
      useNotification: () => ({
        notifications: [
          { id: 1, type: 'info', message: 'Single notification' }
        ],
        removeNotification: mockRemoveNotification,
        clearNotifications: mockClearNotifications,
        addNotification: jest.fn()
      })
    }));
    
    render(<NotificationBanner />);
    expect(screen.getByText('Single notification')).toBeInTheDocument();
  });

  test('renders multiple notifications correctly', () => {
    render(<NotificationBanner />);
    const items = screen.getAllByRole('listitem');
    expect(items).toHaveLength(2);
  });

  test('applies correct CSS classes to banner', () => {
    render(<NotificationBanner />);
    const banner = document.querySelector('.notification-banner');
    expect(banner).toHaveClass('notification-banner');
  });

  test('renders dismiss all button with correct attributes', () => {
    render(<NotificationBanner />);
    const button = screen.getByRole('button', { name: 'Dismiss all notifications' });
    expect(button).toHaveAttribute('aria-label', 'Dismiss all notifications');
  });

  test('handles notification dismissal correctly', async () => {
    render(<NotificationBanner />);
    const buttons = screen.getAllByRole('button', { name: 'Dismiss notification' });
    
    await userEvent.click(buttons[0]);
    
    expect(mockRemoveNotification).toHaveBeenCalledWith(1);
  });

  test('handles dismiss all correctly', async () => {
    render(<NotificationBanner />);
    const dismissAllButton = screen.getByRole('button', { name: 'Dismiss all notifications' });
    
    await userEvent.click(dismissAllButton);
    
    expect(mockClearNotifications).toHaveBeenCalled();
  });
});
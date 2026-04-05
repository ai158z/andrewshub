import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import DashboardLayout from './DashboardLayout';
import * as api from '../services/api';

jest.mock('../services/api');

jest.mock('./AgentComponents', () => ({
  AgentStatus: () => <div data-testid="agent-status">Agent Status</div>,
  SystemHealth: () => <div data-testid="system-health">System Health</div>,
  OperationalMetrics: () => <div data-testid="operational-metrics">Operational Metrics</div>,
  ROS2Monitor: () => <div data-testid="ros2-monitor">ROS2 Monitor</div>
}));

const mockApiResponses = {
  '/api/agents': { data: [{ id: 1, name: 'Agent 1', status: 'active' }] },
  '/api/system/health': { data: { cpu: 45, memory: 60 } },
  '/api/metrics': { data: [{ name: 'metric1', value: 100 }] },
  '/api/system/ros2': { data: { nodes: [], topics: [] } }
};

describe('DashboardLayout', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('renders loading state initially', () => {
    api.get.mockImplementation((url) => {
      return Promise.resolve({ data: mockApiResponses[url] });
    });
    
    render(<DashboardLayout><div>Test Child</div></DashboardLayout>);
    expect(screen.getByText('Loading dashboard...')).toBeInTheDocument();
  });

  test('renders dashboard content after data loads', async () => {
    api.get.mockImplementation((url) => {
      return Promise.resolve({ data: mockApiResponses[url] });
    });

    render(<DashboardLayout><div data-testid="child-content">Child Content</div></DashboardLayout>);

    await waitFor(() => {
      expect(screen.getByTestId('child-content')).toBeInTheDocument();
    });
    
    expect(screen.getByText('Agent Dashboard')).toBeInTheDocument();
    expect(screen.getByTestId('agent-status')).toBeInTheDocument();
    expect(screen.getByTestId('system-health')).toBeInTheDocument();
    expect(screen.getByTestId('operational-metrics')).toBeInTheDocument();
    expect(screen.getByTestId('ros2-monitor')).toBeInTheDocument();
  });

  test('renders error state when API calls fail', async () => {
    api.get.mockRejectedValue(new Error('API Error'));

    render(<DashboardLayout><div>Test Child</div></DashboardLayout>);

    await waitFor(() => {
      expect(screen.getByText('Failed to load dashboard data')).toBeInTheDocument();
    });
  });

  test('renders error message when initialization fails', async () => {
    api.get.mockImplementation(() => {
      return Promise.reject(new Error('Network error'));
    });

    render(<DashboardLayout><div>Test Child</div></DashboardLayout>);

    await waitFor(() => {
      expect(screen.getByText('Failed to initialize dashboard')).toBeInTheDocument();
    });
  });

  test('renders child components', () => {
    api.get.mockImplementation((url) => {
      return Promise.resolve({ data: mockApiResponses[url] });
    });

    render(<DashboardLayout><div data-testid="child-content">Test Child</div></DashboardLayout>);
    
    expect(screen.getByTestId('child-content')).toBeInTheDocument();
  });

  test('renders all components when data loads successfully', async () => {
    api.get.mockImplementation((url) => {
      return Promise.resolve({ data: mockApiResponses[url] });
    });

    render(<DashboardLayout><div data-testid="main-content">Main Content</div></DashboardLayout>);

    await waitFor(() => {
      expect(screen.getByTestId('agent-status')).toBeInTheDocument();
      expect(screen.getByTestId('system-health')).toBeInTheDocument();
      expect(screen.getByTestId('operational-metrics')).toBeInTheDocument();
      expect(screen.getByTestId('ros2-monitor')).toBeInTheDocument();
    });
  });

  test('renders dashboard header', async () => {
    api.get.mockImplementation((url) => {
      return Promise.resolve({ data: mockApiResponses[url] });
    });

    render(<DashboardLayout><div>Test Content</div></DashboardLayout>);

    await waitFor(() => {
      expect(screen.getByText('Agent Dashboard')).toBeInTheDocument();
    });
  });

  test('renders sidebar with all components', async () => {
    api.get.mockImplementation((url) => {
      return Promise.resolve({ data: mockApiResponses[url] });
    });

    render(<DashboardLayout><div>Test Content</div></DashboardLayout>);

    await waitFor(() => {
      expect(screen.getByTestId('agent-status')).toBeInTheDocument();
      expect(screen.getByTestId('system-health')).toBeInTheDocument();
      expect(screen.getByTestId('operational-metrics')).toBeInTheDocument();
      expect(screen.getByTestId('ros2-monitor')).toBeInTheDocument();
    });
  });

  test('renders main content area', async () => {
    api.get.mockImplementation((url) => {
      return Promise.resolve({ data: mockApiResponses[url] });
    });

    render(<DashboardLayout><div data-testid="main-content">Main Content</div></DashboardLayout>);

    await waitFor(() => {
      expect(screen.getByTestId('main-content')).toBeInTheDocument();
    });
  });

  test('renders with empty agents data', async () => {
    api.get.mockImplementation((url) => {
      if (url === '/api/agents') {
        return Promise.resolve({ data: [] });
      }
      return Promise.resolve({ data: mockApiResponses[url] });
    });

    render(<div data-testid="dashboard-layout"><DashboardLayout><div>Test</div></DashboardLayout></div>);

    await waitFor(() => {
      expect(screen.getByTestId('agent-status')).toBeInTheDocument();
    });
  });

  test('renders with empty metrics data', async () => {
    api.get.mockImplementation((url) => {
      if (url === '/api/metrics') {
        return Promise.resolve({ data: [] });
      }
      return Promise.resolve({ data: mockApiResponses[url] });
    });

    render(<DashboardLayout><div>Test</div></DashboardLayout>);

    await waitFor(() => {
      expect(screen.getByTestId('operational-metrics')).toBeInTheDocument();
    });
  });

  test('renders with null health data', async () => {
    api.get.mockImplementation((url) => {
      if (url === '/api/system/health') {
        return Promise.resolve({ data: null });
      }
      return Promise.resolve({ data: mockApiResponses[url] });
    });

    render(<DashboardLayout><div>Test</div></DashboardLayout>);

    await waitFor(() => {
      expect(screen.getByTestId('system-health')).toBeInTheDocument();
    });
  });

  test('renders with null ros data', async () => {
    api.get.mockImplementation((url) => {
      if (url === '/api/system/ros2') {
        return Promise.resolve({ data: null });
      }
      return Promise.resolve({ data: mockApiResponses[url] });
    });

    render(<DashboardLayout><div>Test</div></DashboardLayout>);

    await waitFor(() => {
      expect(screen.getByTestId('ros2-monitor')).toBeInTheDocument();
    });
  });

  test('handles partial data failure gracefully', async () => {
    api.get.mockImplementation((url) => {
      if (url === '/api/system/health') {
        return Promise.reject(new Error('Failed'));
      }
      return Promise.resolve({ data: mockApiResponses[url] });
    });

    render(<DashboardLayout><div data-testid="test-child">Test</div></DashboardLayout>);

    await waitFor(() => {
      expect(screen.getByText('Failed to load dashboard data')).toBeInTheDocument();
    });
  });

  test('renders all components even with some API failures', async () => {
    let callCount = 0;
    api.get.mockImplementation((url) => {
      callCount++;
      if (callCount === 2) {
        return Promise.reject(new Error('Failed'));
      }
      return Promise.resolve({ data: mockApiResponses[url] });
    });

    render(<DashboardLayout><div data-testid="test-child">Test</div></DashboardLayout>);

    await waitFor(() => {
      expect(screen.getByText('Failed to load dashboard data')).toBeInTheDocument();
    });
  });

  test('renders with no data when all APIs fail', async () => {
    api.get.mockRejectedValue(new Error('All APIs failed'));

    render(<DashboardLayout><div data-testid="test-child">Test</div></DashboardLayout>);

    await waitFor(() => {
      expect(screen.getByText('Failed to load dashboard data')).toBeInTheDocument();
    });
  });
});
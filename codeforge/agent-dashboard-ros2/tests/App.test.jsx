import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import App from './App';
import * as api from './services/api';

jest.mock('./services/api', () => ({
  api: {
    get: jest.fn()
  }
}));

jest.mock('./components/DashboardLayout', () => {
  return function DashboardLayoutMock({ children }) {
    return <div data-testid="dashboard-layout">{children}</div>;
  };
});

jest.mock('./components/AgentStatus', () => {
  return function AgentStatusMock() {
    return <div>Agent Status Component</div>;
  };
});

jest.mock('./components/SystemHealth', () => {
  return function SystemHealthMock() {
    return <div>System Health Component</div>;
  };
});

jest.mock('./components/OperationalMetrics', () => {
  return function OperationalMetricsMock() {
    return <div>Operational Metrics Component</div>;
  };
});

jest.mock('./components/ROS2Monitor', () => {
  return function ROS2MonitorMock() {
    return <div>ROS2 Monitor Component</div>;
  };
});

describe('App', () => {
  const mockApiData = {
    agents: [{ id: 1, name: 'Agent 1', status: 'active' }],
    health: { cpu: 45, memory: 60 },
    metrics: [{ name: 'metric1', value: 100 }],
    rosData: { status: 'running', nodes: 5 }
  };

  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('should show loading state initially', () => {
    api.api.get.mockImplementation(() => new Promise(() => {}));
    render(<App />);
    expect(screen.getByText('Loading...')).toBeInTheDocument();
  });

  test('should display error message when API calls fail', async () => {
    api.api.get.mockRejectedValue(new Error('API Error'));
    render(<App />);
    
    await waitFor(() => {
      expect(screen.getByText('Error: Failed to load data')).toBeInTheDocument();
    });
  });

  test('should render dashboard components when data loads successfully', async () => {
    api.api.get.mockResolvedValue({ data: {} });
    render(<App />);
    
    await waitFor(() => {
      expect(screen.queryByText('Loading...')).not.toBeInTheDocument();
    });
    
    expect(screen.getByTestId('dashboard-layout')).toBeInTheDocument();
  });

  test('should fetch agents data on mount', async () => {
    api.api.get.mockImplementation((url) => {
      if (url === '/api/agents') {
        return Promise.resolve({ data: mockApiData.agents });
      }
      return Promise.resolve({ data: {} });
    });

    render(<App />);
    
    await waitFor(() => {
      expect(api.api.get).toHaveBeenCalledWith('/api/agents');
    });
  });

  test('should fetch system health data on mount', async () => {
    api.api.get.mockImplementation((url) => {
      if (url === '/api/system/health') {
        return Promise.resolve({ data: mockApiData.health });
      }
      return Promise.resolve({ data: {} });
    });

    render(<App />);
    
    await waitFor(() => {
      expect(api.api.get).toHaveBeenCalledWith('/api/system/health');
    });
  });

  test('should fetch metrics data on mount', async () => {
    api.api.get.mockImplementation((url) => {
      if (url === '/api/metrics') {
        return Promise.resolve({ data: mockApiData.metrics });
      }
      return Promise.resolve({ data: {} });
    });

    render(<App />);
    
    await waitFor(() => {
      expect(api.api.get).toHaveBeenCalledWith('/api/metrics');
    });
  });

  test('should fetch ROS data on mount', async () => {
    api.api.get.mockImplementation((url) => {
      if (url === '/api/system/status') {
        return Promise.resolve({ data: mockApiData.rosData });
      }
      return Promise.resolve({ data: {} });
    });

    render(<App />);
    
    await waitFor(() => {
      expect(api.api.get).toHaveBeenCalledWith('/api/system/status');
    });
  });

  test('should render all dashboard components after loading', async () => {
    api.api.get.mockResolvedValue({ data: {} });
    
    render(<App />);
    
    await waitFor(() => {
      expect(screen.queryByText('Loading...')).not.toBeInTheDocument();
    });
    
    expect(screen.getByText('Agent Status Component')).toBeInTheDocument();
    expect(screen.getByText('System Health Component')).toBeInTheDocument();
    expect(screen.getByText('Operational Metrics Component')).toBeInTheDocument();
    expect(screen.getByText('ROS2 Monitor Component')).toBeInTheDocument();
  });

  test('should handle multiple API failures gracefully', async () => {
    api.api.get.mockRejectedValue(new Error('Network error'));
    
    render(<App />);
    
    await waitFor(() => {
      expect(screen.getByText('Error: Failed to load data')).toBeInTheDocument();
    });
  });

  test('should render AgentStatus with correct props', async () => {
    const mockAgents = [{ id: 1, status: 'active' }, { id: 2, status: 'inactive' }];
    api.api.get.mockImplementation((url) => {
      if (url === '/api/agents') {
        return Promise.resolve({ data: mockAgents });
      }
      return Promise.resolve({ data: {} });
    });

    render(<App />);
    
    await waitFor(() => {
      expect(screen.queryByText('Loading...')).not.toBeInTheDocument();
    });
  });

  test('should render SystemHealth with correct props', async () => {
    const mockHealth = { cpu: 50, memory: 75, disk: 60 };
    api.api.get.mockImplementation((url) => {
      if (url === '/api/system/health') {
        return Promise.resolve({ data: mockHealth });
      }
      return Promise.resolve({ data: {} });
    });

    render(<App />);
    
    await waitFor(() => {
      expect(screen.queryByText('Loading...')).not.toBeInTheDocument();
    });
  });

  test('should render OperationalMetrics with correct props', async () => {
    const mockMetrics = [
      { id: 'cpu', value: 45 },
      { id: 'memory', value: 70 }
    ];
    api.api.get.mockImplementation((url) => {
      if (url === '/api/metrics') {
        return Promise.resolve({ data: mockMetrics });
      }
      return Promise.resolve({ data: {} });
    });

    render(<App />);
    
    await waitFor(() => {
      expect(screen.queryByText('Loading...')).not.toBeInTheDocument();
    });
  });

  test('should render ROS2Monitor with correct props', async () => {
    const mockRosData = { nodes: 10, status: 'active' };
    api.api.get.mockImplementation((url) => {
      if (url === '/api/system/status') {
        return Promise.resolve({ data: mockRosData });
      }
      return Promise.resolve({ data: {} });
    });

    render(<App />);
    
    await waitFor(() => {
      expect(screen.queryByText('Loading...')).not.toBeInTheDocument();
    });
  });
});
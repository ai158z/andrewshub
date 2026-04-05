import React from 'react';
import { render, waitFor } from '@testing-library/react';
import axios from 'axios';
import ROS2Monitor from '../frontend/src/components/ROS2Monitor';
import * as AgentStatus from '../frontend/src/components/AgentStatus';
import * as SystemHealth from '../frontend/src/components/SystemHealth';
import * as OperationalMetrics from '../frontend/src/components/OperationalMetrics';
import * as DashboardLayout from '../frontend/src/components/DashboardLayout';

jest.mock('axios');
jest.mock('../frontend/src/components/AgentStatus', () => ({ agentData: jest.fn(() => <div>AgentStatus</div>) }));
jest.mock('../frontend/src/components/SystemHealth', () => ({ default: jest.fn(() => <div>SystemHealth</div>) }));
jest.mock('../frontend/src/components/OperationalMetrics', () => ({ default: jest.fn(() => <div>OperationalMetrics</div>) }));
jest.mock('../frontend/src/components/DashboardLayout', () => ({ default: jest.fn(({ children }) => <div>{children}</div>) }));

const mockSystemHealth = { cpu: 50, memory: 60 };
const mockAgents = [
  { id: 1, name: 'agent1', status: 'active' },
  { id: 2, name: 'agent2', status: 'inactive' }
];
const mockMetrics = [
  { name: 'metric1', value: 100 },
  { name: 'metric2', value: 200 }
];

describe('ROS2Monitor', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    jest.useFakeTimers();
  });

  afterEach(() => {
    jest.useRealTimers();
  });

  it('should render loading state initially', async () => {
    axios.get.mockImplementation((url) => {
      if (url === '/api/system/health') {
        return Promise.resolve({ data: mockSystemHealth });
      } else if (url === '/api/agents') {
        return Promise.resolve({ data: mockAgents });
      } else if (url === '/api/metrics') {
        return Promise.resolve({ data: mockMetrics });
      }
    });

    const { getByText, queryByText } = render(<ROS2Monitor />);
    expect(getByText('Loading ROS2 system status...')).toBeInTheDocument();
  });

  it('should render system health data when loaded', async () => {
    axios.get.mockImplementation((url) => {
      if (url === '/api/system/health') {
        return Promise.resolve({ data: mockSystemHealth });
      } else if (url === '/api/agents') {
        return Promise.resolve({ data: [] });
      } else if (url === '/api/metrics') {
        return Promise.resolve({ data: [] });
      }
    });

    const { findByText } = render(<ROS2Monitor />);
    await findByText('SystemHealth');
    expect(SystemHealth.default).toHaveBeenCalledWith({ healthData: mockSystemHealth }, {});
  });

  it('should render agent status components', async () => {
    axios.get.mockImplementation((url) => {
      if (url === '/api/system/health') {
        return Promise.resolve({ data: {} });
      } else if (url === '/api/agents') {
        return Promise.resolve({ data: mockAgents });
      } else if (url === '/api/metrics') {
        return Promise.resolve({ data: [] });
      }
    });

    render(<ROS2Monitor />);
    await waitFor(() => {
      expect(AgentStatus.agentData).toHaveBeenCalledWith({ agentData: mockAgents[0] }, {});
      expect(AgentStatus.agentData).toHaveBeenCalledWith({ agentData: mockAgents[1] }, {});
    });
  });

  it('should render operational metrics', async () => {
    axios.get.mockImplementation((url) => {
      if (url === '/api/system/health') {
        return Promise.resolve({ data: {} });
      } else if (url === '/api/agents') {
        return Promise.resolve({ data: [] });
      } else if (url === '/api/metrics') {
        return Promise.resolve({ data: mockMetrics });
      }
    });

    render(<ROS2Monitor />);
    await waitFor(() => {
      expect(OperationalMetrics.default).toHaveBeenCalledWith({ metricsData: mockMetrics }, {});
    });
  });

  it('should show error message on API failure', async () => {
    axios.get.mockRejectedValue(new Error('API error'));
    
    const { findByText } = render(<ROS2Monitor />);
    await findByText('Error: Failed to fetch system data');
  });

  it('should poll for data every 5 seconds', async () => {
    axios.get.mockImplementation((url) => {
      if (url === '/api/system/health') {
        return Promise.resolve({ data: {} });
      } else if (url === '/api/agents') {
        return Promise.resolve({ data: [] });
      } else if (url === '/api/metrics') {
        return Promise.resolve({ data: [] });
      }
    });

    render(<ROS2Monitor />);
    await waitFor(() => expect(axios.get).toHaveBeenCalledTimes(3));
    
    jest.advanceTimersByTime(5000);
    await waitFor(() => expect(axios.get).toHaveBeenCalledTimes(6));
  });

  it('should clear interval on unmount', async () => {
    axios.get.mockImplementation((url) => {
      if (url === '/api/system/health') {
        return Promise.resolve({ data: {} });
      } else if (url === '/api/agents') {
        return Promise.resolve({ data: [] });
      } else if (url === '/api/metrics') {
        return Promise.resolve({ data: [] });
      }
    });

    const { unmount } = render(<ROS2Monitor />);
    unmount();
    expect(clearInterval).toHaveBeenCalled();
  });

  it('should render DashboardLayout component', async () => {
    axios.get.mockImplementation((url) => {
      if (url === '/api/system/health') {
        return Promise.resolve({ data: {} });
      } else if (url === '/api/agents') {
        return Promise.resolve({ data: [] });
      } else if (url === '/api/metrics') {
        return Promise.resolve({ data: [] });
      }
    });

    render(<ROS2Monitor />);
    await waitFor(() => {
      expect(DashboardLayout.default).toHaveBeenCalled();
    });
  });

  it('should render agent data when available', async () => {
    const agentsWithIds = [
      { id: '1', name: 'agent1', status: 'active' },
      { id: '2', name: 'agent2', status: 'inactive' }
    ];
    
    axios.get.mockImplementation((url) => {
      if (url === '/api/system/health') {
        return Promise.resolve({ data: {} });
      } else if (url === '/api/agents') {
        return Promise.resolve({ data: agentsWithIds });
      } else if (url === '/api/metrics') {
        return Promise.resolve({ data: [] });
      }
    });

    render(<ROS2Monitor />);
    await waitFor(() => {
      expect(AgentStatus.agentData).toHaveBeenCalledWith({ agentData: agentsWithIds[0] }, {});
      expect(AgentStatus.agentData).toHaveBeenCalledWith({ agentData: agentsWithIds[1] }, {});
    });
  });

  it('should not render SystemHealth when data is null', async () => {
    axios.get.mockImplementation((url) => {
      if (url === '/api/system/health') {
        return Promise.resolve({ data: null });
      } else if (url === '/api/agents') {
        return Promise.resolve({ data: [] });
      } else if (url === '/api/metrics') {
        return Promise.resolve({ data: [] });
      }
    });

    const { queryByText } = render(<ROS2Monitor />);
    await waitFor(() => {
      expect(queryByText('SystemHealth')).not.toBeInTheDocument();
    });
  });

  it('should render error when system health fetch fails', async () => {
    axios.get.mockImplementation((url) => {
      if (url === '/api/system/health') {
        return Promise.reject(new Error('API error'));
      } else if (url === '/api/agents') {
        return Promise.resolve({ data: [] });
      } else if (url === '/api/metrics') {
        return Promise.resolve({ data: [] });
      }
    });

    const { findByText } = render(<ROS2Monitor />);
    await findByText('Error: Failed to fetch system data');
  });

  it('should render correctly with empty metrics', async () => {
    axios.get.mockImplementation((url) => {
      if (url === '/api/system/health') {
        return Promise.resolve({ data: {} });
      } else if (url === '/api/agents') {
        return Promise.resolve({ data: [] });
      } else if (url === '/api/metrics') {
        return Promise.resolve({ data: [] });
      }
    });

    render(<ROS2Monitor />);
    await waitFor(() => {
      expect(OperationalMetrics.default).toHaveBeenCalledWith({ metricsData: [] }, {});
    });
  });

  it('should render correctly with empty agents', async () => {
    axios.get.mockImplementation((url) => {
      if (url === '/api/system/health') {
        return Promise.resolve({ data: {} });
      } else if (url === '/api/agents') {
        return Promise.resolve({ data: [] });
      } else if (url === '/api/metrics') {
        return Promise.resolve({ data: [] });
      }
    });

    const { queryByText } = render(<ROS2Monitor />);
    await waitFor(() => {
      expect(queryByText('Agent Status')).not.toBeNull();
    });
  });

  it('should render correctly with null metrics', async () => {
    axios.get.mockImplementation((url) => {
      if (url === '/api/system/health') {
        return Promise.resolve({ data: {} });
      } else if (url === '/api/agents') {
        return Promise.resolve({ data: [] });
      } else if (url === '/api/metrics') {
        return Promise.resolve({ data: null });
      }
    });

    render(<ROS2Monitor />);
    await waitFor(() => {
      expect(OperationalMetrics.default).toHaveBeenCalledWith({ metricsData: null }, {});
    });
  });

  it('should render correctly with null agent data', async () => {
    axios.get.mockImplementation((url) => {
      if (url === '/api/system/health') {
        return Promise.resolve({ data: {} });
      } else if (url === '/api/agents') {
        return Promise.resolve({ data: null });
      } else if (url === '/api/metrics') {
        return Promise.resolve({ data: [] });
      }
    });

    render(<ROS2Monitor />);
    await waitFor(() => {
      expect(AgentStatus.agentData).not.toHaveBeenCalled();
    });
  });

  it('should handle axios error for system health', async () => {
    axios.get.mockImplementation((url) => {
      if (url === '/api/system/health') {
        return Promise.reject(new Error('Network error'));
      } else if (url === '/api/agents') {
        return Promise.resolve({ data: [] });
      } else if (url === '/api/metrics') {
        return Promise.resolve({ data: [] });
      }
    });

    const { findByText } = render(<ROS2Monitor />);
    await findByText('Error: Failed to fetch system data');
  });

  it('should handle axios error for agents', async () => {
    axios.get.mockImplementation((url) => {
      if (url === '/api/system/health') {
        return Promise.resolve({ data: {} });
      } else if (url === '/api/agents') {
        return Promise.reject(new Error('Network error'));
      } else if (url === '/api/metrics') {
        return Promise.resolve({ data: [] });
      }
    });

    render(<ROS2Monitor />);
    await waitFor(() => {
      expect(AgentStatus.agentData).not.toHaveBeenCalled();
    });
  });

  it('should handle axios error for metrics', async () => {
    axios.get.mockImplementation((url) => {
      if (url === '/api/system/health') {
        return Promise.resolve({ data: {} });
      } else if (url === '/api/agents') {
        return Promise.resolve({ data: [] });
      } else if (url === '/api/metrics') {
        return Promise.reject(new Error('Network error'));
      }
    });

    render(<ROS2Monitor />);
    await waitFor(() => {
      expect(OperationalMetrics.default).not.toHaveBeenCalled();
    });
  });

  it('should handle all API calls failing', async () => {
    axios.get.mockRejectedValue(new Error('All requests failed'));

    const { findByText } = render(<ROS2Monitor />);
    await findByText('Error: Failed to fetch system data');
  });

  it('should handle partial data from APIs', async () => {
    axios.get.mockImplementation((url) => {
      if (url === '/api/system/health') {
        return Promise.resolve({ data: null });
      } else if (url === '/api/agents') {
        return Promise.resolve({ data: [] });
      } else if (url === '/api/metrics') {
        return Promise.resolve({ data: [] });
      }
    });

    const { queryByText } = render(<ROS2Monitor />);
    await waitFor(() => {
      expect(queryByText('SystemHealth')).not.toBeInTheDocument();
    });
  });
});
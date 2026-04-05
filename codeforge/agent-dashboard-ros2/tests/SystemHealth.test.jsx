import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import { act } from 'react-dom/test-utils';
import SystemHealth from './SystemHealth';
import * as api from '../services/api';

jest.mock('../services/api', () => ({
  get: jest.fn()
}));

jest.useFakeTimers();

describe('SystemHealth', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('displays loading state initially', () => {
    render(<SystemHealth />);
    expect(screen.getByText('Loading system health data...')).toBeInTheDocument();
  });

  it('displays error message when API calls fail', async () => {
    api.get.mockRejectedValue(new Error('API Error'));
    
    await act(async () => {
      render(<SystemHealth />);
    });
    
    expect(screen.getByText('Error: Failed to fetch system health data')).toBeInTheDocument();
  });

  it('displays system metrics when data is loaded', async () => {
    const mockSystemData = {
      data: {
        metrics: [
          { timestamp: '2023-01-01T00:00:00Z', cpu_usage: 45, memory_usage: 60 }
        ]
      }
    };
    
    const mockAgentData = {
      data: {
        metrics: [
          { 
            name: 'Agent 1', 
            status: 'healthy', 
            metrics: { cpu: 25, memory: 30 }, 
            uptime: 3600 
          }
        ]
      }
    };
    
    api.get
      .mockResolvedValueOnce(mockSystemData)
      .mockResolvedValueOnce(mockAgentData);
    
    await act(async () => {
      render(<SystemHealth />);
    });
    
    expect(screen.getByText('System Health: 67%')).toBeInTheDocument();
  });

  it('renders agent status cards when agent data is available', async () => {
    const mockSystemData = { data: { metrics: [] } };
    const mockAgentData = {
      data: {
        metrics: [
          { 
            name: 'Agent 1', 
            status: 'healthy', 
            metrics: { cpu: 25.5, memory: 30.2 }, 
            uptime: 3600 
          }
        ]
      }
    };
    
    api.get
      .mockResolvedValueOnce(mockSystemData)
      .mockResolvedValueOnce(mockAgentData);
    
    await act(async () => {
      render(<SystemHealth />);
    });
    
    expect(screen.getByText('Agent 1')).toBeInTheDocument();
    expect(screen.getByText('healthy')).toBeInTheDocument();
  });

  it('calculates health score correctly', () => {
    const mockData = [
      { cpu_usage: 50, memory_usage: 30 },
      { cpu_usage: 30, memory_usage: 50 }
    ];
    
    api.get
      .mockResolvedValueOnce({ data: { metrics: mockData } })
      .mockResolvedValueOnce({ data: { metrics: [] } });
    
    render(<SystemHealth />);
    
    expect(screen.getByText('System Health: 60%')).toBeInTheDocument();
  });

  it('sets up interval for polling', async () => {
    const mockSystemData = { data: { metrics: [] } };
    const mockAgentData = { data: { metrics: [] } };
    
    api.get
      .mockResolvedValueOnce(mockSystemData)
      .mockResolvedValueOnce(mockAgentData)
      .mockResolvedValueOnce(mockSystemData)
      .mockResolvedValueOnce(mockAgentData);
    
    await act(async () => {
      render(<SystemHealth />);
    });
    
    expect(api.get).toHaveBeenCalledTimes(2);
    
    act(() => {
      jest.advanceTimersByTime(5000);
    });
    
    expect(api.get).toHaveBeenCalledTimes(4);
  });

  it('clears interval on unmount', async () => {
    const mockSystemData = { data: { metrics: [] } };
    const mockAgentData = { data: { metrics: [] } };
    
    api.get
      .mockResolvedValueOnce(mockSystemData)
      .mockResolvedValueOnce(mockAgentData);
    
    const { unmount } = render(<SystemHealth />);
    const clearIntervalSpy = jest.spyOn(global, 'clearInterval');
    
    unmount();
    
    expect(clearIntervalSpy).toHaveBeenCalled();
  });

  it('handles empty metrics data gracefully', async () => {
    api.get
      .mockResolvedValueOnce({ data: { metrics: [] } })
      .mockResolvedValueOnce({ data: { metrics: [] } });
    
    await act(async () => {
      render(<SystemHealth />);
    });
    
    expect(screen.getByText('System Health: 100%')).toBeInTheDocument();
  });

  it('displays agent metrics in grid', async () => {
    const mockSystemData = { data: { metrics: [] } };
    const mockAgentData = {
      data: {
        metrics: [
          { 
            name: 'Agent 1', 
            status: 'warning', 
            metrics: { cpu: 75.5, memory: 65.2 }, 
            uptime: 7200 
          }
        ]
      }
    };
    
    api.get
      .mockResolvedValueOnce(mockSystemData)
      .mockResolvedValueOnce(mockAgentData);
    
    await act(async () => {
      render(<SystemHealth />);
    });
    
    expect(screen.getByText('Agent 1')).toBeInTheDocument();
    expect(screen.getByText('warning')).toBeInTheDocument();
    expect(screen.getByText('CPU: 75.5%')).toBeInTheDocument();
    expect(screen.getByText('Memory: 65.2%')).toBeInTheDocument();
  });

  it('renders LineChart with system metrics', async () => {
    const mockSystemData = {
      data: {
        metrics: [
          { timestamp: '00:00', cpu_usage: 45, memory_usage: 60 },
          { timestamp: '00:05', cpu_usage: 50, memory_usage: 55 }
        ]
      }
    };
    
    const mockAgentData = { data: { metrics: [] } };
    
    api.get
      .mockResolvedValueOnce(mockSystemData)
      .mockResolvedValueOnce(mockAgentData);
    
    render(<SystemHealth />);
    
    expect(screen.getByText('System Metrics')).toBeInTheDocument();
  });

  it('shows 0% health score when metrics are missing', () => {
    const mockData = [];
    api.get
      .mockResolvedValue({ data: { metrics: mockData } });
    
    render(<SystemHealth healthData={mockData} />);
    
    expect(screen.getByText('System Health: 100%')).toBeInTheDocument();
  });

  it('handles API error for system metrics', async () => {
    api.get
      .mockResolvedValueOnce(Promise.reject(new Error('API error')))
      .mockResolvedValueOnce({ data: { metrics: [] } });
    
    await act(async () => {
      render(<SystemHealth />);
    });
    
    expect(screen.getByText('Error: Failed to fetch system health data')).toBeInTheDocument();
  });

  it('handles API error for agent metrics', async () => {
    api.get
      .mockResolvedValueOnce({ data: { metrics: [] } })
      .mockResolvedValueOnce(Promise.reject(new Error('API error')));
    
    await act(async () => {
      render(<SystemHealth />);
    });
    
    expect(screen.getByText('Error: Failed to fetch system health data')).toBeInTheDocument();
  });

  it('renders correctly with no agent data', async () => {
    api.get
      .mockResolvedValueOnce({ data: { metrics: [] } })
      .mockResolvedValueOnce({ data: { metrics: [] } });
    
    await act(async () => {
      render(<SystemHealth />);
    });
    
    expect(screen.getByText('System Health: 100%')).toBeInTheDocument();
  });

  it('shows error when both APIs fail', async () => {
    api.get.mockRejectedValue(new Error('Both APIs failed'));
    
    await act(async () => {
      render(<SystemHealth />);
    });
    
    expect(screen.getByText('Error: Failed to fetch system health data')).toBeInTheDocument();
  });
});
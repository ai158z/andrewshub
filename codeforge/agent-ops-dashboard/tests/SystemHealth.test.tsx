import React from 'react';
import { render, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import axios from 'axios';
import SystemHealth from '../../src/frontend/components/SystemHealth';

jest.mock('axios');
const mockedAxios = axios as jest.Mocked<typeof axios>;

describe('SystemHealth', () => {
  const mockMetrics = [
    { name: 'CPU Usage', value: 45, timestamp: '2023-01-01T10:00:00Z' },
    { name: 'Memory Usage', value: 60, timestamp: '2023-01-01T10:00:00Z' },
    { name: 'Disk Space', value: 75, timestamp: '2023-01-01T10:00:00Z' }
  ];

  beforeEach(() => {
    mockedAxios.get = jest.fn();
    jest.clearAllMocks();
  });

  it('should render loading state initially', () => {
    const { getByText } = render(<SystemHealth metrics={[]} />);
    expect(getByText('Loading system health data...')).toBeInTheDocument();
  });

  it('should render error state when API call fails', async () => {
    mockedAxios.get.mockRejectedValue(new Error('API Error'));
    
    const { getByText } = render(<SystemHealth metrics={[]} />);
    
    await waitFor(() => {
      expect(getByText('Error: Failed to load system health metrics')).toBeInTheDocument();
    });
  });

  it('should render with provided metrics', () => {
    const { getByText } = render(<SystemHealth metrics={mockMetrics} />);
    expect(getByText('System Health Metrics')).toBeInTheDocument();
  });

  it('should render chart with metrics data', async () => {
    const { getByText } = render(<SystemHealth metrics={mockMetrics} />);
    await waitFor(() => {
      expect(getByText('System Health Metrics')).toBeInTheDocument();
    });
  });

  it('should render metric cards with correct values', () => {
    const { getByText } = render(<SystemHealth metrics={mockMetrics} />);
    
    mockMetrics.forEach(metric => {
      expect(getByText(metric.name)).toBeInTheDocument();
      expect(getByText(metric.value.toString())).toBeInTheDocument();
    });
  });

  it('should fetch metrics when none provided', async () => {
    mockedAxios.get.mockResolvedValue({ data: mockMetrics });
    
    const { getByText } = render(<SystemHealth metrics={[]} />);
    
    await waitFor(() => {
      expect(getByText('System Health Metrics')).toBeInTheDocument();
    });
  });

  it('should show loading state before data loads', () => {
    mockedAxios.get.mockResolvedValue({ data: mockMetrics });
    
    const { getByText } = render(<SystemHealth metrics={[]} />);
    expect(getByText('Loading system health data...')).toBeInTheDocument();
  });

  it('should render metric name in cards', async () => {
    const { getByText } = render(<SystemHealth metrics={mockMetrics} />);
    
    await waitFor(() => {
      expect(getByText('CPU Usage')).toBeInTheDocument();
      expect(getByText('Memory Usage')).toBeInTheDocument();
      expect(getByText('Disk Space')).toBeInTheDocument();
    });
  });

  it('should render metric values in cards', async () => {
    const { getByText } = render(<SystemHealth metrics={mockMetrics} />);
    
    await waitFor(() => {
      expect(getByText('45')).toBeInTheDocument();
      expect(getByText('60')).toBeInTheDocument();
      expect(getByText('75')).toBeInTheDocument();
    });
  });

  it('should render metric timestamps in cards', async () => {
    const { getByText } = render(<SystemHealth metrics={mockMetrics} />);
    
    await waitFor(() => {
      const date = new Date('2023-01-01T10:00:00Z').toLocaleString();
      expect(getByText(date)).toBeInTheDocument();
    });
  });

  it('should render error when metrics array is empty and API fails', async () => {
    mockedAxios.get.mockRejectedValue(new Error('API Error'));
    
    const { getByText } = render(<SystemHealth metrics={[]} />);
    
    await waitFor(() => {
      expect(getByText('Error: Failed to load system health metrics')).toBeInTheDocument();
    });
  });

  it('should not show loading after data is fetched', async () => {
    mockedAxios.get.mockResolvedValue({ data: mockMetrics });
    
    const { queryByText, getByText } = render(<SystemHealth metrics={[]} />);
    
    await waitFor(() => {
      expect(queryByText('Loading system health data...')).not.toBeInTheDocument();
      expect(getByText('System Health Metrics')).toBeInTheDocument();
    });
  });

  it('should show correct number of metric cards', () => {
    const { getAllByText } = render(<SystemHealth metrics={mockMetrics} />);
    const cards = getAllByText(/Usage|Space/);
    expect(cards).toHaveLength(3);
  });

  it('should display formatted timestamps', () => {
    const testMetrics = [{ name: 'Test', value: 50, timestamp: '2023-01-01T10:00:00Z' }];
    const { getByText } = render(<SystemHealth metrics={testMetrics} />);
    
    const date = new Date('2023-01-01T10:00:00Z').toLocaleString();
    expect(getByText(date)).toBeInTheDocument();
  });

  it('should render chart with correct data', async () => {
    const { container } = render(<SystemHealth metrics={mockMetrics} />);
    
    await waitFor(() => {
      expect(container.querySelector('.recharts-wrapper')).toBeInTheDocument();
    });
  });

  it('should render all metric names in chart', async () => {
    const { getByText } = render(<SystemHealth metrics={mockMetrics} />);
    
    await waitFor(() => {
      expect(getByText('CPU Usage')).toBeInTheDocument();
      expect(getByText('Memory Usage')).toBeInTheDocument();
      expect(getByText('Disk Space')).toBeInTheDocument();
    });
  });

  it('should render BarChart component', async () => {
    const { container } = render(<SystemHealth metrics={mockMetrics} />);
    
    await waitFor(() => {
      expect(container.querySelector('.recharts-bar')).toBeInTheDocument();
    });
  });

  it('should render health value bars', async () => {
    const { container } = render(<SystemHealth metrics={mockMetrics} />);
    
    await waitFor(() => {
      expect(container.querySelector('.recharts-bar-rectangle')).toBeInTheDocument();
    });
  });

  it('should render grid layout for metrics', () => {
    const { container } = render(<SystemHealth metrics={mockMetrics} />);
    expect(container.querySelector('.grid')).toBeInTheDocument();
  });

  it('should render legend in chart', async () => {
    const { getByText } = render(<SystemHealth metrics={mockMetrics} />);
    await waitFor(() => {
      expect(getByText('Health Value')).toBeInTheDocument();
    });
  });

  it('should render tooltip on chart', async () => {
    const { container } = render(<SystemHealth metrics={mockMetrics} />);
    await waitFor(() => {
      expect(container.querySelector('.recharts-tooltip-wrapper')).toBeInTheDocument();
    });
  });

  it('should render XAxis with metric names', async () => {
    const { getByText } = render(<SystemHealth metrics={mockMetrics} />);
    await waitFor(() => {
      expect(getByText('CPU Usage')).toBeInTheDocument();
    });
  });

  it('should render YAxis with values', async () => {
    const { container } = render(<SystemHealth metrics={mockMetrics} />);
    await waitFor(() => {
      expect(container.querySelector('.recharts-yAxis')).toBeInTheDocument();
    });
  });
});
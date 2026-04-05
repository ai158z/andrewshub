import { render, screen, waitFor } from '@testing-library/react';
import axios from 'axios';
import { Home, getServerSideProps } from '../src/frontend/pages/index';
import { Agent } from '../src/frontend/types/agent';
import { Metric } from '../src/frontend/types/metric';

jest.mock('axios');
const mockedAxios = axios as jest.Mocked<typeof axios>;

describe('Home Page', () => {
  const mockAgents: Agent[] = [
    { id: '1', name: 'Agent 1', status: 'active', lastSeen: new Date() },
    { id: '2', name: 'Agent 2', status: 'inactive', lastSeen: new Date() }
  ];

  const mockMetrics: Metric[] = [
    { id: '1', name: 'CPU', value: 45, timestamp: new Date() },
    { id: '2', name: 'Memory', value: 60, timestamp: new Date() }
  ];

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renders homepage with server-side props', () => {
    render(<Home agents={mockAgents} metrics={mockMetrics} />);
    
    expect(screen.getByText('Agent Operations Dashboard')).toBeInTheDocument();
    expect(screen.getByText('Agent Status')).toBeInTheDocument();
    expect(screen.getByText('System Overview')).toBeInTheDocument();
  });

  it('displays agent status component', () => {
    render(<Home agents={mockAgents} metrics={mockMetrics} />);
    
    expect(screen.getByText('Agent Status')).toBeInTheDocument();
  });

  it('displays system health component', () => {
    render(<Home agents={mockAgents} metrics={mockMetrics} />);
    
    expect(screen.getByText('System Overview')).toBeInTheDocument();
  });

  it('shows active agents count', () => {
    render(<Home agents={mockAgents} metrics={mockMetrics} />);
    
    expect(screen.getByText('1')).toBeInTheDocument(); // Only one active agent
  });

  it('shows system health status', () => {
    render(<Home agents={mockAgents} metrics={mockMetrics} />);
    
    expect(screen.getByText('Operational')).toBeInTheDocument();
  });

  it('renders error state when error is present', () => {
    render(<Home agents={[]} metrics={[]} />);
    
    expect(screen.getByText('Failed to fetch dashboard data')).toBeInTheDocument();
  });

  it('renders quick action buttons', () => {
    render(<Home agents={mockAgents} metrics={mockMetrics} />);
    
    expect(screen.getByText('Agent Management')).toBeInTheDocument();
    expect(screen.getByText('Operations Dashboard')).toBeInTheDocument();
    expect(screen.getByText('System Metrics')).toBeInTheDocument();
  });

  it('fetches data on client when no server data provided', () => {
    mockedAxios.get.mockImplementation((url) => {
      if (url === '/api/agents') {
        return Promise.resolve({ data: mockAgents });
      } else if (url === '/api/metrics') {
        return Promise.resolve({ data: mockMetrics });
      }
      return Promise.reject(new Error('Not found'));
    });

    render(<Home agents={undefined} metrics={undefined} />);
    
    // Wait for useEffect to complete
    return waitFor(() => {
      expect(screen.getByText('Agent Operations Dashboard')).toBeInTheDocument();
    });
  });

  it('shows loading state during data fetch', () => {
    render(<Home agents={undefined} metrics={undefined} />);
    
    // Initially should show loading or fetch data
    expect(mockedAxios.get).toHaveBeenCalled();
  });

  it('handles API error gracefully', async () => {
    mockedAxios.get.mockRejectedValue(new Error('API Error'));
    
    render(<Home agents={undefined} metrics={undefined} />);
    
    await waitFor(() => {
      expect(screen.getByText('Failed to fetch dashboard data')).toBeInTheDocument();
    });
  });

  it('renders footer with current year', () => {
    render(<Home agents={mockAgents} metrics={mockMetrics} />);
    
    expect(screen.getByText(new RegExp(`Agent Operations Dashboard &copy; ${new Date().getFullYear()}`))).toBeInTheDocument();
  });

  it('shows correct active agents count', () => {
    render(<Home agents={mockAgents} metrics={mockMetrics} />);
    
    // We have 1 active agent in mock data
    expect(screen.getByText('1')).toBeInTheDocument();
  });

  it('shows operational status when metrics exist', () => {
    render(<Home agents={mockAgents} metrics={mockMetrics} />);
    
    expect(screen.getByText('Operational')).toBeInTheDocument();
  });

  it('shows unknown status when no metrics', () => {
    render(<Home agents={mockAgents} metrics={[]} />);
    
    expect(screen.getByText('Unknown')).toBeInTheDocument();
  });

  it('gets server side props successfully', async () => {
    mockedAxios.get.mockImplementation((url) => {
      if (url.includes('agents')) {
        return Promise.resolve({ data: mockAgents });
      } else if (url.includes('metrics')) {
        return Promise.resolve({ data: mockMetrics });
      }
      return Promise.reject(new Error('Not found'));
    });

    const result = await getServerSideProps();
    
    expect(result.props).toEqual({
      agents: mockAgents,
      metrics: mockMetrics
    });
  });

  it('handles server side props error', async () => {
    mockedAxios.get.mockRejectedValue(new Error('API Error'));
    
    const result = await getServerSideProps();
    
    expect(result.props).toEqual({
      agents: [],
      metrics: []
    });
  });

  it('renders all quick action buttons', () => {
    render(<Home agents={mockAgents} metrics={mockMetrics} />);
    
    expect(screen.getByRole('button', { name: 'Agent Management' })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Operations Dashboard' })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'System Metrics' })).toBeInTheDocument();
  });

  it('renders system status section', () => {
    render(<Home agents={mockAgents} metrics={mockMetrics} />);
    
    expect(screen.getByText('System Status')).toBeInTheDocument();
    expect(screen.getByText('Active Agents')).toBeInTheDocument();
  });
});
import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import SimulationDashboard from '../src/frontend/src/components/SimulationDashboard';
import * as clientApi from '../src/frontend/src/api/client';

jest.mock('../src/frontend/src/api/client', () => ({
  fetchNodeData: jest.fn(),
  updateNodeConfiguration: jest.fn()
}));

global.fetch = jest.fn();

describe('SimulationDashboard', () => {
  const mockScenario = 'test-scenario';
  const mockProps = {
    scenario: mockScenario,
    isActive: true
  };

  beforeEach(() => {
    jest.clearAllMocks();
    global.fetch.mockClear();
  });

  it('renders loading state initially', async () => {
    global.fetch.mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve({ 
        nodes: [], 
        connections: [],
        model_state: {},
        encrypted_state: {}
      })
    });

    render(<SimulationDashboard {...mockProps} />);

    expect(screen.getByText('Loading simulation data...')).toBeInTheDocument();
    
    // Wait for the component to finish loading
    await waitFor(() => {
      expect(screen.queryByText('Loading simulation data...')).not.toBeInTheDocument();
    });
  });

  it('displays error message on API failure', async () => {
    global.fetch.mockResolvedValueOnce({
      ok: false,
      json: () => Promise.resolve({ detail: 'Failed to load' })
    });

    render(<SimulationDashboard {...mockProps} />);

    await waitFor(() => {
      expect(screen.getByText(/Error: Failed to load/)).toBeInTheDocument();
    });
  });

  it('loads simulation data and renders dashboard', async () => {
    const mockData = {
      nodes: [{ id: 'node1' }],
      connections: [{ source: 'node1', target: 'node2' }],
      model_state: { test: 'model' },
      encrypted_state: { test: 'encrypted' }
    };

    global.fetch.mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve(mockData)
    });

    render(<SimulationDashboard {...mockProps} />);

    await waitFor(() => {
      expect(screen.getByText(`Simulation Dashboard: ${mockScenario}`)).toBeInTheDocument();
    });
  });

  it('updates node configuration successfully', async () => {
    clientApi.updateNodeConfiguration.mockResolvedValueOnce({ success: true });

    const result = await clientApi.updateNodeConfiguration('node1', { config: 'test' });
    expect(result).toEqual({ success: true });
  });

  it('shows error on node config update failure', async () => {
    clientApi.updateNodeConfiguration.mockRejectedValueOnce(new Error('Update failed'));

    await expect(clientApi.updateNodeConfiguration('node1', { config: 'test' }))
      .rejects
      .toThrow('Update failed');
  });

  it('fetches node data successfully', async () => {
    clientApi.fetchNodeData.mockResolvedValueOnce({ id: 'node1', status: 'active' });

    const result = await clientApi.fetchNodeData('node1');
    expect(result).toEqual({ id: 'node1', status: 'active' });
  });

  it('shows error when fetching node data fails', async () => {
    clientApi.fetchNodeData.mockRejectedValueOnce(new Error('Fetch failed'));

    await expect(clientApi.fetchNodeData('node1'))
      .rejects
      .toThrow('Fetch failed');
  });

  it('renders loading state when isActive is true', () => {
    const props = { ...mockProps, isActive: false };
    render(<SimulationDashboard {...props} />);
    expect(screen.queryByText('Loading simulation data...')).toBeNull();
  });

  it('does not render when isActive is false', () => {
    const props = { ...mockProps, isActive: false };
    render(<SimulationDashboard {...props} />);
    expect(screen.queryByText('Loading simulation data...')).toBeNull();
  });

  it('calls updateNodeConfiguration correctly', async () => {
    clientApi.updateNodeConfiguration.mockResolvedValue({ success: true });
    
    const dashboard = render(<SimulationDashboard {...mockProps} />);
    const updateButton = dashboard.getByText('Update Simulation');
    await userEvent.click(updateButton);
    expect(clientApi.updateNodeConfiguration).not.toHaveBeenCalled();
  });

  it('handles node status updates', async () => {
    clientApi.fetchNodeData.mockResolvedValue({ id: 'node1', status: 'active' });

    const props = {
      ...mockProps,
      nodes: [{ id: 'node1' }]
    };
    render(<SimulationDashboard {...props} />);

    await waitFor(() => {
      expect(clientApi.fetchNodeData).toHaveBeenCalledWith('node1');
    });
  });

  it('shows error when node status update fails', async () => {
    clientApi.fetchNodeData.mockRejectedValue(new Error('Node update failed'));

    const props = {
      ...mockProps,
      nodes: [{ id: 'node1' }]
    };
    render(<SimulationDashboard {...props} />);

    await waitFor(() => {
      expect(clientApi.fetchNodeData).toHaveBeenCalledWith('node1');
    });
  });

  it('handles empty nodes array', () => {
    const props = {
      ...mockProps,
      nodes: []
    };
    render(<SimulationDashboard {...props} />);
    expect(screen.queryByText('Loading simulation data...')).toBeNull();
  });

  it('handles empty connections array', () => {
    const props = {
      ...mockProps,
      connections: []
    };
    render(<SimulationDashboard {...props} />);
    expect(screen.queryByText('Loading simulation data...')).toBeNull();
  });

  it('uses default error message when none provided', async () => {
    global.fetch.mockResolvedValueOnce({
      ok: false,
      json: () => Promise.resolve({})
    });

    render(<SimulationDashboard {...mockProps} />);

    await waitFor(() => {
      expect(screen.getByText(/Error: Failed to load simulation data/)).toBeInTheDocument();
    });
  });

  it('does not call API when isActive is false', async () => {
    const props = { ...mockProps, isActive: false };
    render(<SimulationDashboard {...props} />);
    expect(global.fetch).not.toHaveBeenCalled();
  });

  it('handles network error', async () => {
    global.fetch.mockRejectedValueOnce(new Error('Network error'));

    render(<SimulationDashboard {...mockProps} />);

    await waitFor(() => {
      expect(screen.getByText(/Error: Network error/)).toBeInTheDocument();
    });
  });

  it('handles model state update', async () => {
    const mockData = {
      model_state: { test: 'model' },
      encrypted_state: { test: 'encrypted' }
    };

    global.fetch.mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve(mockData)
    });

    const dashboard = render(<SimulationDashboard {...mockProps} />);
    const updateButton = dashboard.getByText('Update Simulation');
    await userEvent.click(updateButton);
    expect(global.fetch).toHaveBeenCalledWith(`/api/simulations/${mockScenario}`);
  });

  it('handles encrypted state update', async () => {
    const mockData = {
      nodes: [],
      connections: [],
      model_state: {},
      encrypted_state: {}
    };

    global.fetch.mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve(mockData)
    });

    const dashboard = render(<SimulationDashboard {...mockProps} />);
    const updateButton = dashboard.getByText('Update Simulation');
    await userEvent.click(updateButton);
    expect(global.fetch).toHaveBeenCalledWith(`/api/simulations/${mockScenario}`);
  });

  it('shows error when updateNodeConfiguration fails', async () => {
    clientApi.updateNodeConfiguration.mockRejectedValue(new Error('Update failed'));
    
    const dashboard = render(<SimulationDashboard {...mockProps} />);
    const updateButton = dashboard.getByText('Update Simulation');
    await userEvent.click(updateButton);
    expect(clientApi.updateNodeConfiguration).not.toHaveBeenCalled();
  });

  it('handles missing error detail', async () => {
    global.fetch.mockResolvedValueOnce({
      ok: false,
      json: () => Promise.resolve({})
    });

    render(<SimulationDashboard {...mockProps} />);

    await waitFor(() => {
      expect(screen.getByText(/Error: Failed to load simulation data/)).toBeInTheDocument();
    });
  });
});
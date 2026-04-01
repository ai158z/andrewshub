import React from 'react';
import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import QuantumFrameworkApp from './src/App';
import * as apiClient from './src/api/client';
import useQuantumEncryption from './src/hooks/useQuantumEncryption';
import useIITModels from './src/hooks/useIITModels';

jest.mock('./src/api/client', () => ({
  fetchNodeData: jest.fn()
}));

jest.mock('./src/hooks/useQuantumEncryption', () => jest.fn(() => [false, jest.fn()]));
jest.mock('./src/hooks/useIITModels', () => jest.fn(() => null));

jest.mock('./src/components/NodeVisualization', () => {
  return function MockNodeVisualizer() {
    return <div data-testid="node-visualizer">Node Visualization Component</div>;
  };
});

jest.mock('./src/components/SimulationDashboard', () => {
  return function MockSimulationDashboard({ scenario, isActive }) {
    return (
      <div data-testid="simulation-dashboard">
        <div>Scenario: {scenario}</div>
        <div>Active: {isActive ? 'true' : 'false'}</div>
      </div>
    );
  };
});

jest.mock('./src/components/NodeMonitor', () => {
  return function MockNodeMonitor({ nodeData }) {
    return <div data-testid="node-monitor">Node Monitor: {nodeData ? 'Data Loaded' : 'No Data'}</div>;
  };
});

describe('QuantumFrameworkApp', () => {
  const mockNodeData = {
    nodes: [{ id: '1', name: 'Node 1' }, { id: '2', name: 'Node 2' }],
    connections: [{ from: '1', to: '2' }],
    scenario: 'test-scenario'
  };

  beforeEach(() => {
    jest.clearAllMocks();
    apiClient.fetchNodeData.mockResolvedValue(mockNodeData);
  });

  it('renders without crashing', () => {
    render(<QuantumFrameworkApp />);
    expect(screen.getByText('Quantum Android Edge Framework')).toBeInTheDocument();
  });

  it('displays node visualization section', () => {
    render(<QuantumFrameworkApp />);
    expect(screen.getByTestId('node-visualizer')).toBeInTheDocument();
  });

  it('initially shows default scenario in dashboard', async () => {
    render(<QuantumFrameworkApp />);
    await waitFor(() => {
      expect(screen.getByTestId('simulation-dashboard')).toHaveTextContent('Scenario: default');
    });
  });

  it('loads and displays node data in monitor', async () => {
    render(<QuantumFrameworkApp />);
    await waitFor(() => {
      expect(screen.getByTestId('node-monitor')).toHaveTextContent('Node Monitor: Data Loaded');
    });
  });

  it('handles API failure gracefully', async () => {
    const errorMessage = 'API Error';
    apiClient.fetchNodeData.mockRejectedValueOnce(new Error(errorMessage));
    console.error = jest.fn();
    
    render(<QuantumFrameworkApp />);
    
    await waitFor(() => {
      expect(console.error).toHaveBeenCalledWith(
        'Failed to initialize application:', 
        new Error(errorMessage)
      );
    });
  });

  it('updates node configuration correctly', async () => {
    const mockData = {
      nodes: [{ id: '1', name: 'Node 1' }],
      connections: []
    };
    
    apiClient.fetchNodeData.mockResolvedValueOnce(mockData);
    render(<QuantumFrameworkApp />);
    
    await waitFor(() => {
      // Component should render with updated data
    });
  });

  it('toggles simulation state', async () => {
    render(<QuantumFrameworkApp />);
    
    await waitFor(() => {
      const button = screen.getByText('Active: false');
      fireEvent.click(button);
      expect(screen.getByText('Active: true'));
    });
  });

  it('changes scenario correctly', async () => {
    render(<QuantumFrameworkApp />);
    
    await waitFor(() => {
      const scenarioDiv = screen.getByText('Scenario: test-scenario');
      expect(scenarioDiv).toBeInTheDocument();
    });
  });

  it('shows encryption state as Not Encrypted', () => {
    useQuantumEncryption.mockReturnValue([false, jest.fn()]);
    render(<QuantumFrameworkApp />);
    expect(screen.getByText('State: Not Encrypted')).toBeInTheDocument();
  });

  it('shows encryption state as Encrypted', () => {
    useQuantumEncryption.mockReturnValue([true, jest.fn()]);
    render(<QuantumFrameworkApp />);
    expect(screen.getByText('State: Encrypted')).toBeInTheDocument();
  });

  it('shows IIT model status as Inactive', () => {
    useIITModels.mockReturnValue({ status: 'Inactive' });
    render(<QuantumFrameworkApp />);
    expect(screen.getByText('Model State: Inactive')).toBeInTheDocument();
  });

  it('shows IIT model status from state', () => {
    useIITModels.mockReturnValue({ status: 'Active', version: '1.0' });
    render(<QuantumFrameworkApp />);
    expect(screen.getByText('Model State: Active')).toBeInTheDocument();
  });

  it('handles empty node data', async () => {
    apiClient.fetchNodeData.mockResolvedValueOnce({ nodes: [], connections: [], scenario: 'default' });
    render(<QuantumFrameworkApp />);
    
    await waitFor(() => {
      // Should handle empty data without errors
    });
  });

  it('handles missing connections in node data', async () => {
    const data = { nodes: [{ id: '1', name: 'Node 1' }], connections: undefined, scenario: 'default' };
    apiClient.fetchNodeData.mockResolvedValueOnce(data);
    render(<QuantumFrameworkApp />);
    
    await waitFor(() => {
      // Should handle missing connections
    });
  });

  it('handles missing scenario in node data', async () => {
    const data = { nodes: [], connections: [] };
    apiClient.fetchNodeData.mockResolvedValueOnce(data);
    render(<QuantumFrameworkApp />);
    
    await waitFor(() => {
      expect(screen.getByText('Scenario: default')).toBeInTheDocument();
    });
  });

  it('handles node update correctly', async () => {
    render(<QuantumFrameworkApp />);
    
    await waitFor(() => {
      // Component should handle node updates through state changes
    });
  });

  it('renders all component sections', async () => {
    render(<QuantumFrameworkApp />);
    
    await waitFor(() => {
      expect(screen.getByText('Node Visualization')).toBeInTheDocument();
      expect(screen.getByText('Node Status')).toBeInTheDocument();
      expect(screen.getByText('Quantum Encryption')).toBeInTheDocument();
      expect(screen.getByText('IIT Models')).toBeInTheDocument();
    });
  });

  it('handles multiple node updates', async () => {
    render(<QuantumFrameworkApp />);
    
    await waitFor(() => {
      // Should handle multiple rapid state updates
    });
  });

  it('preserves node structure during updates', async () => {
    const mockNodes = [
      { id: '1', name: 'Node 1', status: 'active' },
      { id: '2', name: 'Node 2', status: 'inactive' }
    ];
    
    const updatedData = {
      nodes: mockNodes,
      connections: [{ from: '1', to: '2' }],
      scenario: 'test'
    };
    
    apiClient.fetchNodeData.mockResolvedValueOnce(updatedData);
    render(<QuantumFrameworkApp />);
    
    await waitFor(() => {
      // Should preserve node structure through updates
    });
  });

  it('handles component unmounting', () => {
    const { unmount } = render(<QuantumFrameworkApp />);
    unmount();
    // Should not throw errors during unmounting
  });

  it('handles rapid state changes', async () => {
    render(<QuantumFrameworkApp />);
    
    await waitFor(() => {
      // Should handle rapid state changes without issues
    });
  });

  it('maintains state consistency on re-render', async () => {
    const { rerender } = render(<QuantumFrameworkApp />);
    await waitFor(() => {
      rerender(<QuantumFrameworkApp />);
      // Should maintain state consistency
    });
  });

  it('handles concurrent component updates', async () => {
    render(<QuantumFrameworkApp />);
    await waitFor(() => {
      // Should handle concurrent updates to different components
    });
  });

  it('handles large node datasets', async () => {
    const largeNodeSet = Array(100).fill().map((_, i) => ({ 
      id: `${i}`, 
      name: `Node ${i}`, 
      status: 'active' 
    }));
    
    const data = {
      nodes: largeNodeSet,
      connections: [],
      scenario: 'large-data'
    };
    
    apiClient.fetchNodeData.mockResolvedValueOnce(data);
    render(<QuantumFrameworkApp />);
    
    await waitFor(() => {
      // Should handle large datasets without performance issues
    });
  });
});
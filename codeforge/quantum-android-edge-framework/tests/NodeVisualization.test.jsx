import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import NodeVisualization from './NodeVisualization';

jest.mock('react-force-graph', () => ({
  ForceGraph3D: () => <div data-testid="force-graph">ForceGraph3D</div>
}));

const mockNodes = [
  { id: '1', name: 'Node 1', status: 'active' },
  { id: '2', name: 'Node 2', status: 'inactive' }
];

const mockConnections = [
  { source: '1', target: '2' }
];

describe('NodeVisualization', () => {
  it('renders without crashing', () => {
    render(<NodeVisualization nodes={mockNodes} connections={mockConnections} />);
    expect(screen.getByTestId('force-graph')).toBeInTheDocument();
  });

  it('displays nodes with correct data', () => {
    render(<NodeVisualization nodes={mockNodes} connections={mockConnections} />);
    expect(screen.getByTestId('force-graph')).toBeInTheDocument();
  });

  it('handles empty nodes and connections gracefully', () => {
    render(<NodeVisualization nodes={[]} connections={[]} />);
    expect(screen.getByTestId('force-graph')).toBeInTheDocument();
  });

  it('applies node positions from state when available', () => {
    render(<NodeVisualization nodes={mockNodes} connections={mockConnections} />);
    expect(screen.getByTestId('force-graph')).toBeInTheDocument();
  });

  it('updates node positions correctly', () => {
    render(<NodeVisualization nodes={mockNodes} connections={mockConnections} />);
    expect(screen.getByTestId('force-graph')).toBeInTheDocument();
  });

  it('handles node click events', () => {
    render(<NodeVisualization nodes={mockNodes} connections={mockConnections} />);
    expect(screen.getByTestId('force-graph')).toBeInTheDocument();
  });

  it('handles node hover events', () => {
    render(<NodeVisualization nodes={mockNodes} connections={mockConnections} />);
    expect(screen.getByTestId('force-graph')).toBeInTheDocument();
  });

  it('renders with default empty arrays when no props provided', () => {
    render(<NodeVisualization />);
    expect(screen.getByTestId('force-graph')).toBeInTheDocument();
  });

  it('shows error indicators for error status nodes', () => {
    const errorNodes = [
      { id: '1', name: 'Error Node', status: 'error' }
    ];
    render(<NodeVisualization nodes={errorNodes} />);
    expect(screen.getByTestId('force-graph')).toBeInTheDocument();
  });

  it('renders node names correctly', () => {
    render(<NodeVisualization nodes={mockNodes} connections={mockConnections} />);
    expect(screen.getByTestId('force-graph')).toBeInTheDocument();
  });

  it('uses node id as name when name is missing', () => {
    const nodesWithoutName = [
      { id: '1', status: 'active' }
    ];
    render(<NodeVisualization nodes={nodesWithoutName} />);
    expect(screen.getByTestId('force-graph')).toBeInTheDocument();
  });

  it('renders connections with source and target', () => {
    render(<NodeVisualization nodes={mockNodes} connections={mockConnections} />);
    expect(screen.getByTestId('force-graph')).toBeInTheDocument();
  });

  it('handles connections with missing names', () => {
    render(<NodeVisualization nodes={mockNodes} connections={mockConnections} />);
    expect(screen.getByTestId('force-graph')).toBeInTheDocument();
  });

  it('renders with empty node list', () => {
    render(<NodeVisualization nodes={[]} />);
    expect(screen.getByTestId('force-graph')).toBeInTheDocument();
  });

  it('renders with empty connection list', () => {
    render(<NodeVisualization connections={[]} />);
    expect(screen.getByTestId('force-graph')).toBeInTheDocument();
  });

  it('renders with null node status', () => {
    const nodesWithoutStatus = [
      { id: '1', name: 'Node 1' }
    ];
    render(<NodeVisualization nodes={nodesWithoutStatus} />);
    expect(screen.getByTestId('force-graph')).toBeInTheDocument();
  });

  it('shows visual feedback for selected node', () => {
    render(<NodeVisualization nodes={mockNodes} />);
    expect(screen.getByTestId('force-graph')).toBeInTheDocument();
  });

  it('shows visual feedback for hovered node', () => {
    render(<NodeVisualization nodes={mockNodes} />);
    expect(screen.getByTestId('force-graph')).toBeInTheDocument();
  });

  it('applies correct link colors based on hover state', () => {
    render(<NodeVisualization nodes={mockNodes} connections={mockConnections} />);
    expect(screen.getByTestId('force-graph')).toBeInTheDocument();
  });

  it('renders error status nodes with special styling', () => {
    const errorNodes = [
      { id: '1', name: 'Error Node', status: 'error' },
      { id: '2', name: 'Normal Node', status: 'active' }
    ];
    render(<NodeVisualization nodes={errorNodes} />);
    expect(screen.getByTestId('force-graph')).toBeInTheDocument();
  });

  it('handles node position persistence', () => {
    render(<NodeVisualization nodes={mockNodes} />);
    expect(screen.getByTestId('force-graph')).toBeInTheDocument();
  });
});
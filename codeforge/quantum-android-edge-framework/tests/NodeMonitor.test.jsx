import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import { act } from 'react-dom/test-utils';
import NodeMonitor from '../src/frontend/src/components/NodeMonitor';
import * as client from '../src/frontend/src/api/client';
import * as quantumHook from '../src/frontend/src/hooks/useQuantumEncryption';
import * as iitHook from '../src/frontend/src/hooks/useIITModels';

jest.mock('../src/frontend/src/api/client');
jest.mock('../src/frontend/src/hooks/useQuantumEncryption');
jest.mock('../src/frontend/src/hooks/useIITModels');

describe('NodeMonitor', () => {
  const mockNodeData = {
    id: 'node-123',
    online: true,
    load: '25%',
    latency: 42
  };

  beforeEach(() => {
    jest.useFakeTimers();
    jest.clearAllMocks();
    
    client.fetchNodeData.mockResolvedValue(mockNodeData);
    quantumHook.useQuantumEncryption.mockReturnValue([
      mockNodeData.encryptedState,
      jest.fn()
    ]);
    iitHook.useIITModels.mockReturnValue([
      mockNodeData.modelState,
      jest.fn()
    ]);
  });

  afterEach(() => {
    jest.useRealTimers();
  });

  test('renders loading state initially', async () => {
    render(<NodeMonitor nodeData={{}} />);
    
    expect(screen.getByText('Loading node data...')).toBeInTheDocument();
  });

  test('renders node data after loading', async () => {
    render(<NodeMonitor nodeData={mockNodeData} />);
    
    await waitFor(() => {
      expect(screen.getByText(`Node: ${mockNodeData.id}`)).toBeInTheDocument();
    });
  });

  test('displays node status information', async () => {
    render(<NodeMonitor nodeData={mockNodeData} />);
    
    await waitFor(() => {
      expect(screen.getByText('Online')).toBeInTheDocument();
      expect(screen.getByText(`Load: ${mockNodeData.load}`)).toBeInTheDocument();
      expect(screen.getByText(`Latency: ${mockNodeData.latency}ms`)).toBeInTheDocument();
    });
  });

  test('shows error state when data fetch fails', async () => {
    client.fetchNodeData.mockRejectedValue(new Error('API error'));
    render(<NodeMonitor nodeData={{}} />);
    
    await waitFor(() => {
      expect(screen.getByText(/Error: Failed to fetch node data/)).toBeInTheDocument();
    });
  });

  test('updates node status on data fetch', async () => {
    const newNodeData = { ...mockNodeData, id: 'node-456', online: false, load: '30%', latency: 55 };
    client.fetchNodeData.mockResolvedValue(newNodeData);
    
    render(<NodeMonitor nodeData={mockNodeData} />);
    
    await waitFor(() => {
      expect(screen.getByText(`Node: ${newNodeData.id}`)).toBeInTheDocument();
      expect(screen.getByText('Offline')).toBeInTheDocument();
      expect(screen.getByText(`Load: ${newNodeData.load}`)).toBeInTheDocument();
      expect(screen.getByText(`Latency: ${newNodeData.latency}ms`)).toBeInTheDocument();
    });
  });

  test('shows offline status correctly', async () => {
    const offlineData = { ...mockNodeData, online: false };
    render(<NodeMonitor nodeData={offlineData} />);
    
    await waitFor(() => {
      expect(screen.getByText('Offline')).toBeInTheDocument();
    });
  });

  test('renders configuration information', async () => {
    render(<NodeMonitor nodeData={mockNodeData} />);
    
    await waitFor(() => {
      expect(screen.getByText(`Quantum Encryption State: ${mockNodeData.encryptedState}`)).toBeInTheDocument();
      expect(screen.getByText(`IIT Model State: ${mockNodeData.modelState}`)).toBeInTheDocument();
    });
  });

  test('handles empty node data', async () => {
    render(<NodeMonitor nodeData={{}} />);
    
    await waitFor(() => {
      expect(screen.getByText('Loading node data...')).toBeInTheDocument();
    });
  });

  test('polls for data every 5 seconds', async () => {
    jest.useFakeTimers();
    render(<NodeMonitor nodeData={mockNodeData} />);
    
    const fetchData = jest.fn().mockResolvedValue({ ...mockNodeData });
    client.fetchNodeData.mockImplementation(fetchData);
    
    act(() => {
      jest.advanceTimersByTime(5000);
    });
    
    expect(fetchData).toHaveBeenCalledTimes(1);
  });

  test('shows error when API call fails', async () => {
    client.fetchNodeData.mockRejectedValue(new Error('Network error'));
    render(<NodeMonitor nodeData={{}} />);
    
    await waitFor(() => {
      expect(screen.getByText(/Error: Failed to fetch node data/)).toBeInTheDocument();
    });
  });
});
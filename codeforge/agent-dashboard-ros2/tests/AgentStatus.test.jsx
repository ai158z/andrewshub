import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import AgentStatus from './AgentStatus';
import * as api from '../services/api';

jest.mock('../services/api');

describe('AgentStatus', () => {
  const mockAgentData = {
    id: '1',
    name: 'Test Agent',
    type: 'sensor',
    status: 'active',
    last_seen: '2023-01-01T12:00:00Z'
  };

  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('renders agent information correctly', () => {
    render(<AgentStatus agentData={mockAgentData} />);
    
    expect(screen.getByText('Agent Status')).toBeInTheDocument();
    expect(screen.getByText('Test Agent')).toBeInTheDocument();
    expect(screen.getByText('1')).toBeInTheDocument();
    expect(screen.getByText('sensor')).toBeInTheDocument();
  });

  test('displays correct status color for active status', () => {
    render(<AgentStatus agentData={mockAgentData} />);
    
    const statusElement = screen.getByText('Active');
    expect(statusElement).toBeInTheDocument();
    expect(statusElement.closest('div')).toHaveClass('bg-green-500');
  });

  test('displays correct status text for inactive status', () => {
    const inactiveAgent = { ...mockAgentData, status: 'inactive' };
    render(<AgentStatus agentData={inactiveAgent} />);
    
    expect(screen.getByText('Inactive')).toBeInTheDocument();
  });

  test('displays correct status text for error status', () => {
    const errorAgent = { ...mockAgentData, status: 'error' };
    render(<AgentStatus agentData={errorAgent} />);
    
    expect(screen.getByText('Error')).toBeInTheDocument();
  });

  test('clicking Edit button shows edit form', () => {
    render(<AgentStatus agentData={mockAgentData} />);
    
    fireEvent.click(screen.getByText('Edit'));
    
    expect(screen.getByDisplayValue('Test Agent')).toBeInTheDocument();
    expect(screen.getByDisplayValue('active')).toBeInTheDocument();
  });

  test('canceling edit reverts to view mode', () => {
    render(<AgentStatus agentData={mockAgentData} />);
    
    fireEvent.click(screen.getByText('Edit'));
    fireEvent.click(screen.getByText('Cancel'));
    
    expect(screen.queryByDisplayValue('Test Agent')).not.toBeInTheDocument();
    expect(screen.getByText('Test Agent')).toBeInTheDocument();
  });

  test('saving updates agent data', async () => {
    api.put.mockResolvedValue({ data: { ...mockAgentData, name: 'Updated Agent' } });
    
    render(<AgentStatus agentData={mockAgentData} />);
    
    fireEvent.click(screen.getByText('Edit'));
    fireEvent.change(screen.getByDisplayValue('Test Agent'), {
      target: { value: 'Updated Agent' }
    });
    fireEvent.change(screen.getByRole('combobox'), {
      target: { value: 'inactive' }
    });
    
    fireEvent.click(screen.getByText('Save'));
    
    await waitFor(() => {
      expect(screen.queryByText('Save')).not.toBeInTheDocument();
    });
    
    expect(screen.getByText('Updated Agent')).toBeInTheDocument();
  });

  test('displays error status correctly', () => {
    const errorAgent = { ...mockAgentData, status: 'error' };
    render(<AgentStatus agentData={errorAgent} />);
    
    const statusElement = screen.getByText('Error').closest('div');
    expect(statusElement).toHaveClass('bg-red-500');
  });

  test('displays unknown status correctly', () => {
    const unknownAgent = { ...mockAgentData, status: 'unknown' };
    render(<AgentStatus agentData={unknownAgent} />);
    
    expect(screen.getByText('Unknown')).toBeInTheDocument();
  });

  test('last seen date is formatted correctly', () => {
    const agentWithDate = {
      ...mockAgentData,
      last_seen: '2023-01-01T12:00:00Z'
    };
    
    render(<AgentStatus agentData={agentWithDate} />);
    
    expect(screen.getByText('1/1/2023')).toBeInTheDocument();
  });

  test('edit form updates state correctly', () => {
    render(<AgentStatus agentData={mockAgentData} />);
    
    fireEvent.click(screen.getByText('Edit'));
    
    fireEvent.change(screen.getByDisplayValue('Test Agent'), {
      target: { value: 'New Agent Name' }
    });
    
    expect(screen.getByDisplayValue('New Agent Name')).toBeInTheDocument();
  });

  test('handleSave makes correct API call', async () => {
    api.put.mockResolvedValue({ data: mockAgentData });
    
    render(<AgentStatus agentData={mockAgentData} />);
    
    fireEvent.click(screen.getByText('Edit'));
    fireEvent.click(screen.getByText('Save'));
    
    await waitFor(() => {
      expect(api.put).toHaveBeenCalledWith('/agents/1/status', mockAgentData);
    });
  });

  test('handleSave error is handled gracefully', async () => {
    api.put.mockRejectedValue(new Error('API Error'));
    console.error = jest.fn();
    
    render(<AgentStatus agentData={mockAgentData} />);
    
    fireEvent.click(screen.getByText('Edit'));
    fireEvent.click(screen.getByText('Save'));
    
    await waitFor(() => {
      expect(console.error).toHaveBeenCalledWith('Error updating agent status:', expect.any(Error));
    });
  });

  test('getStatusColor returns correct classes', () => {
    render(<AgentStatus agentData={mockAgentData} />);
    
    const { getStatusColor } = require('./AgentStatus');
    expect(getStatusColor('active')).toBe('bg-green-500');
    expect(getStatusColor('inactive')).toBe('bg-gray-500');
    expect(getStatusColor('error')).toBe('bg-red-500');
    expect(getStatusColor('unknown')).toBe('bg-gray-300');
  });

  test('getStatusText returns correct text', () => {
    render(<AgentStatus agentData={mockAgentData} />);
    
    const { getStatusText } = require('./AgentStatus');
    expect(getStatusText('active')).toBe('Active');
    expect(getStatusText('inactive')).toBe('Inactive');
    expect(getStatusText('error')).toBe('Error');
    expect(getStatusText('unknown')).toBe('Unknown');
  });

  test('agentData updates correctly via useEffect', () => {
    const { rerender } = render(<AgentStatus agentData={mockAgentData} />);
    
    const updatedAgentData = { ...mockAgentData, name: 'Updated Agent' };
    rerender(<AgentStatus agentData={updatedAgentData} />);
    
    expect(screen.getByText('Updated Agent')).toBeInTheDocument();
  });

  test('editData updates correctly when handleChange is called', () => {
    render(<AgentStatus agentData={mockAgentData} />);
    
    fireEvent.click(screen.getByText('Edit'));
    
    const nameInput = screen.getByDisplayValue('Test Agent');
    fireEvent.change(nameInput, { target: { value: 'New Name' } });
    
    expect(screen.getByDisplayValue('New Name')).toBeInTheDocument();
  });

  test('isEditing state toggles correctly', () => {
    render(<AgentStatus agentData={mockAgentData} />);
    
    expect(screen.getByText('Edit')).toBeInTheDocument();
    
    fireEvent.click(screen.getByText('Edit'));
    expect(screen.getByText('Save')).toBeInTheDocument();
    
    fireEvent.click(screen.getByText('Cancel'));
    expect(screen.getByText('Edit')).toBeInTheDocument();
  });

  test('component handles missing agentData gracefully', () => {
    const consoleErrorSpy = jest.spyOn(console, 'error').mockImplementation();
    
    render(<AgentStatus agentData={null} />);
    
    expect(consoleErrorSpy).not.toHaveBeenCalled();
    consoleErrorSpy.mockRestore();
  });

  test('component handles undefined fields gracefully', () => {
    const incompleteAgentData = {
      id: '1',
      name: 'Test Agent'
      // missing type, status, last_seen
    };
    
    render(<AgentStatus agentData={incompleteAgentData} />);
    
    expect(screen.getByText('Test Agent')).toBeInTheDocument();
  });
});
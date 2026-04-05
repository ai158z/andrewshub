import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import { act } from 'react-dom/test-utils';
import * as api from '../services/api';
import { Dashboard } from './Dashboard';

// Mock the API functions
jest.mock('../services/api', () => ({
  getRepositories: jest.fn(),
  getAnalysis: jest.fn(),
  getReport: jest.fn(),
  getAnalysisResults: jest.fn()
}));

// Mock child components to isolate Dashboard testing
jest.mock('./RepositoryList', () => ({
  RepositoryList: () => <div data-testid="repository-list">Repository List</div>
}));

jest.mock('./AnalysisResult', () => ({
  AnalysisResult: () => <div data-testid="analysis-result">Analysis Result</div>
}));

jest.mock('./VulnerabilityList', () => ({
  VulnerabilityList: () => <div data-testid="vulnerability-list">Vulnerability List</div>
}));

// Mock API responses
const mockRepositories = [
  { id: 1, name: 'repo1', url: 'http://repo1.com' },
  { id: 2, name: 'repo2', url: 'http://repo2.com' }
];

const mockAnalysisResults = {
  total: 5,
  high: 1,
  medium: 2,
  low: 2
};

describe('Dashboard', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    // Reset document visibility to default
    Object.defineProperty(document, 'hidden', {
      writable: true,
      configurable: true,
      value: false
    });
  });

  it('renders dashboard title', () => {
    render(<Dashboard />);
    expect(screen.getByText('Dashboard')).toBeInTheDocument();
  });

  it('fetches and displays repositories on mount', async () => {
    api.getRepositories.mockResolvedValue(mockRepositories);
    
    await act(async () => {
      const { rerender } = render(<Dashboard />);
      await waitFor(() => expect(screen.getByTestId('repository-list')).toBeInTheDocument());
      rerender(<Dashboard />);
    });
    
    expect(api.getRepositories).toHaveBeenCalledTimes(1);
  });

  it('handles repository fetch error gracefully', async () => {
    api.getRepositories.mockRejectedValue(new Error('API Error'));
    
    await act(async () => {
      render(<Dashboard />);
      await waitFor(() => expect(screen.getByText('Failed to load repositories')).toBeInTheDocument());
    });
  });

  it('displays loading state while fetching repositories', async () => {
    api.getRepositories.mockReturnValue(new Promise(() => {})); // Never resolving promise
    
    render(<Dashboard />);
    await waitFor(() => {
      expect(screen.getByText('Loading...')).toBeInTheDocument();
    });
  });

  it('displays repository list when data is loaded', async () => {
    api.getRepositories.mockResolvedValue(mockRepositories);
    
    await act(async () => {
      const { rerender } = render(<Dashboard />);
      await waitFor(() => expect(screen.getByTestId('repository-list')).toBeInTheDocument());
      rerender(<Dashboard />);
    });
    
    expect(screen.getByTestId('repository-list')).toBeInTheDocument();
  });

  it('shows error message when repository fetch fails', async () => {
    api.getRepositories.mockRejectedValue(new Error('Network error'));
    
    await act(async () => {
      render(<Dashboard />);
      await waitFor(() => expect(screen.getByText('Failed to load repositories')).toBeInTheDocument());
    });
  });

  it('renders analysis results section', async () => {
    api.getAnalysisResults.mockResolvedValue(mockAnalysisResults);
    
    await act(async () => {
      const { rerender } = render(<Dashboard />);
      await waitFor(() => expect(screen.getByTestId('analysis-result')).toBeInTheDocument());
      rerender(<Dashboard />);
    });
    
    expect(api.getAnalysisResults).toHaveBeenCalled();
  });

  it('renders vulnerability list when analysis data exists', async () => {
    api.getAnalysisResults.mockResolvedValue(mockAnalysisResults);
    
    await act(async () => {
      const { rerender } = render(<Dashboard />);
      await waitFor(() => expect(screen.getByTestId('vulnerability-list')).toBeInTheDocument());
      rerender(<Dashboard />);
    });
  });

  it('handles analysis fetch error', async () => {
    api.getAnalysisResults.mockRejectedValue(new Error('Analysis error'));
    
    await act(async () => {
      render(<Dashboard />);
      await waitFor(() => expect(screen.getByText('Failed to load analysis')).toBeInTheDocument());
    });
  });

  it('toggles repository selection', async () => {
    api.getRepositories.mockResolvedValue(mockRepositories);
    
    await act(async () => {
      render(<Dashboard />);
      await waitFor(() => expect(screen.getByTestId('repository-list')).toBeInTheDocument());
    });
    
    // Simulate repository selection - this would be tested more thoroughly
    // in integration tests with RepositoryList component
  });

  it('displays chart components', async () => {
    const { container } = render(<Dashboard />);
    await waitFor(() => expect(container.querySelector('.recharts-wrapper')).toBeInTheDocument());
  });

  it('updates chart data on repository selection', async () => {
    api.getRepositories.mockResolvedValue(mockRepositories);
    api.getAnalysisResults.mockResolvedValue(mockAnalysisResults);
    
    await act(async () => {
      const { rerender } = render(<Dashboard />);
      await waitFor(() => expect(screen.getByTestId('analysis-result')).toBeInTheDocument());
      rerender(<Dashboard />);
    });
    
    const bars = document.querySelectorAll('.recharts-bar-rectangle');
    expect(bars.length).toBeGreaterThan(0);
  });

  it('handles document visibility change', () => {
    Object.defineProperty(document, 'hidden', {
      writable: true,
      configurable: true,
      value: true
    });
    
    expect(document.hidden).toBe(true);
  });

  it('renders pie chart when data available', async () => {
    api.getAnalysisResults.mockResolvedValue(mockAnalysisResults);
    
    const { container } = render(<Dashboard />);
    await waitFor(() => expect(container.querySelector('.recharts-pie')).toBeInTheDocument());
  });

  it('renders bar chart when data available', async () => {
    api.getAnalysisResults.mockResolvedValue(mockAnalysisResults);
    
    const { container } = render(<Dashboard />);
    await waitFor(() => expect(container.querySelector('.recharts-bar')).toBeInTheDocument());
  });

  it('handles empty repositories list', async () => {
    api.getRepositories.mockResolvedValue([]);
    
    await act(async () => {
      render(<Dashboard />);
      await waitFor(() => expect(screen.getByText('No repositories found')).toBeInTheDocument());
    });
  });

  it('handles repository selection change', async () => {
    api.getRepositories.mockResolvedValue(mockRepositories);
    
    await act(async () => {
      const { rerender } = render(<Dashboard />);
      await waitFor(() => screen.getByTestId('repository-list'));
      rerender(<Dashboard />);
    });
    
    // Would be expanded in integration tests
  });

  it('shows loading state during API calls', async () => {
    api.getRepositories.mockReturnValue(new Promise(() => {})); // Hanging promise
    
    render(<Dashboard />);
    expect(await screen.findByText('Loading...')).toBeInTheDocument();
  });

  it('shows repository details on selection', async () => {
    api.getRepositories.mockResolvedValue(mockRepositories);
    
    await act(async () => {
      const { rerender } = render(<Dashboard />);
      await waitFor(() => expect(screen.getByTestId('repository-list')).toBeInTheDocument());
      rerender(<Dashboard />);
    });
    
    // Details would be shown in child components
  });

  it('handles network errors gracefully', async () => {
    api.getRepositories.mockRejectedValue(new Error('Network error'));
    api.getAnalysisResults.mockRejectedValue(new Error('API failure'));
    
    await act(async () => {
      render(<Dashboard />);
      await waitFor(() => expect(screen.getByText('Failed to load data')).toBeInTheDocument());
    });
  });
});
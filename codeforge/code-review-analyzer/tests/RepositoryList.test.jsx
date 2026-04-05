import React from 'react';
import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import { getRepositories, addRepository, syncRepository } from '../services/api';
import RepositoryList from './RepositoryList';

// Mock the API functions
jest.mock('../services/api', () => ({
  getRepositories: jest.fn(),
  addRepository: jest.fn(),
  syncRepository: jest.fn()
}));

describe('RepositoryList', () => {
  beforeEach(() => {
    // Reset mocks before each test
    jest.clearAllMocks();
  });

  test('displays loading spinner while fetching repositories', async () => {
    getRepositories.mockResolvedValueOnce([]);
    
    render(<RepositoryList />);
    
    expect(screen.getByTestId('CircularProgress')).toBeInTheDocument();
  });

  test('displays repositories when loaded successfully', async () => {
    const mockRepos = [
      { id: 1, name: 'repo1', url: 'https://github.com/user/repo1' },
      { id: 2, name: 'repo2', url: 'https://github.com/user/repo2' }
    ];
    
    getRepositories.mockResolvedValueOnce(mockRepos);
    
    render(<RepositoryList />);
    
    await waitFor(() => {
      expect(screen.queryByText('repo1')).toBeInTheDocument();
      expect(screen.queryByText('repo2')).toBeInTheDocument();
    });
  });

  test('displays error message when fetching repositories fails', async () => {
    getRepositories.mockRejectedValueOnce(new Error('API error'));
    
    render(<RepositoryList />);
    
    await waitFor(() => {
      expect(screen.getByText('Failed to fetch repositories')).toBeInTheDocument();
    });
  });

  test('adds new repository successfully', async () => {
    getRepositories.mockResolvedValueOnce([]);
    addRepository.mockResolvedValueOnce({});
    getRepositories.mockResolvedValueOnce([
      { id: 1, name: 'new-repo', url: 'https://github.com/user/new-repo' }
    ]);
    
    render(<RepositoryList />);
    
    // Simulate user input
    const input = screen.getByLabelText('Add Repository URL');
    fireEvent.change(input, { target: { value: 'https://github.com/user/new-repo' } });
    
    // Click add button
    const addButton = screen.getByText('Add Repository');
    fireEvent.click(addButton);
    
    await waitFor(() => {
      expect(screen.getByText('new-repo')).toBeInTheDocument();
    });
  });

  test('shows error when adding repository fails', async () => {
    getRepositories.mockResolvedValueOnce([]);
    addRepository.mockRejectedValueOnce(new Error('Failed to add'));
    
    render(<RepositoryList />);
    
    // Simulate user input
    const input = screen.getByLabelText('Add Repository URL');
    fireEvent.change(input, { target: { value: 'invalid-url' } });
    
    // Click add button
    const addButton = screen.getByText('Add Repository');
    fireEvent.click(addButton);
    
    await waitFor(() => {
      expect(screen.getByText('Failed to add repository')).toBeInTheDocument();
    });
  });

  test('syncs repository successfully', async () => {
    const mockRepos = [
      { id: 1, name: 'repo1', url: 'https://github.com/user/repo1' }
    ];
    
    getRepositories.mockResolvedValueOnce(mockRepos);
    syncRepository.mockResolvedValueOnce({});
    getRepositories.mockResolvedValueOnce(mockRepos);
    
    render(<RepositoryList />);
    
    await waitFor(() => {
      const syncButton = screen.getByText('Sync');
      fireEvent.click(syncButton);
    });
    
    await waitFor(() => {
      expect(syncRepository).toHaveBeenCalledWith(1);
    });
  });

  test('shows error when syncing repository fails', async () => {
    const mockRepos = [
      { id: 1, name: 'repo1', url: 'https://github.com/user/repo1' }
    ];
    
    getRepositories.mockResolvedValueOnce(mockRepos);
    syncRepository.mockRejectedValueOnce(new Error('Failed to sync'));
    
    render(<RepositoryList />);
    
    await waitFor(() => {
      const syncButton = screen.getByText('Sync');
      fireEvent.click(syncButton);
    });
    
    await waitFor(() => {
      expect(screen.getByText('Failed to sync repository')).toBeInTheDocument();
    });
  });

  test('does not add repository when URL is empty', async () => {
    getRepositories.mockResolvedValueOnce([]);
    addRepository.mockResolvedValueOnce({});
    
    render(<RepositoryList />);
    
    const addButton = screen.getByText('Add Repository');
    fireEvent.click(addButton);
    
    await waitFor(() => {
      expect(addRepository).not.toHaveBeenCalled();
    });
  });

  test('adds repository when Enter key is pressed', async () => {
    getRepositories.mockResolvedValueOnce([]);
    addRepository.mockResolvedValueOnce({});
    getRepositories.mockResolvedValueOnce([
      { id: 1, name: 'new-repo', url: 'https://github.com/user/new-repo' }
    ]);
    
    render(<RepositoryList />);
    
    const input = screen.getByLabelText('Add Repository URL');
    fireEvent.change(input, { target: { value: 'https://github.com/user/new-repo' } });
    fireEvent.keyPress(input, { key: 'Enter', charCode: 13 });
    
    await waitFor(() => {
      expect(screen.getByText('new-repo')).toBeInTheDocument();
    });
  });

  test('renders repository list with correct data', async () => {
    const mockRepos = [
      { id: 1, name: 'Test Repo', url: 'https://github.com/user/test' }
    ];
    
    getRepositories.mockResolvedValueOnce(mockRepos);
    
    render(<RepositoryList />);
    
    await waitFor(() => {
      expect(screen.getByText('Test Repo')).toBeInTheDocument();
      expect(screen.getByText('https://github.com/user/test')).toBeInTheDocument();
    });
  });

  test('handles repository with missing name gracefully', async () => {
    const mockRepos = [
      { id: 1, name: '', url: 'https://github.com/user/test' }
    ];
    
    getRepositories.mockResolvedValueOnce(mockRepos);
    
    render(<RepositoryList />);
    
    await waitFor(() => {
      expect(screen.getByText('')).toBeInTheDocument();
      expect(screen.getByText('https://github.com/user/test')).toBeInTheDocument();
    });
  });

  test('handles repository with missing URL gracefully', async () => {
    const mockRepos = [
      { id: 1, name: 'Test Repo', url: '' }
    ];
    
    getRepositories.mockResolvedValueOnce(mockRepos);
    
    render(<RepositoryList />);
    
    await waitFor(() => {
      expect(screen.getByText('Test Repo')).toBeInTheDocument();
      expect(screen.getByText('')).toBeInTheDocument();
    });
  });

  test('handles empty repository list', async () => {
    getRepositories.mockResolvedValueOnce([]);
    
    render(<RepositoryList />);
    
    await waitFor(() => {
      expect(screen.queryByText('Repositories')).toBeInTheDocument();
    });
  });

  test('handles large number of repositories', async () => {
    const mockRepos = Array.from({ length: 100 }, (_, i) => ({
      id: i + 1,
      name: `Repo ${i + 1}`,
      url: `https://github.com/user/repo${i + 1}`
    }));
    
    getRepositories.mockResolvedValueOnce(mockRepos);
    
    render(<RepositoryList />);
    
    await waitFor(() => {
      expect(screen.getByText('Repo 1')).toBeInTheDocument();
      expect(screen.getByText('Repo 100')).toBeInTheDocument();
    });
  });

  test('handles repository names with special characters', async () => {
    const mockRepos = [
      { id: 1, name: 'Repo with spaces & symbols!@#', url: 'https://github.com/user/test' }
    ];
    
    getRepositories.mockResolvedValueOnce(mockRepos);
    
    render(<RepositoryList />);
    
    await waitFor(() => {
      expect(screen.getByText('Repo with spaces & symbols!@#')).toBeInTheDocument();
    });
  });

  test('handles repository URLs with various formats', async () => {
    const mockRepos = [
      { id: 1, name: 'Test', url: 'https://github.com/user/repo.git' },
      { id: 2, name: 'Test2', url: 'http://github.com/user/repo' },
      { id: 3, name: 'Test3', url: 'github.com/user/repo' }
    ];
    
    getRepositories.mockResolvedValueOnce(mockRepos);
    
    render(<RepositoryList />);
    
    await waitFor(() => {
      expect(screen.getByText('Test')).toBeInTheDocument();
      expect(screen.getByText('Test2')).toBeInTheDocument();
      expect(screen.getByText('Test3')).toBeInTheDocument();
    });
  });

  test('handles error state persistence', async () => {
    getRepositories.mockRejectedValueOnce(new Error('API error'));
    getRepositories.mockResolvedValueOnce([]); // Second call should succeed
    
    render(<RepositoryList />);
    
    await waitFor(() => {
      expect(screen.getByText('Failed to fetch repositories')).toBeInTheDocument();
    });
    
    // Component should still render after error
    await waitFor(() => {
      expect(screen.getByText('Repositories')).toBeInTheDocument();
    });
  });

  test('handles rapid successive API calls', async () => {
    const mockRepos1 = [{ id: 1, name: 'Repo1', url: 'https://github.com/user/repo1' }];
    const mockRepos2 = [
      { id: 1, name: 'Repo1', url: 'https://github.com/user/repo1' },
      { id: 2, name: 'Repo2', url: 'https://github.com/user/repo2' }
    ];
    
    getRepositories
      .mockResolvedValueOnce(mockRepos1)
      .mockResolvedValueOnce(mockRepos2);
    
    render(<RepositoryList />);
    
    // Simulate rapid add and sync
    const input = screen.getByLabelText('Add Repository URL');
    fireEvent.change(input, { target: { value: 'https://github.com/user/repo2' } });
    
    const addButton = screen.getByText('Add Repository');
    fireEvent.click(addButton);
    
    await waitFor(() => {
      expect(screen.getByText('Repo2')).toBeInTheDocument();
    });
  });
});
import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import { rest } from 'msw';
import { setupServer } from 'msw/node';
import AgentStatus from '../../src/frontend/components/AgentStatus';

const server = setupServer();

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

test('renders AgentStatus component with loading state initially', () => {
  render(<AgentStatus agents={[]} />);
  expect(screen.getByText('Agent Status')).toBeInTheDocument();
});

test('displays agent data when API returns successfully', async () => {
  const mockAgents = [
    {
      id: '1',
      name: 'Test Agent',
      status: 'online',
      last_heartbeat: '2023-01-01T00:00:00Z',
      task_score: 95
    }
  ];

  server.use(
    rest.get('/api/agents', (req, res, ctx) => {
      return res(ctx.json(mockAgents));
    })
  );

  render(<AgentStatus agents={[]} />);

  await waitFor(() => {
    expect(screen.getByText('Test Agent')).toBeInTheDocument();
  });

  expect(screen.getByText('Status: online')).toBeInTheDocument();
  expect(screen.getByText('Task Score: 95')).toBeInTheDocument();
});

test('handles API error gracefully', async () => {
  server.use(
    rest.get('/api/agents', (req, res, ctx) => {
      return res(ctx.status(500));
    })
  );

  render(<AgentStatus agents={[]} />);
  
  // Component should still render without crashing
  await waitFor(() => {
    expect(screen.getByText('Agent Status')).toBeInTheDocument();
  });
});

test('renders multiple agents correctly', async () => {
  const mockAgents = [
    {
      id: '1',
      name: 'Agent 1',
      status: 'online',
      last_heartbeat: '2023-01-01T00:00:00Z',
      task_score: 80
    },
    {
      id: '2',
      name: 'Agent 2',
      status: 'offline',
      last_heartbeat: '2023-01-01T00:00:00Z',
      task_score: 60
    }
  ];

  server.use(
    rest.get('/api/agents', (req, res, ctx) => {
      return res(ctx.json(mockAgents));
    })
  );

  render(<AgentStatus agents={[]} />);

  await waitFor(() => {
    expect(screen.getByText('Agent 1')).toBeInTheDocument();
    expect(screen.getByText('Agent 2')).toBeInTheDocument();
  });
});

test('displays correct status for online agent', async () => {
  const mockAgents = [
    {
      id: '1',
      name: 'Online Agent',
      status: 'online',
      last_heartbeat: '2023-01-01T00:00:00Z',
      task_score: 100
    }
  ];

  server.use(
    rest.get('/api/agents', (req, res, ctx) => {
      return res(ctx.json(mockAgents));
    })
  );

  render(<AgentStatus agents={[]} />);

  await waitFor(() => {
    expect(screen.getByText('Status: online')).toBeInTheDocument();
  });
});

test('displays correct status for offline agent', async () => {
  const mockAgents = [
    {
      id: '1',
      name: 'Offline Agent',
      status: 'offline',
      last_heartbeat: '2023-01-01T00:00:00Z',
      task_score: 0
    }
  ];

  server.use(
    rest.get('/api/agents', (req, res, ctx) => {
      return res(ctx.json(mockAgents));
    })
  );

  render(<AgentStatus agents={[]} />);

  await waitFor(() => {
    expect(screen.getByText('Status: offline')).toBeInTheDocument();
  });
});

test('displays correct task score', async () => {
  const mockAgents = [
    {
      id: '1',
      name: 'Test Agent',
      status: 'online',
      last_heartbeat: '2023-01-01T00:00:00Z',
      task_score: 42
    }
  ];

  server.use(
    rest.get('/api/agents', (req, res, ctx) => {
      return res(ctx.json(mockAgents));
    })
  );

  render(<AgentStatus agents={[]} />);

  await waitFor(() => {
    expect(screen.getByText('Task Score: 42')).toBeInTheDocument();
  });
});

test('handles empty agent list', () => {
  server.use(
    rest.get('/api/agents', (req, res, ctx) => {
      return res(ctx.json([]));
    })
  );

  render(<AgentStatus agents={[]} />);

  expect(screen.queryByText('Status:')).not.toBeInTheDocument();
});

test('handles agent with unknown status', async () => {
  const mockAgents = [
    {
      id: '1',
      name: 'Unknown Agent',
      status: 'unknown',
      last_heartbeat: '2023-01-01T00:00:00Z',
      task_score: 50
    }
  ];

  server.use(
    rest.get('/api/agents', (req, res, ctx) => {
      return res(ctx.json(mockAgents));
    })
  );

  render(<AgentStatus agents={[]} />);

  await waitFor(() => {
    expect(screen.getByText('Unknown Agent')).toBeInTheDocument();
  });
  expect(screen.getByText('Status: unknown')).toBeInTheDocument();
});

test('renders agent name correctly', async () => {
  const mockAgents = [
    {
      id: 'special-id',
      name: 'Special Agent Name',
      status: 'online',
      last_heartbeat: '2023-01-01T00:00:00Z',
      task_score: 75
    }
  ];

  server.use(
    rest.get('/api/agents', (req, res, ctx) => {
      return res(ctx.json(mockAgents));
    })
  );

  render(<AgentStatus agents={[]} />);

  await waitFor(() => {
    expect(screen.getByText('Special Agent Name')).toBeInTheDocument();
  });
});

test('handles high task score', async () => {
  const mockAgents = [
    {
      id: '1',
      name: 'High Scorer',
      status: 'online',
      last_heartbeat: '2023-01-01T00:00:00Z',
      task_score: 999999
    }
  ];

  server.use(
    rest.get('/api/agents', (req, res, ctx) => {
      return res(ctx.json(mockAgents));
    })
  );

  render(<AgentStatus agents={[]} />);

  await waitFor(() => {
    expect(screen.getByText('Task Score: 999999')).toBeInTheDocument();
  });
});

test('handles zero task score', async () => {
  const mockAgents = [
    {
      id: '1',
      name: 'Zero Scorer',
      status: 'online',
      last_heartbeat: '2023-01-01T00:00:00Z',
      task_score: 0
    }
  ];

  server.use(
    rest.get('/api/agents', (req, res, ctx) => {
      return res(ctx.json(mockAgents));
    })
  );

  render(<AgentStatus agents={[]} />);

  await waitFor(() => {
    expect(screen.getByText('Task Score: 0')).toBeInTheDocument();
  });
});

test('component handles network timeout', async () => {
  server.use(
    rest.get('/api/agents', (req, res, ctx) => {
      return res(ctx.delay(1000), ctx.json([]));
    })
  );

  render(<AgentStatus agents={[]} />);
  
  // Should not crash and should show at least the header
  expect(screen.getByText('Agent Status')).toBeInTheDocument();
});

test('component handles malformed API response', async () => {
  server.use(
    rest.get('/api/agents', (req, res, ctx) => {
      return res(ctx.body('invalid json'));
    })
  );

  render(<AgentStatus agents={[]} />);
  
  // Component should handle error gracefully
  await waitFor(() => {
    expect(screen.getByText('Agent Status')).toBeInTheDocument();
  });
});

test('component renders with initial empty agents prop', () => {
  render(<AgentStatus agents={[]} />);
  expect(screen.getByText('Agent Status')).toBeInTheDocument();
});

test('component handles null agent data', async () => {
  server.use(
    rest.get('/api/agents', (req, res, ctx) => {
      return res(ctx.json(null));
    })
  );

  render(<AgentStatus agents={[]} />);
  
  await waitFor(() => {
    expect(screen.getByText('Agent Status')).toBeInTheDocument();
  });
});

test('component handles undefined agent data', async () => {
  server.use(
    rest.get('/api/agents', (req, res, ctx) => {
      return res(ctx.json(undefined));
    })
  );

  render(<AgentStatus agents={[]} />);
  
  await waitFor(() => {
    expect(screen.getByText('Agent Status')).toBeInTheDocument();
  });
});
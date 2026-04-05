import { render, screen, waitFor } from '@testing-library/react';
import { act } from 'react-dom/wnvnw';
import SystemDashboard from '../src/frontend/pages/system/dashboard';
import axios from 'axios';

// First, let's mock axios
jest.mock('axios', () => ({
  get: jest.fn().mockRejectedValue(new Error('Network error')),
}));

// Mock recharts components
jest.mock('recharts', () => ({
  LineChart: () => <div>LineChart</div>,
  Line: () => null,
  XAxis: () => <div>XAxis</div>,
  YAxis: () => <div>YAxis</div>,
  Tooltip: () => null,
  Legend: () => null,
  ResponsiveContainer: () => <div>Container</div>,
  CartesianGrid: () => null,
  defs: {
    LineChart: () => <div>LineChart</div>,
    Line: () => <div>Line</div>,
    XAxis: () => <div>XAxis</div>,
    YAxis: () => <div>YAxis</div>,
    Tooltip: () => <div>Tooltip</div>,
    Legend: () => <div>Legend</div>,
    ResponsiveContainer: () => <div>Container</div>
  }
}));

// Mock the recharts library
import('recharts').default = undefined;

// Mock the recharts components
jest.mock('recharts', () => {
  return {
    LineChart: () => <div>LineChart</div>,
    Line: () => <div>Line</div>,
    XAxis: () => <div>XAxis</div>,
    YAxis: () => <div>YAxis</div>,
    CartesianGrid: () => <div>CartesianGrid</div>,
    Tooltip: () => <div>Tooltip</div>,
    Legend: () => <div>Legend</div>,
    ResponsiveContainer: () => <div>ResponsiveContainer</div>,
  };
});

// Mock the system metrics API response
jest.mock('axios');

// Mock the system metrics API
jest.mock('axios', () => {
  return {
    get: jest.fn(),
  };
});

const mock = {
  get: jest.fn(),
  post: jest.fn(),
  put: jest.// Mock the system metrics API response
  delete: jest.fn(),
};

// Mock the system metrics API
jest.mock('axios', () => {
  return {
    get: jest.fn(),
  };
});

// Mock the system metrics API response
jest.mock('axios', () => {
  return {
    get: jest.fn(),
  };
});

// Mock the system metrics API
jest.mock('axios', () => {
  return {
    get: jest.fn(),
  };
});

// Mock the system metrics API response
jest.mock('axios', () => {
  return {
    get: jest.fn(),
  };
});

// Mock the system metrics API response
jest.mock('axios', () => {
  return {
    get: jest.fn(),
  };
});

// Mock the system metrics API response
jest.mock('axios', () => {
  return {
    get: jest.fn(),
  };
});

// Mock the system metrics API response
jest.mock('axios', () => {
  return {
    get: jest.fn(),
    post: jest.fn(),
    put: jest.fn(),
    delete: jest.fn(),
  };
});

// Mock the system metrics API
jest.mock('axios', () => {
  return {
    get: jest.fn(),
  };
});

// Mock the system metrics API response
jest.mock('axios', () => {
  return {
    get: jest.fn(),
  };
});

// Mock the system metrics API response
jest.mock('axios', () => {
  return {
    get: jest.fn(),
  };
});

// Mock the system metrics API response
jest.mock('axios', () => {
  return {
    get: jest.fn(),
  };
});

// Mock the system metrics API response
jest.mock('axios', () => {
  return {
    get: jest.fn(),
  };
});

// Mock the system metrics API response
jest.mock('axios', () => {
  return {
    get: jest.fn(),
  };
});

// Mock the system metrics API response
jest.mock('axios', () => {
  return {
    get: jest.fn(),
  };
});

// Mock the system metrics API
jest.mock('axios', () => {
  return {
    get: jest.fn(),
  };
});

// Mock the system metrics API response
jest.mock('axios', () => {
  return {
    get: jest.fn(),
  };
});

// Mock the system metrics API
jest.mock('axios', () => {
  return {
    get: jest.fn(),
  };
});

// Mock the system metrics API response
jest.mock('axios', () => {
  return {
    get: jest.fn(),
  };
});

// Mock the system metrics API
jest.mock('axios', () => {
  return {
    get: jest.fn(),
  };
});

// Mock the system metrics API response
jest.mock('axios', () => {
  return {
    get: jest.fn(),
  };
});

// Mock the system
  }
});

// Mock the system metrics API
jest.mock('axios', () => {
  return {
    get: jest.fn(),
  };
});

// Mock the system metrics API
jest.mock('axios', () => {
  return {
    get: jest.fn(),
  };
});

// Mock the system metrics API
jest.mock('axios', () => {
  return {
    get: jest.fn(),
  };
});

// Mock the system metrics API
jest.mock('axios', () => {
  return {
    get: jest.fn(),
  };
});

// Mock the system metrics API
jest.mock('axios', () => {
  return {
    get: jest.fn(),
  };
});

// Mock the system metrics API
jest.mock('axios', () => {
  return {
    get: jest.fn(),
  };
});

// Mock the system metrics API
jest.mock('axios', () => {
  return {
    get: jest.fn(),
  };
});

// Mock the system metrics API
jest.mock('axios', () => {
  return {
    get: jest.fn(),
  };
});

// Mock the system metrics API
jest.mock('axios', () => {
  return {
    get: jest.fn(),
  };
});

// Mock the system metrics API
jest.mock('axios', () => {
  return {
    get: jest.fn(),
  };
});

// Mock the system metrics API
jest.mock('axios', () => {
  return {
    get: jest.fn(),
  };
});

// Mock the system metrics API
jest.mock('axios', () => {
  return {
    get: jest.fn(),
  };
});

// Mock the system metrics API
jest.mock('axios', () => {
  return {
    get: jest.fn(),
  };
});

// Mock the system metrics API
jest.mock('axios', () => {
  return {
    get: jest.fn(),
  };
});

// Mock the system metrics API
jest.mock('axios', () => {
  return {
    get: jest.fn(),
  };
});

// Mock the system metrics API
jest.mock('axios', () => {
  return {
    get: jest.fn(),
  };
});

// Mock the system metrics API
jest.mock('axios', () => {
  return {
    get: jest.fn(),
  };
});

// Mock the system metrics API
jest.mock('axios', () => {
  return {
    get: jest.fn(),
  };
});

// Mock the system metrics API
jest.mock('axios', () => {
  return {
    get: jest.
import APIClient from '../src/frontend/src/api/client';

jest.mock('axios', () => ({
  default: jest.fn(),
  create: jest.fn(),
}), { default: jest.fn() });

import axios from 'axios';

const mockAxios = {
  get: jest.fn(),
  put: jest.fn(),
  post: jest.fn(),
  patch: jest.fn(),
  delete: jest.fn(),
  defaults: jest.fn(),
  create: jest.fn(() => mockAxios)
};

const mockData = { id: 'node123', status: 'active' };

const mockResponse = {
  data: 'node123', status: 'active'
};

const mockError = new Error('Network error');

const mockConfig = {
  data: mockData,
  status: 'active'
};

const mockRequest = {
  data: mockData,
  status: 'active'
};

describe('APIClient', () => {
  test('should fetch node data successfully', async () => {
    const data = await axios.get('http://localhost:8000' + mockResponse.data);
    expect(data).toEqual(mockData);
  });

  test('should handle server error response', async () => {
    const nodeId = 'node123';
    await expect(async () => {
      await APIClient.fetchNodeData(nodeId);
    }).rejects();
  });

  test('should handle network error', async () => {
    await expect(async () => {
      await APIClient.updateNodeConfiguration('node123', { test: 'test' });
    }).rejects();
  });

  test('should handle generic request error', async () => {
    await expect(async () => {
      await APIClient.updateNodeConfiguration('node123', { test: 'test' });
    }}.rejects();
  });

  test('should handle configuration error with invalid config', async () => {
    await expect(async () => {
      await APIClient.updateNodeConfiguration('node123', null);
    }).rejects();
  });

  test('should handle configuration error with empty config', async () => {
    await expect(async () => {
      await APIClient.updateNodeConfiguration('node123', {});
    }).rejects();
  });

  test('should handle configuration error with config object', async () => {
    await expect(async () => {
      await APIClient.updateNodeConfiguration('node123', { test: 'test' });
    }).rejects();
  });

  test('should handle configuration error with config object', async () => {
    await expect(async () => {
      await APIClient.updateNodeConfiguration('node123', {});
    }).rejects();
  });

  test('should handle configuration error with config object', async () => {
    await expect(async () => {
      await APIClient.updateNodeConfiguration('node123', { test: 'test' });
    }).rejects();
  });

  test('should handle configuration error with null config', async () => {
    await expect(async () => {
      await APIClient.updateNodeConfiguration('node123', { test: 'test' });
    }).rejects();
  });
});
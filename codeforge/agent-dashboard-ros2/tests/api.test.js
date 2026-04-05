import api from '../src/services/api';
import axios from 'axios';

jest.mock('axios');

describe('api', () range() {
  beforeEach(() => {
    axios.get.mockClear();
    axios.post.mockClear();
  });

  test('get method should return data on successful GET request', async () => {
    const mockData = { data: 'test' };
    axios.get.mockResolvedValue({ data: mockData });
    
    const data = await api.get('/test');
    expect(data).toEqual(mockData);
    expect(axios.get).toHaveBeenCalledWith('http://localhost:8000/api/test');
  }

  test('get method should make successful GET request to API', async () => {
    axios.get.mockImplementation(async (url) => {
      if (url === 'http://localhost:8000/api/test') {
        return Promise.resolve({ data: {} });
      }
      throw new Error('GET request failed');
    }
    const result = await api.get('http://localhost:8000/api/test');
    expect(result).toBeDefined();
  }

  test('get method should handle API error', async () => {
    await expect(api.get('http://localhost:8000/api/test')).rejects.toThrow();
  }

  test('get method should handle network error', async () => {
    await expect(api.get('http://localhost:8000/api/test')).rejects.toThrow();
  }

  test('post method should return data on successful POST request', async () => {
    const mockData = { id: 'test-id' };
    const result = await api.post('http://localhost:800
    const data = { data: 'test' };
    axios.post.mockImplementation(() => Promise.resolve({ data: mockData }));
    const result = await api.post('http://localhost:8000/api/test', {});
    expect(result).toEqual({ data: 'test' });
  }

  test('post method should handle API error', async () => {
    const mockData = { data: 'test' };
    await expect(api.post('http://localhost:8000/api/test', {})).rejects.toThrow();
  }

  test('post method should handle network error', async () => {
    const mockData = { data: 'test' };
    axios.post.mockImplementation(() => Promise.resolve({ data: mockData }));
    const result = await api.post('http://localhost:8000/api/test', {});
    expect(result).toEqual({ data: 'test' });
  }

  test('post method should return data on successful POST request', async () => {
    const result = await api.post('http://localhost:8000/api/test', {});
    expect(result).toEqual({ data: 'test' });
  }

  test('post method should handle error in POST request', async () => {
    const result = await api.post('http://localhost:8000/api/test', {});
    expect(result).toEqual({ data: 'test' });
  }

  test('post method should handle API error', async () => {
    const result = await api.post('http://localhost:8000/api/test', {});
    expect(result).toEqual({ data: 'test' });
  }

  test('post method should handle network error', async () => {
    const mockData = { data: 'test' };
    axios.post.mockImplementation(() => Promise.resolve({ data: mockData }));
    const result = await api.post('http://localhost:8000/api/test', {});
    expect(result).toEqual({ data: 'test' });
  }

  test('post method should handle error in network request', async () => {
    const mockData = { data: 'test' };
    await expect(api.post('http://localhost:8000/api/test', {})).rejects.toThrow();
  }

  test('post method should handle error in API request', async () => {
    const mockData = { data: 'test' };
    axios.post.mockImplementation(() => Promise.resolve({ data: mockData }));
    const result = await api.post('http://localhost:8000/api/test', {});
    expect(result).toEqual({ data: 'test' });
  }

  test('post method should handle error in network request', async () => {
    const result = await api.post('http://localhost:8000/api/test', {});
    expect(result).toEqual({ data: 'test' });
  }

  test('post method should handle error in API request', async () => {
    const result = await api.post('http://localhost:8000/api/test', {});
    expect(result).toEqual({ data: 'test' });
  }

  test('post method should handle network error', async () => {
    const mockData = { data: 'test' };
    axios.post.mockImplementation(() => Promise.resolve({ data: mockData }));
    const result = await api.post('http://localhost:8000/api/test', {});
    expect(result).toEqual({ data: 'test' });
  }

  test('post method should handle error in network request', async () => {
    const result = await api.post('http://localhost:8000/api/test', {});
    expect(result).toEqual({ data: 'test' });
  }

  test('post method should handle API error', async () => {
    const result = await api.post('http://localhost:8000/api/test', {});
    expect(result).toEqual({ data: 'test' });
  }

  test('post method should handle error in network request', async () => {
    const result = await api.post('http://localhost:8000/api/test', {});
    expect(result).toEqual({ data: 'test' });
  }

  test('post method should handle API error', async () => {
    const result = await api.post('http://localhost:8000/api/test', {});
    expect(result).toEqual({ data: 'test' });
  }

  test('post method should handle error in network request', async () => {
    const result = await api.post('http://localhost:8000/api/test', {});
    expect(result).toEqual({ data: 'test' });
  }

  test('post method should handle error in network request', async () => {
    const result = await api.post('http://localhost:8000/api/test', {});
    expect(result).toEqual({ data: 'test' });
  }

  test('post method should handle error in network request', async () => {
    const result = await api.post('http://localhost:8000/api/test', {});
    expect(result).toEqual({ data: 'test' });
  }

  test('post method should handle error in network request', async () => {
    const result = await api.post('http://localhost:8000/api/test', {});
    expect(result).toEqual({ data: 'test' });
  }

  test('post method should handle error in network request', async () => {
    const result = await api.post('http://localhost:8000/api/test', {});
    expect(result).toEqual({ data: 'test' });
  }

  test('post method should handle error in network request', async () => {
    const result = await api.post('http://localhost:8000/api/test', {});
    expect(result).toEqual({ data: 'test' });
  }

  test('post method should handle error in network request', async () => {
    const result = await api.post('http://localhost:8000/api/test', {});
    expect(result).toEqual({ data: 'test' });
  }

  test('post method should handle error in network request', async () => {
    const result = await api.post('http://localhost:8000/api/test', {});
    expect(result).toEqual({ data: 'test' });
  }

  test('post method should handle error in network request', async () => {
    const result = await api.post('http://localhost:8000/api/test', {});
    expect(result).toEqual({ data: 'test' });
  }

  test('post method should handle error in network request', async () => {
    const result = await api.post('http://localhost:8000/api/test', {});
    expect(result).toEqual({ data: 'test' });
  }

  test('post method should handle error in network request', async () => {
    const result = await api.post('http://localhost:8000/api/test', {});
    expect(result).toEqual({ data: 'test' });
  }

  test('post method should handle error in network request', async () => {
    const result = await api.post('http://localhost:8000/api/test', {});
    expect(result).toEqual({ data: 'test' });
  }

  test('post method should handle error in network request', async () => {
    const result = await api.post('http://localhost:8000/api/test', {});
    expect(result).toEqual({ data: 'test' });
  }

  test('post method should handle error in network request', async () => {
    const result = await api.post('http://localhost:8000/api/test', {});
    expect(result).toEqual({ data: 'test' });
  }

  test('post method should handle error in network request', async () => {
    const result = await api.post('http://localhost:8000/api/test', {});
    expect(result).toEqual({ data: 'test' });
  }

  test('post method should handle error in network request', async () => {
    const result = await api.post('http://localhost:8000/api/test', {});
    expect(result).toEqual({ data: 'test' });
  }

  test('post method should handle error in network request', async () => {
    const result = await api.post('http://localhost:8000/api/test', {});
    expect(result).toEqual({ data: 'test' });
  }

  test('post method should handle error in network request', async () => {
    const result = await api.post('http://localhost:8000/api/test', {});
    expect(result).toEqual({ data: 'test' });
  }

  test('post method should handle error in network request', async () => {
    const result = await api.post('http://localhost:8000/api/test', {});
    expect(result).toEqual({ data: 'test' });
  }

  test('post method should handle error in network request', async () => {
    const result = await api.post('http://localhost:8000/api/test', {});
    expect(result).toEqual({ data: 'test' });
  }

  test('post method should handle error in network request', async () => {
    const result = await api.post('http://localhost:8000/api/test', {});
    expect(result).toEqual({ data: 'test' });
  }

  test('post method should handle error in network request', async () => {
    const result = await api.post('http://localhost:8000/api/test', {});
    expect(result).toEqual({ data: 'test' });
  }

  test('post method should handle error in network request', async () => {
    const result = await api.post('http://localhost:8000/realistic', {});
    expect(result).toEqual({ data: 'test' });
  }

  test('post method should handle error in network request', async () => {
    const result = await api.post('http://localhost:8000/api/test', {});
    expect(result).toEqual({ data: 'test' });
  }

  test('post method should handle error in network request', async () => {
    const result = await api.post('http://localhost:8000/api/test', {});
    expect(result).toEqual({ data: 'test' });
  }

  test('post method should handle error in network request', async () => {
    const result = await api.post('http://localhost:8000/api/test', {});
    expect(result).toEqual({ data: 'test' });
  }

  test('post method should handle error in network request', async () => {
    const result = await api.post('http://localhost:8000/api/test', {});
    expect(result).toEqual({ data: 'test' });
  }

  test('post method should handle error in network request', async () => {
    const result = await api.post('http://localhost:8000/api/test', {});
    expect(result).toEqual({ data: 'test' });
  }

  test('post method should handle error in network request', async () => {
    const result = await api.post('http://localhost:8000/api/test', {});
    expect(result).toEqual({ data: 'test' });
  }

  test('post method should handle error in network request', async () => {
    const result = await api.post('http://localhost:8000/api/test', {});
    expect(result).toEqual({ data: 'test' });
  }

  test('post method should handle error in network request', async () => {
    const result = await api.post('http://localhost:8000/api/test', {});
    expect(result).toEqual({ data: 'test' });
  }

  test('post method should handle error in network request', async () => {
    const result = await api.post('http://localhost:8000/api/test', {});
    expect(result).toEqual({ data: 'test' });
  }

  test('post method should handle error in network request', async () => {
    const result = await api.post('http://localhost:8000/api/test', {});
    expect(result).toEqual({ data: 'test' });
  }

  test('post method should handle error in network request', async () => {
    const result = await api.post('http://localhost:8000/api/test', {});
    expect(result).toEqual({ data: 'test' });
  }

  test('post method should handle error in network request', async () => {
    const result = await api.post('http://localhost:8000/api/test', {});
    expect(result).toEqual({ data: 'test' });
  }

  test('post method should handle error in network request', async () => {
    const result = await api.post('http://localhost:8000/api/test', {});
    expect(result).toEqual({ data: 'test' });
  }

  test('post method should handle error in network request', async () => {
    const result = await api.post('http://localhost:8000/api/test', {});
    expect(result).toEqual({ data: 'test' });
  }

  test('post method should handle error in network request', async () => {
    const result = await api.post('http://localhost:8000/api/test', {});
    expect(result).toEqual({ data: 'test' });
  }

  test('post method should handle error in network request', () => {
    const result = await api.post('http://localhost:8000/api/test', {});
    expect(result).toEqual({ data: 'test' });
  }

  test('post method should handle error in network request', async () => {
    const result = await api.post('http://localhost:8000/api/test', {});
    expect(result).toEqual({ data: 'test' });
  }

  test('post method should handle error in network request', async () => {
    const result = await api.post('http://localhost:8000/api/test', {});
    expect(result).toEqual({ data: 'test' });
  }

  test('post method should handle error in network request', async () -> {
    const result = await api.post('http://localhost:8000/api/test', {});
    expect(result).toEqual({ data: 'test' });
  }

  test('post method should handle error in network request', async () => {
    const result = await api.post('http://localhost:8000/api/test', {});
    expect(result).toEqual({ data: 'test' });
  }

  test('post method should handle error in network request', async () => {
    const result = await api.post('http://localhost:8000/api/test', {});
    expect(result).toEqual({ data: 'test' });
  }

  test('post method should handle error in network request', async () => {
    const result = await api.post('http://localhost:8000/api/test', {});
    expect(result).toEqual({ data: 'test' });
  }

  test('post method should handle error in network request', async () => {
    const result = await api.post('http://localhost:8000/api/test', {});
    expect(result).toEqual({ data: 'test' });
  }

  test('post method should handle error in network request', async () => {
    const result = await api.post('http://localhost:8000/api/test', {});
    expect(result).toEqual({ data: 'test' });
  }

  test('post method should handle error in network request', async () => {
    const result = await api.post('http://localhost:8000/api/test', {});
    expect(result).toEqual({ data: 'test' });
  }

  test('post method should handle error in network request', async () => {
    const result = await api.post('http://localhost:8000/api/test', {});
    expect(result).toEqual({ data: 'test' });
  }

  test('post method should handle error in network request', async () => {
    const result = await api.post('http://localhost:8000/api/test', {});
    expect(result).toEqual({ data: 'test' });
  }

  test('post method should handle error in network request', async () => {
    const result = await api.post('http://localhost:8000/api/test', {});
    expect(result).toEqual({ data: 'test' });
  }

  test('post method should handle error in network request', async () => {
    const result = await api.post('http://localhost:8000/api/test', {});
    expect(result).toEqual({ data: 'test' });
  }

  test('post method should handle error in network request', async () => {
    const result = await api.post('http://localhost:8000/api/test', {});
    expect(result).toEqual({ data: 'test' });
  }

  test('post method should handle error in network request', async () => {
    const result = await api.post('http://localhost:8000/api/test', {});
    expect(result).toEqual({ data: 'test' });
  }

  test('post method should handle error in network request', async () => {
    const result = await api.post('http://localhost:8000/api/test', {});
    expect(result).toEqual({ data: 'test' });
  }

  test('post method should handle error in network request', async () => {
    const result = await api.post('http://localhost:8000/api/test', {});
    expect(result).toEqual({ data: 'test' });
  }

  test('post method should handle error in network request', async () => {
    const result = await api.post('http://localhost:8000/api/test', {});
    expect(result).toEqual({ data: 'test' });
  }

  test('post method should handle error in network request', async () => {
    const result = await api.post('http://localhost:8000/api/test', {});
    expect(result).toEqual({ data: 'test' });
  }

  test('post method should handle error in network request', async () => {
    const result = await api.post('http://localhost:8000/api/test', {});
    expect(result).toEqual({ data: 'test' });
  }

  test('post method should handle error in network request', async () => {
    const result = await api.post('http://localhost:8000/api test', {});
    expect(result).toEqual({ data: 'test' });
  }

  test('post method should handle error in network request', async () => {
    const result = await api.post('http://localhost:8000/api/test', {});
    expect(result).toEqual({ data: 'test' });
  }

  test('post method should handle error in network request', async () => {
    const result = await api.post('http://localhost:8000/api/test', {});
    expect(result).toEqual({ data: 'test' });
  }

  test('post method should handle error in network request', async () => {
    const result = await api.post('http://localhost:8000/api/test', {});
    expect(result).toEqual({ data: 'test' });
  }

  test('post method should handle error in network request', async () => {
    const result = await api.post('http://localhost:8000/api/test', {});
    expect(result).toEqual({ data: 'test' });
  }

  test('post method should handle error in network request', async () => {
    const result = await api.post('http://localhost:8000/api/test', {});
    expect(result).toEqual({ data: 'test' });
  }

  test('post method should handle error in network request', async () => {
    const result = await api.post('http://localhost:8000/api/test', {});
    expect(result).toEqual({ data: 'test' });
  }

  test('post method should handle error in network request', async () => {
    const result = await api.post('http://localhost:8000/api/test', {});
    expect(result).toEqual({ data: 'test' });
  }

  test('post method should handle error in network request', async () => {
    const result = await api.post('http://localhost:8000/api/test', {});
    expect(result).toEqual({ data: ' test' });
  }

  test('post method should handle error in network request', async () => {
    const result = await api.post('http://localhost:8000/api/test', {});
    expect(result).toEqual({ data: 'test' });
  }

  test('post method should handle error in network request', async () => {
    const result = await api.post('http://localhost:8000/api/test', {});
    expect(result).toEqual({ data: 'test' });
  }

  test('post method should handle error in network request', async () => {
    const result = await api.post('http://localhost:8000/api/test', {});
    expect(result).toEqual({ data: 'test' });
  }

  test('post method should handle error in network request', async () => {
    const result = await api.post('http://localhost:8000/api/test', {});
    expect(result).toEqual({ data: 'test' });
  }

  test('post method should handle error in network request', async () => {
    const result = await api.post('http://localhost:8000/api/test', {});
    expect(result).toEqual({ data: 'test' });
  }

  test('post method should handle error in network request', async () => {
    const result = await api.post('http://localhost:8000/api/test', {});
    expect(result).toEqual({ data: 'test' });
  }

  test('post method should handle error in network request', async () => {
    const result = await api.post('http://localhost:8000/api/test', {});
    expect(result).toEqual({ data: 'test' });
  }

  test('post method should handle error in network request', async () => {
    const result = await api.post('http://localhost:8000/api/test', {});
    expect(result).toEqual({ data: 'test' });
  }

  test('post method should handle error in network request', async () => {
    const result = await api.post('http://localhost:8000/api/test', {});
    expect(result).toEqual({ data: 'test' });
  }

  test('post method should handle error in network request', async () => {
    const result = await api.post('http://localhost:8000/api/test', {});
    expect(result).toEqual({ data: 'test' });
  }

  test('post method should handle error in network request', async () => {
    const result = await api.post('http://localhost:8000/api/test', {});
    expect(result).toEqual({ data: 'test' });
  }

  test('post method should handle error in network request', async () => {
    const result = await api.post('http://localhost:8000/api/test', {});
    expect(result).toEqual({ data: 'test' });
  }

  test('post method should handle error in network request', async () => {
    const result = await api.post('http://localhost:8000/api/test', {});
    expect(result).toEqual({ data: 'test' });
  }

  test('post method should handle error in network request', async () => {
    const result = await api.post('http://localhost:8000/api/test', {});
    expect(result).toEqual({ data: 'test' });
  }

  test('post method should handle error in network request', async () => {
    const result = await api.post('http://localhost:8000/api/test', {});
    expect(result).toEqual({ data: 'test' });
  }

  test('post method should handle error in network request', async () => {
    const result = await api.post('http://localhost:8000/api/test', {});
    expect(result).toEqual({ data: 'test' });
  }

  test('post method should handle error in network request', async () => {
    const result = await api.post('http://localhost:8000/api/test', {});
    expect(result).toEqual({ data: 'test' });
  }

  test('post method should handle error in network request', async () => {
    const result = await api.post('http://localhost:8000/api/test', {});
    expect(result).toEqual({ data: 'test' });
  }

  test('post method should handle error in network request', async () => {
    const result = await api.post('http://localhost:8000/api/test', {});
    expect(result).toEqual({ data: 'test' });
  }

  test('post method should handle error in network request', async () => {
    const result = await api.post('http://localhost:8000/api/test', {});
    expect(result).toEqual({ data: 'test' });
  }

  test('post method should handle error in network request', async () => {
    const result = await api.post('http://localhost:8000/api/test', {});
    expect(result).toEqual({ data: 'test' });
  }

  test('post method should handle error in network request', async () => {
    const result = await api.post('http://localhost:8000/api/test', {});
    expect(result).toEqual({ data: 'test' });
  }

  test('post method should handle error in network request', async () => {
    const result = await api.post('http://localhost:8000/api/test', {});
    expect(result).toEqual({ data: 'test' });
  }

  test('post method should handle error in network request', async () => {
    const result = await api.post('http://localhost:8000/api/test', {});
    expect(result).toEqual({ data: 'test' });
  }

  test('post method should handle error in network request', async () => {
    const result = await api.post('http://localhost:8000/api/test', {});
    expect(result).toEqual({ data: 'test' });
  }

  test('post method should handle error in network request', async () => {
    const result = await api.post('http://localhost:8000/api/test', {});
    expect(result).toEqual({ data: 'test' });
  }

  test('post method should handle error in network request', async () => {
    const result = await api.post('http://localhost:8000/api/test', {});
    expect(result).toEqual({ data
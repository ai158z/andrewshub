import { fetchWithCache, isOnline } from '../src/utils';
import { openDB } from 'idb-keyval';

jest.mock('idb-keyval', () => ({
  openDB: jest.fn()
}));

global.fetch = jest.fn();
global.navigator.onLine = true;

const mockDB = {
  transaction: jest.fn().mockReturnThis(),
  objectStore: jest.fn().mockReturnThis(),
  put: jest.fn().mockResolvedValue(undefined),
  get: jest.fn().mockResolvedValue(undefined),
  done: Promise.resolve()
};

describe('isOnline', () => {
  it('should return true when navigator.onLine is true', () => {
    global.navigator.onLine = true;
    expect(isOnline()).toBe(true);
  });

  it('should return false when navigator.onLine is false', () => {
    global.navigator.onLine = false;
    expect(isOnline()).toBe(false);
  });
});

describe('fetchWithCache', () => {
  const url = 'https://api.example.com/data';
  const mockData = { test: 'data' };
  const mockResponse = { ok: true, json: jest.fn().mockResolvedValue(mockData) };

  beforeEach(() => {
    jest.clearAllMocks();
    openDB.mockResolvedValue(mockDB);
    global.fetch.mockResolvedValue(mockResponse);
    mockDB.get.mockResolvedValue({ data: mockData, timestamp: Date.now() });
  });

  it('should fetch data from network when cache is empty', async () => {
    mockDB.get.mockResolvedValueOnce(null);
    const data = await fetchWithCache(url);
    expect(data).toEqual(mockData);
    expect(global.fetch).toHaveBeenCalledWith(url, {});
  });

  it('should return cached data when not expired', async () => {
    const recentTimestamp = Date.now() - 60000; // 1 minute ago
    mockDB.get.mockResolvedValueOnce({ data: mockData, timestamp: recentTimestamp });
    const data = await fetchWithCache(url);
    expect(data).toEqual(mockData);
    expect(global.fetch).not.toHaveBeenCalled();
  });

  it('should fetch fresh data when cache is expired', async () => {
    const expiredTimestamp = Date.now() - 31 * 60000; // 31 minutes ago
    mockDB.get.mockResolvedValueOnce({ data: mockData, timestamp: expiredTimestamp });
    const data = await fetchWithCache(url);
    expect(data).toEqual(mockData);
    expect(global.fetch).toHaveBeenCalledWith(url, {});
  });

  it('should return fresh data and update cache', async () => {
    mockDB.get.mockResolvedValueOnce(null);
    const data = await fetchWithCache(url);
    expect(data).toEqual(mockData);
    expect(mockDB.put).toHaveBeenCalledWith({ data: mockData, timestamp: expect.any(Number) }, url);
  });

  it('should return cached data when offline and no fresh data', async () => {
    global.navigator.onLine = false;
    const recentTimestamp = Date.now() - 60000; // 1 minute ago
    mockDB.get.mockResolvedValueOnce({ data: mockData, timestamp: recentTimestamp });
    const data = await fetchWithCache(url);
    expect(data).toEqual(mockData);
  });

  it('should throw error when offline and no cache', async () => {
    global.navigator.onLine = false;
    mockDB.get.mockResolvedValueOnce(null);
    await expect(fetchWithCache(url)).rejects.toThrow();
  });

  it('should throw error when network fails and no cache', async () => {
    global.fetch.mockRejectedValue(new Error('Network error'));
    mockDB.get.mockResolvedValueOnce(null);
    await expect(fetchWithCache(url)).rejects.toThrow('Network error');
  });

  it('should throw error when response is not ok', async () => {
    const errorResponse = { ok: false, status: 500 };
    global.fetch.mockResolvedValue(errorResponse);
    mockDB.get.mockResolvedValueOnce(null);
    await expect(fetchWithCache(url)).rejects.toThrow('HTTP error! status: 500');
  });

  it('should use cached data when network fails but cache exists', async () => {
    global.fetch.mockRejectedValue(new Error('Network error'));
    const recentTimestamp = Date.now() - 60000;
    mockDB.get.mockResolvedValueOnce({ data: mockData, timestamp: recentTimestamp });
    const data = await fetchWithCache(url);
    expect(data).toEqual(mockData);
  });

  it('should return stale cached data when offline', async () => {
    global.navigator.onLine = false;
    const oldTimestamp = Date.now() - 31 * 60000; // 31 minutes ago (stale)
    mockDB.get.mockResolvedValueOnce({ data: mockData, timestamp: oldTimestamp });
    const data = await fetchWithCache(url);
    expect(data).toEqual(mockData);
  });

  it('should throw error when network fails and we are online with no cache', async () => {
    global.fetch.mockRejectedValue(new Error('Network error'));
    global.navigator.onLine = true;
    mockDB.get.mockResolvedValueOnce(null);
    await expect(fetchWithCache(url)).rejects.toThrow('Network error');
  });
});
import { createFastAPIMiddleware } from '../src/middleware/fastapi.middleware';
import { rateLimiter } from '../src/rate-limiter';
import { generateKey } from '../src/utils';

jest.mock('../src/rate-limiter', () => ({
  rateLimiter: jest.fn()
}));

jest.mock('../src/utils', () => ({
  generateKey: jest.fn()
}));

describe('FastAPI Middleware', () => {
  const mockConfig = {
    limit: 10,
    windowMs: 60000,
    keyGenerator: undefined
  };

  const mockApp = {
    use: jest.fn()
  };

  const mockNext = jest.fn();
  const mockRes = {
    status: jest.fn().mockReturnThis(),
    send: jest.fn()
  };

  beforeEach(() => {
    jest.clearAllMocks();
    (generateKey as jest.Mock).mockImplementation((prefix, key) => `${prefix}:${key}`);
  });

  it('should register middleware with the app', () => {
    const middleware = createFastAPIMiddleware(mockConfig);
    middleware(mockApp);
    
    expect(mockApp.use).toHaveBeenCalledTimes(1);
    expect(typeof mockApp.use.mock.calls[0][0]).toBe('function');
  });

  it('should call rateLimiter with generated key', async () => {
    (rateLimiter as jest.Mock).mockResolvedValue(true);
    
    const middleware = createFastAPIMiddleware(mockConfig);
    middleware(mockApp);
    
    const middlewareFn = mockApp.use.mock.calls[0][0];
    const req = { ip: '127.0.0.1' };
    
    await middlewareFn(req, mockRes, mockNext);
    
    expect(generateKey).toHaveBeenCalledWith('rate_limit', '127.0.0.1');
    expect(rateLimiter).toHaveBeenCalledWith('rate_limit:127.0.0.1', 10, 60000);
  });

  it('should use IP address as key when no user ID and no keyGenerator', async () => {
    (rateLimiter as jest.Mock).mockResolvedValue(true);
    
    const middleware = createFastAPIMiddleware(mockConfig);
    middleware(mockApp);
    
    const middlewareFn = mockApp.use.mock.calls[0][0];
    const req = { ip: '192.168.1.1' };
    
    await middlewareFn(req, mockRes, mockNext);
    
    expect(generateKey).toHaveBeenCalledWith('rate_limit', '192.168.1.1');
  });

  it('should use user ID as key when available and no IP', async () => {
    (rateLimiter as jest.Mock).mockResolvedValue(true);
    
    const middleware = createFastAPIMiddleware(mockConfig);
    middleware(mockApp);
    
    const middlewareFn = mockApp.use.mock.calls[0][0];
    const req = { user: { id: 'user123' } };
    
    await middlewareFn(req, mockRes, mockNext);
    
    expect(generateKey).toHaveBeenCalledWith('rate_limit', 'user123');
  });

  it('should use custom keyGenerator when provided', async () => {
    const customConfig = {
      ...mockConfig,
      keyGenerator: (req: any) => req.headers['x-api-key'] || 'default'
    };
    
    (rateLimiter as jest.Mock).mockResolvedValue(true);
    
    const middleware = createFastAPIMiddleware(customConfig);
    middleware(mockApp);
    
    const middlewareFn = mockApp.use.mock.calls[0][0];
    const req = { headers: { 'x-api-key': 'api-key-123' } };
    
    await middlewareFn(req, mockRes, mockNext);
    
    expect(generateKey).toHaveBeenCalledWith('rate_limit', 'api-key-123');
  });

  it('should call next when not rate limited', async () => {
    (rateLimiter as jest.Mock).mockResolvedValue(true);
    
    const middleware = createFastAPIMiddleware(mockConfig);
    middleware(mockApp);
    
    const middlewareFn = mockApp.use.mock.calls[0][0];
    const req = { ip: '127.0.0.1' };
    
    await middlewareFn(req, mockRes, mockNext);
    
    expect(mockNext).toHaveBeenCalled();
    expect(mockRes.status).not.toHaveBeenCalled();
  });

  it('should return 429 when rate limited', async () => {
    (rateLimiter as jest.Mock).mockResolvedValue(false);
    
    const middleware = createFastAPIMiddleware(mockConfig);
    middleware(mockApp);
    
    const middlewareFn = mockApp.use.mock.calls[0][0];
    const req = { ip: '127.0.0.1' };
    
    await middlewareFn(req, mockRes, mockNext);
    
    expect(mockRes.status).toHaveBeenCalledWith(429);
    expect(mockRes.send).toHaveBeenCalledWith('Too Many Requests');
    expect(mockNext).not.toHaveBeenCalled();
  });

  it('should use default key when no IP or user ID available', async () => {
    (rateLimiter as jest.Mock).mockResolvedValue(true);
    
    const middleware = createFastAPIMiddleware(mockConfig);
    middleware(mockApp);
    
    const middlewareFn = mockApp.use.mock.calls[0][0];
    const req = { headers: {} };
    
    await middlewareFn(req, mockRes, mockNext);
    
    expect(generateKey).toHaveBeenCalledWith('rate_limit', 'unknown');
  });

  it('should pass rate limiter config values correctly', async () => {
    const config = {
      limit: 100,
      windowMs: 300000
    };
    
    (rateLimiter as jest.Mock).mockResolvedValue(true);
    
    const middleware = createFastAPIMiddleware(config);
    middleware(mockApp);
    
    const middlewareFn = mockApp.use.mock.calls[0][0];
    const req = { ip: '127.0.0.1' };
    
    await middlewareFn(req, mockRes, mockNext);
    
    expect(rateLimiter).toHaveBeenCalledWith('rate_limit:127.0.0.1', 100, 300000);
  });
});
import { Request, Response, NextFunction } from 'express';
import { createExpressMiddleware } from '../src/middleware/express.middleware';
import { rateLimiter } from '../src/rate-limiter';
import { generateKey } from '../src/utils';

jest.mock('../src/rate-limiter');
jest.mock('../src/utils');

const mockRateLimiter = rateLimiter as jest.MockedFunction<typeof rateLimiter>;
const mockGenerateKey = generateKey as jest.MockedFunction<typeof generateKey>;

describe('createExpressMiddleware', () => {
  const config = {
    windowMs: 60000,
    limit: 5,
    keyGenerator: undefined
  };

  const mockRequest = {
    ip: '127.0.0.1',
    socket: { remoteAddress: '127.0.0.1' }
  } as Request;

  const mockResponse = {
    status: jest.fn().mockReturnThis(),
    json: jest.fn()
  } as unknown as Response;

  const mockNext = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('should call next() when rate limit is not exceeded', async () => {
    mockRateLimiter.mockResolvedValue(true);
    mockGenerateKey.mockReturnValue('key');

    const middleware = createExpressMiddleware(config);
    await middleware(mockRequest, mockResponse, mockNext);

    expect(mockGenerateKey).toHaveBeenCalledWith('ip', '127.0.0.1');
    expect(mockRateLimiter).toHaveBeenCalledWith('key', 5, 60000);
    expect(mockNext).toHaveBeenCalled();
    expect(mockResponse.status).not.toHaveBeenCalled();
  });

  it('should use custom keyGenerator when provided', async () => {
    const customConfig = {
      ...config,
      keyGenerator: jest.fn().mockReturnValue('custom-key')
    };

    mockRateLimiter.mockResolvedValue(true);

    const middleware = createExpressMiddleware(customConfig);
    await middleware(mockRequest, mockResponse, mockNext);

    expect(customConfig.keyGenerator).toHaveBeenCalledWith(mockRequest);
    expect(mockRateLimiter).toHaveBeenCalledWith('custom-key', 5, 60000);
    expect(mockNext).toHaveBeenCalled();
  });

  it('should return 429 when rate limit is exceeded', async () => {
    mockRateLimiter.mockResolvedValue(false);
    mockGenerateKey.mockReturnValue('key');

    const middleware = createExpressMiddleware(config);
    await middleware(mockRequest, mockResponse, mockNext);

    expect(mockResponse.status).toHaveBeenCalledWith(429);
    expect(mockResponse.json).toHaveBeenCalledWith({
      error: 'Too Many Requests',
      message: 'Rate limit exceeded'
    });
    expect(mockNext).not.toHaveBeenCalled();
  });

  it('should return 500 when rate limiter throws an error', async () => {
    mockRateLimiter.mockRejectedValue(new Error('Rate limiter error'));
    mockGenerateKey.mockReturnValue('key');

    const middleware = createExpressMiddleware(config);
    await middleware(mockRequest, mockResponse, mockNext);

    expect(mockResponse.status).toHaveBeenCalledWith(500);
    expect(mockResponse.json).toHaveBeenCalledWith({
      error: 'Internal Server Error',
      message: 'Rate limiting service error'
    });
    expect(mockNext).not.toHaveBeenCalled();
  });

  it('should use socket.remoteAddress when req.ip is not available', async () => {
    const requestWithoutIp = {
      socket: { remoteAddress: '192.168.1.1' }
    } as Request;

    mockRateLimiter.mockResolvedValue(true);
    mockGenerateKey.mockImplementation((_, ip) => `key-${ip}`);

    const middleware = createExpressMiddleware(config);
    await middleware(requestWithoutIp, mockResponse, mockNext);

    expect(mockGenerateKey).toHaveBeenCalledWith('ip', '192.168.1.1');
    expect(mockNext).toHaveBeenCalled();
  });

  it('should handle empty IP gracefully', async () => {
    const requestWithoutIp = {} as Request;

    mockRateLimiter.mockResolvedValue(true);
    mockGenerateKey.mockImplementation((_, ip) => `key-${ip}`);

    const middleware = createExpressMiddleware(config);
    await middleware(requestWithoutIp, mockResponse, mockNext);

    expect(mockGenerateKey).toHaveBeenCalledWith('ip', '');
    expect(mockNext).toHaveBeenCalled();
  });

  it('should pass limit and windowMs to rateLimiter', async () => {
    const customConfig = { ...config, limit: 10, windowMs: 120000 };
    mockRateLimiter.mockResolvedValue(true);
    mockGenerateKey.mockReturnValue('key');

    const middleware = createExpressMiddleware(customConfig);
    await middleware(mockRequest, mockResponse, mockNext);

    expect(mockRateLimiter).toHaveBeenCalledWith('key', 10, 120000);
    expect(mockNext).toHaveBeenCalled();
  });
});
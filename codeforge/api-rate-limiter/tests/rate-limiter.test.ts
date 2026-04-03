import { rateLimiter } from '../src/rate-limiter';
import Redis from 'ioredis';
import { RateLimitResult } from '../src/types';

jest.mock('ioredis');

const MockRedis = Redis as jest.MockedClass<typeof Redis>;
const mockEval = jest.fn();

beforeEach(() => {
  mockEval.mockClear();
  MockRedis.mock.instances[0].eval = mockEval;
});

describe('rateLimiter', () => {
  it('should allow request when under limit', async () => {
    mockEval.mockResolvedValue([true, 1, 5000]);
    
    const result = await rateLimiter('user:123', 5, 60000);
    
    expect(result).toEqual({
      success: true,
      count: 1,
      resetTime: 5000,
      limit: 5,
      remaining: 4
    });
  });

  it('should reject request when over limit', async () => {
    mockEval.mockResolvedValue([false, 6, 3000]);
    
    const result = await rateLimiter('user:123', 5, 60000);
    
    expect(result).toEqual({
      success: false,
      count: 6,
      resetTime: 3000,
      limit: 5,
      remaining: 0
    });
  });

  it('should handle Redis ZCOUNT returning zero', async () => {
    mockEval.mockResolvedValue([true, 0, 60000]);
    
    const result = await rateLimiter('user:123', 10, 60000);
    
    expect(result.success).toBe(true);
    expect(result.count).toBe(0);
    expect(result.remaining).toBe(10);
  });

  it('should handle Redis PTTL returning negative value', async () => {
    mockEval.mockResolvedValue([true, 1, -1]);
    
    const result = await rateLimiter('user:123', 5, 60000);
    
    expect(result.resetTime).toBe(60000);
  });

  it('should pass correct parameters to Redis script', async () => {
    mockEval.mockResolvedValue([true, 1, 5000]);
    
    const key = 'api:test';
    const limit = 10;
    const windowMs = 30000;
    const now = Date.now();
    const windowStart = now - windowMs;
    
    await rateLimiter(key, limit, windowMs);
    
    expect(mockEval).toHaveBeenCalledWith(
      expect.any(String),
      1,
      key,
      windowStart,
      now,
      limit
    );
  });

  it('should throw error when Redis throws error', async () => {
    mockEval.mockRejectedValue(new Error('Redis connection failed'));
    
    await expect(rateLimiter('user:123', 5, 60000))
      .rejects
      .toThrow('Rate limiter error: Redis connection failed');
  });

  it('should handle non-Error thrown by Redis', async () => {
    mockEval.mockRejectedValue('Unknown Redis error');
    
    await expect(rateLimiter('user:123', 5, 60000))
      .rejects
      .toThrow('Rate limiter error: Unknown error');
  });

  it('should handle empty key', async () => {
    mockEval.mockResolvedValue([true, 1, 5000]);
    
    const result = await rateLimiter('', 5, 60000);
    
    expect(result.success).toBe(true);
  });

  it('should handle zero limit', async () => {
    mockEval.mockResolvedValue([false, 1, 0]);
    
    const result = await rateLimiter('user:123', 0, 60000);
    
    expect(result.success).toBe(false);
    expect(result.remaining).toBe(0);
  });

  it('should handle zero windowMs', async () => {
    mockEval.mockResolvedValue([true, 1, 0]);
    
    const result = await rateLimiter('user:123', 5, 0);
    
    expect(result.resetTime).toBe(0);
  });

  it('should handle large limit values', async () => {
    mockEval.mockResolvedValue([true, 999999, 3000]);
    
    const result = await rateLimiter('user:123', 1000000, 60000);
    
    expect(result.count).toBe(999999);
    expect(result.remaining).toBe(1);
  });

  it('should handle negative count from Redis', async () => {
    mockEval.mockResolvedValue([true, -5, 3000]);
    
    const result = await rateLimiter('user:123', 5, 60000);
    
    expect(result.count).toBe(-5);
    expect(result.remaining).toBe(10); // Math.max(0, 5 - (-5)) = 10
  });

  it('should handle limit equal to count', async () => {
    mockEval.mockResolvedValue([true, 5, 1000]);
    
    const result = await rateLimiter('user:123', 5, 60000);
    
    expect(result.success).toBe(true);
    expect(result.remaining).toBe(0);
  });

  it('should handle count exceeding limit', async () => {
    mockEval.mockResolvedValue([false, 10, 2000]);
    
    const result = await rateLimiter('user:123', 5, 60000);
    
    expect(result.success).toBe(false);
    expect(result.remaining).toBe(0);
  });

  it('should handle concurrent calls with same key', async () => {
    const results: RateLimitResult[] = [];
    mockEval.mockResolvedValue([true, 1, 5000]);
    
    // Simulate concurrent requests
    await Promise.all([
      rateLimiter('user:123', 5, 60000).then(r => results.push(r)),
      rateLimiter('user:123', 5, 60000).then(r => results.push(r))
    ]);
    
    expect(results).toHaveLength(2);
  });
});
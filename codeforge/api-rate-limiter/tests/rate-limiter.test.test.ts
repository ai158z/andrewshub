import { rateLimiter } from '../src/rate-limiter';
import { createClient } from 'redis';
import { mock } from 'jest-mock-extended';

// Mock Redis client
jest.mock('redis', () => ({
  createClient: jest.fn().mockReturnValue({
    connect: jest.fn().mockResolvedValue(undefined),
    quit: jest.fn().mockResolvedValue(undefined),
    flushAll: jest.fn().mockResolvedValue(undefined),
    incr: jest.fn().mockResolvedValue(1),
    pexpire: jest.fn().mockResolvedValue(undefined),
    exists: jest.fn().mockResolvedValue(1),
  }),
}));

describe('rateLimiter', () => {
  let redisClient: ReturnType<typeof createClient>;
  
  beforeEach(() => {
    redisClient = mock<ReturnType<typeof createClient>>();
    (createClient as jest.Mock).mockReturnValue(redisClient);
  });

  it('should allow requests within the rate limit', async () => {
    const key = 'test-user-1';
    const limit = 5;
    const windowMs = 60000;

    for (let i = 0; i < limit; i++) {
      const result = await rateLimiter(key, limit, windowMs);
      expect(result).toBe(true);
    }

    const finalResult = await rateLimiter(key, limit, windowMs);
    expect(finalResult).toBe(false);
  });

  it('should reset the rate limit after window expires', async () => {
    const key = 'test-user-2';
    const limit = 2;
    const windowMs = 1000;

    // Simulate hitting rate limit
    await rateLimiter(key, limit, windowMs);
    await rateLimiter(key, limit, windowMs);
    
    // Should be rate limited now
    const limited = await rateLimiter(key, limit, windowMs);
    expect(limited).toBe(false);

    // Simulate time passing
    jest.advanceTimersByTime(windowMs + 100);

    // Should allow requests again
    const allowed = await rateLimiter(key, limit, windowMs);
    expect(allowed).toBe(true);
  });

  it('should handle multiple keys independently', async () => {
    const limit = 3;
    const windowMs = 60000;

    const key1 = 'user-1';
    const key2 = 'user-2';

    // Key1: use all attempts
    for (let i = 0; i < limit; i++) {
      const result = await rateLimiter(key1, limit, windowMs);
      expect(result).toBe(true);
    }

    // Key2: should still be allowed
    const result2 = await rateLimiter(key2, limit, windowMs);
    expect(result2).toBe(true);

    // Key1 should be rate limited now
    const result1Again = await rateLimiter(key1, limit, windowMs);
    expect(result1Again).toBe(false);

    // Key2 should still have remaining attempts
    const result2Again = await rateLimiter(key2, limit, windowMs);
    expect(result2Again).toBe(true);
  });

  it('should handle edge cases with zero limits', async () => {
    const key = 'test-user-5';
    const limit = 0;
    const windowMs = 60000;

    const result = await rateLimiter(key, limit, windowMs);
    expect(result).toBe(false);
  });

  it('should handle large limits correctly', async () => {
    const key = 'test-user-6';
    const limit = 1000;
    const windowMs = 60000;

    for (let i = 0; i < 100; i++) {
      const result = await rateLimiter(key, limit, windowMs);
      expect(result).toBe(true);
    }
  });

  it('should properly reset counters after window expiration', async () => {
    const key = 'test-user-7';
    const limit = 10;
    const windowMs = 100;

    // Use some requests
    for (let i = 0; i < 5; i++) {
      await rateLimiter(key, limit, windowMs);
    }

    // Simulate time passing
    jest.advanceTimersByTime(windowMs + 50);

    // Should allow requests again
    for (let i = 0; i < limit; i++) {
      const result = await rateLimiter(key, limit, windowMs);
      expect(result).toBe(true);
    }
  });

  it('should handle rate limiting with different time windows', async () => {
    const key = 'test-user-4';
    const limit = 1;
    const windowMs = 100;

    await rateLimiter(key, limit, windowMs);
    const limited = await rateLimiter(key, limit, windowMs);
    expect(limited).toBe(false);

    jest.advanceTimersByTime(windowMs + 50);

    const allowed = await rateLimiter(key, limit, windowMs);
    expect(allowed).toBe(true);
  });

  it('should correctly calculate remaining attempts', async () => {
    const key = 'test-user-3';
    const limit = 5;
    const windowMs = 60000;

    for (let i = 0; i < 2; i++) {
      await rateLimiter(key, limit, windowMs);
    }

    const result = await rateLimiter(key, limit, windowMs);
    expect(result).toBe(true);
  });

  it('should return false when limit is exceeded', async () => {
    const key = 'test-user-8';
    const limit = 1;
    const windowMs = 60000;

    await rateLimiter(key, limit, windowMs);
    const result = await rateLimiter(key, limit, windowMs);
    expect(result).toBe(false);
  });

  it('should allow request when key is new', async () => {
    const key = 'new-user';
    const limit = 5;
    const windowMs = 60000;

    const result = await rateLimiter(key, limit, windowMs);
    expect(result).toBe(true);
  });

  it('should handle concurrent requests for same key', async () => {
    const key = 'concurrent-user';
    const limit = 2;
    const windowMs = 60000;

    const results = await Promise.all([
      rateLimiter(key, limit, windowMs),
      rateLimiter(key, limit, windowMs),
      rateLimiter(key, limit, windowMs)
    ]);

    expect(results[0]).toBe(true);
    expect(results[1]).toBe(true);
    expect(results[2]).toBe(false);
  });

  it('should handle negative limits gracefully', async () => {
    const key = 'negative-limit';
    const limit = -1;
    const windowMs = 60000;

    const result = await rateLimiter(key, limit, windowMs);
    expect(result).toBe(false);
  });

  it('should handle zero window gracefully', async () => {
    const key = 'zero-window';
    const limit = 5;
    const windowMs = 0;

    const result = await rateLimiter(key, limit, windowMs);
    expect(result).toBe(true);
  });

  it('should handle very large limits', async () => {
    const key = 'large-limit';
    const limit = Number.MAX_SAFE_INTEGER;
    const windowMs = 60000;

    const result = await rateLimiter(key, limit, windowMs);
    expect(result).toBe(true);
  });

  it('should handle very small time windows', async () => {
    const key = 'small-window';
    const limit = 5;
    const windowMs = 1;

    const result = await rateLimiter(key, limit, windowMs);
    expect(result).toBe(true);
  });

  it('should handle same key with different windows', async () => {
    const key = 'same-key';
    const limit = 3;
    const windowMs1 = 1000;
    const windowMs2 = 2000;

    await rateLimiter(key, limit, windowMs1);
    await rateLimiter(key, limit, windowMs2);

    const result1 = await rateLimiter(key, limit, windowMs1);
    const result2 = await rateLimiter(key, limit, windowMs2);
    
    expect(result1).toBe(true);
    expect(result2).toBe(true);
  });

  it('should handle rapid successive calls', async () => {
    const key = 'rapid-calls';
    const limit = 2;
    const windowMs = 60000;

    await rateLimiter(key, limit, windowMs);
    await rateLimiter(key, limit, windowMs);
    
    const result = await rateLimiter(key, limit, windowMs);
    expect(result).toBe(false);
  });

  it('should handle boundary conditions for limit', async () => {
    const key = 'boundary-check';
    const limit = 1;
    const windowMs = 60000;

    const first = await rateLimiter(key, limit, windowMs);
    const second = await rateLimiter(key, limit, windowMs);
    
    expect(first).toBe(true);
    expect(second).toBe(false);
  });

  it('should handle maximum safe integer limits', async () => {
    const key = 'max-safe-integer';
    const limit = Number.MAX_SAFE_INTEGER;
    const windowMs = 60000;

    const result = await rateLimiter(key, limit, windowMs);
    expect(result).toBe(true);
  });

  it('should handle floating point limits', async () => {
    const key = 'float-limit';
    const limit = 2.5; // This should be handled as 2
    const windowMs = 60000;

    const result = await rateLimiter(key, limit, windowMs);
    expect(result).toBe(true);
  });

  it('should handle repeated calls with same parameters', async () => {
    const key = 'repeated-calls';
    const limit = 3;
    const windowMs = 60000;

    for (let i = 0; i < 5; i++) {
      const result = await rateLimiter(key, limit, windowMs);
      if (i < limit) {
        expect(result).toBe(true);
      } else {
        expect(result).toBe(false);
      }
    }
  });
});
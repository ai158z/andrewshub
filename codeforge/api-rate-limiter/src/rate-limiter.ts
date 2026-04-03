import Redis from 'ioredis';
import { RateLimitResult } from './types';

const redis = new Redis(process.env.REDIS_URL || 'redis://localhost:6379');

export async function rateLimiter(
  key: string,
  limit: number,
  windowMs: number
): Promise<RateLimitResult> {
  try {
    const now = Date.now();
    const windowStart = now - windowMs;
    
    const luaScript = `
      local key = KEYS[1]
      local windowStart = ARGV[1]
      local windowEnd = ARGV[2]
      local limit = tonumber(ARGV[3])
      
      redis.call('ZREMRANGEBYSCORE', key, 0, windowStart)
      local currentCount = redis.call('ZCOUNT', key, windowStart, windowEnd)
      
      if currentCount >= limit then
        local ttl = redis.call('PTTL', key)
        return {false, currentCount, ttl > 0 and ttl or 0}
      end
      
      redis.call('ZADD', key, windowEnd, windowEnd)
      redis.call('EXPIRE', key, math.ceil(windowEnd / 1000))
      
      local newCount = redis.call('ZCOUNT', key, windowStart, windowEnd)
      local ttl = redis.call('PTTL', key)
      return {true, newCount, ttl > 0 and ttl or 0}
    `;
    
    const result: [boolean, number, number] = await redis.eval(
      luaScript,
      1,
      key,
      windowStart.toString(),
      now.toString(),
      limit.toString()
    ) as [boolean, number, number];
    
    const [success, count, resetTime] = result;
    
    return {
      success,
      count,
      resetTime: resetTime || windowMs,
      limit,
      remaining: Math.max(0, limit - count)
    };
  } catch (error) {
    throw new Error(`Rate limiter error: ${error instanceof Error ? error.message : 'Unknown error'}`);
  }
}
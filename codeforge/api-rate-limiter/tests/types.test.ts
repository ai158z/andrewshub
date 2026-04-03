import { RateLimitConfig, RateLimitResult, KeyGeneratorFunction } from './types';

describe('RateLimitConfig', () => {
  it('should accept required windowMs and limit properties', () => {
    const config: RateLimitConfig = {
      windowMs: 60000,
      limit: 100
    };
    expect(config.windowMs).toBe(60000);
    expect(config.limit).toBe(100);
  });

  it('should accept optional keyGenerator function', () => {
    const keyGen: KeyGeneratorFunction = (req: any) => req.ip;
    const config: RateLimitConfig = {
      windowMs: 60000,
      limit: 100,
      keyGenerator: keyGen
    };
    expect(typeof config.keyGenerator).toBe('function');
  });

  it('should accept optional skip function', () => {
    const config: RateLimitConfig = {
      windowMs: 60000,
      limit: 100,
      skip: (req, res) => false
    };
    expect(typeof config.skip).toBe('function');
  });

  it('should accept optional onLimitReached function', () => {
    const config: RateLimitConfig = {
      windowMs: 60000,
      limit: 100,
      onLimitReached: (req, res, next) => {}
    };
    expect(typeof config.onLimitReached).toBe('function');
  });

  it('should accept optional handler function', () => {
    const config: RateLimitConfig = {
      windowMs: 60000,
      limit: 100,
      handler: (req, res, next) => {}
    };
    expect(typeof config.handler).toBe('function');
  });

  it('should accept skipFailedRequests boolean', () => {
    const config: RateLimitConfig = {
      windowMs: 60000,
      limit: 100,
      skipFailedRequests: true
    };
    expect(config.skipFailedRequests).toBe(true);
  });

  it('should accept skipSuccessfulRequests boolean', () => {
    const config: RateLimitConfig = {
      windowMs: 60000,
      limit: 100,
      skipSuccessfulRequests: true
    };
    expect(config.skipSuccessfulRequests).toBe(true);
  });

  it('should accept requestPropertyName string', () => {
    const config: RateLimitConfig = {
      windowMs: 60000,
      limit: 100,
      requestPropertyName: 'rateLimit'
    };
    expect(config.requestPropertyName).toBe('rateLimit');
  });
});

describe('RateLimitResult', () => {
  it('should have all required properties with correct types', () => {
    const result: RateLimitResult = {
      allowed: true,
      limit: 100,
      remaining: 50,
      resetTime: Date.now() + 60000,
      windowMs: 60000
    };
    
    expect(result.allowed).toBe(true);
    expect(typeof result.limit).toBe('number');
    expect(typeof result.remaining).toBe('number');
    expect(typeof result.resetTime).toBe('number');
    expect(typeof result.windowMs).toBe('number');
  });

  it('should allow allowed property to be false', () => {
    const result: RateLimitResult = {
      allowed: false,
      limit: 100,
      remaining: 0,
      resetTime: Date.now() + 60000,
      windowMs: 60000
    };
    expect(result.allowed).toBe(false);
  });
});

describe('KeyGeneratorFunction', () => {
  it('should be a function type that accepts req and returns string', () => {
    const keyGen: KeyGeneratorFunction = (req: any) => {
      return req.headers['x-forwarded-for'] || req.connection.remoteAddress;
    };
    
    const mockReq = {
      headers: { 'x-forwarded-for': '192.168.1.1' },
      connection: { remoteAddress: '127.0.0.1' }
    };
    
    const result = keyGen(mockReq);
    expect(typeof result).toBe('string');
  });
});
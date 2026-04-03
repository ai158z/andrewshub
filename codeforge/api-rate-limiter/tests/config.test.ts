import { validateConfig, RateLimitConfig } from './config';

describe('validateConfig', () => {
  const validConfig: RateLimitConfig = {
    windowMs: 60000,
    limit: 100,
    keyGenerator: jest.fn()
  };

  it('should validate a correct config object', () => {
    expect(() => validateConfig(validConfig)).not.toThrow();
  });

  it('should return the same config object when valid', () => {
    const result = validateConfig(validConfig);
    expect(result).toEqual(validConfig);
  });

  it('should throw error when config is null', () => {
    expect(() => validateConfig(null as any)).toThrow('RateLimitConfig must be an object');
  });

  it('should throw error when config is not an object', () => {
    expect(() => validateConfig('' as any)).toThrow('RateLimitConfig must be an object');
  });

  it('should throw error when windowMs is not a number', () => {
    const invalidConfig = { ...validConfig, windowMs: 'invalid' as any };
    expect(() => validateConfig(invalidConfig)).toThrow('windowMs must be a positive number');
  });

  it('should throw error when windowMs is zero', () => {
    const invalidConfig = { ...validConfig, windowMs: 0 };
    expect(() => validateConfig(invalidConfig)).toThrow('windowMs must be a positive number');
  });

  it('should throw error when windowMs is negative', () => {
    const invalidConfig = { ...validConfig, windowMs: -1 };
    expect(() => validateConfig(invalidConfig)).toThrow('windowMs must be a positive number');
  });

  it('should throw error when limit is not a number', () => {
    const invalidConfig = { ...validConfig, limit: 'invalid' as any };
    expect(() => validateConfig(invalidConfig)).toThrow('limit must be a positive number');
  });

  it('should throw error when limit is zero', () => {
    const invalidConfig = { ...validConfig, limit: 0 };
    expect(() => validateConfig(invalidConfig)).toThrow('limit must be a positive number');
  });

  it('should throw error when limit is negative', () => {
    const invalidConfig = { ...validConfig, limit: -1 };
    expect(() => validateConfig(invalidConfig)).toThrow('limit must be a positive number');
  });

  it('should throw error when keyGenerator is not a function', () => {
    const invalidConfig = { ...validConfig, keyGenerator: 'invalid' as any };
    expect(() => validateConfig(invalidConfig)).toThrow('keyGenerator must be a function or undefined');
  });

  it('should not throw when keyGenerator is undefined', () => {
    const configWithoutKeyGenerator = { windowMs: 60000, limit: 100 };
    expect(() => validateConfig(configWithoutKeyGenerator as RateLimitConfig)).not.toThrow();
  });

  it('should not throw when keyGenerator is a valid function', () => {
    const config = { windowMs: 60000, limit: 100, keyGenerator: jest.fn() };
    expect(() => validateConfig(config)).not.toThrow();
  });

  it('should throw error when keyGenerator is null', () => {
    const invalidConfig = { windowMs: 60000, limit: 100, keyGenerator: null };
    expect(() => validateConfig(invalidConfig as any)).toThrow();
  });

  it('should accept config with valid windowMs and limit', () => {
    const config = { windowMs: 1000, limit: 10 };
    expect(() => validateConfig(config)).not.toThrow();
  });

  it('should accept config with floating point values', () => {
    const config = { windowMs: 1.5, limit: 10.5 };
    expect(() => validateConfig(config)).not.toThrow();
  });

  it('should handle config without keyGenerator', () => {
    const config = { windowMs: 60000, limit: 100 };
    expect(validateConfig(config)).toEqual(config);
  });

  it('should handle config with keyGenerator function', () => {
    const config = { windowMs: 60000, limit: 100, keyGenerator: jest.fn() };
    expect(validateConfig(config)).toEqual(config);
  });

  it('should handle minimum positive values', () => {
    const config = { windowMs: 1, limit: 1 };
    expect(validateConfig(config)).toEqual(config);
  });

  it('should handle large positive values', () => {
    const config = { windowMs: Number.MAX_SAFE_INTEGER, limit: Number.MAX_SAFE_INTEGER };
    expect(validateConfig(config)).toEqual(config);
  });
});
import { generateKey, calculateResetTime } from './utils';

describe('generateKey', () => {
  it('should generate a valid SHA256 hex string', () => {
    const result = generateKey('prefix', 'identifier');
    expect(result).toMatch(/^[a-f0-9]{64}$/);
  });

  it('should generate consistent keys for same inputs', () => {
    const key1 = generateKey('test', 'user123');
    const key2 = generateKey('test', 'user123');
    expect(key1).toBe(key2);
  });

  it('should generate different keys for different prefixes', () => {
    const key1 = generateKey('prefix1', 'identifier');
    const key2 = generateKey('prefix2', 'identifier');
    expect(key1).not.toBe(key2);
  });

  it('should generate different keys for different identifiers', () => {
    const key1 = generateKey('prefix', 'identifier1');
    const key2 = generateKey('prefix', 'identifier2');
    expect(key1).not.toBe(key2);
  });

  it('should throw TypeError for non-string prefix', () => {
    expect(() => generateKey(123 as any, 'identifier'))
      .toThrow(TypeError);
  });

  it('should throw TypeError for non-string identifier', () => {
    expect(() => generateKey('prefix', 123 as any))
      .toThrow(TypeError);
  });

  it('should handle empty strings', () => {
    const result = generateKey('', '');
    expect(result).toHaveLength(64);
    expect(result).toMatch(/^[a-f0-9]{64}$/);
  });
});

describe('calculateResetTime', () => {
  it('should calculate future reset time', () => {
    const now = Date.now();
    const windowMs = 60000;
    const resetTime = calculateResetTime(windowMs);
    expect(resetTime).toBeGreaterThan(now);
  });

  it('should return same reset time when called twice in same window', () => {
    const windowMs = 60000;
    const reset1 = calculateResetTime(windowMs);
    const reset2 = calculateResetTime(windowMs);
    expect(reset1).toBe(reset2);
  });

  it('should throw TypeError for non-number windowMs', () => {
    expect(() => calculateResetTime('invalid' as any))
      .toThrow(TypeError);
  });

  it('should throw TypeError for zero windowMs', () => {
    expect(() => calculateResetTime(0))
      .toThrow(TypeError);
  });

  it('should throw TypeError for negative windowMs', () => {
    expect(() => calculateResetTime(-1000))
      .toThrow(TypeError);
  });

  it('should calculate correct reset time for 1 minute window', () => {
    const now = 1000000;
    jest.spyOn(global.Date, 'now').mockImplementation(() => now);
    
    const windowMs = 60000;
    const expected = 1020000; // Next minute boundary
    const result = calculateResetTime(windowMs);
    
    expect(result).toBe(expected);
  });
});
import * as crypto from 'crypto';

export function generateKey(prefix: string, identifier: string): string {
  if (typeof prefix !== 'string' || typeof identifier !== 'string') {
    throw new TypeError('Prefix and identifier must be strings');
  }

  const hash = crypto.createHash('sha256');
  hash.update(prefix + identifier);
  return hash.digest('hex');
}

export function calculateResetTime(windowMs: number): number {
  if (typeof windowMs !== 'number' || windowMs <= 0) {
    throw new TypeError('windowMs must be a positive number');
  }

  const now = Date.now();
  const resetTime = Math.ceil(now / windowMs) * windowMs;
  return resetTime;
}
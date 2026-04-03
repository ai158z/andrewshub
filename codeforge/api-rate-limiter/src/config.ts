import { Request } from 'express';

export interface RateLimitConfig {
  windowMs: number;
  limit: number;
  keyGenerator?: (req: Request) => string;
}

export interface RateLimitResult {
  success: boolean;
  limit: number;
  remaining: number;
  resetTime: number;
}

export type KeyGeneratorFunction = (req: Request) => string;

export const validateConfig = (config: RateLimitConfig): RateLimitConfig => {
  if (!config || typeof config !== 'object') {
    throw new Error('RateLimitConfig must be an object');
  }

  if (typeof config.windowMs !== 'number' || config.windowMs <= 0) {
    throw new Error('windowMs must be a positive number');
  }

  if (typeof config.limit !== 'number' || config.limit <= 0) {
    throw new Error('limit must be a positive number');
  }

  if (config.keyGenerator !== undefined && typeof config.keyGenerator !== 'function') {
    throw new Error('keyGenerator must be a function or undefined');
  }

  return config;
};
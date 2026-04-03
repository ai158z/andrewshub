import { createExpressMiddleware } from './middleware/express.middleware';
import { createFastAPIMiddleware } from './middleware/fastapi.middleware';
import { rateLimiter } from './rate-limiter';
import { RateLimitConfig } from './config';
import { RequestHandler } from 'express';

export { rateLimiter, createExpressMiddleware, createFastAPIMiddleware };

export const createExpressMiddlewareWithDefaults = (config?: RateLimitConfig): RequestHandler => {
  const defaultConfig: RateLimitConfig = {
    windowMs: 900000,
    max: 100,
    keyGenerator: (req) => req.ip.toString(),
  };
  
  const finalConfig = config ? { ...defaultConfig, ...config } : defaultConfig;
  
  return createExpressMiddleware(finalConfig);
};

export const createFastAPIMiddlewareWithDefaults = (config?: RateLimitConfig) => {
  const defaultConfig: RateLimitConfig = {
    windowMs: 900000,
    max: 100,
    keyGenerator: (req) => req.ip.toString(),
  };
  
  const finalConfig = config ? { ...defaultConfig, ...config } : defaultConfig;
  
  return createFastAPIMiddleware(finalConfig);
};

export const rateLimiterWithDefaults = (config?: RateLimitConfig) => {
  const defaultConfig: RateLimitConfig = {
    windowMs: 900000,
    max: 100,
    keyGenerator: (req) => req.ip.toString(),
  };
  
  const finalConfig = config ? { ...defaultConfig, ...config } : defaultConfig;
  
  return rateLimiter(finalConfig);
};
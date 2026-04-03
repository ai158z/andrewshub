import { Request, Response, NextFunction, RequestHandler } from 'express';
import { RateLimitConfig } from '../config';
import { rateLimiter } from '../rate-limiter';
import { generateKey } from '../utils';

export function createExpressMiddleware(config: RateLimitConfig): RequestHandler {
  const { windowMs, limit, keyGenerator } = config;

  return async (req: Request, res: Response, next: NextFunction): Promise<void> => {
    try {
      const key = keyGenerator 
        ? keyGenerator(req) 
        : generateKey('ip', req.ip || req.socket.remoteAddress || '');

      const allowed = await rateLimiter(key, limit, windowMs);
      
      if (!allowed) {
        res.status(429).json({
          error: 'Too Many Requests',
          message: 'Rate limit exceeded'
        });
        return;
      }

      next();
    } catch (error) {
      next(error);
    }
  };
}
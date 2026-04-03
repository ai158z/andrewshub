import request from 'supertest';
import express, { Request, Response } from 'express';
import { createExpressMiddleware } from '../src/middleware/express.middleware';
import { RateLimitConfig } from '../src/config';

describe('Express Middleware', () => {
  let app: express.Application;
  let config: RateLimitConfig;

  beforeEach(() => {
    app = express();
    config = {
      windowMs: 60000,
      limit: 5,
      keyGenerator: (req: Request) => `test-key-${req.ip}`
    };
  });

  it('should allow requests under the limit', async () => {
    const middleware = createExpressMiddleware(config);
    app.use(middleware);
    app.get('/test', (_req: Request, res: Response) => {
      res.status(200).send('OK');
    });

    const response = await request(app).get('/test');
    expect(response.status).toBe(200);
    expect(response.text).toBe('OK');
  });

  it('should block requests over the limit', async () => {
    const middleware = createExpressMiddleware(config);
    app.use(middleware);
    app.get('/test', (_req: Request, res: Response) => {
      res.status(200).send('OK');
    });

    // Make 5 requests to reach the limit
    for (let i = 0; i < 5; i++) {
      await request(app).get('/test');
    }

    // 6th request should be blocked
    const response = await request(app).get('/test');
    expect(response.status).toBe(429);
    expect(response.body).toHaveProperty('error');
    expect(response.body.error).toBe('Too many requests, please try again later.');
  });

  it('should include rate limit headers', async () => {
    const middleware = createExpressMiddleware(config);
    app.use(middleware);
    app.get('/test', (_req: Request, res: Response) => {
      res.status(200).send('OK');
    });

    const response = await request(app).get('/test');
    expect(response.headers).toHaveProperty('x-ratelimit-limit');
    expect(response.headers).toHaveProperty('x-ratelimit-remaining');
    expect(response.headers).toHaveProperty('x-ratelimit-reset');
  });

  it('should use custom key generator when provided', async () => {
    const customConfig: RateLimitConfig = {
      ...config,
      keyGenerator: (req: Request) => `custom-key-${req.headers['x-custom-header'] || 'default'}`
    };
    
    const middleware = createExpressMiddleware(customConfig);
    app.use(middleware);
    app.get('/test', (_req: Request, res: Response) => {
      res.status(200).send('OK');
    });

    const response = await request(app)
      .get('/test')
      .set('x-custom-header', 'test-value');
      
    expect(response.status).toBe(200);
    expect(response.text).toBe('OK');
  });

  it('should handle missing key generator gracefully', async () => {
    const configWithoutKeyGen: RateLimitConfig = {
      windowMs: 60000,
      limit: 1
    };
    
    const middleware = createExpressMiddleware(configWithoutKeyGen);
    app.use(middleware);
    app.get('/test', (_req: Request, res: Response) => {
      res.status(200).send('OK');
    });

    // First request should pass
    const response1 = await request(app).get('/test');
    expect(response1.status).toBe(200);

    // Second request should be blocked
    const response2 = await request(app).get('/test');
    expect(response2.status).toBe(429);
  });

  it('should reset rate limit after window expires', async () => {
    const shortWindowConfig: RateLimitConfig = {
      windowMs: 1000, // 1 second window
      limit: 1,
      keyGenerator: (req: Request) => `short-window-key-${req.ip}`
    };
    
    const middleware = createExpressMiddleware(shortWindowConfig);
    app.use(middleware);
    app.get('/test', (_req: Request, res: Response) => {
      res.status(200).send('OK');
    });

    // First request should pass
    const response1 = await request(app).get('/test');
    expect(response1.status).toBe(200);

    // Second request should be blocked
    const response2 = await request(app).get('/test');
    expect(response2.status).toBe(429);

    // Wait for window to reset
    await new Promise(resolve => setTimeout(resolve, 1100));

    // Request after window reset should pass
    const response3 = await request(app).get('/test');
    expect(response3.status).toBe(200);
  });

  it('should handle multiple clients independently', async () => {
    const middleware = createExpressMiddleware(config);
    app.use(middleware);
    app.get('/test', (_req: Request, res: Response) => {
      res.status(200).send('OK');
    });

    // Make requests from different "clients"
    await request(app).get('/test').set('x-forwarded-for', '1.1.1.1');
    await request(app).get('/test').set('x-forwarded-for', '2.2.2.2');

    // Both should still be under limit
    const response1 = await request(app).get('/test').set('x-forwarded-for', '1.1.1.1');
    const response2 = await request(app).get('/test').set('x-forwarded-for', '2.2.2.2');
    
    expect(response1.status).toBe(200);
    expect(response2.status).toBe(200);
  });

  it('should handle invalid windowMs gracefully', async () => {
    const invalidConfig: RateLimitConfig = {
      ...config,
      windowMs: 0
    };
    
    const middleware = createExpressMiddleware(invalidConfig);
    app.use(middleware);
    app.get('/test', (_req: Request, res: Response) => {
      res.status(200).send('OK');
    });

    const response = await request(app).get('/test');
    expect(response.status).toBe(200);
  });

  it('should handle invalid limit gracefully', async () => {
    const invalidConfig: RateLimitConfig = {
      ...config,
      limit: 0
    };
    
    const middleware = createExpressMiddleware(invalidConfig);
    app.use(middleware);
    app.get('/test', (_req: Request, res: Response) => {
      res.status(200).send('OK');
    });

    const response = await request(app).get('/test');
    expect(response.status).toBe(429);
  });

  it('should work with default key generator when none provided', async () => {
    const configWithoutKeyGen: RateLimitConfig = {
      windowMs: 60000,
      limit: 1
    };
    
    const middleware = createExpressMiddleware(configWithoutKeyGen);
    app.use(middleware);
    app.get('/test', (_req: Request, res: Response) => {
      res.status(200).send('OK');
    });

    const response = await request(app).get('/test');
    expect(response.status).toBe(200);
  });

  it('should handle negative windowMs', async () => {
    const invalidConfig: RateLimitConfig = {
      ...config,
      windowMs: -1000
    };
    
    const middleware = createExpressMiddleware(invalidConfig);
    app.use(middleware);
    app.get('/test', (_req: Request, res: Response) => {
      res.status(200).send('OK');
    });

    const response = await request(app).get('/test');
    expect(response.status).toBe(200);
  });

  it('should handle negative limit', async () => {
    const invalidConfig: RateLimitConfig = {
      ...config,
      limit: -1
    };
    
    const middleware = createExpressMiddleware(invalidConfig);
    app.use(middleware);
    app.get('/test', (_req: Request, res: Response) => {
      res.status(200).send('OK');
    });

    const response = await request(app).get('/test');
    expect(response.status).toBe(429);
  });

  it('should handle zero limit', async () => {
    const zeroLimitConfig: RateLimitConfig = {
      ...config,
      limit: 0
    };
    
    const middleware = createExpressMiddleware(zeroLimitConfig);
    app.use(middleware);
    app.get('/test', (_req: Request, res: Response) => {
      res.status(200).send('OK');
    });

    const response = await request(app).get('/test');
    expect(response.status).toBe(429);
  });

  it('should handle concurrent requests properly', async () => {
    const middleware = createExpressMiddleware(config);
    app.use(middleware);
    app.get('/test', (_req: Request, res: Response) => {
      // Simulate some processing time
      setTimeout(() => {
        res.status(200).send('OK');
      }, 10);
    });

    // Send multiple concurrent requests
    const requests = Array(3).fill(null).map(() => request(app).get('/test'));
    const responses = await Promise.all(requests);
    
    // All should be allowed since under limit
    responses.forEach(response => {
      expect(response.status).toBe(200);
    });
  });

  it('should handle very large windowMs', async () => {
    const largeWindowConfig: RateLimitConfig = {
      ...config,
      windowMs: 3600000 // 1 hour
    };
    
    const middleware = createExpressMiddleware(largeWindowConfig);
    app.use(middleware);
    app.get('/test', (_req: Request, res: Response) => {
      res.status(200).send('OK');
    });

    const response = await request(app).get('/test');
    expect(response.status).toBe(200);
  });

  it('should handle very large limit', async () => {
    const largeLimitConfig: RateLimitConfig = {
      ...config,
      limit: 1000000
    };
    
    const middleware = createExpressMiddleware(largeLimitConfig);
    app.use(middleware);
    app.get('/test', (_req: Request, res: Response) => {
      res.status(200).send('OK');
    });

    const response = await request(app).get('/test');
    expect(response.status).toBe(200);
  });

  it('should handle multiple middleware instances', async () => {
    const config1: RateLimitConfig = {
      ...config,
      limit: 2
    };
    const config2: RateLimitConfig = {
      ...config,
      limit: 1,
      keyGenerator: (req: Request) => `second-${req.ip}`
    };
    
    const middleware1 = createExpressMiddleware(config1);
    const middleware2 = createExpressMiddleware(config2);
    
    app.use(middleware1);
    app.use(middleware2);
    
    app.get('/test', (_req: Request, res: Response) => {
      res.status(200).send('OK');
    });

    // First request should pass
    const response1 = await request(app).get('/test');
    expect(response1.status).toBe(200);

    // Second request should be blocked by middleware2
    const response2 = await request(app).get('/test');
    expect(response2.status).toBe(429);
  });
});
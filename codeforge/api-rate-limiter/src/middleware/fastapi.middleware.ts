import { RateLimitConfig }

interface FastAPI {
  use: (middleware: any) => void;
}

interface Request {
  headers: Record<string, string>;
  ip?: string;
  user?: { id?: string };
}

export const createFastAPIMiddleware = (config: RateLimitConfig) => {
  return (app: FastAPI) => {
    app.use(async (req: Request, res: any, next: any) => {
      const keyGenerator = config.keyGenerator || ((req: Request) => {
        return req.ip || req.user?.id || 'unknown';
      });
      
      const key = keyGenerator(req);
      const isAllowed = await rateLimiter(
        generateKey('rate_limit', key),
        config.limit,
        config.windowMs
      );
      
      if (!isAllowed) {
        res.status(429).send('Too Many Requests');
        return;
      }
      
      next();
    });
  };
};
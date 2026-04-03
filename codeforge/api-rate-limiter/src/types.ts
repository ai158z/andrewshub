export interface RateLimitConfig {
  windowMs: number;
  limit: number;
  keyGenerator?: (req: any) => string;
  skip?: (req: any, res: any) => boolean;
  onLimitReached?: (req: any, res: any, next: any) => void;
  handler?: (req: any, res: any, next: any) => void;
  skipFailedRequests?: boolean;
  skipSuccessfulRequests?: boolean;
  requestPropertyName?: string;
}

export interface RateLimitResult {
  allowed: boolean;
  limit: number;
  remaining: number;
  resetTime: number;
  windowMs: number;
}

export type KeyGeneratorFunction = (req: any) => string;
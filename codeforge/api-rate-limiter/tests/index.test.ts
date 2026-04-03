import { createExpressMiddleware, createFastAPIMiddleware, rateLimiter } from '../src/index';
import { RequestHandler } from 'express';

jest.mock('../src/middleware/express.middleware', () => ({
  createExpressMiddleware: jest.fn(),
}));

jest.mock('../src/middleware/fastapi.middleware', () => ({
  createFastAPIMiddleware: jest.fn(),
}));

jest.mock('../src/rate-limiter', () => ({
  rateLimiter: jest.fn(),
}));

describe('Middleware Factory Functions', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('createExpressMiddleware', () => {
    it('should create express middleware function', () => {
      const mockHandler: RequestHandler = jest.fn();
      (createExpressMiddleware as jest.Mock).mockReturnValue(mockHandler);
      
      const middleware = createExpressMiddleware();
      expect(middleware).toBeInstanceOf(Function);
    });

    it('should throw error when express middleware creation fails', () => {
      (createExpressMiddleware as jest.Mock).mockImplementation(() => {
        throw new Error('Middleware creation failed');
      });

      expect(() => createExpressMiddleware()).toThrow('Middleware creation failed');
    });
  });

  describe('createFastAPIMiddleware', () => {
    it('should create FastAPI middleware', () => {
      (createFastAPIMiddleware as jest.Mock).mockImplementation(() => ({
        onExecute: jest.fn(),
        onSubscribe: jest.fn(),
      }));

      const result = createFastAPIMiddleware();
      expect(result).toEqual({
        onExecute: expect.any(Function),
        onSubscribe: expect.any(Function),
      });
    });

    it('should handle FastAPI middleware error', () => {
      (createFastAPIMiddleware as jest.Mock).mockImplementation(() => {
        throw new Error('FastAPI middleware creation failed');
      });

      expect(() => createFastAPIMiddleware()).toThrow('FastAPI middleware creation failed');
    });
  });

  describe('rateLimiter', () => {
    it('should create rate limiter', () => {
      (rateLimiter as jest.Mock).mockReturnValue({
        handleRequest: jest.fn(),
      });

      const result = rateLimiter();
      expect(result).toEqual({
        handleRequest: expect.any(Function),
      });
    });

    it('should handle rate limiter error', () => {
      (rateLimiter as jest.Mock).mockImplementation(() => {
        throw new Error('Rate limiter creation failed');
      });

      expect(() => rateLimiter()).toThrow('Rate limiter creation failed');
    });
  });
});
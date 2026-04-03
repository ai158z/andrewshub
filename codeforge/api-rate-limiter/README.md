# API Rate Limiter

A robust rate limiting library for public API endpoints with Redis integration. Enforces configurable rate limits and provides middleware for Express.js and FastAPI frameworks.

## Features

- **Configurable Rate Limits**: Set request limits per time window (e.g., 100 requests/minute/IP)
- **Multi-framework Support**: Ready-to-use middleware for Express.js and FastAPI
- **Redis Integration**: Efficient request tracking using Redis for distributed rate limiting
- **Automatic Blocking**: Returns 429 status code when rate limits are exceeded
- **Docker Support**: Containerized deployment ready
- **TypeScript Support**: Full TypeScript definitions included

## Prerequisites

- Node.js >= 14.x
- Redis server
- Docker and Docker Compose (for containerized deployment)

## Installation

```bash
npm install api-rate-limiter
```

### Development Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd api-rate-limiter
```

2. Install dependencies:
```bash
npm install
```

3. Copy and configure environment variables:
```bash
cp .env.example .env
```

4. Start Redis using Docker Compose:
```bash
docker-compose up -d redis
```

## Environment Variables

Create a `.env` file with the following variables:

```env
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
RATE_LIMIT_WINDOW=60
RATE_LIMIT_MAX=100
```

## Usage

### Express.js Integration

```typescript
import express from 'express';
import { createRateLimiter } from 'api-rate-limiter';

const app = express();
const rateLimiter = createRateLimiter({
  windowMs: 60000, // 1 minute
  max: 100, // limit each IP to 100 requests per windowMs
  message: 'Too many requests, please try again later',
  statusCode: 429
});

app.use('/api/', rateLimiter.expressMiddleware);

app.get('/api/data', (req, res) => {
  res.json({ message: 'Data retrieved successfully' });
});

app.listen(3000);
```

### FastAPI Integration

```typescript
import { createRateLimiter } from 'api-rate-limiter';

const rateLimiter = createRateLimiter({
  windowMs: 60000,
  max: 100,
  message: 'Too many requests, please try again later',
  statusCode: 429
});

// Apply to your FastAPI routes
app.use('/api/', rateLimiter.fastifyMiddleware);
```

## API Documentation

### `createRateLimiter(options)`

Creates a rate limiter instance with the specified options.

**Parameters:**
- `options`: Configuration object with the following properties:
  - `windowMs`: Time window in milliseconds (default: 60000)
  - `max`: Maximum requests per window (default: 100)
  - `message`: Response message for rate limit exceeded (default: 'Too many requests')
  - `statusCode`: HTTP status code for rate limit exceeded (default: 429)

**Returns:** Rate limiter instance with middleware methods

### Middleware Methods

- `expressMiddleware`: Express.js middleware function
- `fastifyMiddleware`: FastAPI middleware function

## Project Structure

```
api-rate-limiter/
├── src/
│   ├── index.ts              # Main entry point
│   ├── rate-limiter.ts      # Core rate limiting logic
│   ├── config.ts           # Configuration interface
│   ├── types.ts            # Type definitions
│   ├── utils.ts           # Utility functions
│   └── middleware/
│       ├── express.middleware.ts
│       └── fastapi.middleware.ts
├── tests/
│   ├── rate-limiter.test.ts
│   ├── express.middleware.test.ts
│   └── fastapi.middleware.test.ts
├── Dockerfile
├── docker-compose.yml
├── package.json
├── tsconfig.json
└── jest.config.js
```

## Testing

Run the test suite:

```bash
npm test
```

### Run tests with coverage:

```bash
npm run test:coverage
```

### Test individual components:

```bash
npm run test:unit src/rate-limiter.test.ts
npm run test:unit src/middleware/express.middleware.test.ts
npm run test:unit src/middleware/fastapi.middleware.test.ts
```

## Deployment

### Docker Deployment

1. Build the Docker image:

```bash
docker build -t api-rate-limiter .
```

2. Run with Docker Compose:

```bash
docker-compose up -d
```

### Environment Configuration

Ensure Redis is accessible and configure the following environment variables:

```env
REDIS_HOST=your-redis-host
REDIS_PORT=6379
```

## Docker Compose Setup

The project includes Docker Compose configuration for development:

```yaml
version: '3.8'
services:
  redis:
    image: redis:alpine
    ports:
      - "6379:6379"
```

To start the development environment:

```bash
docker-compose up -d
```

This will start Redis and make it available at `localhost:6379`.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a pull request

## Support

For support, please open an issue on the repository.

## Changelog

### 1.0.0
- Initial release with Express.js and FastAPI middleware support
- Redis integration for distributed rate limiting
- Docker Compose development setup
- Comprehensive test suite

## Authors

- **api-rate-limiter team**

## Keywords

- rate-limiting
- express-middleware
- redis
- api-protection
- typescript

## Development Scripts

- `npm run build` - Compile TypeScript to JavaScript
- `npm run test` - Run test suite
- `npm run test:watch` - Run tests in watch mode
- `npm run dev` - Run development server
- `npm run start` - Start production server

## Dependencies

- redis: ^4.0.0
- ioredis: ^5.0.0
- @types/redis: ^2.8.0
- @types/ioredis: ^4.0.0
- express: ^4.18.0
- jest: ^29.0.0
- typescript: ^4.9.0

---

**Note**: This is a library meant to be integrated into existing Node.js applications. It does not provide a standalone service but rather tools to implement rate limiting in your APIs.
# Staking Dashboard PWA

A Progressive Web Application (PWA) for staking dashboards with offline functionality, push notifications, and home screen installation capabilities.

## Features

- ✅ **Offline Support**: Full offline functionality with cached data and assets
- 📱 **PWA Installation**: Installable on home screen like native apps
- 🔔 **Push Notifications**: Real-time notifications support
- ⚡ **Fast Loading**: Cached static assets and API responses
- 🔄 **Background Sync**: Staking operations work offline and sync when online
- 🌐 **Network Awareness**: Automatic detection of online/offline status
- 📊 **Caching Strategies**: Intelligent cache management for optimal performance

## Prerequisites

- Node.js >= 16.x
- npm >= 8.x
- Modern browser with PWA support

## Installation & Setup

```bash
# Clone the repository
git clone <repository-url>
cd staking-dashboard-pwa

# Install dependencies
npm install

# Start development server
npm start
```

### Build for Production

```bash
# Create production build
npm run build
```

## Environment Variables

Create a `.env` file in the project root:

```env
REACT_APP_API_URL=https://api.staking-service.com
REACT_APP_PUSH_PUBLIC_KEY=your-vapid-public-key
```

## Usage Examples

### Registering the Application

```javascript
// src/index.js
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import * as serviceWorker from './serviceWorker';

// Enable service worker for PWA features
serviceWorker.register();
```

### Service Worker Registration

```javascript
// src/register-service-worker.js
const isLocalhost = Boolean(
  window.location.hostname === 'localhost' ||
  window.location.hostname === '[::1]' ||
  window.location.hostname.match(
    /^127(?:\.[0-9]+){0,2}\.[0-9]+$/
  )
);

export function register(config) {
  if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
      const swUrl = `${process.env.PUBLIC_URL}/service-worker.js`;
      
      if (isLocalhost) {
        checkValidServiceWorker(swUrl, config);
      } else {
        registerValidSW(swUrl, config);
      }
    });
  }
}
```

## Project Structure

```
staking-dashboard-pwa/
├── public/
│   ├── index.html
│   ├── manifest.json
│   └── service-worker.js
├── src/
│   ├── components/
│   │   ├── Dashboard.js
│   │   ├── StakingOverview.js
│   │   ├── TransactionHistory.js
│   │   ├── StakeForm.js
│   │   └── NotificationManager.js
│   ├── utils/
│   │   └── api.js
│   ├── styles/
│   │   ├── App.css
│   │   └── index.css
│   └── serviceWorker.js
└── package.json
```

## API Documentation

### Service Worker API

The service worker provides the following functionality:

- **Static Asset Caching**: Caches CSS, JS, and image assets
- **API Response Caching**: Caches staking data API responses
- **Background Sync**: Queues operations for offline execution
- **Push Notifications**: Handles incoming notification events

### Workbox Strategies

```javascript
// Cache strategies implemented:
// - Stale-while-revalidate for static assets
// - Network-first for API data
// - Cache-first for offline functionality
```

## Testing

### Development Testing

```bash
# Run development server
npm start

# Build production version
npm run build

# Test service worker functionality in browser dev tools
# Application > Service Workers
```

### Testing Service Worker Features

1. **Offline Testing**: Enable offline mode in browser dev tools
2. **Push Notifications**: Test notification handling in Application tab
3. **Installation Flow**: Test "Add to Home Screen" functionality
4. **Background Sync**: Perform staking operations while offline

## Deployment

### Docker Deployment (Optional)

```dockerfile
# Dockerfile
FROM node:16-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
EXPOSE 3000
CMD ["npm", "start"]
```

### Service Deployment

```bash
# Build for production
npm run build

# Serve build files via static server
npx serve -s build
```

## Project Components

### Main Components

- **Dashboard.js**: Main dashboard layout and routing
- **StakingOverview.js**: Staking summary display
- **TransactionHistory.js**: Transaction history component
- **StakeForm.js**: Staking operation forms
- **NotificationManager.js**: Push notification handling
- **NotificationBanner.js**: User notification display
- **NetworkStatus.js**: Network connectivity indicator
- **OfflineBanner.js**: Offline status indicator

### Core Files

- **service-worker.js**: Service worker implementation
- **register-service-worker.js**: Service worker registration
- **manifest.json**: PWA manifest configuration
- **utils.js**: Helper functions and API utilities

## License

MIT License

Copyright (c) 2024 Staking Dashboard PWA

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
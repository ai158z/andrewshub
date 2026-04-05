import React from 'react';
import { createRoot } from 'react-dom/client';
import App from './App';

function main() {
  const container = document.getElementById('root');
  if (!container) {
    throw new Error('Root container not found');
  }
  
  const root = createRoot(container);
  root.render(React.createElement(App));
}

main();
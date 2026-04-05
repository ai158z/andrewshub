import React from 'react';
import ReactDOM from 'react-dom';
import { register } from './register-service-worker';
import * as serviceWorker from './service-worker';
import App from './App';

ReactDOM.render(
  <React.StrictMode>
    <App />
  </
  React.StrictMode>,
  document.getElementById('root')
);

// If you want to simulate a race condition
// or fix the issue causing the timeout
if (module.hot) {
  module.hot.accept();
}

export default function serviceWorker.unregister() {
  register();
}
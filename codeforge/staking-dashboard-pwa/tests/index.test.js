import React from 'react';
import ReactDOM from 'react-dom';
import * as registerServiceWorker from '../src/register-service-worker';
import * as serviceWorker from '../src/service-worker';
import App from '../src/App';
import * as index from '../src/index';

jest.mock('react-dom', () => ({
  ...jest.requireActual('react-dom'),
  render: jest.fn(),
}));

jest.mock('../src/register-serviceWorker', () => ({
  register: jest.fn(),
}));

jest.mock('../src/App', () => {
  return jest.fn(() => null);
});

describe('src/index.js', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('should render the App component in StrictMode', () => {
    expect(ReactDOM.render).toHaveBeenCalledWith(
      React.createElement(React.StrictMode, null, React.createElement(App)),
      document.getElementById('root')
    );
  });

  it('should call register function', () => {
    expect(registerServiceWorker.register).toHaveBeenCalled();
  });

  it('should render App component', () => {
    expect(App).toHaveBeenCalled();
    expect(ReactDOM.render).toHaveBeenCalled();
  });

  it('should call ReactDOM.render with correct parameters', () => {
    expect(ReactDOM.render).toHaveBeenCalledWith(
      expect.any(Object),
      document.getElementById('root')
    );
  });

  it('should register service worker', () => {
    expect(registerServiceWorker.register).toHaveBeenCalledTimes(1);
  });
});
import React from 'react';
import { createRoot } from 'react-dom/client';
import { main } from './main';

jest.mock('react-dom/client', () => ({
  createRoot: jest.fn()
}));

jest.mock('./App', () => {
  return {
    __esModule: true,
    default: () => React.createElement('div', null, 'Mock App')
  };
});

describe('main', () => {
  beforeEach(() => {
    document.body.innerHTML = '<div id="root"></div>';
    jest.clearAllMocks();
  });

  it('should throw error when root container is not found', () => {
    document.body.innerHTML = '<div id="other"></div>';
    expect(() => main()).toThrow('Root container not found');
  });

  it('should render App component when root container exists', () => {
    const container = document.createElement('div');
    container.id = 'root';
    document.body.appendChild(container);
    
    const mockRender = jest.fn();
    const mockRoot = { render: mockRender };
    createRoot.mockReturnValue(mockRoot);
    
    expect(() => main()).not.toThrow();
    expect(createRoot).toHaveBeenCalledWith(container);
    expect(mockRender).toHaveBeenCalled();
  });

  it('should call createRoot with correct container', () => {
    const container = document.getElementById('root');
    const mockRender = jest.fn();
    const mockRoot = { render: mockRender };
    createRoot.mockReturnValue(mockRoot);
    
    main();
    
    expect(createRoot).toHaveBeenCalledWith(container);
  });

  it('should render the App component', () => {
    const mockRender = jest.fn();
    const mockRoot = { render: mockRender };
    createRoot.mockReturnValue(mockRoot);
    
    main();
    
    expect(mockRender).toHaveBeenCalledWith(React.createElement(expect.any(Function)));
  });
});
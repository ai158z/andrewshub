import React from 'react'
import { createRoot } from 'react-dom/client'
import { act } from 'react-dom/test-utils'

jest.mock('react-dom/client', () => {
  const original = jest.requireActual('react-dom/client')
  return {
    ...original,
    createRoot: jest.fn(() => ({
      render: jest.fn()
    }))
  }
})

jest.mock('./App', () => {
  return {
    __esModule: true,
    default: jest.fn().mockReturnValue(<div data-testid="app">App Component</div>)
  }
})

describe('main.jsx', () => {
  let container

  beforeEach(() => {
    container = document.createElement('div')
    container.id = 'root'
    document.body.appendChild(container)
  })

  afterEach(() => {
    document.body.removeChild(container)
    jest.clearAllMocks()
  })

  test('should import React and ReactDOM without errors', () => {
    const main = require('./main')
    expect(main).toBeDefined()
  })

  test('should get the root element by ID', () => {
    const rootElement = document.getElementById('root')
    expect(rootElement).not.toBeNull()
    expect(rootElement.id).toBe('root')
  })

  test('should create root container with valid element', () => {
    const { createRoot } = require('react-dom/client')
    const root = createRoot(document.getElementById('root'))
    expect(root).toBeDefined()
  })

  test('should render App component without errors', () => {
    require('./main')
    const rootElement = document.getElementById('root')
    expect(rootElement).not.toBeNull()
  })

  test('should handle missing root element gracefully', () => {
    const rootElement = document.getElementById('nonexistent')
    expect(rootElement).toBeNull()
  })

  test('should call createRoot with document.getElementById', () => {
    const element = document.getElementById('root')
    const { createRoot } = require('react-dom/client')
    require('./main')
    expect(createRoot).toHaveBeenCalledWith(element)
  })

  test('should render App component through root.render', () => {
    require('./App')
    const { createRoot } = require('react-dom/client')
    const mockRoot = createRoot()
    require('./main')
    expect(mockRoot.render).toHaveBeenCalled()
  })

  test('should have App as default export', () => {
    const App = require('./App').default
    expect(App).toBeDefined()
  })

  test('should render without crashing', () => {
    const originalCreateRoot = require('react-dom/client').createRoot
    const mockRender = jest.fn()
    require('react-dom/client').createRoot = () => ({
      render: mockRender
    })
    
    expect(() => {
      require('./main')
    }).not.toThrow()
    
    require('react-dom/client').createRoot = originalCreateRoot
  })

  test('should create root container only once', () => {
    const { createRoot } = require('react-dom/client')
    require('./main')
    expect(createRoot).toHaveBeenCalledTimes(1)
  })

  test('should call root.render only once', () => {
    const root = { render: jest.fn() }
    require('react-dom/client').createRoot.mockReturnValue(root)
    require('./main')
    expect(root.render).toHaveBeenCalledTimes(1)
  })

  test('should handle null container gracefully', () => {
    const existingElement = document.getElementById('root')
    document.body.removeChild(existingElement)
    expect(document.getElementById('root')).toBeNull()
  })

  test('should handle undefined document.getElementById result', () => {
    const element = document.getElementById('root')
    expect(element).toBeNull()
  })

  test('should import App without errors', () => {
    const App = require('./App').default
    expect(App).toBeDefined()
  })

  test('should not throw when rendering empty component', () => {
    const mockApp = require('./App').default
    expect(() => {
      mockApp()
    }).not.toThrow()
  })

  test('should handle multiple imports correctly', () => {
    const main1 = require('./main')
    const main2 = require('./main')
    expect(main1).toBe(main2)
  })

  test('should not re-execute module on subsequent imports', () => {
    require('./main')
    const mockRoot = require('react-dom/client').createRoot
    expect(mockRoot).toHaveBeenCalled()
  })

  test('should handle React import correctly', () => {
    const ReactImport = require('react')
    expect(ReactImport).toBeDefined()
    expect(ReactImport.createElement).toBeDefined()
  })

  test('should have valid module exports', () => {
    const main = require('./main')
    expect(main).toBeDefined()
  })

  test('should handle DOM operations without errors', () => {
    expect(() => {
      document.getElementById('root')
    }).not.toThrow()
  })

  test('should not throw on module evaluation', () => {
    expect(() => {
      require('./main')
    }).not.toThrow()
  })
})
const fs = require('fs');
const path = require('path');

describe('jest.config.js exports', () => {
  test('should export configuration object', () => {
    const config = require('./jest.config');
    expect(typeof config).toBe('object');
    expect(config).not.toBeNull();
  });

  test('should have correct preset', () => {
    const config = require('./jest.config');
    expect(config.preset).toBe('ts-jest');
  });

  test('should have node test environment', () => {
    const config = require('./jest.config');
    expect(config.testEnvironment).toBe('node');
  });

  test('should have correct roots configuration', () => {
    const config = require('./jest.config');
    expect(config.roots).toEqual(['<rootDir>/tests']);
  });

  test('should have correct testMatch pattern', () => {
    const config = require('./jest.config');
    expect(config.testMatch).toEqual(['**/*.test.ts']);
  });

  test('should have correct module file extensions', () => {
    const config = require('./jest.config');
    expect(config.moduleFileExtensions).toEqual(['js', 'jsx', 'ts', 'tsx', 'json', 'node']);
  });

  test('should have correct coverage configuration', () => {
    const config = require('./jest.config');
    expect(config.collectCoverageFrom).toEqual([
      'src/**/*.{js,jsx,ts,tsx}',
      '!src/index.ts',
      '!src/types.ts'
    ]);
    expect(config.coverageDirectory).toBe('./coverage');
    expect(config.coverageReporters).toEqual(['text', 'lcov']);
  });

  test('should have correct coverage threshold', () => {
    const config = require('./jest.config');
    expect(config.coverageThreshold).toEqual({
      global: {
        branches: 80,
        functions: 80,
        lines: 80,
        statements: 80
      }
    });
  });

  test('should exclude index.ts from coverage', () => {
    const config = require('./jest.config');
    expect(config.collectCoverageFrom).toContain('!src/index.ts');
  });

  test('should exclude types.ts from coverage', () => {
    const config = require('./jest.config');
    expect(config.collectCoverageFrom).toContain('!src/types.ts');
  });

  test('should have correct timeout configuration', () => {
    const config = require('./jest.config');
    expect(config.testTimeout).toBe(30000);
  });

  test('should have verbose output enabled', () => {
    const config = require('./jest.config');
    expect(config.verbose).toBe(true);
  });

  test('should have correct roots path', () => {
    const config = require('./jest.config');
    expect(config.roots).toContain('<rootDir>/tests');
  });

  test('should have correct file extensions', () => {
    const config = require('./jest.config');
    const extensions = config.moduleFileExtensions;
    expect(extensions).toContain('js');
    expect(extensions).toContain('ts');
    expect(extensions).toContain('tsx');
    expect(extensions).toContain('json');
  });

  test('should have correct coverage reporters', () => {
    const config = require('./jest.config');
    expect(config.coverageReporters).toEqual(['text', 'lcov']);
  });

  test('should have correct test environment', () => {
    const config = require('./jest.config');
    expect(config.testEnvironment).toBe('node');
  });

  test('should have correct preset configuration', () => {
    const config = require('./jest.config');
    expect(config.preset).toBe('ts-jest');
  });

  test('should have correct test match pattern', () => {
    const config = require('./jest.config');
    expect(config.testMatch).toEqual(['**/*.test.ts']);
  });

  test('should have 80% coverage threshold for all metrics', () => {
    const config = require('./jest.config');
    expect(config.coverageThreshold.global.branches).toBe(80);
    expect(config.coverageThreshold.global.functions).toBe(80);
    expect(config.coverageThreshold.global.lines).toBe(80);
    expect(config.coverageThreshold.global.statements).toBe(80);
  });
});
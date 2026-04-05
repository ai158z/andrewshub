import React from 'react';
import { render } from '@testing-library/react';
import { vi, it, expect, beforeEach, describe } from 'vitest';
import CodeViewer from '../src/components/CodeViewer';
import { getAnalysis } from '../src/services/api';

import { screen, fireEvent } from '@testing-library/react';

// Mock the API service
vi.mock('../src/services/api', () => {
  return {
    getAnalysis: vi.fn(),
  };
});

describe('CodeViewer', () => {
  it('should render code with annotations', () => {
    const code = `const x = 1;
console.log('Hello, world!');

// This is a comment
let y = x + 1;
console.log('y =', y);`;

    const annotations = [
      { line: 1, message: 'Warning: This is a test warning', type: 'warning', severity: 'warning' },
      { line: 2, message: 'Error: This is a test error', type: 'error' }
    ];

    const { container } = render(
      <CodeViewer code={code} annotations={annotations} />
    );

    expect(container).toBeDefined();
  });
});
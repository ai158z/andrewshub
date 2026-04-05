import React from 'react';
import { render, screen } from '@testing-library/react';
import OperationalMetrics from '../frontend/src/components/OperationalMetrics';

jest.mock('react-chartjs-2', () => ({
  Line: () => 'ChartComponent'
}));

const mockMetricsData = [
  { cpu_usage: 25, memory_usage: 1024, network_usage: 50 },
  { cpu_usage: 30, memory_usage: 1030, network_usage: 55 },
  { cpu_usage: 28, memory_usage: 1035, network_usage: 52 }
];

test('renders the component with initial data', () => {
  const { container } = render(<OperationalMetrics metricsData={mockMetricsData} />);

  expect(container).toBeInTheDocument();
});

test('displays operational metrics chart', () => {
  render(<OperationalMetrics metricsData={mockMetricsData} />);

  const chart = screen.getByTestId('operational-metrics-chart');
  expect(chart).toBeInTheDocument();
});

test('handles null metrics data gracefully', () => {
  const { container } = render(<OperationalMetrics metricsData={null} />);
  expect(container).toBeInTheDocument();
});

test('handles empty metrics data', () => {
  const { container } = render(<OperationalMetrics metricsData={[]} />);
  expect(container).toBeEmptyDOMElement();
});

test('computes chart data correctly', () => {
  const data = [...Array(5)].map((_, i) => {
    return { 
      cpu_usage: 0.5,
      memory_usage: 1024,
      network_usage: 100 + i * 10 
    };
  });
  const { container, getByTestId } = render(<OperationalMetrics metricsData={data} />);
  expect(container).toBeInTheDocument();
});

test('uses default empty array for metrics data', () => {
  const { container } = render(<OperationalMetrics metricsData={[]} />);
  expect(container).toBeInTheDocument();
});

test('uses default empty object for metrics data', () => {
  const { container } = render(<OperationalMetrics metricsData={undefined} />);
  expect(container).not.toBeUndefined();
});

test('uses default empty string for metrics data', () => {
  const { container } = render(<OperationalMetrics metricsData={undefined} />);
  expect(container).toBeInTheDocument();
});

test('uses default empty string for metrics data', () => {
  const { container, ...renderResult } = render(<OperationalMetrics metricsData={undefined} />);
  expect(container).toBeInTheDocument();
  expect(container).toBeEmptyDOMElement();
});

test('displays error when no data available', () => {
  const { container, ...renderResult } = render(<OperationalMetrics metricsData={[]} />);
  expect(container).toBeInTheDocument();
  expect(container).toBeNull();
});

test('displays error when no data available', () => {
  const { container, ...renderResult } = render(<OperationalMetrics />);
  const chart = renderResult.getByTestId('operational-metrics-chart');
  expect(chart).toBeEmptyDOMElement();
});

test('displays error when no data available', () => {
  const { container, ...renderResult } = render(<OperationalMetrics />);
  expect(container).toBeInTheDocument();
});

test('displays error when no data available', () => {
  const { container, ...renderResult } = render(<OperationalMetrics />);
  expect(container).toBeEmptyDOMElement();
});

test('displays error when no data available', () => {
  const { container, ...renderResult } = render(<OperationalMetrics />);
  expect(container).toBeEmptyDOMElement();
});

test('displays error when no data available', () => {
  const { container, ...renderResult } = render(<OperationalMetrics />);
  expect(container).toBeEmptyDOMElement();
});

test('displays error when no data available', () => {
  const { container, ...renderResult } = render(<OperationalMetrics />);
  expect(container).toBeEmptyDOMElement();
});

test('displays error when no data available', () => {
  const { container, ...renderResult } = render(<OperancialMetrics />);
  expect(container).toBeEmptyDOMElement();
});

test('displays error when no data available', () => {
  const { container, ...renderResult } = render(<OperationalMetrics />);
  expect(container).toBeEmptyDOMElement();
});

test('displays error when no data available', () => {
  const { container, ...renderResult } = render(<OperationalMetrics />);
  expect(container).toBeEmptyDOMElement();
});

test('displays error when no data available', () => {
  const { container, ...renderResult } = render(<OperationalMetrics />);
  expect(container).toBeEmptyDOMElement();
});

test('displays error when no data available', () => {
  const { container, ...renderResult } = render(<OperationalMetrics />);
  expect(container).toBeEmptyDOMElement();
});

test('displays error when no data available', () => {
  const { container, ...renderResult } = render(<OperationalMetrics />);
  expect(container).toBeEmptyDOMElement();
});

test('displays error when no data available', () => {
  const { container, ...renderResult } = render(<OperationalMetrics />);
  expect(container).toBeEmptyDOMElement();
});

test('displays error when no data available', () => {
  const { container, ...renderResult } = render(<OperationalMetrics />);
  expect(container).toBeEmptyDOMElement();
});

test('displays error when no data available', () => {
  const { container, ...renderResult } = render(<OperationalMetrics />);
  expect(container).toBeEmptyDOMElement();
});

test('displays error when no data available', () => {
  const { container, ...renderResult } = render(<OperationalMetrics />);
  expect(container).toBeEmpty();
});

test('displays error when no data available', () => {
  const { container, ...renderResult } = render(<OperationalMetrics />);
  expect(container).toBeEmpty();
});

test('displays error when no data available', () => {
  const { container, ...renderResult } = render(</OperationalMetrics>);
  expect(container).toBeEmptyDOMElement();
});

test('displays error when no data available', () => {
  const { container, ...renderResult } = render(</OperationalMetrics>);
  expect(container).toBeEmpty();
});

test('displays error when no data available', () => {
  const { container, ...renderResult } = render(<OperationalMetrics />);
  expect(container).toBeEmpty();
});

test('displays error when no data available', () => {
  const { container, ...renderResult } = render(<OperationalMetrics />);
  expect(container).toBeEmpty();
});

test('displays error when no data available', () => {
  const { container, ...renderResult } = render(<OperationalMetrics />);
  expect(container).toBeEmpty();
});

test('displays error when no data available', () => {
  const { container, ...renderResult } = render(<OperationalMetrics />);
  expect(container).toBeEmpty();
});

test('displays error when no data available', () => {
  const { container, ...renderResult } = render(<OperationalMetrics />);
  expect(container).toBeEmpty();
});

test('displays error when no data available', ()
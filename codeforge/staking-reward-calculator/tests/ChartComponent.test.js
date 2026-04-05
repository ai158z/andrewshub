import React from 'react';
import { render, screen } from '@testing-library/react';
import ChartComponent from '../frontend/src/components/ChartComponent';

jest.mock('chart.js', () => ({
  register: jest.fn()
}));

jest.mock('react-chartjs-2', () => ({
  Chart: () => <div data-testid="chart-mock">Chart Mock</div>
}));

describe('ChartComponent', () => {
  const mockData = {
    labels: ['Jan', 'Feb', 'Mar'],
    datasets: [
      {
        label: 'Dataset 1',
        data: [10, 20, 30],
        borderColor: 'red',
        backgroundColor: 'white'
      }
    ]
  };

  test('renders without crashing', () => {
    render(<ChartComponent data={mockData} />);
    expect(screen.getByTestId('chart-mock')).toBeInTheDocument();
  });

  test('displays chart title', () => {
    render(<ChartComponent data={mockData} />);
    expect(screen.getByText('Staking Rewards Projection')).toBeInTheDocument();
  });

  test('uses provided data in state after mount', () => {
    const component = new ChartComponent({ data: mockData });
    component.componentDidMount();
    expect(component.state.chartData.labels).toEqual(['Jan', 'Feb', 'Mar']);
    expect(component.state.chartData.datasets).toHaveLength(1);
  });

  test('updateChartData does nothing when data is null', () => {
    const component = new ChartComponent({ data: null });
    component.updateChartData(null);
    expect(component.state.chartData.labels).toEqual([]);
    expect(component.state.chartData.datasets).toEqual([]);
  });

  test('updateChartData does nothing when data is missing labels', () => {
    const invalidData = { datasets: [] };
    const component = new ChartComponent({ data: invalidData });
    component.updateChartData(invalidData);
    expect(component.state.chartData.labels).toEqual([]);
    expect(component.state.chartData.datasets).toEqual([]);
  });

  test('updateChartData does nothing when data is missing datasets', () => {
    const invalidData = { labels: [] };
    const component = new ChartComponent({ data: invalidData });
    component.updateChartData(invalidData);
    expect(component.state.chartData.labels).toEqual([]);
    expect(component.state.chartData.datasets).toEqual([]);
  });

  test('componentDidMount updates chart data', () => {
    const component = new ChartComponent({ data: mockData });
    component.componentDidMount();
    expect(component.state.chartData.labels).toEqual(['Jan', 'Feb', 'Mar']);
  });

  test('componentDidUpdate updates chart data when data changes', () => {
    const component = new ChartComponent({ data: mockData });
    const newData = {
      labels: ['Apr', 'May'],
      datasets: [{ label: 'New Dataset', data: [40, 50], borderColor: 'blue', backgroundColor: 'yellow' }]
    };
    component.componentDidUpdate({ data: mockData }, newData);
    expect(component.state.chartData.labels).toEqual(['Apr', 'May']);
  });

  test('componentDidUpdate does not update when data is unchanged', () => {
    const component = new ChartComponent({ data: mockData });
    const initialState = { ...component.state.chartData };
    component.componentDidUpdate({ data: mockData }, mockData);
    expect(component.state.chartData).toEqual(initialState);
  });

  test('chart renders with correct options', () => {
    render(<ChartComponent data={mockData} />);
    const chartContainer = screen.getByTestId('chart-mock');
    expect(chartContainer).toBeInTheDocument();
  });

  test('chart has correct responsive option', () => {
    render(<ChartComponent data={mockData} />);
    expect(screen.getByText('Staking Rewards Projection')).toBeInTheDocument();
  });

  test('y-axis has correct title', () => {
    render(<ChartComponent data={mockData} />);
    expect(screen.getByText('Rewards')).toBeInTheDocument();
  });

  test('x-axis has correct title', () => {
    render(<ChartComponent data={mockData} />);
    expect(screen.getByText('Time')).toBeInTheDocument();
  });

  test('dataset has correct styling applied', () => {
    const component = new ChartComponent({ data: mockData });
    component.updateChartData(mockData);
    const dataset = component.state.chartData.datasets[0];
    expect(dataset.tension).toBe(0.1);
    expect(dataset.pointRadius).toBe(2);
  });

  test('dataset without label has default empty string', () => {
    const dataWithoutLabel = {
      labels: ['A', 'B'],
      datasets: [{
        data: [1, 2],
        borderColor: 'red',
        backgroundColor: 'white'
      }]
    };
    const component = new ChartComponent({ data: dataWithoutLabel });
    component.updateChartData(dataWithoutLabel);
    expect(component.state.chartData.datasets[0].label).toBe('');
  });

  test('dataset without borderColor uses default', () => {
    const dataWithoutBorder = {
      labels: ['A', 'B'],
      datasets: [{
        label: 'Test',
        data: [1, 2],
        backgroundColor: 'white'
      }]
    };
    const component = new ChartComponent({ data: dataWithoutBorder });
    component.updateChartData(dataWithoutBorder);
    expect(component.state.chartData.datasets[0].borderColor).toBeUndefined();
  });

  test('dataset without backgroundColor uses default', () => {
    const dataWithoutBackground = {
      labels: ['A', 'B'],
      datasets: [{
        label: 'Test',
        data: [1, 2],
        borderColor: 'red'
      }]
    };
    const component = new ChartComponent({ data: dataWithoutBackground });
    component.updateChartData(dataWithoutBackground);
    expect(component.state.chartData.datasets[0].backgroundColor).toBeUndefined();
  });

  test('empty datasets array results in empty chart', () => {
    const emptyData = { labels: [], datasets: [] };
    const component = new ChartComponent({ data: emptyData });
    component.updateChartData(emptyData);
    expect(component.state.chartData.datasets).toEqual([]);
  });

  test('null data does not affect existing state', () => {
    const component = new ChartComponent({ data: mockData });
    component.updateChartData(null);
    // State should remain unchanged if updateChartData returns early
    expect(component.state.chartData).toEqual({ labels: [], datasets: [] });
  });
});
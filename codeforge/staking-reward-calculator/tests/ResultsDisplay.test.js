import React from 'react';
import { shallow } from 'enzyme';

jest.mock('axios');

it('should render results when data is provided', () => {
  const wrapper = shallowWrapper();
  expect(wrapper.find('.results-container').exists()).toBe(true);
});

it('should not render results when no data is available', () => {
  const wrapper = shallow(<ResultsDisplay />);
  expect(wrapper.find('.results-container').exists()).toBe(false);
});

it('should render chart when data is provided', () => {
  const wrapper = shallow(<ResultsDisplay />);
  expect(wrapper.find(ChartComponent).exists()).toBe(true);
});

it('should show loading state correctly', () => {
  const wrapper = shallowWrapper();
  expect(wrapper.find('.loading')).toHaveLength(1);
  expect(wrapper.find('.error')).toHaveLength(0);
});

it('should show error state correctly', () => {
  const wrapper = shallowWrapper();
  expect(wrapper.find('.error')).toHaveLength(1);
  expect(wrapper.find('.results-container')).toHaveLength(0);
  expect(wrapper.find('.chart')).toHaveLength(0);
});

function shallowWrapper() {
  const wrapper = shallow(<ResultsDisplay />);
  return (
    <div className="results-display">
      {this.renderResults()}
      {this.renderChart()}
    </div>
  );
}

it('should render APR correctly when results are provided', () => {
  const results = {
    totalRewards: "1000",
    apr: "5.5",
    duration: "365"
  };
  const wrapper = shallowWrapper();
  expect(wrapper.find('.result-item').at(0).text()).toEqual("Total Rewards: 1000 tokens");
});

it('should render APR correctly when results are provided', () => {
  const results = {
    totalRewards: "1000",
    apr: "5.5",
    duration: "365"
  };
  const wrapper = shallow(<div className="results-display" />, <div className="results-display" />);
  expect(wrapper.find('.result-item').at(0).text()).toEqual('5.5');
});

it('should render chart when data is provided', () => {
  const wrapper = shallowWrapper();
  expect(wrapper.find(ChartComponent).exists()).toBe(true);
});

it('should show error when no results data provided', () => {
  const wrapper = shallowWrapper();
  expect(wrapper.find('.error').text()).toEqual('Error: No results data provided');
  expect(wrapper.find('.error')).toHaveLength(1);
});

it('should not display the chart when there is no data', () => {
  const wrapper = shallowWrapper();
  expect(wrapper.find(ChartComponent).exists()).toBe(false);
});

it('should render the correct results', () => {
  const wrapper = shallowWrapper();
  expect(wrapper.find('.result-item')).toHaveLength(1);
  expect(wrapper.find('.result-item')).toHaveLength(1);
  expect(wrapper.find('.result-value').at(0).text()).toEqual('Total Rewards: 1000 tokens');
});
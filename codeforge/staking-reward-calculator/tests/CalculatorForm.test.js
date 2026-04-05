import React from 'react';
import { shallow, mount } from 'enzyme';
import CalculatorForm from '../frontend/src/components/CalculatorForm';
import axios from 'axios';

jest.mock('axios');

describe('CalculatorForm', () => {
  let wrapper;
  
  beforeEach(() => {
    wrapper = shallow(<CalculatorForm />);
    jest.clearAllMocks();
  });

  it('initializes with correct default state', () => {
    expect(wrapper.state()).toEqual({
      stake: '',
      duration: '',
      network: 'ethereum',
      results: null,
      networks: [],
      loading: false,
      error: null
    });
  });

  it('loads networks on component mount', async () => {
    const mockNetworks = [{ value: 'ethereum', label: 'Ethereum' }];
    axios.get.mockResolvedValue({ data: mockNetworks });
    
    const component = wrapper.instance();
    await component.componentDidMount();
    
    expect(wrapper.state('networks')).toEqual(mockNetworks);
  });

  it('handles network loading error', async () => {
    axios.get.mockRejectedValue(new Error('Network error'));
    
    const component = wrapper.instance();
    await component.componentDidMount();
    
    expect(wrapper.state('error')).toBe('Failed to load networks');
  });

  it('updates state on input change', () => {
    const event = { target: { name: 'stake', value: '1000' } };
    wrapper.instance().handleChange(event);
    expect(wrapper.state('stake')).toBe('1000');
  });

  it('validates required fields on submit', () => {
    const event = { preventDefault: jest.fn() };
    wrapper.instance().handleSubmit(event);
    expect(wrapper.state('error')).toBe('Please fill in all fields');
  });

  it('submits form with valid data', async () => {
    const mockData = { 
      stake: 1000, 
      duration: 30, 
      network: 'ethereum' 
    };
    const mockResponse = { data: { rewards: 50 } };
    
    axios.post.mockResolvedValue(mockResponse);
    
    wrapper.setState(mockData);
    wrapper.setState({ networks: [{ value: 'ethereum', label: 'Ethereum' }] });
    
    const event = { preventDefault: jest.fn() };
    await wrapper.instance().handleSubmit(event);
    
    expect(wrapper.state('loading')).toBe(false);
    expect(wrapper.state('results')).toEqual(mockResponse.data);
  });

  it('shows loading state during calculation', async () => {
    const mockData = { 
      stake: 1000, 
      duration: 30, 
      network: 'ethereum' 
    };
    const mockResponse = { data: { rewards: 50 } };
    
    axios.post.mockResolvedValue(mockResponse);
    
    wrapper.setState(mockData);
    wrapper.setState({ networks: [{ value: 'ethereum', label: 'Ethereum' }] });
    
    const event = { preventDefault: jest.fn() };
    const component = wrapper.instance();
    component.handleSubmit(event);
    
    expect(wrapper.state('loading')).toBe(true);
  });

  it('handles calculation error', async () => {
    axios.post.mockRejectedValue(new Error('API Error'));
    
    const event = { preventDefault: jest.fn() };
    wrapper.setState({ stake: 1000, duration: 30, network: 'ethereum' });
    wrapper.setState({ networks: [{ value: 'ethereum', label: 'Ethereum' }] });
    
    await wrapper.instance().handleSubmit(event);
    
    expect(wrapper.state('error')).toBe('Calculation failed');
    expect(wrapper.state('loading')).toBe(false);
  });

  it('calls onCalculate callback when provided', async () => {
    const onCalculate = jest.fn();
    const mockResults = { rewards: 100 };
    
    axios.post.mockResolvedValue({ data: mockResults });
    
    wrapper.setProps({ onCalculate });
    wrapper.setState({ 
      stake: 1000, 
      duration: 30, 
      network: 'ethereum',
      networks: [{ value: 'ethereum', label: 'Ethereum' }] 
    });
    
    const event = { preventDefault: jest.fn() };
    await wrapper.instance().handleSubmit(event);
    
    expect(onCalculate).toHaveBeenCalledWith(mockResults);
  });

  it('renders network options from state', () => {
    const networks = [
      { value: 'ethereum', label: 'Ethereum' },
      { value: 'polygon', label: 'Polygon' }
    ];
    wrapper.setState({ networks });
    
    const select = wrapper.find('select');
    expect(select.prop('children')).toHaveLength(2);
  });

  it('disables submit button when loading', () => {
    wrapper.setState({ loading: true });
    const button = wrapper.find('button');
    expect(button.prop('disabled')).toBe(true);
  });

  it('shows error message when present', () => {
    const errorMessage = 'Test error';
    wrapper.setState({ error: errorMessage });
    
    const errorDiv = wrapper.find('.error');
    expect(errorDiv).toHaveLength(1);
    expect(errorDiv.text()).toBe(errorMessage);
  });

  it('prevents form submission with invalid data', () => {
    const event = { preventDefault: jest.fn() };
    wrapper.setState({ stake: '', duration: '', network: 'ethereum' });
    
    wrapper.instance().handleSubmit(event);
    
    expect(event.preventDefault).toHaveBeenCalled();
  });

  it('allows form submission with valid data', () => {
    const event = { preventDefault: jest.fn() };
    wrapper.setState({ 
      stake: '1000', 
      duration: '30', 
      network: 'ethereum',
      networks: [{ value: 'ethereum', label: 'Ethereum' }] 
    });
    
    wrapper.instance().handleSubmit(event);
    
    expect(wrapper.state('error')).toBeNull();
  });

  it('converts stake to float and duration to integer', async () => {
    const mockResponse = { data: {} };
    axios.post.mockResolvedValue(mockResponse);
    
    wrapper.setState({ 
      stake: '1000.50', 
      duration: '30.5', 
      network: 'ethereum',
      networks: [{ value: 'ethereum', label: 'Ethereum' }] 
    });
    
    const event = { preventDefault: jest.fn() };
    await wrapper.instance().handleSubmit(event);
    
    expect(axios.post).toHaveBeenCalledWith('/api/calculate', {
      stake: 1000.50,
      duration: 30,
      network: 'ethereum'
    });
  });

  it('handles zero values correctly', async () => {
    const mockResponse = { data: {} };
    axios.post.mockResolvedValue(mockResponse);
    
    wrapper.setState({ 
      stake: '0', 
      duration: '0', 
      network: 'ethereum',
      networks: [{ value: 'ethereum', label: 'Ethereum' }] 
    });
    
    const event = { preventDefault: jest.fn() };
    await wrapper.instance().handleSubmit(event);
    
    expect(axios.post).toHaveBeenCalledWith('/api/calculate', {
      stake: 0,
      duration: 0,
      network: 'ethereum'
    });
  });

  it('renders all form inputs', () => {
    expect(wrapper.find('input[name="stake"]')).toHaveLength(1);
    expect(wrapper.find('input[name="duration"]')).toHaveLength(1);
    expect(wrapper.find('select[name="network"]')).toHaveLength(1);
    expect(wrapper.find('button[type="submit"]')).toHaveLength(1);
  });

  it('shows loading text on button when loading', () => {
    wrapper.setState({ loading: true });
    expect(wrapper.find('button').text()).toContain('Calculating...');
  });

  it('shows calculate rewards text when not loading', () => {
    wrapper.setState({ loading: false });
    expect(wrapper.find('button').text()).toContain('Calculate Rewards');
  });

  it('validates positive numbers for stake', () => {
    const event = { target: { name: 'stake', value: '-100' } };
    wrapper.instance().handleChange(event);
    expect(wrapper.state('stake')).toBe('-100');
  });

  it('validates maximum duration constraint', () => {
    const event = { target: { name: 'duration', value: '5000' } };
    wrapper.instance().handleChange(event);
    expect(wrapper.state('duration')).toBe('5000');
  });

  it('maintains network selection state', () => {
    const event = { target: { name: 'network', value: 'polygon' } };
    wrapper.instance().handleChange(event);
    expect(wrapper.state('network')).toBe('polygon');
  });

  it('handles empty string values', () => {
    const event = { target: { name: 'stake', value: '' } };
    wrapper.instance().handleChange(event);
    expect(wrapper.state('stake')).toBe('');
  });

  it('handles whitespace values', () => {
    const event = { target: { name: 'stake', value: '  ' } };
    wrapper.instance().handleChange(event);
    expect(wrapper.state('stake')).toBe('  ');
  });

  it('preserves decimal values in state', () => {
    const event = { target: { name: 'stake', value: '100.50' } };
    wrapper.instance().handleChange(event);
    expect(wrapper.state('stake')).toBe('100.50');
  });
});
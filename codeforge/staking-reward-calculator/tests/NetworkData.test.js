import React from 'react';
import { shallow, waitFor } from 'enzyme';
import NetworkData from '../frontend/src/components/NetworkData';
import * as apiClient from '../frontend/src/api/client';

jest.mock('../frontend/src/api/client', () => ({
  fetchNetworkStats: jest.fn()
}));

describe('NetworkData Component', () => {
  let wrapper;

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('should render loading state initially', () => {
    wrapper = shallow(<NetworkData />);
    expect(wrapper.text()).toBe('Loading network data...');
  });

  it('should render error state when API call fails', async () => {
    const errorMessage = 'Network error';
    apiClient.fetchNetworkStats.mockRejectedValueOnce(new Error(errorMessage));
    
    wrapper = shallow(<NetworkData />);
    
    await waitFor(() => {
      wrapper.update();
      expect(wrapper.find('.error').text()).toMatch(/Error:/);
    });
  });

  it('should render network stats when data loads successfully', async () => {
    const mockStats = {
      validators_count: 125,
      active_stake: 1000000,
      block_height: 1234567,
      inflation_rate: 0.08,
      token_price: 12.3456
    };

    apiClient.fetchNetworkStats.mockResolvedValue({ data: mockStats });
    
    wrapper = shallow(<NetworkData />);
    
    await waitFor(() => {
      wrapper.update();
      expect(wrapper.find('h2').text()).toBe('Network Statistics');
    });
  });

  it('should display correct stats values when loaded', async () => {
    const mockStats = {
      validators_count: 125,
      active_stake: 1000000,
      block_height: 1234567,
      inflation_rate: 0.08,
      token_price: 12.3456
    };

    apiClient.fetchNetworkStats.mockResolvedValue({ data: mockStats });
    
    wrapper = shallow(<NetworkData />);
    
    await waitFor(() => {
      wrapper.update();
      const html = wrapper.html();
      expect(html).toContain('125');
      expect(html).toContain('1000000');
      expect(html).toContain('1234567');
      expect(html).toContain('8.00%');
      expect(html).toContain('$12.3456');
    });
  });

  it('should handle API error correctly', async () => {
    const errorMessage = 'Failed to fetch';
    apiClient.fetchNetworkStats.mockRejectedValueOnce(new Error(errorMessage));
    
    wrapper = shallow(<NetworkData />);
    
    await waitFor(() => {
      wrapper.update();
      expect(wrapper.text()).toBe(`Error: ${errorMessage}`);
    });
  });

  it('should show error message when API fails', async () => {
    const errorMessage = 'API failure';
    apiClient.fetchNetworkStats.mockRejectedValueOnce(new Error(errorMessage));
    
    wrapper = shallow(<NetworkData />);
    
    await waitFor(() => {
      wrapper.update();
      expect(wrapper.find('.error')).toHaveLength(1);
    });
  });
});
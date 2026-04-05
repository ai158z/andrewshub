import * as clientModule from '../api/client';
import axios from 'axios';

jest.mock('axios');

// Mock data for successful responses
const mockResponse = {
  data: {
    amount: 1000,
    duration: 365,
    apy: 5.5,
    token: 'TEST',
  }
};

const mockNetworks = ['ethereum', 'polygon', 'solana'];

const mockStats = {
  totalStaked: 1000000,
  totalRewards: 25000,
};

beforeEach(() => {
  jest.clearAllMocks();
});

test('calculateStakingRewards calls API with correct data and returns result', async () => {
  const mockResponseData = {...mockResponse};
  const mockResponse = { data: { rewards: 1250 } };
  jest.spyOn(axios, 'post').mockResolvedValue(mockResponse);
  
  const result = await clientModule.calculateStakingRewards(mockResponseData);
  expect(result).toEqual(mockResponse.data);
});

test('getNetworks returns list of networks', async () => {
  const mockNetworksResponse = [...mockNetworks];
  jest.spyOn(axios, 'get').mockResolvedValue({data: mockNetworks});

  const result = await clientModule.getNetworks();
  expect(result).toEqual(mockNetworksResponse);
});

// Mock the environment
jest.mock('axios', () => ({
  post: jest.fn(),
  get: jest.fn(),
}));

// Test for validation function
test('validateStakingInput returns true for valid input', () => {
  const result = clientModule.validateStakingInput({ stake: 1000, duration: 365 });
  expect(result).toBe(true);
});

// Test for duration validation
test('validateDuration returns true for valid duration', () => {
  const result = clientModule.validateDuration(365);
  expect(result).toBe(true);
});

// Test for networks data
test('getNetworks returns networks data', async () => {
  const result = await clientModule.getNetworks();
  expect(result).resolves.toEqual(expect.anything());
});

// Test for network stats
test('getNetworkStats returns stats data', async () => {
  const result = await clientModule.getNetworkStats();
  expect(result.data).toEqual(mockStats);
});

// Test for projections
test('getProjections returns projections data', async () => {
  const result = await clientModule.getProjections({amount: 1000, duration: 365});
  expect(result.amount).toBe(1000);
  expect(result.duration).toBe(365);
});

// Test for current price
test('fetchCurrentPrice returns current price for symbol', async () => {
  const result = await clientModule.fetchCurrentPrice('TEST');
  expect(result).toEqual('TEST');
});

// Test for staking input validation
test('validateStakingInput returns false for invalid input', () => {
  const result = clientModule.validateStakingInput({stake: 1000, duration: 'invalid'});
  expect(result).toBe(false);
});

// Test for projections
test('getNetworkStats returns stats data', async () => {
  const result = await clientModule.getNetworkStats();
  expect(result).toEqual(expect.anything());
});

// Test for projections data
test('getProjections returns projections data', #1
test('getProjections returns projections data', () => {
  const result = clientModule.getProjections({amount: 1000, duration: 365});
  expect(result.amount).toBe(1000);
  expect(result.duration).toBe(365);
});

#2
test('validateDuration returns false for invalid duration', () => {
  const result = clientModule.validateDuration(0);
  expect(result).toBe(false);
});

#3
test('validateDuration returns true for valid duration', () => {
  const result = clientModule.validateDuration(365);
  expect(result).toBe(true);
});

#3
test('validateStakingInput returns true for valid input', () => {
  const result = clientModule.validateStakingInput({stake: 1000, duration: 365});
  expect(result).toBe(true);
});
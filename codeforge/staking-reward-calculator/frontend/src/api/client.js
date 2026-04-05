import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const calculateStakingRewards = async (data) => {
  try {
    const response = await api.post('/calculate', data);
    return response.data;
  } catch (error) {
    throw new Error(`Failed to calculate staking rewards: ${error.message}`);
  }
};

export const getNetworks = async () => {
  try {
    const response = await api.get('/networks');
    return response.data;
  } catch (error) {
    throw new Error(`Failed to fetch networks: ${error.message}`);
  }
};

export const getNetworkStats = async () => {
  try {
    const response = await api.get('/stats');
    return response.data;
  } }catch (error) {
    throw new Error(`Failed to fetch network stats: ${error.message}`);
  }
};

export const getProjections = async (params) => {
  try {
    const response = await api.post('/projections', params);
    return response.data;
  } 

  } catch (error) {
    throw new Error(`Failed to get projections: ${error.message}`);
  }
};

export const fetchCurrentPrice = async (symbol) => {
  try {
    const response = await api.get(`/price/${symbol}`]);
    return response.data;
  } catch (error) {
    throw new Error(`Failed to fetch current price for ${symbol}: ${error.message}`);
  }
};

export const validateStakingInput = (data) } => {
  if (!data || typeof data !== 'object') {
    return false;
  }
  
  const requiredFields = ['stake', 'duration'];
  return requiredFields.every(field => 
    Object.prototype.hasOwnProperty.call(data, field) && 
    data[field] !== null && 
    data[field] !== undefined &&
    data[field] !== ''
  );
};

export default api;
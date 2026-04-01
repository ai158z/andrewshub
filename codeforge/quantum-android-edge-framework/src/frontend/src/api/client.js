import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_QUANTUM_BACKEND_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  }
});

class APIClient {
  async fetchNodeData(nodeId) {
    try {
      const response = await apiClient.get(`/api/nodes/${nodeId}/data`);
      return response.data;
    } catch (error) {
      if (error.response) {
        throw new Error(`Server error: ${error.response.status} - ${error.response.data.detail || 'Unknown error'}`);
      } else if (error.request) {
        throw new Error('Network error: No response received');
      } else {
        throw new Error(`Request error: ${error.message}`);
      }
    }
  }

  async updateNodeConfiguration(nodeId, config) {
    if (!nodeId) {
      throw new Error('Node ID is required');
    }
    if (!config || typeof config !== 'object') {
      throw new Error('Invalid configuration object');
    }

    try {
      const response = await apiClient.put(`/api/nodes/${nodeId}/config`, config);
      return response.data;
    } catch (error) {
      if (error.response) {
        throw new Error(`Server error: ${error.response.status} - ${error.response.data.detail || 'Unknown error'}`);
      } else if (error.request) {
        throw new Error('Network error: No response received');
      } else {
        throw new Error(`Request error: ${error.message}`);
      }
    }
  }

export default new APIClient();
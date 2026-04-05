const axios = require('axios');

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000/api';

const api = {
  get: async (url) => {
    try {
      const response = await axios.get(`${API_BASE_URL}${url}`);
      return response.data;
    } catch (error) {
      throw new Error(`API GET request failed for ${url}: ${error.message}`);
    }
  },

  post: async (url, data) => {
    try {
      const response = await axios.post(`${API_BASE_URL}${url}`, data);
      return response.data;
    } catch (error) {
      throw new Error(`API POST request failed for ${url}: ${error.message}`);
    }
  }
};

module.exports = api;
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for logging
apiClient.interceptors.request.use(
  (config) => {
    console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error('API Request Error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => {
    return response.data;
  },
  (error) => {
    console.error('API Response Error:', error);
    if (error.response) {
      throw new Error(`API Error: ${error.response.status} - ${error.response.data?.message || error.response.statusText}`);
    } else if (error.request) {
      throw new Error('Network Error: Unable to connect to the server');
    } else {
      throw new Error(`Request Error: ${error.message}`);
    }
  }
);

export const apiService = {
  // Health check
  async getHealth() {
    return await apiClient.get('/health');
  },

  // Data endpoints
  async getDataSummary() {
    return await apiClient.get('/data/summary');
  },

  async getPriceSeries() {
    return await apiClient.get('/data/price-series');
  },

  // Event endpoints
  async getEventSummary() {
    return await apiClient.get('/events/summary');
  },

  // Model endpoints
  async getModelStatus() {
    return await apiClient.get('/model/status');
  },

  async getChangePoints() {
    return await apiClient.get('/model/changepoints');
  },

  async getEventCoefficients() {
    return await apiClient.get('/model/event-coefficients');
  },

  async getSegments() {
    return await apiClient.get('/model/segments');
  },

  async runModel() {
    return await apiClient.post('/model/run');
  },

  // Analysis endpoints
  async getCorrelationAnalysis() {
    return await apiClient.get('/analysis/correlation');
  },

  // Utility methods
  async checkConnection() {
    try {
      await this.getHealth();
      return true;
    } catch (error) {
      console.error('Connection check failed:', error);
      return false;
    }
  },

  // Error handling helper
  handleError(error) {
    console.error('API Service Error:', error);
    throw error;
  },
};

export default apiService; 
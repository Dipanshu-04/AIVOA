import axios from 'axios';

// Base URL defaults to the local FastAPI server port 8000.
// In a production environment, this should be set via process.env.REACT_APP_API_URL
const API_BASE_URL = 'http://localhost:8000/api';

/**
 * A configured Axios client instance to be used across the frontend application.
 * Centralizing this allows for easy implementation of auth interceptors later if needed.
 */
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor for global error logging
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

export default apiClient;

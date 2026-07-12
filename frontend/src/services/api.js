import axios from 'axios';

/**
 * Centered Axios Instance configuration
 * Connects to the Customer Segmentation System backend API.
 */
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request Interceptor
api.interceptors.request.use(
  (config) => {
    // Perform actions before request is sent (e.g., attach auth tokens if added in the future)
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    // Handle request errors
    return Promise.reject(error);
  }
);

// Response Interceptor
api.interceptors.response.use(
  (response) => {
    // Any status code that lies within the range of 2xx triggers this function
    return response;
  },
  (error) => {
    // Any status codes that falls outside the range of 2xx triggers this function
    // Centralized error logging and handling
    const customError = {
      message: error.message,
      status: error.response?.status,
      data: error.response?.data,
    };
    
    console.error('[API Service Error]:', customError);
    return Promise.reject(customError);
  }
);

export default api;

import axios from 'axios';

// Create axios instance with base configuration
const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add JWT token to headers
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('diabetesPredict_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle common errors
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.response?.status === 401) {
      // Token expired or invalid - clear token and redirect to login
      localStorage.removeItem('diabetesPredict_token');
      localStorage.removeItem('diabetesPredict_user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Authentication API functions
export const authAPI = {
  signup: (userData) => api.post('/auth/signup', userData),
  login: (email, password) => {
    const formData = new URLSearchParams();
    formData.append('username', email); // OAuth2 expects 'username' field
    formData.append('password', password);
    
    return api.post('/auth/login', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });
  },
  getCurrentUser: () => api.get('/auth/me'),
  logout: () => {
    localStorage.removeItem('diabetesPredict_token');
    localStorage.removeItem('diabetesPredict_user');
  },
};

// Generic API functions
export const apiHelpers = {
  // Handle API errors consistently
  handleError: (error) => {
    if (error.response) {
      // Server responded with error status
      const message = error.response.data?.detail || error.response.data?.message || 'An error occurred';
      return { success: false, message, status: error.response.status };
    } else if (error.request) {
      // Network error
      return { success: false, message: 'Network error. Please check your connection.' };
    } else {
      // Other error
      return { success: false, message: error.message || 'An unexpected error occurred' };
    }
  },

  // Handle API success responses
  handleSuccess: (response, successMessage = null) => {
    return {
      success: true,
      data: response.data,
      message: successMessage,
      status: response.status
    };
  }
};

export default api;

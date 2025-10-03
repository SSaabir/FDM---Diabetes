import axios from 'axios';

// Create axios instance with base configuration
const api = axios.create({
  baseURL: import.meta.env.RAILWAY_BACKEND || 'https://fdm-diabetes-production.up.railway.app',
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
    // Only auto-logout on 401 for specific auth endpoints, not all requests
    if (error.response?.status === 401) {
      const url = error.config?.url || '';
      
      // Only auto-logout for critical auth endpoints
      if (url.includes('/auth/me') || url.includes('/admin/me')) {
        console.warn('Authentication token invalid, redirecting to login');
        localStorage.removeItem('diabetesPredict_token');
        localStorage.removeItem('diabetesPredict_user_type');
        localStorage.removeItem('diabetesPredict_user_info');
        localStorage.removeItem('diabetesPredict_user');
        
        // Avoid infinite redirect loops
        if (!window.location.pathname.includes('/login')) {
          window.location.href = '/login';
        }
      }
      // For other 401 errors, just let the component handle them
    }
    return Promise.reject(error);
  }
);

// Authentication API functions
export const authAPI = {
  signup: (userData) => api.post('/auth/signup', userData),
  
  // Unified login for both users and admins
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
  
  // Get current user info (works for both users and admins)
  getCurrentUser: () => api.get('/auth/me'),
  
  // Get current admin info (admin-specific endpoint)
  getCurrentAdmin: () => api.get('/admin/me'),
  
  // Logout function
  logout: () => {
    localStorage.removeItem('diabetesPredict_token');
    localStorage.removeItem('diabetesPredict_user_type');
    localStorage.removeItem('diabetesPredict_user_info');
    localStorage.removeItem('diabetesPredict_user');
  },
};

// Prediction API functions
export const predictionAPI = {
  // Get diabetes risk prediction (try public endpoint first, then authenticated)
  predict: async (predictionData) => {
    try {
      // Try public endpoint first (higher rate limit, no auth required)
      return await api.post('/api/predict-public', predictionData);
    } catch (error) {
      if (error.response?.status === 429) {
        // If rate limited on public, try authenticated endpoint
        console.warn('Public endpoint rate limited, trying authenticated endpoint');
        return await api.post('/api/predict', predictionData);
      }
      throw error;
    }
  },
  
  // Validate prediction input
  validateInput: (predictionData) => api.post('/api/validate-input', predictionData),
  
  // Get model information
  getModelInfo: () => api.get('/api/model-info'),
};

// Chat AI API functions
export const chatAPI = {
  // Send message to AI chat
  sendMessage: (message, context = null) => api.post('/api/chat', { 
    message, 
    context 
  }),
  
  // Get conversation history
  getHistory: (limit = 10) => api.get(`/api/chat/history?limit=${limit}`),
  
  // Clear conversation history
  clearHistory: () => api.delete('/api/chat/history'),
  
  // Get suggested questions
  getSuggestions: () => api.get('/api/chat/suggestions'),
  
  // Get quick response (without saving to history)
  quickResponse: (message) => api.post('/api/chat/quick-response', null, {
    params: { message }
  }),
};

// Admin API functions
export const adminAPI = {
  // Get current admin info
  getCurrentAdmin: () => api.get('/admin/me'),
  
  // Create new admin (superadmin only)
  createAdmin: (adminData) => api.post('/admin/create-admin', adminData),
  
  // List all admins (superadmin only)
  listAdmins: () => api.get('/admin/list-admins'),
  
  // Delete admin (superadmin only)
  deleteAdmin: (adminId) => api.delete(`/admin/delete-admin/${adminId}`),
  
  // Get admin statistics
  getAdminStats: () => api.get('/admin/stats'),
};

// Profile API functions
export const profileAPI = {
  // Update user profile information
  updateProfile: (profileData) => api.put('/auth/profile', profileData),
  
  // Change user password
  changePassword: (passwordData) => api.put('/auth/change-password', passwordData),
  
  // Upload profile avatar
  uploadAvatar: (formData) => api.post('/auth/upload-avatar', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  }),
  
  // Delete profile avatar
  deleteAvatar: () => api.delete('/auth/avatar'),
  
  // Get user profile (detailed version)
  getProfile: () => api.get('/auth/profile'),
  
  // Update profile preferences
  updatePreferences: (preferences) => api.put('/auth/preferences', preferences),
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

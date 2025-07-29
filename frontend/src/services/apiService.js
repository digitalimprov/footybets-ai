import axios from 'axios';
import toast from 'react-hot-toast';

// API Configuration - Australian deployment
const API_CONFIG = {
  // Primary API base URL (Australian region)
  baseURL: process.env.NODE_ENV === 'production' 
    ? 'https://footybets-backend-818397187963.australia-southeast1.run.app/api'
    : 'http://localhost:8000/api',
  
  // Fallback URLs for high availability
  fallbackURLs: [
    'https://api.footybets.ai/api',
    'https://footybets-backend-818397187963.us-central1.run.app/api'
  ],
  
  timeout: 10000, // 10 seconds - good for Australian connectivity
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'X-Region': 'australia-southeast1',
    'X-Timezone': 'Australia/Sydney'
  }
};

// Create axios instance with Australian-optimized settings
const apiClient = axios.create(API_CONFIG);

// Request interceptor - add auth token and Australian locale
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('accessToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    
    // Add Australian locale and timezone
    config.headers['Accept-Language'] = 'en-AU';
    config.headers['X-User-Timezone'] = Intl.DateTimeFormat().resolvedOptions().timeZone || 'Australia/Sydney';
    
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor with Australian error handling
apiClient.interceptors.response.use(
  (response) => {
    return response;
  },
  async (error) => {
    const originalRequest = error.config;
    
    // Handle 401 errors (authentication)
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      // Clear invalid tokens
      localStorage.removeItem('accessToken');
      localStorage.removeItem('userData');
      
      // Redirect to login for Australian users
      if (window.location.pathname !== '/login') {
        toast.error('Session expired. Please log in again.');
        window.location.href = '/login';
      }
      
      return Promise.reject(error);
    }
    
    // Handle network errors with Australian context
    if (!error.response) {
      toast.error('Network error. Please check your internet connection.');
      console.error('Network Error:', error.message);
    }
    
    // Handle server errors with Australian support contact
    if (error.response?.status >= 500) {
      toast.error('Server error. Our Australian support team has been notified.');
      console.error('Server Error:', error.response);
  }
    
    return Promise.reject(error);
  }
);

// API service methods optimized for Australian AFL data
const apiService = {
  // Authentication endpoints
  auth: {
    login: (credentials) => apiClient.post('/auth/login', credentials),
    register: (userData) => apiClient.post('/auth/register', userData),
    logout: () => apiClient.post('/auth/logout'),
    refreshToken: () => apiClient.post('/auth/refresh'),
    forgotPassword: (email) => apiClient.post('/auth/forgot-password', { email }),
    resetPassword: (data) => apiClient.post('/auth/reset-password', data),
    verifyEmail: (token) => apiClient.post('/auth/verify-email', { token }),
    verifyToken: () => apiClient.get('/auth/verify-token')
  },

  // AFL predictions (Australian timezone optimized)
  predictions: {
    getAll: (params = {}) => apiClient.get('/predictions', { 
      params: { 
        ...params, 
        timezone: 'Australia/Sydney',
        currency: 'AUD'
      } 
    }),
    getById: (id) => apiClient.get(`/predictions/${id}`),
    create: (data) => apiClient.post('/predictions', data),
    update: (id, data) => apiClient.put(`/predictions/${id}`, data),
    delete: (id) => apiClient.delete(`/predictions/${id}`),
    generate: (gameData) => apiClient.post('/predictions/generate', gameData),
    updateAccuracy: (id, accuracy) => apiClient.put(`/predictions/${id}/accuracy`, { accuracy })
  },

  // AFL games and fixtures (Australian focused)
  games: {
    getAll: (params = {}) => apiClient.get('/games', { 
      params: { 
        ...params,
        timezone: 'Australia/Sydney'
      } 
    }),
    getById: (id) => apiClient.get(`/games/${id}`),
    getUpcoming: () => apiClient.get('/games/upcoming'),
    getByRound: (round, season) => apiClient.get(`/games/round/${round}`, { 
      params: { season, timezone: 'Australia/Sydney' } 
    }),
    getByTeam: (teamId) => apiClient.get(`/games/team/${teamId}`)
  },

  // Analytics with Australian market focus
  analytics: {
    getOverview: () => apiClient.get('/analytics/overview'),
    getPerformance: () => apiClient.get('/analytics/performance'),
    getAccuracy: () => apiClient.get('/analytics/accuracy'),
    getTrends: () => apiClient.get('/analytics/trends'),
    getTeamStats: (teamId) => apiClient.get(`/analytics/teams/${teamId}`),
    getMarketData: () => apiClient.get('/analytics/market', {
      params: { region: 'australia', currency: 'AUD' }
    })
  },

  // User management
  users: {
    getProfile: () => apiClient.get('/users/profile'),
    updateProfile: (data) => apiClient.put('/users/profile', data),
    changePassword: (data) => apiClient.put('/users/change-password', data),
    deleteAccount: () => apiClient.delete('/users/account'),
    getSubscription: () => apiClient.get('/users/subscription'),
    updateSubscription: (plan) => apiClient.put('/users/subscription', { plan })
  },

  // Admin endpoints (Australian region)
  admin: {
    getUsers: () => apiClient.get('/admin/users'),
    getSystemStats: () => apiClient.get('/admin/system-stats'),
    getSecurityLogs: () => apiClient.get('/admin/security-logs'),
    getContent: () => apiClient.get('/admin/content'),
    updateUser: (id, data) => apiClient.put(`/admin/users/${id}`, data),
    deleteUser: (id) => apiClient.delete(`/admin/users/${id}`),
    generateContent: (data) => apiClient.post('/admin/generate-content', data)
  },

  // Content and tips (Australian AFL focus)
  content: {
    getTips: (params = {}) => apiClient.get('/content/tips', { 
      params: { 
        ...params,
        region: 'australia',
        league: 'afl'
      } 
    }),
    getArticles: () => apiClient.get('/content/articles'),
    getById: (id) => apiClient.get(`/content/${id}`),
    create: (data) => apiClient.post('/content', data),
    update: (id, data) => apiClient.put(`/content/${id}`, data),
    delete: (id) => apiClient.delete(`/content/${id}`)
  },

  // Health check for Australian infrastructure
  health: () => apiClient.get('/health'),
  
  // Region-specific utilities
  utils: {
    getAustralianTime: () => apiClient.get('/utils/time/australia'),
    convertCurrency: (amount, from, to) => apiClient.get('/utils/currency/convert', {
      params: { amount, from, to }
    }),
    getAFLTeams: () => apiClient.get('/utils/afl/teams'),
    getAFLFixtures: (round, season) => apiClient.get('/utils/afl/fixtures', {
      params: { round, season }
    })
  }
};

export default apiService; 
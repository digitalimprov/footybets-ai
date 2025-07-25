import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';
import * as SecureStore from 'expo-secure-store';

const API_BASE_URL = process.env.EXPO_PUBLIC_API_URL || 'http://localhost:8000';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
api.interceptors.request.use(
  async (config) => {
    // Add auth token if available
    const token = await SecureStore.getItemAsync('authToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => {
    return response.data;
  },
  async (error) => {
    // Handle 401 errors by clearing auth token
    if (error.response?.status === 401) {
      await SecureStore.deleteItemAsync('authToken');
      // You might want to redirect to login here
    }
    throw error;
  }
);

export const apiService = {
  // Authentication
  login: async (credentials) => {
    return api.post('/api/auth/login', credentials);
  },

  register: async (userData) => {
    return api.post('/api/auth/register', userData);
  },

  logout: async () => {
    await SecureStore.deleteItemAsync('authToken');
    return api.post('/api/auth/logout');
  },

  // Games API
  getGames: async (params = {}) => {
    return api.get('/api/games', { params });
  },

  getUpcomingGames: async (days = 7) => {
    return api.get('/api/games/upcoming', { params: { days } });
  },

  getGame: async (gameId) => {
    return api.get(`/api/games/${gameId}`);
  },

  // Predictions API
  getPredictions: async (limit = 50, params = {}) => {
    return api.get('/api/predictions', { params: { limit, ...params } });
  },

  getUpcomingPredictions: async (days = 7) => {
    return api.get('/api/predictions/upcoming', { params: { days } });
  },

  getPrediction: async (predictionId) => {
    return api.get(`/api/predictions/${predictionId}`);
  },

  generatePredictions: async (days = 7) => {
    return api.post('/api/predictions/generate', null, { params: { days } });
  },

  updatePredictionAccuracy: async () => {
    return api.post('/api/predictions/update-accuracy');
  },

  // Analytics API
  getAnalyticsOverview: async (period = 'all', season = null) => {
    const params = { period };
    if (season) params.season = season;
    return api.get('/api/analytics/overview', { params });
  },

  getTeamPerformance: async (season = null, limit = 18) => {
    const params = { limit };
    if (season) params.season = season;
    return api.get('/api/analytics/team-performance', { params });
  },

  getPredictionTrends: async (days = 30) => {
    return api.get('/api/analytics/prediction-trends', { params: { days } });
  },

  generateAnalytics: async (periodType = 'weekly') => {
    return api.post('/api/analytics/generate-analytics', null, { params: { period_type: periodType } });
  },

  // Scraping API
  scrapeHistoricalData: async (startSeason = 2020, endSeason = 2024) => {
    return api.post('/api/scraping/historical-data', null, { 
      params: { start_season: startSeason, end_season: endSeason } 
    });
  },

  scrapeSeason: async (season = 2024) => {
    return api.post('/api/scraping/season', null, { params: { season } });
  },

  scrapeUpcomingGames: async () => {
    return api.post('/api/scraping/upcoming-games');
  },

  getScrapingStatus: async () => {
    return api.get('/api/scraping/status');
  },

  cleanupData: async () => {
    return api.post('/api/scraping/cleanup');
  },

  // Health check
  healthCheck: async () => {
    return api.get('/health');
  },

  // User tips (coming soon)
  submitUserTip: async (tipData) => {
    return api.post('/api/user-tips', tipData);
  },

  getUserTips: async (userId) => {
    return api.get(`/api/user-tips/user/${userId}`);
  },

  // Notifications
  registerForPushNotifications: async (expoPushToken) => {
    return api.post('/api/notifications/register', { token: expoPushToken });
  },

  updateNotificationSettings: async (settings) => {
    return api.put('/api/notifications/settings', settings);
  },
};

export default apiService; 
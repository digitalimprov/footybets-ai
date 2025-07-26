import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

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
  (config) => {
    // Add any auth tokens here if needed
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
  (error) => {
    console.error('API Error:', error);
    throw error;
  }
);

export const apiService = {
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

  getPredictionByGame: async (gameId) => {
    return api.get('/api/predictions', { params: { game_id: gameId } });
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

  // Content Management API
  getContent: async (params = {}) => {
    return api.get('/api/content', { params });
  },

  getFeaturedContent: async (limit = 5) => {
    return api.get('/api/content/featured', { params: { limit } });
  },

  getContentById: async (contentId) => {
    return api.get(`/api/content/${contentId}`);
  },

  getContentBySlug: async (slug) => {
    return api.get(`/api/content/slug/${slug}`);
  },

  generateContent: async (contentData) => {
    return api.post('/api/content/generate', contentData);
  },

  generateGameAnalysis: async (gameId) => {
    return api.post(`/api/content/generate/game-analysis/${gameId}`);
  },

  generateTeamPreview: async (teamId, season = 2024) => {
    return api.post(`/api/content/generate/team-preview/${teamId}`, null, { params: { season } });
  },

  updateContent: async (contentId, updates) => {
    return api.put(`/api/content/${contentId}`, updates);
  },

  publishContent: async (contentId) => {
    return api.post(`/api/content/${contentId}/publish`);
  },

  archiveContent: async (contentId) => {
    return api.post(`/api/content/${contentId}/archive`);
  },

  deleteContent: async (contentId) => {
    return api.delete(`/api/content/${contentId}`);
  },

  getContentTemplates: async () => {
    return api.get('/api/content/templates');
  },

  getContentAnalytics: async (contentId, period = 'daily') => {
    return api.get(`/api/content/${contentId}/analytics`, { params: { period } });
  },
};

export default apiService; 
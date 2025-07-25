import AsyncStorage from '@react-native-async-storage/async-storage';
import * as SecureStore from 'expo-secure-store';

// Storage keys
const STORAGE_KEYS = {
  USER_PREFERENCES: 'user_preferences',
  CACHED_PREDICTIONS: 'cached_predictions',
  CACHED_GAMES: 'cached_games',
  CACHED_ANALYTICS: 'cached_analytics',
  LAST_SYNC: 'last_sync',
  THEME: 'theme',
  NOTIFICATION_SETTINGS: 'notification_settings',
  OFFLINE_DATA: 'offline_data',
};

// Secure storage keys (for sensitive data)
const SECURE_KEYS = {
  AUTH_TOKEN: 'auth_token',
  REFRESH_TOKEN: 'refresh_token',
  USER_CREDENTIALS: 'user_credentials',
  BIOMETRIC_ENABLED: 'biometric_enabled',
};

export const storageService = {
  // AsyncStorage methods
  async setItem(key, value) {
    try {
      const jsonValue = JSON.stringify(value);
      await AsyncStorage.setItem(key, jsonValue);
    } catch (error) {
      console.error('Error saving data:', error);
    }
  },

  async getItem(key) {
    try {
      const jsonValue = await AsyncStorage.getItem(key);
      return jsonValue != null ? JSON.parse(jsonValue) : null;
    } catch (error) {
      console.error('Error reading data:', error);
      return null;
    }
  },

  async removeItem(key) {
    try {
      await AsyncStorage.removeItem(key);
    } catch (error) {
      console.error('Error removing data:', error);
    }
  },

  async clear() {
    try {
      await AsyncStorage.clear();
    } catch (error) {
      console.error('Error clearing data:', error);
    }
  },

  // Secure storage methods
  async setSecureItem(key, value) {
    try {
      const jsonValue = JSON.stringify(value);
      await SecureStore.setItemAsync(key, jsonValue);
    } catch (error) {
      console.error('Error saving secure data:', error);
    }
  },

  async getSecureItem(key) {
    try {
      const jsonValue = await SecureStore.getItemAsync(key);
      return jsonValue != null ? JSON.parse(jsonValue) : null;
    } catch (error) {
      console.error('Error reading secure data:', error);
      return null;
    }
  },

  async removeSecureItem(key) {
    try {
      await SecureStore.deleteItemAsync(key);
    } catch (error) {
      console.error('Error removing secure data:', error);
    }
  },

  // User preferences
  async saveUserPreferences(preferences) {
    await this.setItem(STORAGE_KEYS.USER_PREFERENCES, preferences);
  },

  async getUserPreferences() {
    return await this.getItem(STORAGE_KEYS.USER_PREFERENCES) || {};
  },

  // Cached data
  async cachePredictions(predictions) {
    await this.setItem(STORAGE_KEYS.CACHED_PREDICTIONS, {
      data: predictions,
      timestamp: Date.now(),
    });
  },

  async getCachedPredictions() {
    const cached = await this.getItem(STORAGE_KEYS.CACHED_PREDICTIONS);
    if (cached && Date.now() - cached.timestamp < 5 * 60 * 1000) { // 5 minutes
      return cached.data;
    }
    return null;
  },

  async cacheGames(games) {
    await this.setItem(STORAGE_KEYS.CACHED_GAMES, {
      data: games,
      timestamp: Date.now(),
    });
  },

  async getCachedGames() {
    const cached = await this.getItem(STORAGE_KEYS.CACHED_GAMES);
    if (cached && Date.now() - cached.timestamp < 10 * 60 * 1000) { // 10 minutes
      return cached.data;
    }
    return null;
  },

  async cacheAnalytics(analytics) {
    await this.setItem(STORAGE_KEYS.CACHED_ANALYTICS, {
      data: analytics,
      timestamp: Date.now(),
    });
  },

  async getCachedAnalytics() {
    const cached = await this.getItem(STORAGE_KEYS.CACHED_ANALYTICS);
    if (cached && Date.now() - cached.timestamp < 30 * 60 * 1000) { // 30 minutes
      return cached.data;
    }
    return null;
  },

  // Authentication
  async saveAuthToken(token) {
    await this.setSecureItem(SECURE_KEYS.AUTH_TOKEN, token);
  },

  async getAuthToken() {
    return await this.getSecureItem(SECURE_KEYS.AUTH_TOKEN);
  },

  async removeAuthToken() {
    await this.removeSecureItem(SECURE_KEYS.AUTH_TOKEN);
  },

  async saveRefreshToken(token) {
    await this.setSecureItem(SECURE_KEYS.REFRESH_TOKEN, token);
  },

  async getRefreshToken() {
    return await this.getSecureItem(SECURE_KEYS.REFRESH_TOKEN);
  },

  async removeRefreshToken() {
    await this.removeSecureItem(SECURE_KEYS.REFRESH_TOKEN);
  },

  // Theme
  async saveTheme(theme) {
    await this.setItem(STORAGE_KEYS.THEME, theme);
  },

  async getTheme() {
    return await this.getItem(STORAGE_KEYS.THEME) || 'light';
  },

  // Notification settings
  async saveNotificationSettings(settings) {
    await this.setItem(STORAGE_KEYS.NOTIFICATION_SETTINGS, settings);
  },

  async getNotificationSettings() {
    return await this.getItem(STORAGE_KEYS.NOTIFICATION_SETTINGS) || {
      predictions: true,
      gameResults: true,
      weeklySummary: true,
      sound: true,
      vibration: true,
    };
  },

  // Offline data
  async saveOfflineData(key, data) {
    const offlineData = await this.getItem(STORAGE_KEYS.OFFLINE_DATA) || {};
    offlineData[key] = {
      data,
      timestamp: Date.now(),
    };
    await this.setItem(STORAGE_KEYS.OFFLINE_DATA, offlineData);
  },

  async getOfflineData(key) {
    const offlineData = await this.getItem(STORAGE_KEYS.OFFLINE_DATA) || {};
    return offlineData[key]?.data || null;
  },

  async clearOfflineData() {
    await this.removeItem(STORAGE_KEYS.OFFLINE_DATA);
  },

  // Sync status
  async updateLastSync() {
    await this.setItem(STORAGE_KEYS.LAST_SYNC, Date.now());
  },

  async getLastSync() {
    return await this.getItem(STORAGE_KEYS.LAST_SYNC);
  },

  // Biometric settings
  async setBiometricEnabled(enabled) {
    await this.setSecureItem(SECURE_KEYS.BIOMETRIC_ENABLED, enabled);
  },

  async isBiometricEnabled() {
    return await this.getSecureItem(SECURE_KEYS.BIOMETRIC_ENABLED) || false;
  },

  // Clear all data (logout)
  async clearAllData() {
    try {
      await AsyncStorage.clear();
      await SecureStore.deleteItemAsync(SECURE_KEYS.AUTH_TOKEN);
      await SecureStore.deleteItemAsync(SECURE_KEYS.REFRESH_TOKEN);
      await SecureStore.deleteItemAsync(SECURE_KEYS.USER_CREDENTIALS);
    } catch (error) {
      console.error('Error clearing all data:', error);
    }
  },
};

// Load stored data on app startup
export const loadStoredData = async () => {
  try {
    // Load user preferences
    const preferences = await storageService.getUserPreferences();
    
    // Load cached data
    const cachedPredictions = await storageService.getCachedPredictions();
    const cachedGames = await storageService.getCachedGames();
    const cachedAnalytics = await storageService.getCachedAnalytics();
    
    // Load theme
    const theme = await storageService.getTheme();
    
    // Load notification settings
    const notificationSettings = await storageService.getNotificationSettings();
    
    return {
      preferences,
      cachedPredictions,
      cachedGames,
      cachedAnalytics,
      theme,
      notificationSettings,
    };
  } catch (error) {
    console.error('Error loading stored data:', error);
    return {};
  }
}; 
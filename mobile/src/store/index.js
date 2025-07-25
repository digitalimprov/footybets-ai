import { configureStore } from '@reduxjs/toolkit';
import { persistStore, persistReducer } from 'redux-persist';
import AsyncStorage from '@react-native-async-storage/async-storage';

import predictionsReducer from './slices/predictionsSlice';
import gamesReducer from './slices/gamesSlice';
import analyticsReducer from './slices/analyticsSlice';
import authReducer from './slices/authSlice';
import notificationsReducer from './slices/notificationsSlice';

const persistConfig = {
  key: 'root',
  storage: AsyncStorage,
  whitelist: ['auth', 'predictions', 'games'], // Only persist these reducers
};

const persistedAuthReducer = persistReducer(persistConfig, authReducer);
const persistedPredictionsReducer = persistReducer(
  { ...persistConfig, key: 'predictions' },
  predictionsReducer
);
const persistedGamesReducer = persistReducer(
  { ...persistConfig, key: 'games' },
  gamesReducer
);

export const store = configureStore({
  reducer: {
    auth: persistedAuthReducer,
    predictions: persistedPredictionsReducer,
    games: persistedGamesReducer,
    analytics: analyticsReducer,
    notifications: notificationsReducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: {
        ignoredActions: ['persist/PERSIST', 'persist/REHYDRATE'],
      },
    }),
});

export const persistor = persistStore(store); 
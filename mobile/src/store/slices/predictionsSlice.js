import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { apiService } from '../../services/apiService';

// Async thunks
export const fetchPredictions = createAsyncThunk(
  'predictions/fetchPredictions',
  async (params = {}) => {
    const response = await apiService.getPredictions(50, params);
    return response;
  }
);

export const fetchUpcomingPredictions = createAsyncThunk(
  'predictions/fetchUpcomingPredictions',
  async (days = 7) => {
    const response = await apiService.getUpcomingPredictions(days);
    return response;
  }
);

export const generatePredictions = createAsyncThunk(
  'predictions/generatePredictions',
  async (days = 7) => {
    const response = await apiService.generatePredictions(days);
    return response;
  }
);

export const updatePredictionAccuracy = createAsyncThunk(
  'predictions/updateAccuracy',
  async () => {
    const response = await apiService.updatePredictionAccuracy();
    return response;
  }
);

const initialState = {
  predictions: [],
  upcomingPredictions: [],
  loading: false,
  error: null,
  lastUpdated: null,
  generating: false,
};

const predictionsSlice = createSlice({
  name: 'predictions',
  initialState,
  reducers: {
    clearPredictions: (state) => {
      state.predictions = [];
      state.upcomingPredictions = [];
    },
    setLoading: (state, action) => {
      state.loading = action.payload;
    },
    setError: (state, action) => {
      state.error = action.payload;
    },
    updatePrediction: (state, action) => {
      const { id, updates } = action.payload;
      const prediction = state.predictions.find(p => p.id === id);
      if (prediction) {
        Object.assign(prediction, updates);
      }
    },
  },
  extraReducers: (builder) => {
    builder
      // Fetch predictions
      .addCase(fetchPredictions.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchPredictions.fulfilled, (state, action) => {
        state.loading = false;
        state.predictions = action.payload;
        state.lastUpdated = new Date().toISOString();
      })
      .addCase(fetchPredictions.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message;
      })
      // Fetch upcoming predictions
      .addCase(fetchUpcomingPredictions.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchUpcomingPredictions.fulfilled, (state, action) => {
        state.loading = false;
        state.upcomingPredictions = action.payload;
      })
      .addCase(fetchUpcomingPredictions.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message;
      })
      // Generate predictions
      .addCase(generatePredictions.pending, (state) => {
        state.generating = true;
        state.error = null;
      })
      .addCase(generatePredictions.fulfilled, (state, action) => {
        state.generating = false;
        // Refresh predictions after generation
        state.lastUpdated = new Date().toISOString();
      })
      .addCase(generatePredictions.rejected, (state, action) => {
        state.generating = false;
        state.error = action.error.message;
      })
      // Update accuracy
      .addCase(updatePredictionAccuracy.fulfilled, (state) => {
        state.lastUpdated = new Date().toISOString();
      });
  },
});

export const {
  clearPredictions,
  setLoading,
  setError,
  updatePrediction,
} = predictionsSlice.actions;

export default predictionsSlice.reducer; 
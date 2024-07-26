
import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import axios from 'axios';

export const checkSyncStatus = createAsyncThunk(
  'sync/checkStatus',
  async ({ taskId }, { getState, rejectWithValue }) => {
    try {
      const { sync } = getState();
      console.log(`Checking sync status for task ${taskId}. Current state:`, sync);
      const response = await axios.get(`/api/scraper/status/?task_id=${taskId}`);
      console.log('Sync status API response:', response.data);
      return response.data;
    } catch (err) {
      console.error('Sync status check failed:', err);
      return rejectWithValue(err.response?.data || err.message);
    }
  }
);

const initialState = {
  syncStatus: 'idle',
  progress: 0,
  taskId: null,
  error: null,
  totalItems: null,
  currentItem: 0,
  userId: null,
  currentVehicle: null,
};


export const syncSlice = createSlice({
  name: 'sync',
  initialState,
  reducers: {
    setSyncStatus: (state, action) => {
      state.syncStatus = action.payload;
    },
    setProgress: (state, action) => {
      state.progress = action.payload;
    },
    setTaskId: (state, action) => {
      state.taskId = action.payload;
    },
    setError: (state, action) => {
      state.error = action.payload;
    },
    resetSync: (state) => {
      state.syncStatus = 'idle';
      state.progress = 0;
      state.taskId = null;
      state.error = null;
      state.totalItems = null;
      state.currentItem = 0;
      state.currentVehicle = null;
    },
    setUserId: (state, action) => {
      state.userId = action.payload;
    },
    clearUserState: (state) => {
      state.userId = null;
      state.taskId = null;
      state.syncStatus = 'idle';
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(checkSyncStatus.pending, (state) => {
        console.log('Sync status check pending');
        state.syncStatus = 'checking';
      })
      .addCase(checkSyncStatus.fulfilled, (state, action) => {
        console.log('Sync status check fulfilled:', action.payload);
        if (action.payload.userId && action.payload.userId !== state.userId) {
          console.log('Ignoring update for different user');
          return;
        }
        if (action.payload.state === 'SUCCESS') {
          state.syncStatus = 'completed';
          state.progress = 100;
          state.currentVehicle = null;
        } else if (action.payload.state === 'FAILURE') {
          state.syncStatus = 'error';
          state.error = 'Sync failed. Please try again.';
          state.currentVehicle = null;
        } else if (action.payload.state === 'PROGRESS') {
          state.syncStatus = 'syncing';
          state.totalItems = action.payload.total;
          state.currentItem = action.payload.current;
          state.currentVehicle = action.payload.currentVehicle || null;
          if (state.totalItems && state.totalItems !== 'unknown') {
            state.progress = Math.round((state.currentItem / state.totalItems) * 100);
          } else {
            state.progress = 0;
          }
        }
      })
      .addCase(checkSyncStatus.rejected, (state, action) => {
        console.log('Sync status check rejected:', action.error);
        state.syncStatus = 'error';
        state.error = action.error.message || 'Failed to check sync status';
        state.currentVehicle = null;
      });
  },
});


export const { setSyncStatus, setProgress, setTaskId, setError, resetSync, setUserId, clearUserState } = syncSlice.actions;

export default syncSlice.reducer;

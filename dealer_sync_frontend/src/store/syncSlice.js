import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import axios from 'axios';

export const checkSyncStatus = createAsyncThunk(
  'sync/checkStatus',
  async ({ taskId, userId }, { rejectWithValue }) => {
    try {
      const response = await axios.get(`http://localhost:8000/api/scraper/status/?task_id=${taskId}`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('access_token')}`
        }
      });
      return { ...response.data, userId };
    } catch (err) {
      return rejectWithValue(err.response.data);
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
    },
    setUserId: (state, action) => {
      state.userId = action.payload;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(checkSyncStatus.pending, (state) => {
        state.syncStatus = 'checking';
      })
      .addCase(checkSyncStatus.fulfilled, (state, action) => {
        if (action.payload.userId !== state.userId) {
          return; // Ignore updates for other users
        }
        if (action.payload.state === 'SUCCESS') {
          state.syncStatus = 'completed';
          state.progress = 100;
        } else if (action.payload.state === 'FAILURE') {
          state.syncStatus = 'error';
          state.error = 'Sync failed. Please try again.';
        } else if (action.payload.state === 'PROGRESS') {
          state.syncStatus = 'syncing';
          state.totalItems = action.payload.total || state.totalItems;
          state.currentItem = action.payload.current;
          if (state.totalItems) {
            state.progress = Math.round((state.currentItem / state.totalItems) * 100);
          }
        }
      })
      .addCase(checkSyncStatus.rejected, (state, action) => {
        state.syncStatus = 'error';
        state.error = action.payload || 'Failed to check sync status';
      });
  },
});

export const { setSyncStatus, setProgress, setTaskId, setError, resetSync, setUserId } = syncSlice.actions;

export default syncSlice.reducer;

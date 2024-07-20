import { configureStore } from '@reduxjs/toolkit';
import syncReducer from './syncSlice';

export const store = configureStore({
  reducer: {
    sync: syncReducer,
  },
});

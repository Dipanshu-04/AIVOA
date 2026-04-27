import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface UiState {
  isLoading: boolean;
  error: string | null;
}

const initialState: UiState = {
  isLoading: false,
  error: null,
};

const uiSlice = createSlice({
  name: 'ui',
  initialState,
  reducers: {
    // Toggles the loading overlay when waiting for the backend
    setLoading(state, action: PayloadAction<boolean>) {
      state.isLoading = action.payload;
      if (action.payload) {
        state.error = null; // Clear old errors when starting a new request
      }
    },
    // Sets an error message to be displayed in a banner
    setError(state, action: PayloadAction<string | null>) {
      state.error = action.payload;
      state.isLoading = false;
    }
  }
});

export const { setLoading, setError } = uiSlice.actions;
export default uiSlice.reducer;

// ---
// Explanation:
// `uiSlice` separates transient UI states (like loaders and error messages) 
// from actual domain data, making the app easier to debug and test.

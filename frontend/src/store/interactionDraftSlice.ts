import { createSlice, PayloadAction } from '@reduxjs/toolkit';

export interface InteractionDraftState {
  draft: Record<string, any>;
  missingFields: string[];
  uncertainFields: string[];
}

const initialState: InteractionDraftState = {
  draft: {},
  missingFields: [],
  uncertainFields: []
};

const interactionDraftSlice = createSlice({
  name: 'interactionDraft',
  initialState,
  reducers: {
    // Overwrites the entire draft state with the deterministic UI payload returned from the backend LangGraph
    setDraftState(state, action: PayloadAction<InteractionDraftState>) {
      state.draft = action.payload.draft || {};
      state.missingFields = action.payload.missingFields || [];
      state.uncertainFields = action.payload.uncertainFields || [];
    },
    clearDraft(state) {
      state.draft = {};
      state.missingFields = [];
      state.uncertainFields = [];
    }
  }
});

export const { setDraftState, clearDraft } = interactionDraftSlice.actions;
export default interactionDraftSlice.reducer;

// ---
// Explanation:
// `interactionDraftSlice` holds the structured JSON extracted by the AI. It guarantees 
// that the form on the left pane exactly mirrors what the backend considers to be the current state.

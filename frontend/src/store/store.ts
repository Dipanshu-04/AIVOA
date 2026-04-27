import { configureStore } from '@reduxjs/toolkit';
import chatReducer from './chatSlice';
import interactionDraftReducer from './interactionDraftSlice';
import uiReducer from './uiSlice';

export const store = configureStore({
  reducer: {
    chat: chatReducer,
    interaction: interactionDraftReducer,
    ui: uiReducer,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;

// ---
// Explanation:
// `store.ts` initializes the Redux store by combining the slices. 
//
// Data Flow (Chat to Form):
// 1. User types natural language in the Chat pane and hits Send.
// 2. The React frontend dispatches `setLoading(true)` and calls the backend `/chat` API.
// 3. The backend LangGraph agent extracts entities and returns an updated `ui_payload`.
// 4. The frontend receives the response, dispatches `setLoading(false)`, and dispatches 
//    `setDraftState` with the new JSON.
// 5. The Left pane (read-only form) re-renders instantly by selecting `state.interaction.draft` 
//    from Redux, providing the user with real-time visual feedback of what the AI extracted.

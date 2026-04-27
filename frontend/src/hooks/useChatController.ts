import { useCallback } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { RootState } from '../store/store';
import { addMessage } from '../store/chatSlice';
import { setDraftState } from '../store/interactionDraftSlice';
import { setLoading, setError } from '../store/uiSlice';
import { sendChatMessage } from '../api/chatApi';

/**
 * A custom hook that orchestrates the data flow between the Chat UI, 
 * the Redux store, and the backend FastAPI service.
 */
export const useChatController = () => {
  const dispatch = useDispatch();
  const currentDraft = useSelector((state: RootState) => state.interaction.draft);

  const sendMessage = useCallback(async (text: string) => {
    // 1. Instantly render user message in UI for a snappy UX
    dispatch(addMessage({
      id: Date.now().toString(),
      sender: 'user',
      text,
      timestamp: new Date().toISOString()
    }));

    dispatch(setLoading(true));
    dispatch(setError(null));

    try {
      // 2. Transmit to backend
      const response = await sendChatMessage({
        message: text,
        // Pass the full draft so the backend LLM has the exact same state the UI does
        current_draft: currentDraft, 
      });

      // 3. Render agent's textual reply
      dispatch(addMessage({
        id: (Date.now() + 1).toString(),
        sender: 'agent',
        text: response.reply,
        timestamp: new Date().toISOString()
      }));

      // 4. Update the read-only form state instantly
      if (response.interaction_draft) {
        // Handle variations in how the backend structures the payload
        const draftObj = response.interaction_draft.draft_interaction || response.interaction_draft;
        const missing = response.interaction_draft.missing_fields || [];
        const uncertain = response.interaction_draft.uncertain_fields || [];
        
        dispatch(setDraftState({
          draft: draftObj,
          missingFields: missing,
          uncertainFields: uncertain
        }));
      }

    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || err.message || 'Failed to communicate with agent.';
      dispatch(setError(errorMessage));
    } finally {
      dispatch(setLoading(false));
    }
  }, [dispatch, currentDraft]);

  return { sendMessage };
};

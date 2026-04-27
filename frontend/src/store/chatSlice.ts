import { createSlice, PayloadAction } from '@reduxjs/toolkit';

export interface ChatMessage {
  id: string;
  sender: 'user' | 'agent';
  text: string;
  timestamp: string;
}

interface ChatState {
  messages: ChatMessage[];
}

const initialState: ChatState = {
  messages: [
    {
      id: 'welcome-1',
      sender: 'agent',
      text: 'Hello! I am your AI assistant. How can I help you log an interaction today?',
      timestamp: new Date().toISOString()
    }
  ],
};

const chatSlice = createSlice({
  name: 'chat',
  initialState,
  reducers: {
    // Add a single message to the chat history
    addMessage(state, action: PayloadAction<ChatMessage>) {
      state.messages.push(action.payload);
    },
    // Used to clear chat on new session
    clearMessages(state) {
      state.messages = initialState.messages;
    }
  }
});

export const { addMessage, clearMessages } = chatSlice.actions;
export default chatSlice.reducer;

// ---
// Explanation:
// `chatSlice` manages the conversational history. The chat drives the form; this slice 
// simply displays what the user and the LLM have said so far.

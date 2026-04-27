import React from 'react';
import { render, screen } from '@testing-library/react';
import { Provider } from 'react-redux';
import { configureStore } from '@reduxjs/toolkit';
import AssistantChat from '../components/AssistantChat';
import InteractionForm from '../components/InteractionForm';
import chatReducer from '../store/chatSlice';
import interactionDraftReducer, { setDraftState } from '../store/interactionDraftSlice';
import uiReducer, { setConfirmationRequired } from '../store/uiSlice';

// A lightweight mock store for testing Redux integration
const createTestStore = () => configureStore({
  reducer: {
    chat: chatReducer,
    interaction: interactionDraftReducer,
    ui: uiReducer,
  }
});

// Mock the API hook to avoid real network calls
jest.mock('../hooks/useChatController', () => ({
  useChatController: () => ({
    sendMessage: jest.fn(),
  })
}));

describe('Chat and UI Integration Flow', () => {
  it('renders chat interface correctly', () => {
    const store = createTestStore();
    render(
      <Provider store={store}>
        <AssistantChat />
      </Provider>
    );
    expect(screen.getByPlaceholderText(/describe/i)).toBeInTheDocument();
  });

  it('displays confirmation dialog when requiresConfirmation is true', () => {
    const store = createTestStore();
    store.dispatch(setConfirmationRequired({ required: true, prompt: 'Are you sure you want to save?' }));
    
    render(
      <Provider store={store}>
        <AssistantChat />
      </Provider>
    );
    
    expect(screen.getByText(/Are you sure you want to save/i)).toBeInTheDocument();
    expect(screen.getByText(/Confirm/i)).toBeInTheDocument();
    expect(screen.getByText(/Cancel/i)).toBeInTheDocument();
  });

  it('updates read-only form when draft state changes', () => {
    const store = createTestStore();
    // Simulate backend response updating the draft
    store.dispatch(setDraftState({
      draft: { hcp_name: 'Dr. Sarah Smith', interaction_type: 'In-person' },
      missingFields: ['sentiment'],
      uncertainFields: []
    }));

    render(
      <Provider store={store}>
        <InteractionForm />
      </Provider>
    );

    // Check if the form reflects the Redux state
    expect(screen.getByText('Dr. Sarah Smith')).toBeInTheDocument();
    expect(screen.getByText('In-person')).toBeInTheDocument();
  });
});

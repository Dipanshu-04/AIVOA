import React from 'react';
import Layout from './components/Layout';
import InteractionForm from './components/InteractionForm';
import AssistantChat from './components/AssistantChat';

const App: React.FC = () => {
  return (
    <Layout 
      formPaneContent={<InteractionForm />} 
      chatPaneContent={<AssistantChat />} 
    />
  );
};

export default App;

// ---
// Explanation:
// `App.tsx` wires the layout components together and hooks into the Redux state to display 
// conditional UI states such as loading overlays, error banners, and confirmation dialogs.

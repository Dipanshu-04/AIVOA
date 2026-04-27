import React, { ReactNode } from 'react';

interface LayoutProps {
  formPaneContent: ReactNode;
  chatPaneContent: ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ formPaneContent, chatPaneContent }) => {
  return (
    <div className="app-container">
      <header className="app-header">
        Log HCP Interaction
      </header>
      
      <main className="main-layout">
        {/* Left Pane: Read-Only Interaction Form */}
        <section className="form-pane">
          <div className="form-header">Interaction Details</div>
          
          {/* 
            A wrapper to enforce the read-only constraint functionally.
            Setting pointer-events to none prevents the user from clicking into, 
            focusing, or typing in any standard form inputs rendered within.
          */}
          <div style={{ pointerEvents: 'none', opacity: 0.95 }}>
            {formPaneContent}
          </div>
        </section>

        {/* Right Pane: AI Assistant Chat */}
        <section className="chat-pane">
          <div className="chat-header">
            <span role="img" aria-label="robot">🤖</span> AI Assistant
          </div>
          {chatPaneContent}
        </section>
      </main>
    </div>
  );
};

export default Layout;

// ---
// Explanation:
// `Layout.tsx` defines the core split-pane shell as requested. It enforces the read-only requirement 
// on the left pane using CSS (`pointerEvents: 'none'`), ensuring users cannot manually 
// fill out the form, effectively driving all interaction through the chat pane on the right.

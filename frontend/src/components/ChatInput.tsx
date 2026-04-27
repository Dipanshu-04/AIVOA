import React, { useState, useRef, useEffect, KeyboardEvent } from 'react';

interface ChatInputProps {
  onSendMessage: (text: string) => void;
  isLoading: boolean;
  showLogButton?: boolean;
}

const ChatInput: React.FC<ChatInputProps> = ({ onSendMessage, isLoading, showLogButton = false }) => {
  const [inputValue, setInputValue] = useState('');
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const adjustHeight = () => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 150)}px`;
    }
  };

  useEffect(() => {
    adjustHeight();
  }, [inputValue]);

  const handleSend = () => {
    if (inputValue.trim() && !isLoading) {
      onSendMessage(inputValue.trim());
      setInputValue('');
      if (textareaRef.current) {
        textareaRef.current.style.height = 'auto';
      }
    }
  };

  const handleLogClick = () => {
    if (!isLoading) {
      onSendMessage("Yes, log it.");
      setInputValue('');
    }
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div style={{ position: 'relative', marginTop: '16px' }}>
      {showLogButton && (
        <button
          onClick={handleLogClick}
          disabled={isLoading}
          style={{
            position: 'absolute',
            bottom: '100%',
            right: '0',
            marginBottom: '12px',
            padding: '10px 20px',
            backgroundColor: '#10b981',
            color: 'white',
            border: 'none',
            borderRadius: '24px',
            cursor: isLoading ? 'not-allowed' : 'pointer',
            fontWeight: 600,
            boxShadow: '0 4px 6px -1px rgba(16, 185, 129, 0.4), 0 2px 4px -1px rgba(16, 185, 129, 0.2)',
            transition: 'all 0.2s ease',
            zIndex: 10
          }}
        >
          ✓ Log Interaction
        </button>
      )}
      <div className="chat-input-area" style={{ display: 'flex', gap: '12px', alignItems: 'flex-end' }}>
        <textarea 
          ref={textareaRef}
          placeholder="Type here to log details (e.g. 'Met Dr. Smith...')" 
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyDown={handleKeyDown}
          disabled={isLoading}
          rows={1}
          style={{ 
            flex: 1, 
            padding: '12px 16px', 
            borderRadius: '24px', 
            border: '1px solid #cbd5e1', 
            outline: 'none', 
            fontFamily: 'inherit',
            fontSize: '0.95rem',
            backgroundColor: isLoading ? '#f8fafc' : '#ffffff',
            resize: 'none',
            overflowY: 'auto',
            maxHeight: '150px',
            lineHeight: '1.5'
          }}
        />
        <button 
          onClick={handleSend}
          disabled={isLoading || !inputValue.trim()}
          style={{ 
            padding: '12px 24px', 
            height: '48px', // Matches the default single-line height of the textarea
            backgroundColor: (isLoading || !inputValue.trim()) ? '#94a3b8' : '#3b82f6', 
            color: 'white', 
            border: 'none', 
            borderRadius: '24px', 
            cursor: (isLoading || !inputValue.trim()) ? 'not-allowed' : 'pointer', 
            fontWeight: 600,
            transition: 'background-color 0.2s',
            whiteSpace: 'nowrap'
          }}
        >
          Send
        </button>
      </div>
    </div>
  );
};

export default ChatInput;

// ---
// Explanation:
// `ChatInput` provides the text input field and submit button. It restricts submission when 
// empty or when the app is in a loading state, ensuring the user doesn't spam the API 
// while the LangGraph agent is processing a turn.

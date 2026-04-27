import React, { useRef, useEffect } from 'react';
import { useSelector } from 'react-redux';
import { RootState } from '../store/store';
import { useChatController } from '../hooks/useChatController';
import ChatMessage from './ChatMessage';
import ChatInput from './ChatInput';

const AssistantChat: React.FC = () => {
  const { sendMessage } = useChatController();
  const messages = useSelector((state: RootState) => state.chat.messages);
  const { isLoading, error } = useSelector((state: RootState) => state.ui);
  const { draft, missingFields } = useSelector((state: RootState) => state.interaction);
  
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  const handleSendMessage = (text: string) => {
    sendMessage(text);
  };

  const showLogButton = !!draft.hcp_name && missingFields.length === 0 && !draft.id;

  return (
    <>
      <div className="chat-messages" style={{ display: 'flex', flexDirection: 'column' }}>
        {messages.map((msg) => (
          <ChatMessage 
            key={msg.id} 
            sender={msg.sender} 
            text={msg.text} 
            timestamp={msg.timestamp} 
          />
        ))}

        {isLoading && (
          <div style={{ display: 'flex', gap: '8px', alignItems: 'center', margin: '16px 0', color: '#64748b', fontSize: '0.9rem' }}>
            <span>Agent is typing...</span>
          </div>
        )}

        {error && (
          <div className="error-banner">
            <strong>Error:</strong> {error}
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      <ChatInput onSendMessage={handleSendMessage} isLoading={isLoading} showLogButton={showLogButton} />
    </>
  );
};

export default AssistantChat;

// ---
// Explanation:
// `AssistantChat` orchestrates the right-hand panel. It ties `ChatInput` and `ChatMessage` 
// together with Redux state. It includes auto-scrolling to the newest message.

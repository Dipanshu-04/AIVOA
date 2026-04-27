import React from 'react';

interface ChatMessageProps {
  sender: 'user' | 'agent';
  text: string;
  timestamp: string;
}

const ChatMessage: React.FC<ChatMessageProps> = ({ sender, text, timestamp }) => {
  const isUser = sender === 'user';
  
  // Format the time gracefully (e.g., "14:30")
  const formattedTime = new Date(timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

  // Render markdown-style bold text (**text**)
  const renderText = (content: string) => {
    const parts = content.split(/(\*\*.*?\*\*)/g);
    return parts.map((part, index) => {
      if (part.startsWith('**') && part.endsWith('**') && part.length > 4) {
        return <strong key={index}>{part.slice(2, -2)}</strong>;
      }
      return <React.Fragment key={index}>{part}</React.Fragment>;
    });
  };

  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      alignItems: isUser ? 'flex-end' : 'flex-start',
      marginBottom: '8px',
      width: '100%'
    }}>
      <div style={{
        maxWidth: '85%',
        padding: '12px 16px',
        borderRadius: isUser ? '16px 16px 0 16px' : '16px 16px 16px 0',
        backgroundColor: isUser ? '#3b82f6' : '#ffffff',
        color: isUser ? '#ffffff' : '#1e293b',
        boxShadow: isUser ? 'none' : '0 1px 2px rgba(0,0,0,0.05)',
        border: isUser ? 'none' : '1px solid #e2e8f0',
        lineHeight: 1.5,
        fontSize: '0.95rem',
        whiteSpace: 'pre-wrap'
      }}>
        {renderText(text)}
      </div>
      <span style={{ 
        fontSize: '0.7rem', 
        color: '#94a3b8', 
        marginTop: '4px',
        padding: '0 4px'
      }}>
        {isUser ? 'You' : 'AI Assistant'} • {formattedTime}
      </span>
    </div>
  );
};

export default ChatMessage;

// ---
// Explanation:
// `ChatMessage` handles the visual display of individual bubbles in the chat.
// It differentiates between user (blue, right-aligned) and agent (white, left-aligned) messages,
// creating a familiar and clean conversational UI.

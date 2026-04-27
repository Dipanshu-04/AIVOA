import React from 'react';

interface SentimentSelectorViewProps {
  sentiment: string | null | undefined;
}

const SentimentSelectorView: React.FC<SentimentSelectorViewProps> = ({ sentiment }) => {
  const options = ['Positive', 'Neutral', 'Negative'];
  const normalizedSentiment = sentiment ? sentiment.toLowerCase() : null;

  return (
    <div style={{ marginBottom: '16px' }}>
      <label style={{ display: 'block', fontSize: '0.875rem', fontWeight: 600, color: '#475569', marginBottom: '8px' }}>
        Observed/Inferred HCP Sentiment
      </label>
      <div style={{ display: 'flex', gap: '16px' }}>
        {options.map((opt) => {
          const isSelected = normalizedSentiment === opt.toLowerCase();
          return (
            <div 
              key={opt}
              style={{
                padding: '6px 16px',
                borderRadius: '16px',
                border: `1px solid ${isSelected ? '#3b82f6' : '#e2e8f0'}`,
                backgroundColor: isSelected ? '#eff6ff' : '#f8fafc',
                color: isSelected ? '#1d4ed8' : '#64748b',
                fontWeight: isSelected ? 600 : 400,
                display: 'flex',
                alignItems: 'center',
                gap: '6px',
                transition: 'all 0.2s ease-in-out'
              }}
            >
              <span style={{ 
                width: '12px', 
                height: '12px', 
                borderRadius: '50%', 
                backgroundColor: isSelected ? '#3b82f6' : 'transparent',
                border: `1px solid ${isSelected ? '#3b82f6' : '#94a3b8'}`,
                display: 'inline-block'
              }} />
              {opt}
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default SentimentSelectorView;

// ---
// Explanation:
// `SentimentSelectorView` provides a clean, read-only visualization of the sentiment analysis 
// performed by the AI. It simulates the look of a segmented control or radio buttons, but 
// remains strictly read-only to adhere to the chat-first architecture requirement.

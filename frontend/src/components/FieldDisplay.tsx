import React from 'react';

interface FieldDisplayProps {
  label: string;
  value: string | string[] | null | undefined;
  isMissing: boolean;
  isUncertain: boolean;
}

const FieldDisplay: React.FC<FieldDisplayProps> = ({ label, value, isMissing, isUncertain }) => {
  const isEmpty = !value || (Array.isArray(value) && value.length === 0);
  
  let statusColor = 'transparent';
  let statusText = '';
  let borderStyle = '1px solid #e2e8f0';

  if (isMissing) {
    statusColor = '#fef2f2'; // light red background
    borderStyle = '1px solid #ef4444'; // red border
    statusText = 'Required by AI';
  } else if (isUncertain) {
    statusColor = '#fffbeb'; // light amber background
    borderStyle = '1px solid #f59e0b'; // amber border
    statusText = 'Please clarify in chat';
  } else if (!isEmpty) {
    statusColor = '#f0fdf4'; // light green background
    borderStyle = '1px solid #10b981'; // green border
    statusText = '';
  }

  const renderValue = () => {
    if (isEmpty) return <span style={{ color: '#94a3b8', fontStyle: 'italic' }}>Pending...</span>;
    if (Array.isArray(value)) {
      return (
        <ul style={{ margin: 0, paddingLeft: '20px' }}>
          {value.map((item, idx) => <li key={idx}>{item}</li>)}
        </ul>
      );
    }
    return <span>{value}</span>;
  };

  return (
    <div style={{ marginBottom: '16px' }}>
      <label style={{ display: 'block', fontSize: '0.875rem', fontWeight: 600, color: '#475569', marginBottom: '4px' }}>
        {label}
      </label>
      <div style={{ 
        padding: '10px 12px', 
        backgroundColor: statusColor, 
        border: borderStyle,
        borderRadius: '6px',
        minHeight: '42px',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        position: 'relative',
        transition: 'all 0.2s ease-in-out'
      }}>
        {renderValue()}
        
        {statusText && (
          <span style={{ 
            position: 'absolute', 
            top: '-10px', 
            right: '10px', 
            backgroundColor: 'white', 
            fontSize: '0.65rem', 
            padding: '0 4px',
            color: isMissing ? '#ef4444' : isUncertain ? '#f59e0b' : '#10b981',
            fontWeight: 600,
            borderRadius: '4px'
          }}>
            {statusText}
          </span>
        )}
      </div>
    </div>
  );
};

export default FieldDisplay;

// ---
// Explanation:
// `FieldDisplay` is a highly reusable component that visually renders the state of extracted data.
// It uses color-coded borders and badges (Green = Extracted, Red = Missing, Amber = Uncertain) 
// to instantly convey what the AI agent knows and what it needs, without allowing the user to click and type.

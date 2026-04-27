import React from 'react';
import { useSelector } from 'react-redux';
import { RootState } from '../store/store';
import FieldDisplay from './FieldDisplay';
import SentimentSelectorView from './SentimentSelectorView';

const InteractionForm: React.FC = () => {
  // Bind directly to the deterministic UI payload stored in Redux
  const { draft, missingFields, uncertainFields } = useSelector((state: RootState) => state.interaction);

  const isMissing = (field: string) => missingFields.includes(field);
  const isUncertain = (field: string) => uncertainFields.includes(field);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
      
      <div style={{ display: 'flex', gap: '16px' }}>
        <div style={{ flex: 1 }}>
          <FieldDisplay 
            label="HCP Name" 
            value={draft.hcp_name} 
            isMissing={isMissing('hcp_name')} 
            isUncertain={isUncertain('hcp_name')} 
          />
        </div>
        <div style={{ flex: 1 }}>
          <FieldDisplay 
            label="Interaction Type" 
            value={draft.interaction_type} 
            isMissing={isMissing('interaction_type')} 
            isUncertain={isUncertain('interaction_type')} 
          />
        </div>
      </div>

      <div style={{ display: 'flex', gap: '16px' }}>
        <div style={{ flex: 1 }}>
          <FieldDisplay 
            label="Date" 
            value={draft.interaction_date} 
            isMissing={isMissing('interaction_date')} 
            isUncertain={isUncertain('interaction_date')} 
          />
        </div>
        <div style={{ flex: 1 }}>
          <FieldDisplay 
            label="Time" 
            value={draft.interaction_time} 
            isMissing={isMissing('interaction_time')} 
            isUncertain={isUncertain('interaction_time')} 
          />
        </div>
      </div>

      <FieldDisplay 
        label="Attendees" 
        value={draft.attendees} 
        isMissing={isMissing('attendees')} 
        isUncertain={isUncertain('attendees')} 
      />

      <FieldDisplay 
        label="Topics Discussed" 
        value={draft.topics_discussed} 
        isMissing={isMissing('topics_discussed')} 
        isUncertain={isUncertain('topics_discussed')} 
      />

      <div style={{ padding: '16px', backgroundColor: '#f8fafc', borderRadius: '8px', marginBottom: '16px', border: '1px solid #e2e8f0' }}>
        <h4 style={{ margin: '0 0 12px 0', fontSize: '0.875rem', color: '#475569' }}>Materials & Samples</h4>
        <FieldDisplay 
          label="Materials Shared" 
          value={draft.materials_shared} 
          isMissing={isMissing('materials_shared')} 
          isUncertain={isUncertain('materials_shared')} 
        />
        <FieldDisplay 
          label="Samples Distributed" 
          value={draft.samples_distributed} 
          isMissing={isMissing('samples_distributed')} 
          isUncertain={isUncertain('samples_distributed')} 
        />
      </div>

      <SentimentSelectorView sentiment={draft.sentiment} />

      <FieldDisplay 
        label="Outcomes" 
        value={draft.outcomes} 
        isMissing={isMissing('outcomes')} 
        isUncertain={isUncertain('outcomes')} 
      />

      <FieldDisplay 
        label="Follow-up Actions" 
        value={draft.follow_ups} 
        isMissing={isMissing('follow_ups')} 
        isUncertain={isUncertain('follow_ups')} 
      />
      
      {/* Show a confirmation banner when the backend updates the ID indicating a successful save */}
      {draft.id && (
        <div style={{ marginTop: '16px', padding: '12px', backgroundColor: '#ecfdf5', color: '#065f46', borderRadius: '6px', textAlign: 'center', fontWeight: 500, border: '1px solid #a7f3d0' }}>
          ✓ Interaction Saved Successfully (ID: {draft.id})
        </div>
      )}
    </div>
  );
};

export default InteractionForm;

// ---
// Explanation:
// `InteractionForm.tsx` maps the entire Redux state to the read-only visual components.
// Because we pass the `isMissing` and `isUncertain` flags down, the UI creates a dynamic 
// mapping that provides immediate, visual feedback on what the agent needs from the user next.

"""
Assumptions:
- Using Pydantic V2.
- The schemas capture partial updates as `InteractionDraft` fields can be entirely optional while the agent is extracting them.
"""
from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import date, time, datetime

class InteractionBase(BaseModel):
    hcp_id: Optional[str] = None
    hcp_name: Optional[str] = None
    interaction_type: Optional[str] = None
    interaction_date: Optional[date] = None
    interaction_time: Optional[time] = None
    attendees: Optional[str] = None
    topics_discussed: Optional[str] = None
    materials_shared: Optional[str] = None
    samples_distributed: Optional[str] = None
    sentiment: Optional[str] = None
    outcomes: Optional[str] = None
    follow_ups: Optional[str] = None

class InteractionDraft(InteractionBase):
    """Represents the mutable form state being driven by the AI chat."""
    pass

class InteractionCreate(InteractionBase):
    user_id: str
    status: str = "DRAFT"

class InteractionUpdate(InteractionBase):
    status: Optional[str] = None

class InteractionResponse(InteractionBase):
    id: str
    user_id: str
    status: str
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# ---
# Explanation: 
# Validates interaction payloads. Crucially defines `InteractionDraft`, which allows 
# partial state transfer between frontend Redux state and backend LangGraph agent.

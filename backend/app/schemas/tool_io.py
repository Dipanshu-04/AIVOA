"""
Assumptions:
- Using Pydantic V2 for LangGraph tool input definitions.
"""
from pydantic import BaseModel, Field
from typing import Optional, List

class LogInteractionInput(BaseModel):
    user_id: str = Field(..., description="ID of the sales rep")
    hcp_id: Optional[str] = Field(None, description="ID of the HCP, if known")
    hcp_name: Optional[str] = Field(None, description="Name of the HCP")
    interaction_type: Optional[str] = Field(None, description="Type of interaction (Meeting, Email, etc.)")
    interaction_date: Optional[str] = Field(None, description="Date in YYYY-MM-DD")
    interaction_time: Optional[str] = Field(None, description="Time in HH:MM")
    attendees: Optional[str] = Field(None, description="Other attendees")
    topics_discussed: Optional[str] = Field(None, description="Summary of topics")
    sentiment: Optional[str] = Field(None, description="Sentiment (Positive, Neutral, Negative)")
    outcomes: Optional[str] = Field(None, description="Outcomes or agreements")
    status: str = Field("DRAFT", description="Status of the interaction: DRAFT or SAVED")
    interaction_id: Optional[str] = Field(None, description="ID if updating an existing draft to SAVED")

class EditInteractionInput(BaseModel):
    interaction_id: str = Field(..., description="ID of the interaction to edit")
    hcp_id: Optional[str] = Field(None)
    hcp_name: Optional[str] = Field(None)
    interaction_type: Optional[str] = Field(None)
    interaction_date: Optional[str] = Field(None)
    interaction_time: Optional[str] = Field(None)
    attendees: Optional[str] = Field(None)
    topics_discussed: Optional[str] = Field(None)
    sentiment: Optional[str] = Field(None)
    outcomes: Optional[str] = Field(None)
    status: Optional[str] = Field(None)

class SearchHCPInput(BaseModel):
    name_query: str = Field(..., description="Name of the HCP to search for")
    specialty: Optional[str] = Field(None, description="Optional specialty to filter by")

class AddMaterialsOrSamplesInput(BaseModel):
    interaction_id: str = Field(..., description="ID of the interaction")
    material_names: List[str] = Field(default_factory=list, description="List of material names to attach")
    sample_names: List[str] = Field(default_factory=list, description="List of sample names to attach")

class SuggestFollowUpInput(BaseModel):
    interaction_id: str = Field(..., description="ID of the interaction to generate follow-ups for")
    context_summary: str = Field(..., description="Summary of the interaction to base suggestions on")

# ---
# Explanation:
# Defines strict Pydantic schemas for the 5 LangGraph tools. This guarantees 
# that when the LLM decides to call a tool, it populates exactly the required arguments,
# ensuring type safety and preventing runtime errors in the database layer.

"""
Assumptions:
- Using Pydantic V2
- Defines the input/output protocol for the `/chat` agent endpoint, plus internal extraction schemas for LangGraph.
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List

class ChatRequest(BaseModel):
    message: str = Field(..., description="The natural language input from the user")
    current_draft: Optional[Dict[str, Any]] = Field(None, description="The full current interaction draft state")

class ChatResponse(BaseModel):
    reply: str = Field(..., description="The AI's textual response to the user")
    interaction_draft: Optional[Dict[str, Any]] = Field(None, description="The updated state of the interaction form")

class ExtractionResult(BaseModel):
    """
    Schema for the LLM to output structured extraction from the user's natural language.
    Used internally by the LangGraph tools.
    """
    hcp_name: Optional[str] = Field(None, description="Name of the health care professional")
    interaction_type: Optional[str] = Field(None, description="Type of interaction, e.g., Meeting, Email")
    interaction_date: Optional[str] = Field(None, description="Date of the interaction in YYYY-MM-DD format")
    interaction_time: Optional[str] = Field(None, description="Time of the interaction in HH:MM format")
    attendees: Optional[str] = Field(None, description="Other attendees present")
    topics_discussed: Optional[str] = Field(None, description="Summary of topics discussed")
    sentiment: Optional[str] = Field(None, description="Inferred sentiment: Positive, Neutral, or Negative")
    materials_shared: Optional[List[str]] = Field(None, description="Names of materials shared")
    samples_distributed: Optional[List[str]] = Field(None, description="Names of samples distributed")
    outcomes: Optional[str] = Field(None, description="Key outcomes or agreements")
    follow_ups: Optional[List[str]] = Field(None, description="Suggested follow-up tasks")

# ---
# Explanation: 
# This file bridges the LangGraph agent capabilities with the HTTP API. ChatRequest/Response 
# manages the interactive loop, while ExtractionResult ensures the LLM returns deterministic JSON form data.

from typing import TypedDict, Annotated, List, Dict, Any, Optional
import operator
from langchain_core.messages import BaseMessage

class AgentState(TypedDict):
    """
    LangGraph state definition for the AI-first HCP interaction agent.
    """
    # Core conversation history
    messages: Annotated[List[BaseMessage], operator.add]
    
    # Context identifiers
    user_id: str
    conversation_id: str
    
    # The inferred goal of the user (e.g., 'log_interaction', 'search_hcp')
    intent: Optional[str]
    
    # The current mutable state of the UI form
    draft_interaction: Dict[str, Any]
    
    # Fields required but not yet provided by the user
    missing_fields: List[str]
    
    # Fields that were extracted but with low confidence
    uncertain_fields: List[str]
    
    # The verified HCP record from the database
    selected_hcp: Optional[Dict[str, Any]]
    
    # Next tool requested by the LLM
    tool_to_call: Optional[str]
    
    # Result returned from the tool execution
    tool_result: Optional[Any]
    
    # Specific question the AI needs the user to answer
    clarification_question: Optional[str]
    
    # Tracking the last executed graph node or action for audit
    last_action: Optional[str]
    
    # The structured JSON payload to return to the React frontend
    ui_payload: Optional[Dict[str, Any]]
    
    # The extraction from the latest message alone
    current_extraction: Optional[Dict[str, Any]]

# ---
# Explanation:
# `state.py` defines the LangGraph state. The agent is chat-first and updates a read-only form;
# this state dict acts as the single source of truth during a single execution turn. 
# It supports tracking what fields are missing or uncertain (for clarifications), 
# tracks tool requests and results, and finally packages a `ui_payload` to sync the frontend Redux store.

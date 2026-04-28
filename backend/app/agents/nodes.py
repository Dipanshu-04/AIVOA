"""
Assumptions:
- Simplified lightweight intent classification logic for demonstration.
- `ExtractionService` from `app.services.extractor` is used to parse unstructured data.
- Tools are available in `app.agents.tools`.
"""
from typing import Dict, Any
from langchain_core.messages import AIMessage
from app.agents.state import AgentState
from app.agents.constants import *
from app.services.extractor import ExtractionService
from app.agents.tools import (
    log_interaction, edit_interaction, search_hcp, 
    add_materials_or_samples, suggest_follow_up, recall_interactions,
    delete_interactions
)

# Initialize the extractor service
extractor = ExtractionService()

async def understand_intent_node(state: AgentState) -> Dict[str, Any]:
    """Determines the user's intent based on the latest message."""
    last_msg = state["messages"][-1].content.lower() if state.get("messages") else ""
    
    intent = INTENT_GENERAL_CHAT
    if any(kw in last_msg for kw in ["delete", "remove", "erase", "clear logs", "discard"]):
        intent = INTENT_DELETE
    elif any(kw in last_msg for kw in ["tell me about", "tell me", "about log", "about my", "details", "previous", "recent", "history", "past", "show me", "who did i meet", "my logs", "recall", "list"]):
        intent = INTENT_RECALL
    elif any(kw in last_msg for kw in ["save", "log it", "go ahead", "submit", "confirm", "yes, log it", "yes log it"]):
        intent = INTENT_SAVE_INTERACTION
    elif any(kw in last_msg for kw in ["log", "met ", "i met", "visited", "called", "spoke", "interaction", "had a meeting", "had a call"]):
        intent = INTENT_LOG_INTERACTION
    elif "edit" in last_msg or "update" in last_msg or "change" in last_msg:
        intent = INTENT_EDIT_INTERACTION
    elif "search" in last_msg or "find" in last_msg:
        intent = INTENT_SEARCH_HCP
        
    return {"intent": intent, "last_action": "understand_intent"}

async def extract_entities_node(state: AgentState) -> Dict[str, Any]:
    """Uses the ExtractionService to parse the message into the draft state."""
    last_msg = state["messages"][-1].content if state.get("messages") else ""
    draft = state.get("draft_interaction", {})
    intent = state.get("intent")
    
    # Do not pass draft context to the LLM for recall/delete commands, 
    # to prevent it from forcefully retaining draft context in its extraction.
    extraction_context = draft if intent not in [INTENT_RECALL, INTENT_DELETE] else {}
    
    # Invoke the LLM to extract data
    extraction_result = await extractor.extract(last_msg, extraction_context)
    
    # Merge extracted fields into draft (only if they aren't None/empty to avoid overwriting valid data)
    new_draft = dict(draft)
    extracted_dict = extraction_result.model_dump(exclude_none=True)
    
    uncertain = extracted_dict.pop("uncertain_fields", [])
    
    for k, v in extracted_dict.items():
        if v: # If it has a truthy value (not empty string or empty list)
            new_draft[k] = v
            
    return {
        "draft_interaction": new_draft, 
        "uncertain_fields": uncertain,
        "current_extraction": extracted_dict,
        "last_action": ACTION_EXTRACT_ENTITIES
    }

async def validate_draft_node(state: AgentState) -> Dict[str, Any]:
    """Checks if the draft has all required fields for a final save."""
    draft = state.get("draft_interaction", {})
    missing = []
    
    # Always calculate missing fields so the UI and response can reference them
    for field in REQUIRED_INTERACTION_FIELDS:
        if not draft.get(field):
            missing.append(field)
                
    # If there are uncertain fields, we need clarification before executing DB tools
    clarification = None
    if state.get("intent") == INTENT_LOG_INTERACTION:
        if state.get("uncertain_fields"):
            clarification = f"I wasn't completely sure about: {', '.join(state['uncertain_fields'])}. Could you clarify before we save?"
        
    return {
        "missing_fields": missing,
        "clarification_question": clarification,
        "last_action": "validate_draft"
    }

async def route_tool_node(state: AgentState) -> Dict[str, Any]:
    """Decides which tool to call based on intent and validation."""
    intent = state.get("intent")
    clarification = state.get("clarification_question")
    tool_name = None
    
    if clarification:
        # Don't call a tool yet if we need clarification
        pass
    elif intent == INTENT_DELETE:
        tool_name = "delete_interactions"
    elif intent == INTENT_RECALL:
        tool_name = "recall_interactions"
    elif intent == INTENT_SEARCH_HCP:
        tool_name = "search_hcp"
    elif intent == INTENT_SAVE_INTERACTION and not state.get("missing_fields"):
        tool_name = "log_interaction"
    elif intent == INTENT_LOG_INTERACTION:
        # We don't save automatically. We stay in draft mode.
        tool_name = None
    elif intent == INTENT_EDIT_INTERACTION:
        tool_name = "edit_interaction"
        
    return {"tool_to_call": tool_name, "last_action": "route_tool"}

async def tool_execution_node(state: AgentState) -> Dict[str, Any]:
    """Executes the selected tool and returns the result."""
    tool_name = state.get("tool_to_call")
    draft = state.get("draft_interaction", {})
    result = None
    
    if tool_name == "log_interaction":
        result = log_interaction.invoke({
            "user_id": state.get("user_id", "default_user_1"),
            "hcp_id": draft.get("hcp_id"), 
            "hcp_name": draft.get("hcp_name"),
            "interaction_type": draft.get("interaction_type"),
            "interaction_date": draft.get("interaction_date"),
            "interaction_time": draft.get("interaction_time"),
            "attendees": draft.get("attendees"),
            "topics_discussed": draft.get("topics_discussed"),
            "sentiment": draft.get("sentiment"),
            "outcomes": draft.get("outcomes"),
            "status": "SAVED",
            "interaction_id": draft.get("id")
        })
        if "interaction_id" in result:
            draft["id"] = result["interaction_id"]
            
        # The user requested to clear the form so they can start the next log seamlessly.
        draft = {}
    elif tool_name == "search_hcp":
        # Extract the search query natively from the last message or draft
        query = draft.get("hcp_name") or state["messages"][-1].content
        result = search_hcp.invoke({"name_query": query})
        
    elif tool_name == "edit_interaction":
        interaction_id = draft.get("id")
        
        # If the draft has no id, look up the interaction by HCP name
        if not interaction_id:
            current_ext = state.get("current_extraction", {})
            lookup_name = current_ext.get("hcp_name") or draft.get("hcp_name")
            if lookup_name:
                from app.db.session import SessionLocal
                from app.models.interaction import Interaction
                db = SessionLocal()
                try:
                    match = (
                        db.query(Interaction)
                        .filter(
                            Interaction.user_id == state.get("user_id", "demo-user-1"),
                            Interaction.hcp_name.ilike(f"%{lookup_name}%"),
                        )
                        .order_by(Interaction.created_at.desc())
                        .first()
                    )
                    if match:
                        interaction_id = match.id
                finally:
                    db.close()
        
        if not interaction_id:
            result = {"status": "error", "message": "Could not find the interaction to edit. Please specify the HCP name."}
        else:
            result = edit_interaction.invoke({
                "interaction_id": interaction_id,
                "hcp_id": draft.get("hcp_id"),
                "hcp_name": draft.get("hcp_name"),
                "interaction_type": draft.get("interaction_type"),
                "interaction_date": draft.get("interaction_date"),
                "interaction_time": draft.get("interaction_time"),
                "attendees": draft.get("attendees"),
                "topics_discussed": draft.get("topics_discussed"),
                "sentiment": draft.get("sentiment"),
                "outcomes": draft.get("outcomes"),
            })
        
    elif tool_name == "recall_interactions":
        current_ext = state.get("current_extraction", {})
        last_msg = state["messages"][-1].content.lower() if state.get("messages") else ""
        result = recall_interactions.invoke({
            "user_id": state.get("user_id", "demo-user-1"),
            "hcp_name": current_ext.get("hcp_name"),
            "limit": 10,
            "raw_query": last_msg
        })
    elif tool_name == "delete_interactions":
        current_ext = state.get("current_extraction", {})
        last_msg = state["messages"][-1].content.lower() if state.get("messages") else ""
        result = delete_interactions.invoke({
            "user_id": state.get("user_id", "demo-user-1"),
            "hcp_name": current_ext.get("hcp_name"),
            "interaction_date": current_ext.get("interaction_date"),
            "raw_query": last_msg
        })
    # Also update materials/followups in draft if we run those tools
    elif tool_name == "add_materials_or_samples":
        pass
    
    return {"tool_result": result, "tool_to_call": None, "last_action": ACTION_CALL_TOOL, "draft_interaction": draft}

async def respond_node(state: AgentState) -> Dict[str, Any]:
    """Generates the final response and the UI state payload to sync the React frontend."""
    if state.get("clarification_question"):
        msg = state["clarification_question"]
    elif state.get("tool_result"):
        msg = state["tool_result"].get("message", "Action completed successfully.")
    else:
        # User is just chatting and data was extracted but no tool run
        missing = state.get("missing_fields", [])
        if missing:
            formatted_missing = [f.replace("_", " ").title() for f in missing]
            if len(formatted_missing) > 1:
                missing_str = ", ".join(formatted_missing[:-1]) + " and " + formatted_missing[-1]
            else:
                missing_str = formatted_missing[0]
            msg = f"Got it, I've updated the draft. We still need the {missing_str}. Whenever you're ready, just let me know."
        else:
            msg = "That's all I need, press the Log Interaction button when you're ready to save the details."
        
    ui_payload = {
        "draft_interaction": state.get("draft_interaction", {}),
        "missing_fields": state.get("missing_fields", []),
        "uncertain_fields": state.get("uncertain_fields", [])
    }
    
    return {
        "messages": [AIMessage(content=msg)],
        "ui_payload": ui_payload,
        "last_action": ACTION_FINISH
    }

# ---
# Explanation:
# The `nodes.py` file contains the logic that runs at each step of the LangGraph state machine.
# They update the `AgentState` by classifying intents, extracting entities via the Groq LLM service, 
# validating rules, routing to/executing LangChain tools, and finally packaging a UI payload 
# so the React frontend can update the read-only form instantly in sync with the chat.

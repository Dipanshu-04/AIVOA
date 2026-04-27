"""
Constants used across the LangGraph agent nodes and routing.
"""

# Intents
INTENT_LOG_INTERACTION = "log_interaction"
INTENT_EDIT_INTERACTION = "edit_interaction"
INTENT_SEARCH_HCP = "search_hcp"
INTENT_ADD_MATERIALS = "add_materials_or_samples"
INTENT_RECALL = "recall_interactions"
INTENT_DELETE = "delete_interactions"
INTENT_GENERAL_CHAT = "general_chat"
INTENT_SAVE_INTERACTION = "save_interaction"

# Action Labels (Node names / last_action values)
ACTION_EXTRACT_ENTITIES = "extract_entities"
ACTION_ASK_CLARIFICATION = "ask_clarification"
ACTION_CALL_TOOL = "call_tool"
ACTION_UPDATE_DRAFT = "update_draft"
ACTION_SAVE_FINAL = "save_final"
ACTION_FINISH = "finish"

# Required fields to consider an interaction "complete" and ready for final save
REQUIRED_INTERACTION_FIELDS = [
    "hcp_name",
    "interaction_type",
    "interaction_date",
    "outcomes"
]

# ---
# Explanation:
# `constants.py` centralizes string literals for intents, routing actions, and business logic
# (like required fields). This prevents subtle bugs caused by typos across different agent nodes
# and makes it easy to add or modify rules for the state machine.

"""
Assumptions:
- Using `langgraph` StateGraph.
- The workflow follows a clear, linear path with conditional routing for tool execution.
"""
from langgraph.graph import StateGraph, END
from app.agents.state import AgentState
from app.agents.nodes import (
    understand_intent_node,
    extract_entities_node,
    validate_draft_node,
    route_tool_node,
    tool_execution_node,
    respond_node
)

def should_execute_tool(state: AgentState) -> str:
    """Conditional edge router: determines if we jump to tool execution or directly to the response."""
    if state.get("tool_to_call"):
        return "tool_execution_node"
    return "respond_node"

def build_hcp_graph() -> StateGraph:
    """Builds and compiles the main LangGraph workflow for the HCP CRM module."""
    workflow = StateGraph(AgentState)

    # Add Nodes
    workflow.add_node("understand_intent_node", understand_intent_node)
    workflow.add_node("extract_entities_node", extract_entities_node)
    workflow.add_node("validate_draft_node", validate_draft_node)
    workflow.add_node("route_tool_node", route_tool_node)
    workflow.add_node("tool_execution_node", tool_execution_node)
    workflow.add_node("respond_node", respond_node)

    # Define Edges
    workflow.set_entry_point("understand_intent_node")
    
    workflow.add_edge("understand_intent_node", "extract_entities_node")
    workflow.add_edge("extract_entities_node", "validate_draft_node")
    workflow.add_edge("validate_draft_node", "route_tool_node")
    
    # Conditional routing based on whether a tool needs to be executed
    # If the draft needs clarification, we skip tool execution and go straight to responding.
    workflow.add_conditional_edges(
        "route_tool_node",
        should_execute_tool,
        {
            "tool_execution_node": "tool_execution_node",
            "respond_node": "respond_node"
        }
    )
    
    # After a tool executes, always respond to the user
    workflow.add_edge("tool_execution_node", "respond_node")
    workflow.add_edge("respond_node", END)

    return workflow.compile()

# ---
# Explanation:
# The `hcp_graph.py` ties the individual nodes together into a state machine using LangGraph.
# It defines a strict sequential flow: Understand Intent -> Extract Entities -> Validate Draft -> Route.
# A conditional edge then determines if a tool executes (e.g., saving to DB) or if it directly 
# responds (e.g., asking the user for missing fields). This architecture prevents complex tangles.

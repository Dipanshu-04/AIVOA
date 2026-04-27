from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.chat import ChatRequest, ChatResponse
from app.agents.hcp_graph import build_hcp_graph
from app.models.interaction import Interaction
from langchain_core.messages import HumanMessage
import uuid

router = APIRouter()

# Compile the LangGraph graph once at startup
hcp_agent_graph = build_hcp_graph()

@router.post("/", response_model=ChatResponse)
async def process_chat(request: ChatRequest, db: Session = Depends(get_db)):
    """
    Main endpoint for the chat interface. Takes the natural language input and current 
    draft state, routes it through the LangGraph agent, and returns the response and updated UI payload.
    """
    try:
        # Initialize the state. In a real scenario, conversation history might be loaded from DB.
        initial_state = {
            "messages": [HumanMessage(content=request.message)],
            "user_id": "demo-user-1", 
            "conversation_id": str(uuid.uuid4()),
            "draft_interaction": request.current_draft or {},
            "missing_fields": [],
            "uncertain_fields": []
        }

        # Run the compiled LangGraph workflow
        final_state = await hcp_agent_graph.ainvoke(initial_state)

        # Extract the AI's final response and the structured UI payload
        ai_response = final_state["messages"][-1].content
        ui_payload = final_state.get("ui_payload", {})

        return ChatResponse(
            reply=ai_response,
            interaction_draft=ui_payload
        )
        
    except Exception as e:
        # Catch and surface agent or parsing failures cleanly
        raise HTTPException(status_code=500, detail=f"Agent error: {str(e)}")

# ---
# Explanation:
# The `chat.py` router wraps the complex LangGraph execution inside a clean REST API. 
# It handles the IO bridging between the React frontend's natural language and the backend's state machine.

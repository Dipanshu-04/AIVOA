import asyncio
from app.agents.hcp_graph import build_hcp_graph
from langchain_core.messages import HumanMessage

async def main():
    graph = build_hcp_graph()
    
    # Simulate drafting
    initial_draft = {}
    print("USER: I met Dr. Steve on wednesday April 22. He was in a good mood and asked me about all our new offerings. I showed him our brochure. He ordered 18 new x-ray machines. This was a Meeting.")
    state1 = await graph.ainvoke({
        "messages": [HumanMessage(content="I met Dr. Steve on wednesday April 22. He was in a good mood and asked me about all our new offerings. I showed him our brochure. He ordered 18 new x-ray machines. This was a Meeting.")],
        "user_id": "demo-user-1",
        "draft_interaction": initial_draft,
        "missing_fields": [],
        "uncertain_fields": []
    })
    
    print(f"AGENT: {state1['messages'][-1].content}")
    print(f"DRAFT: {state1['ui_payload']}")
    
    # Simulate saving
    print("\nUSER: yes log it")
    state2 = await graph.ainvoke({
        "messages": [HumanMessage(content="yes log it")],
        "user_id": "demo-user-1",
        "draft_interaction": state1["ui_payload"]["draft_interaction"],
        "missing_fields": [],
        "uncertain_fields": []
    })
    
    print(f"AGENT: {state2['messages'][-1].content}")
    print(f"DRAFT: {state2['ui_payload']}")

asyncio.run(main())

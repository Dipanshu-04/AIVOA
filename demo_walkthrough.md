# Demo Walkthrough Script: AI-First HCP CRM Module

## 1. Suggested Demo Order
1. **Introduction:** Briefly explain the goal (replacing tedious forms with a smart chat interface).
2. **UI Tour:** Show the two-pane layout (read-only form on the left, chat on the right).
3. **Scenario 1 - Logging & Search (`search_hcp`, `log_interaction`):** Log a new interaction, resolve ambiguity.
4. **Scenario 2 - Editing (`edit_interaction`):** Update the draft natively via chat.
5. **Scenario 3 - Adding Assets (`add_materials_or_samples`, `suggest_follow_up`):** Add samples and schedule a task.
6. **Architecture Breakdown:** Explain LangGraph, FastAPI, and Redux.
7. **Conclusion:** Summarize why AI-first is the future of CRM.

---

## 2. Screen Action Checklist
- [ ] Have the application running (`npm run dev` and `uvicorn app.main:app`).
- [ ] Clear the database or ensure the `seed_data.py` demo data is fresh.
- [ ] Open the browser to the application frontend.
- [ ] Open the browser console or network tab (optional) to show real-time JSON payloads updating.
- [ ] Have the architecture diagram or `README.md` open in another tab to show the LangGraph flow.

---

## 3. Spoken Script

**(Introduction - 2 minutes)**
"Hi everyone, thanks for your time today. For my hiring assessment, I was tasked with building an AI-First CRM module for Healthcare Professionals. 

The core problem with traditional CRMs in pharma is friction. Sales reps spend hours manually clicking through dropdowns and text boxes after a long day of meetings. My goal was to flip this paradigm: instead of the user adapting to the software, the software adapts to the user. 

Let me show you what I mean."

**(UI Tour - 1 minute)**
*(Action: Hover over the left and right panes)*
"What you see here is a strict two-pane layout. On the right, we have a natural language chat interface. On the left, we have the structured CRM form. Notice that the form on the left is completely read-only. The only way to interact with this application is by talking to the AI agent. The AI acts as the intelligent bridge between unstructured human thought and our rigid MySQL database."

**(Scenario 1: Logging and Search - 3 minutes)**
"Let's say I just got out of a meeting. I'll type: *'I just met with Dr. Smith. We talked about OncoBoost efficacy.'*"
*(Action: Type and send message)*

"Notice what happens. The form on the left instantly updates. The AI extracted 'Dr. Smith' and the topic 'OncoBoost efficacy'. But the AI also halted execution. It's asking me *which* Dr. Smith I meant, because it used the `search_hcp` tool against our database and found two: Sarah Smith and Steven Smith."

*(Action: Type 'Sarah. She was very positive.')*
"I'll clarify that it's Sarah and add that she was positive. The AI updates the sentiment field to 'Positive', links the correct HCP ID, and now realizes it's still missing the interaction date. This demonstrates the validation node in our LangGraph agent—it won't save incomplete data."

*(Action: Type 'It happened today at 2 PM. Save it.')*
"I'll provide the date and time. Now, because I asked it to save, it's invoking the `log_interaction` tool. Because writing to the database is a high-risk action, the UI catches this and prompts me for a final confirmation."
*(Action: Click Confirm)*

**(Scenario 2: Editing - 2 minutes)**
"Let's say I made a mistake. I'll tell the AI: *'Actually, change her sentiment to neutral, she had some concerns about the side effects.'*"
*(Action: Type and send message)*

"The AI automatically invokes the `edit_interaction` tool. It updates the draft payload, and the React UI instantly reflects this change on the left. No manual form hunting required."

**(Scenario 3: Assets and Follow-ups - 2 minutes)**
"Finally, reps often leave physical samples or need to schedule tasks. I'll type: *'Add that I gave her 2 packs of the OncoBoost starter kit, and remind me to email her the Phase III clinical trial PDF next Friday.'*"
*(Action: Type and send message)*

"In a single prompt, the agent orchestrates two different tools. It uses `add_materials_or_samples` to link the inventory to this interaction, and it uses `suggest_follow_up` to create a pending task for next Friday. You can see both reflected instantly in our structured data."

**(Architecture Breakdown - 3 minutes)**
*(Action: Switch to README or architecture diagram)*
"To make this work seamlessly, I built a robust monorepo architecture. 
The backend is powered by FastAPI and LangGraph. LangGraph is crucial here because it allows us to build a cyclical state machine. The agent loops through nodes: Understand Intent -> Extract Entities using Groq's fast LLM -> Validate against Pydantic schemas -> Ask for Clarification if needed -> Route to Tools -> Execute. 

This state is then passed to the React frontend, where Redux Toolkit captures the JSON payload and instantly re-renders the read-only form, giving the user immediate, deterministic feedback."

**(Conclusion - 1 minute)**
"To summarize: by utilizing an AI-first design pattern, we've reduced a 3-minute manual data entry task into a 15-second natural conversation. The LangGraph agent ensures data integrity by enforcing structured schemas and database lookups, while the read-only UI provides absolute transparency into what the AI is doing. 

Thank you, and I'd love to answer any questions about the implementation."

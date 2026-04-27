# AI-First HCP CRM Module

## Summary
The AI-First HCP (Health Care Professional) CRM Module is a proof-of-concept application designed to revolutionize how pharmaceutical sales representatives log interactions. Instead of manually clicking through complex forms, reps simply chat with an AI assistant in natural language. The AI autonomously extracts structured data, identifies missing information, asks clarifying questions, and executes database actions.

## Why AI-First?
Traditional CRMs force users to adapt to the software—navigating endless dropdowns and text fields. This "AI-First" approach flips the paradigm: the software adapts to the user. 
- **Frictionless Data Entry:** Reps type or dictate a raw summary ("Met Dr. Smith, gave him 2 samples of CardioGuard...").
- **Deterministic UI:** The chat interface drives a strictly read-only structured form, giving immediate visual feedback of what the AI understands.
- **Intelligent Routing:** The agent knows when to save a draft, when to query the database for HCP details, and when to ask for human confirmation before committing records.

## Architecture Overview
The application uses a modern monorepo architecture with a strict separation of concerns, communicating via REST:
- **Backend:** FastAPI (Python) powers the REST endpoints. LangGraph orchestrates the stateful LLM agent. Groq (`gpt-oss-120b`) provides high-speed, deterministic inference via structured outputs. SQLAlchemy manages the MySQL database.
- **Frontend:** React (TypeScript) provides the UI shell. A strict two-pane layout ensures all data entry flows through the chat pane on the right, dynamically rendering the read-only structured interaction form on the left using Redux state management.

## Tech Stack
- **Backend:** Python 3.10+, FastAPI, LangGraph, LangChain, Groq API, SQLAlchemy 2.0, MySQL (with local SQLite fallback for dev).
- **Frontend:** React 18, TypeScript, Redux Toolkit, Axios, Vanilla CSS (Inter font).

## Folder Structure
```text
AIVOA/
├── backend/
│   ├── app/
│   │   ├── agents/      # LangGraph state machine, nodes, and tools
│   │   ├── api/         # FastAPI route handlers (chat, hcps, interactions)
│   │   ├── db/          # SQLAlchemy session setup
│   │   ├── models/      # Database schemas (HCP, Interaction, etc.)
│   │   ├── prompts/     # System prompts & entity extraction logic
│   │   ├── schemas/     # Pydantic validation schemas
│   │   ├── seed/        # Demo data (demo_data.json) and seeding script
│   │   ├── services/    # External services (e.g., Groq extraction)
│   │   └── main.py      # FastAPI entry point
│   ├── .env
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── api/         # Axios client and services
│   │   ├── components/  # React components (Layout, Form, Chat)
│   │   ├── hooks/       # Custom React hooks (useChatController)
│   │   ├── store/       # Redux slices (chat, interactionDraft, ui)
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   └── .env
└── README.md
```

## LangGraph Agent Design
The backend agent is designed as a directed cyclic graph (State Machine):
1. **Understand Intent:** Classifies if the user is logging, editing, or searching.
2. **Extract Entities:** Parses the natural language into a strictly typed Pydantic JSON draft.
3. **Validate:** Checks against business rules (e.g., missing required fields).
4. **Clarify (Conditional):** If data is missing/uncertain, the agent halts tool execution and asks the user for clarification.
5. **Route & Execute:** If valid and complete, the agent executes the appropriate tool.
6. **Respond:** Returns the textual reply and the updated UI payload to the frontend.

## The 7 Core Tools
1. **`log_interaction`**: Creates a new interaction record in the database. Requires explicit confirmation via a "Log Interaction" button or command.
2. **`edit_interaction`**: Updates an existing draft or saved interaction.
3. **`search_hcp`**: Queries the database to find a specific doctor by name/specialty to resolve ambiguities.
4. **`add_materials_or_samples`**: Links specific brochures or physical drug samples to the interaction.
5. **`suggest_follow_up`**: Creates a follow-up task (e.g., "Send email next Tuesday") linked to the interaction.
6. **`recall_interactions`**: Retrieves and lists the user's past interaction logs, optionally filtered by HCP.
7. **`delete_interactions`**: Safely deletes specific interaction logs based on the HCP name or date using robust DB string matching fallback.

## API Endpoints
- `POST /api/chat/`: The main bridge. Accepts a message string, processes it via LangGraph, and returns the AI reply + deterministic UI draft state.
- `GET /api/interactions/`: Fetch saved interactions.
- `GET /api/hcps/`: Fuzzy search master HCP data.

## Frontend Data Flow
1. User types in `<ChatInput />` and hits send.
2. `useChatController` dispatches the message to Redux to update the chat list and calls `/api/chat/`.
3. The response payload (draft JSON + missing/uncertain flags) is dispatched to the `interactionDraftSlice`.
4. `<InteractionForm />` (the left pane) automatically and instantly re-renders to visualize the new state, using color-coded borders to highlight AI extractions.

## Setup Instructions

### Environment Variables
**Backend (`backend/.env`):**
```env
GROQ_API_KEY=your_groq_api_key_here
# Optional: defaults to local sqlite database if omitted
DATABASE_URL=mysql+pymysql://user:password@localhost:3306/aivoa_crm 
```

**Frontend (`frontend/.env`):**
```env
REACT_APP_API_URL=http://localhost:8000/api
```

### Running the Application

**1. Database Seeding:**
```bash
cd backend
# Seeds 10 HCPs, materials, samples, and demo interactions
python app/seed/seed_data.py
```

**2. Start Backend:**
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

**3. Start Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## Demo Scenarios

**Scenario 1: Logging a New Interaction (Tools used: `search_hcp`, `log_interaction`)**
- *User:* "I just met with Dr. Smith."
- *Agent:* "Which Dr. Smith? I see Sarah Smith (Oncology) and Steven Smith (Cardiology)." (Uses `search_hcp`)
- *User:* "Sarah. We discussed OncoBoost. She seemed positive."
- *Agent:* "Great. I've noted that down. I'm missing the date and time. When did this happen?"
- *User:* "Today at 2 PM."
- *Agent:* "Thanks! That's all the information I need. Click the Log Interaction button when you're ready."
- *User:* (Clicks green button or types "Save it")
- *Agent:* (Executes `log_interaction` and clears the form for the next entry)

**Scenario 2: Adding Samples & Follow-ups (Tools used: `add_materials_or_samples`, `suggest_follow_up`)**
- *User:* "Add that I gave her 2 packs of the OncoBoost starter kit."
- *Agent:* (Executes tool, updates draft UI to reflect samples).
- *User:* "Remind me to email her the Phase III PDF next Friday."
- *Agent:* (Uses `suggest_follow_up` to create a pending follow-up task).

**Scenario 3: Editing (Tool used: `edit_interaction`)**
- *User:* "Actually, change her sentiment to neutral, she had some concerns about side effects."
- *Agent:* (Uses `edit_interaction` to update the draft/database record and refreshes the UI).

**Scenario 4: Recalling & Deleting (Tools used: `recall_interactions`, `delete_interactions`)**
- *User:* "List my past interactions."
- *Agent:* (Uses `recall_interactions` to present a clean, bulleted summary of recent logs).
- *User:* "Can you delete interaction with Dr. Gandhi?"
- *Agent:* (Uses robust fallback string matching inside `delete_interactions` to locate and safely remove the record).

## Future Improvements
- **Voice-to-Text Summarization:** Allow reps to record a voice note in the car; use OpenAI's Whisper API to transcribe, then pass the raw transcript directly into the LangGraph pipeline for instant, hands-free logging.
- **RAG (Retrieval-Augmented Generation):** Connect the agent to internal medical guidelines so the rep can ask scientific questions while simultaneously logging the call.
- **Analytics Dashboard:** Build out a management view to analyze interaction sentiments and sample distribution rates across territories.

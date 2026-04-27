from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.chat import router as chat_router
from app.api.interactions import router as interactions_router
from app.api.hcps import router as hcps_router
from app.db.session import engine, Base
import app.models.hcp
import app.models.interaction
import app.models.material
import app.models.follow_up
import app.models.user

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI-First CRM HCP Module",
    description="Backend API for managing interactions and chatting with the LangGraph agent.",
    version="1.0.0"
)

# Configure CORS to allow the React frontend to communicate with the FastAPI backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For development only; should be restricted in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API Routers
app.include_router(chat_router, prefix="/api/chat", tags=["Chat Interface"])
app.include_router(interactions_router, prefix="/api/interactions", tags=["Interactions Data"])
app.include_router(hcps_router, prefix="/api/hcps", tags=["HCP Master Data"])

@app.get("/health", tags=["System"])
def health_check():
    """Simple health check endpoint."""
    return {"status": "ok", "message": "API is running"}

# ---
# Explanation:
# `main.py` is the application entry point. It bootstraps the FastAPI application, 
# configures necessary middleware like CORS, and wires up all the specific route handlers.

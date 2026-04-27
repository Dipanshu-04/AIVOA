from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.interaction import Interaction
from app.schemas.interaction import InteractionResponse

router = APIRouter()

@router.get("/", response_model=List[InteractionResponse])
def read_interactions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve all saved or drafted interactions.
    """
    interactions = db.query(Interaction).offset(skip).limit(limit).all()
    return interactions

@router.get("/{interaction_id}", response_model=InteractionResponse)
def read_interaction(interaction_id: str, db: Session = Depends(get_db)):
    """
    Retrieve a specific interaction by its ID.
    """
    interaction = db.query(Interaction).filter(Interaction.id == interaction_id).first()
    if not interaction:
        raise HTTPException(status_code=404, detail="Interaction not found")
    return interaction

@router.delete("/{interaction_id}")
def delete_interaction(interaction_id: str, db: Session = Depends(get_db)):
    """
    Delete an interaction record.
    """
    interaction = db.query(Interaction).filter(Interaction.id == interaction_id).first()
    if not interaction:
        raise HTTPException(status_code=404, detail="Interaction not found")
    
    db.delete(interaction)
    db.commit()
    return {"status": "success", "message": "Interaction deleted"}

# ---
# Explanation:
# The `interactions.py` router provides standard CRUD operations for the interaction records. 
# While the LangGraph agent handles creation and edits via chat, these endpoints support 
# dashboard views or direct UI deletions.

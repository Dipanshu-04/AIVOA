from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.session import get_db
from app.models.hcp import HCP
from app.schemas.hcp import HCPResponse

router = APIRouter()

@router.get("/", response_model=List[HCPResponse])
def search_hcps(
    query: Optional[str] = Query(None, description="Search by name"),
    specialty: Optional[str] = Query(None, description="Filter by specialty"),
    db: Session = Depends(get_db)
):
    """
    Search for Health Care Professionals using a fuzzy search. 
    Useful for UI auto-complete or manual lookup functionalities.
    """
    db_query = db.query(HCP)
    
    if query:
        search_term = f"%{query}%"
        db_query = db_query.filter(
            HCP.first_name.ilike(search_term) | HCP.last_name.ilike(search_term)
        )
        
    if specialty:
        db_query = db_query.filter(HCP.specialty.ilike(specialty))
        
    hcps = db_query.all()
    return hcps

@router.get("/{hcp_id}", response_model=HCPResponse)
def get_hcp(hcp_id: str, db: Session = Depends(get_db)):
    """
    Get details of a specific HCP by ID.
    """
    hcp = db.query(HCP).filter(HCP.id == hcp_id).first()
    if not hcp:
        raise HTTPException(status_code=404, detail="HCP not found")
    return hcp

# ---
# Explanation:
# The `hcps.py` router exposes the master HCP data. It allows the frontend to query 
# specific HCPs or populate UI dropdowns if a user wants to manually inspect records.

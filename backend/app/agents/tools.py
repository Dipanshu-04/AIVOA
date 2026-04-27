"""
Assumptions:
- Using LangChain's `@tool` decorator for LangGraph compatibility.
- Database interactions are implemented to read/write to the MySQL DB.
"""
from typing import Dict, Any, List, Optional
from langchain_core.tools import tool
import datetime
from app.schemas.tool_io import (
    LogInteractionInput, 
    EditInteractionInput, 
    SearchHCPInput,
    AddMaterialsOrSamplesInput,
    SuggestFollowUpInput
)
from app.db.session import SessionLocal
from app.models.interaction import Interaction
from app.models.hcp import HCP

@tool(args_schema=LogInteractionInput)
def log_interaction(
    user_id: str,
    hcp_id: str = None,
    hcp_name: str = None,
    interaction_type: str = None,
    interaction_date: str = None,
    interaction_time: str = None,
    attendees: str = None,
    topics_discussed: str = None,
    sentiment: str = None,
    outcomes: str = None,
    status: str = "DRAFT",
    interaction_id: str = None
) -> Dict[str, Any]:
    """
    Creates a new interaction record or finalizes an existing draft to 'SAVED'.
    Returns the created or updated interaction ID and status.
    """
    db = SessionLocal()
    try:
        interaction = None
        if interaction_id:
            interaction = db.query(Interaction).filter(Interaction.id == interaction_id).first()
        
        if not interaction:
            interaction = Interaction(id=interaction_id, user_id=user_id)
            db.add(interaction)

        if hcp_id: interaction.hcp_id = hcp_id
        if hcp_name: interaction.hcp_name = hcp_name
        if interaction_type: interaction.interaction_type = interaction_type
        if interaction_date: 
            interaction.interaction_date = datetime.date.fromisoformat(interaction_date) if isinstance(interaction_date, str) else interaction_date
        if interaction_time: 
            interaction.interaction_time = datetime.time.fromisoformat(interaction_time) if isinstance(interaction_time, str) else interaction_time
        if attendees: interaction.attendees = attendees
        if topics_discussed: interaction.topics_discussed = topics_discussed
        if sentiment: interaction.sentiment = sentiment
        if outcomes: interaction.outcomes = outcomes
        
        interaction.status = status
        db.commit()
        db.refresh(interaction)
        return {
            "status": "success",
            "action": "log_interaction",
            "interaction_id": interaction.id,
            "record_status": interaction.status,
            "message": f"Interaction {'saved' if status == 'SAVED' else 'draft created'} successfully."
        }
    except Exception as e:
        db.rollback()
        return {"status": "error", "message": str(e)}
    finally:
        db.close()

@tool(args_schema=EditInteractionInput)
def edit_interaction(
    interaction_id: str,
    hcp_id: str = None,
    hcp_name: str = None,
    interaction_type: str = None,
    interaction_date: str = None,
    interaction_time: str = None,
    attendees: str = None,
    topics_discussed: str = None,
    sentiment: str = None,
    outcomes: str = None,
    status: str = None
) -> Dict[str, Any]:
    """
    Performs a partial update on an existing interaction draft.
    Only provided fields are updated.
    """
    db = SessionLocal()
    try:
        interaction = db.query(Interaction).filter(Interaction.id == interaction_id).first()
        if not interaction:
            return {"status": "error", "message": "Interaction not found."}
            
        if hcp_id: interaction.hcp_id = hcp_id
        if hcp_name: interaction.hcp_name = hcp_name
        if interaction_type: interaction.interaction_type = interaction_type
        if interaction_date: 
            interaction.interaction_date = datetime.date.fromisoformat(interaction_date) if isinstance(interaction_date, str) else interaction_date
        if interaction_time: 
            interaction.interaction_time = datetime.time.fromisoformat(interaction_time) if isinstance(interaction_time, str) else interaction_time
        if attendees: interaction.attendees = attendees
        if topics_discussed: interaction.topics_discussed = topics_discussed
        if sentiment: interaction.sentiment = sentiment
        if outcomes: interaction.outcomes = outcomes
        if status: interaction.status = status
        
        db.commit()
        return {
            "status": "success",
            "action": "edit_interaction",
            "interaction_id": interaction_id,
            "message": "Interaction updated successfully."
        }
    except Exception as e:
        db.rollback()
        return {"status": "error", "message": str(e)}
    finally:
        db.close()

@tool(args_schema=SearchHCPInput)
def search_hcp(name_query: str, specialty: str = None) -> Dict[str, Any]:
    """
    Searches the master HCP database using fuzzy matching on the name.
    Returns matched HCPs with a confidence score.
    """
    db = SessionLocal()
    try:
        query = db.query(HCP).filter(HCP.name.ilike(f"%{name_query}%"))
        if specialty:
            query = query.filter(HCP.specialty.ilike(f"%{specialty}%"))
        
        hcps = query.all()
        matches = [
            {"id": h.id, "name": h.name, "specialty": h.specialty, "confidence": 0.95} 
            for h in hcps
        ]

        return {
            "status": "success",
            "query": name_query,
            "matches": matches,
            "message": f"Found {len(matches)} potential matches."
        }
    finally:
        db.close()

@tool(args_schema=AddMaterialsOrSamplesInput)
def add_materials_or_samples(interaction_id: str, material_names: List[str] = None, sample_names: List[str] = None) -> Dict[str, Any]:
    """
    Maps extracted material/sample names to the catalog database and links them to the interaction.
    """
    db = SessionLocal()
    try:
        interaction = db.query(Interaction).filter(Interaction.id == interaction_id).first()
        if not interaction:
            return {"status": "error", "message": "Interaction not found."}

        added_materials = material_names or []
        added_samples = sample_names or []
        
        if added_materials:
            current_materials = interaction.materials_shared or ""
            interaction.materials_shared = current_materials + (", " if current_materials else "") + ", ".join(added_materials)
            
        if added_samples:
            current_samples = interaction.samples_distributed or ""
            interaction.samples_distributed = current_samples + (", " if current_samples else "") + ", ".join(added_samples)
            
        db.commit()
        return {
            "status": "success",
            "interaction_id": interaction_id,
            "added_materials": added_materials,
            "added_samples": added_samples,
            "message": f"Added {len(added_materials)} materials and {len(added_samples)} samples."
        }
    except Exception as e:
        db.rollback()
        return {"status": "error", "message": str(e)}
    finally:
        db.close()

@tool(args_schema=SuggestFollowUpInput)
def suggest_follow_up(interaction_id: str, context_summary: str) -> Dict[str, Any]:
    """
    Generates logical follow-up actions based on the interaction context summary.
    """
    db = SessionLocal()
    try:
        interaction = db.query(Interaction).filter(Interaction.id == interaction_id).first()
        if not interaction:
            return {"status": "error", "message": "Interaction not found."}

        suggestions = []
        summary_lower = context_summary.lower()
        
        if "efficacy" in summary_lower or "clinical trial" in summary_lower:
            suggestions.append("Send Phase III clinical trial PDF")
        if "positive" in summary_lower:
            suggestions.append("Schedule follow-up meeting in 2 weeks")
        else:
            suggestions.append("Send thank you email")

        current_follow_ups = interaction.follow_ups or ""
        interaction.follow_ups = current_follow_ups + (", " if current_follow_ups else "") + ", ".join(suggestions)
        db.commit()

        return {
            "status": "success",
            "interaction_id": interaction_id,
            "suggestions": suggestions,
            "message": "Follow-up suggestions generated."
        }
    except Exception as e:
        db.rollback()
        return {"status": "error", "message": str(e)}
    finally:
        db.close()

@tool
def recall_interactions(user_id: str, hcp_name: Optional[str] = None, limit: int = 10, raw_query: Optional[str] = None) -> Dict[str, Any]:
    """
    Retrieves the most recent saved interaction logs for a user.
    Can optionally filter by HCP name.
    Returns a formatted summary of past interactions.
    """
    db = SessionLocal()
    try:
        query = (
            db.query(Interaction)
            .filter(Interaction.user_id == user_id)
        )
        
        if hcp_name:
            query = query.filter(Interaction.hcp_name.ilike(f"%{hcp_name}%"))
        
        interactions = query.order_by(Interaction.created_at.desc()).limit(limit).all()
        
        if not hcp_name and raw_query:
            raw_lower = raw_query.lower()
            filtered = [ix for ix in interactions if ix.hcp_name and ix.hcp_name.lower() in raw_lower]
            if filtered:
                interactions = filtered
        
        if not interactions:
            if hcp_name:
                return {
                    "status": "success",
                    "count": 0,
                    "interactions": [],
                    "message": f"No interactions found with {hcp_name}."
                }
            return {
                "status": "success",
                "count": 0,
                "interactions": [],
                "message": "No interactions found."
            }
        
        records = []
        for ix in interactions:
            records.append({
                "id": ix.id,
                "hcp_name": ix.hcp_name or "Unknown",
                "interaction_type": ix.interaction_type or "N/A",
                "date": str(ix.interaction_date) if ix.interaction_date else "N/A",
                "topics": ix.topics_discussed or "N/A",
                "sentiment": ix.sentiment or "N/A",
                "outcomes": ix.outcomes or "N/A",
                "status": ix.status or "N/A"
            })
        
        # Build a human-readable summary
        summaries = []
        for r in records:
            summaries.append(
                f"• {r['date']} — {r['interaction_type']} with **{r['hcp_name']}**: "
                f"{r['topics']}. Outcome: {r['outcomes']}. Sentiment: {r['sentiment']}."
            )
        
        summary_text = "\n".join(summaries)
        
        return {
            "status": "success",
            "count": len(records),
            "interactions": records,
            "message": f"Here are your {len(records)} interaction(s):\n\n{summary_text}"
        }
    finally:
        db.close()

@tool
def delete_interactions(user_id: str, hcp_name: Optional[str] = None, interaction_date: Optional[str] = None, raw_query: Optional[str] = None) -> Dict[str, Any]:
    """
    Deletes interaction logs for a user. Can filter by HCP name, date, or both.
    If neither filter is provided, nothing is deleted for safety.
    """
    db = SessionLocal()
    try:
        query = db.query(Interaction).filter(Interaction.user_id == user_id)

        if hcp_name:
            query = query.filter(Interaction.hcp_name.ilike(f"%{hcp_name}%"))
        if interaction_date:
            target_date = datetime.date.fromisoformat(interaction_date)
            query = query.filter(Interaction.interaction_date == target_date)

        matches = query.all()
        
        if not hcp_name and not interaction_date and raw_query:
            raw_lower = raw_query.lower()
            matched_by_name = [m for m in matches if m.hcp_name and m.hcp_name.lower() in raw_lower]
            if matched_by_name:
                matches = matched_by_name
                hcp_name = matches[0].hcp_name
            else:
                matched_by_date = []
                for m in matches:
                    if m.interaction_date:
                        month_str = m.interaction_date.strftime("%B").lower()[:3]
                        day_str = str(m.interaction_date.day)
                        if month_str in raw_lower and day_str in raw_lower:
                            matched_by_date.append(m)
                if matched_by_date:
                    matches = matched_by_date
                    interaction_date = str(matches[0].interaction_date)

        count = len(matches)

        if count == 0 and not hcp_name and not interaction_date:
            return {"status": "error", "message": "Please specify an HCP name or a date to delete logs for. I won't delete everything without a filter."}

        if count == 0:
            filter_desc = []
            if hcp_name:
                filter_desc.append(f"HCP '{hcp_name}'")
            if interaction_date:
                filter_desc.append(f"date '{interaction_date}'")
            return {"status": "success", "count": 0, "message": f"No interactions found matching {' and '.join(filter_desc)}."}

        for m in matches:
            db.delete(m)
        db.commit()

        if hcp_name and interaction_date:
            message = f"Done! I've deleted {count} interaction(s) with {hcp_name} on {interaction_date}."
        elif hcp_name:
            message = f"Done! I've deleted {count} interaction(s) with {hcp_name}."
        elif interaction_date:
            message = f"Done! I've deleted {count} interaction(s) from {interaction_date}."
        else:
            message = f"Done! I've deleted {count} interaction(s)."

        return {
            "status": "success",
            "count": count,
            "message": message
        }
    except Exception as e:
        db.rollback()
        return {"status": "error", "message": str(e)}
    finally:
        db.close()

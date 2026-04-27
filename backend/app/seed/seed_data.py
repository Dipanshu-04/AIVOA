"""
Database seeding script to load demo_data.json into the database.
"""
import json
import os
import sys
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import text

# Add the project root to the path so we can import app modules if run as a script
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.db.session import SessionLocal, engine, Base
from app.models.hcp import HCP
from app.models.interaction import Interaction
from app.models.material import Material, Sample
from app.models.follow_up import FollowUp
from app.models.user import User

def load_json(filepath: str) -> dict:
    """Loads seed data from the JSON file."""
    with open(filepath, "r") as f:
        return json.load(f)

def seed_database():
    """Reads demo_data.json and inserts records into the database."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, "demo_data.json")
    
    data = load_json(json_path)
    
    # Ensure all tables defined via models are created
    Base.metadata.create_all(bind=engine)
    
    db: Session = SessionLocal()
    
    try:
        print("Seeding Users...")
        for user_data in data["users"]:
            user = User(**user_data)
            db.merge(user)
        
        print("Seeding HCPs...")
        for hcp_data in data["hcps"]:
            hcp = HCP(**hcp_data)
            db.merge(hcp)
            
        print("Seeding Materials...")
        for mat_data in data["materials"]:
            mat = Material(**mat_data)
            db.merge(mat)
            
        print("Seeding Samples...")
        for sam_data in data["samples"]:
            if "expiry_date" in sam_data and sam_data["expiry_date"]:
                sam_data["expiry_date"] = datetime.strptime(sam_data["expiry_date"], "%Y-%m-%d").date()
            sam = Sample(**sam_data)
            db.merge(sam)
            
        print("Seeding Interactions...")
        for int_data in data["interactions"]:
            if "interaction_date" in int_data and int_data["interaction_date"]:
                int_data["interaction_date"] = datetime.strptime(int_data["interaction_date"], "%Y-%m-%d").date()
            if "interaction_time" in int_data and int_data["interaction_time"]:
                int_data["interaction_time"] = datetime.strptime(int_data["interaction_time"], "%H:%M").time()
            interaction = Interaction(**int_data)
            db.merge(interaction)
            
        print("Seeding Follow-Ups...")
        for fu_data in data["follow_ups"]:
            if "due_date" in fu_data and fu_data["due_date"]:
                fu_data["due_date"] = datetime.strptime(fu_data["due_date"], "%Y-%m-%d").date()
            fu = FollowUp(**fu_data)
            db.merge(fu)
            
        db.commit()
        print("Database seeded successfully!")
        
    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()

# ---
# Explanation:
# The `seed_data.py` script reads from `demo_data.json` to populate the database with realistic demo data.
# This ensures that all 5 LangGraph tools (search HCPs, add materials, etc.) 
# have realistic context to query against during application demonstrations.

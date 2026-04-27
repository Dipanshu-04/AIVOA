"""
Assumptions:
- Using SQLAlchemy 2.0 style syntax.
- The `Base` declarative class will be defined in `app.db.base`.
- Assuming standard `uuid4` generation for IDs to support MySQL VARCHAR(36) primary keys easily.
"""
import uuid
from datetime import datetime
from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

# from app.db.base import Base  # Assuming this exists based on project structure
from app.db.session import Base

class HCP(Base):
    __tablename__ = "hcps"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    specialty: Mapped[str | None] = mapped_column(String(100))
    email: Mapped[str | None] = mapped_column(String(255), unique=True)
    phone: Mapped[str | None] = mapped_column(String(50))
    location: Mapped[str | None] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # interactions = relationship("Interaction", back_populates="hcp")

# ---
# Explanation: 
# This file fits into the project as the database model representing a Health Care Professional. 
# It ensures our backend can store and retrieve the master data for HCPs securely using SQLAlchemy.

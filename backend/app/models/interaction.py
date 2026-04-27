"""
Assumptions:
- Using SQLAlchemy 2.0 style syntax.
- The `Base` declarative class is available in `app.db.base`.
- Related models like HCP and FollowUp are imported as strings for relationship setup.
"""
import uuid
from datetime import date, time, datetime
from typing import Optional
from sqlalchemy import String, Text, Date, Time, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

# from app.db.base import Base
from app.db.session import Base

class Interaction(Base):
    __tablename__ = "interactions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    hcp_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("hcps.id", ondelete="SET NULL"))
    hcp_name: Mapped[Optional[str]] = mapped_column(String(255))
    interaction_type: Mapped[Optional[str]] = mapped_column(String(50))
    interaction_date: Mapped[Optional[date]] = mapped_column(Date)
    interaction_time: Mapped[Optional[time]] = mapped_column(Time)
    attendees: Mapped[Optional[str]] = mapped_column(Text)
    topics_discussed: Mapped[Optional[str]] = mapped_column(Text)
    materials_shared: Mapped[Optional[str]] = mapped_column(Text)
    samples_distributed: Mapped[Optional[str]] = mapped_column(Text)
    sentiment: Mapped[Optional[str]] = mapped_column(String(50))
    outcomes: Mapped[Optional[str]] = mapped_column(Text)
    follow_ups: Mapped[Optional[str]] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(20), default="DRAFT", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # hcp = relationship("HCP", back_populates="interactions")
    # follow_ups = relationship("FollowUp", back_populates="interaction", cascade="all, delete-orphan")

# ---
# Explanation: 
# This file is the core database model for the application. It represents both the draft state 
# being actively edited by the AI agent and the finalized, logged interactions.

"""
Assumptions:
- Including Sample model in this file as they represent shared resources context.
"""
import uuid
from datetime import date, datetime
from sqlalchemy import String, Text, DateTime, Date
from sqlalchemy.orm import Mapped, mapped_column

# from app.db.base import Base
from app.db.session import Base

class Material(Base):
    __tablename__ = "materials"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    type: Mapped[str | None] = mapped_column(String(50))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class Sample(Base):
    __tablename__ = "samples"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    lot_number: Mapped[str | None] = mapped_column(String(100))
    expiry_date: Mapped[date | None] = mapped_column(Date)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

# ---
# Explanation: 
# This file stores master data schemas for Materials and Samples that can be 
# suggested by the AI agent and distributed to HCPs during interactions.

"""
Assumptions:
- Using Pydantic V2
"""
from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional
from datetime import datetime

class HCPBase(BaseModel):
    first_name: str
    last_name: str
    specialty: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    location: Optional[str] = None

class HCPCreate(HCPBase):
    pass

class HCPResponse(HCPBase):
    id: str
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# ---
# Explanation: 
# This schema file is responsible for request and response validation for HCP endpoints,
# decoupling the API's interface from internal SQLAlchemy representations.

# models.py

from datetime import datetime
from typing import Dict, Literal, Optional
from uuid import UUID

from pydantic import BaseModel

# -----------------------------
# API Models
# -----------------------------

class RegisterRequest(BaseModel):
    category: Literal["activity_provider", "semantic_label", "analyzer", "llm"]
    name: str
    description: str
    schema: Optional[Dict] = None
    cookie: Optional[Dict] = None

class RegisterResponse(BaseModel):
    uuid: UUID
    registered_at: datetime

class ResolveResponse(BaseModel):
    uuid: UUID
    cookie: Optional[Dict] = None

class PropertiesRequest(BaseModel):
    uuid: UUID
    category: str
    properties: Dict
    cookie: Optional[Dict] = None

class PropertiesResponse(BaseModel):
    uuid: UUID
    category: str
    properties: Dict
    cookie: Optional[Dict]
    updated_at: datetime

# -----------------------------
# Internal Model
# -----------------------------

class RegistryEntry(BaseModel):
    uuid: UUID
    category: str
    name: str
    description: str
    schema: Optional[Dict]
    cookie: Optional[Dict]
    version: int
    registered_at: datetime
    deprecated: bool

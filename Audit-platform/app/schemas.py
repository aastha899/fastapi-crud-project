from pydantic import BaseModel
from datetime import datetime

class AuditCreate(BaseModel):
    title: str
    owner: str
    status: str = "OPEN"

class AuditUpdate(BaseModel):
    title: str | None = None
    owner: str | None = None
    status: str | None = None

class AuditOut(BaseModel):
    id: int
    title: str
    owner: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
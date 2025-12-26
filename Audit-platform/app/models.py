from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from .database import Base

class AuditRecord(Base):
    __tablename__ = "audit_records"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    status = Column(String, default="OPEN")   # OPEN / IN_REVIEW / CLOSED
    owner = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
import uuid
from datetime import datetime
from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from app.config.database import Base

class __Resource__(Base):
    __tablename__ = "__resource__s"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, index=True)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    
    # Add your columns here
    name = Column(String(100), nullable=True)

    def __repr__(self):
        return f"<__Resource__(id={self.id})>"

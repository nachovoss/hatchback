from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict

class __Resource__Base(BaseModel):
    name: Optional[str] = None

class __Resource__Create(__Resource__Base):
    pass

class __Resource__Update(__Resource__Base):
    pass

class __Resource__Response(__Resource__Base):
    id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

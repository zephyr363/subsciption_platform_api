from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class SessionList(BaseModel):
    id: UUID
    device_id: UUID
    user_id: UUID
    expires_at: datetime
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class SessionCreate(BaseModel):
    user_id: UUID
    device_id: Optional[UUID] = None
    model_config = ConfigDict(from_attributes=True)


class SessionUpdate(BaseModel):
    expires_at: Optional[datetime] = None
    device_id: Optional[UUID] = None

    model_config = ConfigDict(from_attributes=True)

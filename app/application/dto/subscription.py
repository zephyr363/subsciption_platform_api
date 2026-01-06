from uuid import UUID
from pydantic import BaseModel

from app.infrastructure.models.sqla import SubscriptionStatus


class SubscriptionBase(BaseModel):
    id: UUID
    user_id: UUID
    plan_id: UUID
    status: SubscriptionStatus


class SubscriptionCreate(BaseModel):
    user_id: UUID
    plan_id: UUID

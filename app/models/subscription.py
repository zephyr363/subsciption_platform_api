from .base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import UUID, ForeignKey, Enum as SQLAEnum
from enum import Enum
import uuid

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .plan import Plan
    from .user import User


class SubscriptionStatus(Enum):
    TRIAL = "trial"
    ACTIVE = "active"
    INACTIVE = "inactive"
    EXPIRED = "expired"
    CANCELLED = "cancelled"


class Subscription(Base):
    __tablename__ = "subscriptions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id"),
    )
    plan_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("plans.id"),
    )
    status: Mapped[SubscriptionStatus] = mapped_column(
        SQLAEnum(SubscriptionStatus),
        nullable=False,
    )

    user: Mapped["User"] = relationship(back_populates="subsciptions")
    plan: Mapped["Plan"] = relationship(back_populates="subscriptions")

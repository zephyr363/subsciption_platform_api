import uuid
from decimal import Decimal
from typing import TYPE_CHECKING, List

from sqlalchemy import UUID, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .subscription import Subscription


class Plan(Base):
    __tablename__ = "plans"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )
    features: Mapped[str] = mapped_column(
        String(600),
        nullable=False,
    )
    duration_days: Mapped[int] = mapped_column(
        nullable=False,
    )
    is_active: Mapped[bool] = mapped_column(
        default=True,
    )
    is_trial: Mapped[bool] = mapped_column(
        default=False,
    )

    subscriptions: Mapped[List["Subscription"]] = relationship(back_populates="plan")

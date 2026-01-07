import uuid
from datetime import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import UUID, DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .session import Session
    from .subscription import Subscription


class User(Base):
    __tablename__ = "users"
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    first_name: Mapped[str] = mapped_column(
        String(length=255),
        nullable=True,
        default="",
    )
    last_name: Mapped[str] = mapped_column(
        String(length=255),
        nullable=True,
        default="",
    )
    email: Mapped[str] = mapped_column(
        nullable=False,
        unique=True,
    )
    password_hash: Mapped[str] = mapped_column(
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    is_active: Mapped[bool] = mapped_column(
        default=True,
    )
    is_staff: Mapped[bool] = mapped_column(
        default=False,
    )
    is_superuser: Mapped[bool] = mapped_column(
        default=False,
    )

    sessions: Mapped[List["Session"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )

    subscriptions: Mapped[List["Subscription"]] = relationship(back_populates="user")

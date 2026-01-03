import uuid
from datetime import datetime, UTC
from sqlalchemy import UUID, DateTime, ForeignKey
from .base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User


class Session(Base):
    __tablename__ = "sessions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE")
    )
    device_id: Mapped[uuid.UUID] = mapped_column(
        unique=True,
        default=uuid.uuid4,
    )
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now(UTC),
    )

    user: Mapped["User"] = relationship(
        back_populates="sessions",
    )

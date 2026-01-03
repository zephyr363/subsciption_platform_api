from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import UUID, String
import uuid
from .base import Base
from typing import TYPE_CHECKING, List

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

    sessions: Mapped[List["Session"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )

    subsciptions: Mapped[List["Subscription"]] = relationship(back_populates="plan")

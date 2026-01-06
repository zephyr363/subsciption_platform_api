from dataclasses import dataclass
from datetime import datetime, timedelta
from uuid import UUID, uuid4
from app.config import settings


@dataclass
class SessionEntity:
    id: UUID
    user_id: UUID
    device_id: UUID
    created_at: datetime
    expires_at: datetime

    @classmethod
    def create(
        cls,
        user_id: UUID,
        device_id: UUID,
    ) -> "SessionEntity":
        created_at = datetime.now()
        expires_at = created_at + timedelta(seconds=settings.auth.cookie_max_age)
        return cls(
            id=uuid4(),
            user_id=user_id,
            device_id=device_id,
            created_at=created_at,
            expires_at=expires_at,
        )

    def is_expired(self) -> bool:
        return datetime.now() > self.expires_at

    def refresh_expiry(self) -> None:
        self.expires_at = datetime.now() + timedelta(
            seconds=settings.auth.cookie_max_age
        )

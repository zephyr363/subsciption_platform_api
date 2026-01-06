from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import UUID, uuid4


@dataclass
class UserEntity:
    id: UUID
    email: str
    password_hash: str
    created_at: datetime
    first_name: str = ""
    last_name: str = ""
    is_active: bool = True
    is_staff: bool = False
    is_superuser: bool = False

    @classmethod
    def create(
        cls,
        email: str,
        password_hash: str,
        first_name: str = "",
        last_name: str = "",
        is_active: bool = True,
        is_staff: bool = False,
        is_superuser: bool = False,
    ) -> "UserEntity":
        return cls(
            id=uuid4(),
            email=email,
            password_hash=password_hash,
            first_name=first_name,
            last_name=last_name,
            is_active=is_active,
            is_staff=is_staff,
            is_superuser=is_superuser,
            created_at=datetime.now(UTC),
        )

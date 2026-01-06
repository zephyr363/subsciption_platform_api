from abc import ABC, abstractmethod
from typing import Optional


from app.domain.entities.user import UserEntity


class IUserRepository(ABC):
    @abstractmethod
    async def save(
        self,
        entity: UserEntity,
    ) -> UserEntity: ...

    @abstractmethod
    async def get_by_email(
        self,
        email: str,
    ) -> Optional[UserEntity]: ...

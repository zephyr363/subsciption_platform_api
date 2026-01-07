from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities.session import SessionEntity


class ISessionRepository(ABC):
    @abstractmethod
    async def save(
        self,
        entity: SessionEntity,
    ) -> SessionEntity: ...

    @abstractmethod
    async def get(
        self,
        session_id: UUID,
    ) -> SessionEntity: ...

    @abstractmethod
    async def get_by_device_id(
        self,
        device_id: UUID,
    ) -> SessionEntity: ...

    @abstractmethod
    async def update(
        self,
        entity: SessionEntity,
    ) -> SessionEntity: ...

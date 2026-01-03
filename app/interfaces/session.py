from abc import ABC, abstractmethod
from uuid import UUID

from app.dto.session import SessionCreate, SessionList, SessionUpdate


class ISessionRepository(ABC):
    @abstractmethod
    async def create(
        self,
        payload: SessionCreate,
    ) -> SessionList: ...

    @abstractmethod
    async def get(
        self,
        session_id: UUID,
    ) -> SessionList | None: ...

    @abstractmethod
    async def get_by_device_id(
        self,
        device_id: UUID,
    ) -> SessionList | None: ...

    @abstractmethod
    async def update(
        self,
        session_id: UUID,
        payload: SessionUpdate,
    ) -> SessionList: ...

from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from app.domain.entities.subscription import SubscriptionEntity


class ISubscriptionRepository(ABC):
    @abstractmethod
    async def save(self, entity: SubscriptionEntity) -> SubscriptionEntity: ...

    @abstractmethod
    async def get_active_by_user(
        self, user_id: UUID
    ) -> Optional[SubscriptionEntity]: ...

from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from app.domain.entities.plan import PlanEntity


class IPlanRepository(ABC):
    @abstractmethod
    async def save(self, entity: PlanEntity) -> PlanEntity:
        pass

    @abstractmethod
    async def get_by_id(self, plan_id: UUID) -> Optional[PlanEntity]:
        pass

    @abstractmethod
    async def get_trial_plan(self) -> Optional[PlanEntity]:
        pass

from typing import Optional
from uuid import UUID

from sqlalchemy import select
from app.domain.entities import PlanEntity
from app.domain.interfaces.plan import IPlanRepository

from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.models.sqla import Plan


class PlanRepositoryImpl(IPlanRepository):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def save(
        self,
        entity: PlanEntity,
    ) -> PlanEntity:
        plan = Plan(
            id=entity.id,
            name=entity.name,
            description=entity.features,
            price=entity.price,
            duration_days=entity.duration_days,
            is_trial=entity.is_trial,
            is_active=entity.is_active,
        )
        self.db_session.add(plan)
        await self.db_session.commit()
        await self.db_session.refresh(plan)
        return PlanEntity(
            id=plan.id,
            name=plan.name,
            features=plan.features,
            price=plan.price,
            duration_days=plan.duration_days,
            is_trial=plan.is_trial,
            is_active=plan.is_active,
        )

    async def get_by_id(self, plan_id: UUID) -> Optional[PlanEntity]:
        result = await self.db_session.get(Plan, plan_id)
        if result:
            return PlanEntity(
                id=result.id,
                name=result.name,
                features=result.features,
                price=result.price,
                duration_days=result.duration_days,
                is_trial=result.is_trial,
                is_active=result.is_active,
            )

    async def get_trial_plan(self) -> Optional[PlanEntity]:
        query = await self.db_session.execute(
            select(Plan).where(Plan.is_trial & Plan.is_active)
        )
        result = query.scalars().first()
        if result:
            return PlanEntity(
                id=result.id,
                name=result.name,
                features=result.features,
                price=result.price,
                duration_days=result.duration_days,
                is_trial=result.is_trial,
                is_active=result.is_active,
            )

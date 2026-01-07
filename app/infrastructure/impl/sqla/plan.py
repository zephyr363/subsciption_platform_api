from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities import PlanEntity
from app.domain.interfaces.plan import IPlanRepository
from app.infrastructure.exceptions import PlanNotFoundError
from app.infrastructure.mappers.sqla import PlanMapping
from app.infrastructure.models.sqla import Plan


class PlanRepositoryImpl(IPlanRepository):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def save(
        self,
        entity: PlanEntity,
    ) -> PlanEntity:
        plan = PlanMapping.to_orm(entity)
        self.db_session.add(plan)
        return PlanMapping.from_orm(plan)

    async def get_by_id(self, plan_id: UUID) -> PlanEntity:
        result = await self.db_session.get(Plan, plan_id)
        if not result:
            raise PlanNotFoundError("PLan not found")
        return PlanMapping.from_orm(result)

    async def get_trial_plan(self) -> PlanEntity:
        query = await self.db_session.execute(
            select(Plan).where(Plan.is_trial & Plan.is_active)
        )
        try:
            res = query.scalar_one()
        except NoResultFound:
            raise PlanNotFoundError("Plan not found")
        return PlanMapping.from_orm(res)

from app.domain.entities import PlanEntity
from app.domain.interfaces.plan import IPlanRepository
from app.application.dto.plan import PlanCreate


class CreatePlanUseCase:
    def __init__(self, plan_repo: IPlanRepository):
        self.plan_repo = plan_repo

    async def execute(self, payload: PlanCreate):
        return await self.plan_repo.save(PlanEntity.create(**payload.model_dump()))

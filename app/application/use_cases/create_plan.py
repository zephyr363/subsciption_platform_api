from app.application.dto.plan import PlanCreate
from app.application.ports.uow import IUnitOfWork
from app.domain.entities import PlanEntity
from app.domain.interfaces.plan import IPlanRepository


class CreatePlanUseCase:
    def __init__(self, uow: IUnitOfWork, plan_repo: IPlanRepository):
        self.uow = uow
        self.plan_repo = plan_repo

    async def execute(
        self,
        payload: PlanCreate,
    ):
        try:
            res = await self.plan_repo.save(
                PlanEntity.create(
                    **payload.model_dump(),
                ),
            )
            await self.uow.commit()
            return res
        except Exception as e:
            await self.uow.rollback()
            raise e

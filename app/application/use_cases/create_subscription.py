from uuid import UUID

from app.application.ports.uow import IUnitOfWork
from app.domain.entities.subscription import SubscriptionEntity
from app.domain.interfaces.plan import IPlanRepository
from app.domain.interfaces.subscription import ISubscriptionRepository


class CreateTrialSubscriptionUseCase:
    def __init__(
        self,
        uow: IUnitOfWork,
        subscription_repo: ISubscriptionRepository,
        plan_repo: IPlanRepository,
    ):
        self.uow = uow
        self.subscription_repo = subscription_repo
        self.plan_repo = plan_repo

    async def execute(self, user_id: UUID) -> SubscriptionEntity:
        try:
            plan = await self.plan_repo.get_trial_plan()
            subscription = SubscriptionEntity.create_trial(
                user_id=user_id,
                plan=plan,
            )
            await self.subscription_repo.save(subscription)
            await self.uow.commit()
            return subscription
        except Exception as e:
            await self.uow.rollback()
            raise e

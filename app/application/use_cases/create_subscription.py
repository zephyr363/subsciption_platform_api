from uuid import UUID
from app.domain.entities.subscription import SubscriptionEntity
from app.domain.exceptions.plan import TrialPlanNotFound
from app.domain.exceptions.subscription import ActiveSubscriptionExists
from app.domain.interfaces.plan import IPlanRepository
from app.domain.interfaces.subscription import ISubscriptionRepository


class CreateTrialSubscriptionUseCase:
    def __init__(
        self,
        subscription_repo: ISubscriptionRepository,
        plan_repo: IPlanRepository,
    ):
        self.subscription_repo = subscription_repo
        self.plan_repo = plan_repo

    async def execute(self, user_id: UUID) -> SubscriptionEntity:
        active = await self.subscription_repo.get_active_by_user(user_id)
        if active:
            raise ActiveSubscriptionExists("User already has an active subscription")

        plan = await self.plan_repo.get_trial_plan()
        if not plan:
            raise TrialPlanNotFound("Trial plan not found")

        subscription = SubscriptionEntity.create_trial(
            user_id=user_id,
            plan=plan,
        )

        await self.subscription_repo.save(subscription)

        return subscription

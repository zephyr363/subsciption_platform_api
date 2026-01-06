from typing import Optional
from uuid import UUID
from sqlalchemy import select
from app.domain.entities.subscription import SubscriptionEntity
from app.domain.interfaces.subscription import ISubscriptionRepository

from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.models.sqla import Subscription


class SubscriptionRepositoryImpl(ISubscriptionRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def save(self, entity: SubscriptionEntity) -> SubscriptionEntity:
        subscription = Subscription(
            id=entity.id,
            user_id=entity.user_id,
            plan_id=entity.plan_id,
            status=entity.status,
            started_at=entity.started_at,
            ends_at=entity.ends_at,
        )
        self.session.add(subscription)
        await self.session.commit()
        await self.session.refresh(subscription)
        return SubscriptionEntity(
            id=subscription.id,
            user_id=subscription.user_id,
            plan_id=subscription.plan_id,
            status=subscription.status,
            started_at=subscription.started_at,
            ends_at=subscription.ends_at,
        )

    async def get_active_by_user(self, user_id: UUID) -> Optional[SubscriptionEntity]:
        stmt = select(Subscription).where(Subscription.user_id == user_id)
        res = await self.session.execute(stmt)
        subscription = res.scalar_one_or_none()
        return (
            SubscriptionEntity(
                id=subscription.id,
                user_id=subscription.user_id,
                plan_id=subscription.plan_id,
                status=subscription.status,
                started_at=subscription.started_at,
                ends_at=subscription.ends_at,
            )
            if subscription
            else None
        )

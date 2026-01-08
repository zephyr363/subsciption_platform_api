from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, NoResultFound, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.subscription import SubscriptionEntity
from app.domain.interfaces.subscription import ISubscriptionRepository
from app.infrastructure.exceptions import (
    SubscriptionAlreadyExistsError,
    SubscriptionNotFoundError,
    SubscriptionSaveError,
)
from app.infrastructure.mappers.sqla import SubscriptionMapping
from app.infrastructure.models.sqla import Subscription


class SubscriptionRepositoryImpl(ISubscriptionRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def save(self, entity: SubscriptionEntity) -> SubscriptionEntity:
        subscription = SubscriptionMapping.to_orm(entity)
        self.session.add(subscription)
        try:
            await self.session.flush()
        except IntegrityError as e:
            raise SubscriptionAlreadyExistsError("Subscription already exists") from e
        except SQLAlchemyError as e:
            raise SubscriptionSaveError("Failed to create subscription") from e

        return entity

    async def get_active_by_user(
        self,
        user_id: UUID,
    ) -> SubscriptionEntity:
        stmt = select(Subscription).where(Subscription.user_id == user_id)
        res = await self.session.execute(stmt)
        try:
            subscription = res.scalar_one()
        except NoResultFound as err:
            raise SubscriptionNotFoundError("Subscription not found") from err
        return SubscriptionMapping.from_orm(subscription)

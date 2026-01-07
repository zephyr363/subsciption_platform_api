from app.domain.entities import SubscriptionEntity
from app.infrastructure.models.sqla import Subscription

from .base import BaseSQLAMapping


class SubscriptionMapping(BaseSQLAMapping[Subscription, SubscriptionEntity]):
    @staticmethod
    def from_orm(orm_obj: Subscription) -> SubscriptionEntity:
        return SubscriptionEntity(
            id=orm_obj.id,
            user_id=orm_obj.user_id,
            plan_id=orm_obj.plan_id,
            status=orm_obj.status,
            started_at=orm_obj.started_at,
            ends_at=orm_obj.ends_at,
        )

    @staticmethod
    def to_orm(entity: SubscriptionEntity) -> Subscription:
        return Subscription(
            id=entity.id,
            user_id=entity.user_id,
            plan_id=entity.plan_id,
            status=entity.status,
            started_at=entity.started_at,
            ends_at=entity.ends_at,
        )

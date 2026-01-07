from app.domain.entities import PlanEntity
from app.infrastructure.models.sqla import Plan

from .base import BaseSQLAMapping


class PlanMapping(BaseSQLAMapping[Plan, PlanEntity]):
    @staticmethod
    def from_orm(orm_obj: Plan) -> PlanEntity:
        return PlanEntity(
            id=orm_obj.id,
            name=orm_obj.name,
            features=orm_obj.features,
            price=orm_obj.price,
            duration_days=orm_obj.duration_days,
            is_active=orm_obj.is_active,
            is_trial=orm_obj.is_trial,
        )

    @staticmethod
    def to_orm(entity: PlanEntity) -> Plan:
        return Plan(
            id=entity.id,
            name=entity.name,
            features=entity.features,
            price=entity.price,
            duration_days=entity.duration_days,
            is_active=entity.is_active,
            is_trial=entity.is_trial,
        )

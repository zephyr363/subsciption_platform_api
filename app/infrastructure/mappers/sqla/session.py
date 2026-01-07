from app.domain.entities import SessionEntity
from app.infrastructure.models.sqla import Session

from .base import BaseSQLAMapping


class SessionMapping(BaseSQLAMapping[Session, SessionEntity]):
    @staticmethod
    def from_orm(orm_obj: Session) -> SessionEntity:
        return SessionEntity(
            id=orm_obj.id,
            user_id=orm_obj.user_id,
            device_id=orm_obj.device_id,
            expires_at=orm_obj.expires_at,
            created_at=orm_obj.created_at,
        )

    @staticmethod
    def to_orm(entity: SessionEntity) -> Session:
        return Session(
            id=entity.id,
            user_id=entity.user_id,
            device_id=entity.device_id,
            expires_at=entity.expires_at,
            created_at=entity.created_at,
        )

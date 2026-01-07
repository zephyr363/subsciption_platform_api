from app.domain.entities import UserEntity
from app.infrastructure.models.sqla.user import User

from .base import BaseSQLAMapping


class UserMapping(BaseSQLAMapping[User, UserEntity]):
    @staticmethod
    def from_orm(orm_obj: User) -> UserEntity:
        return UserEntity(
            id=orm_obj.id,
            email=orm_obj.email,
            password_hash=orm_obj.password_hash,
            is_active=orm_obj.is_active,
            is_staff=orm_obj.is_staff,
            is_superuser=orm_obj.is_superuser,
            created_at=orm_obj.created_at,
        )

    @staticmethod
    def to_orm(entity: UserEntity) -> User:
        return User(
            id=entity.id,
            email=entity.email,
            password_hash=entity.password_hash,
            is_active=entity.is_active,
            is_staff=entity.is_staff,
            is_superuser=entity.is_superuser,
            created_at=entity.created_at,
        )

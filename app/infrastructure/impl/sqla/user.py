from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities import UserEntity
from app.domain.exceptions.user import UserAlreadyExists
from app.domain.interfaces.user import IUserRepository
from app.infrastructure.models.sqla import User

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError


class UserRepositoryImpl(IUserRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def save(
        self,
        entity: UserEntity,
    ) -> UserEntity:
        user = User(
            id=entity.id,
            email=entity.email,
            first_name=entity.first_name,
            last_name=entity.last_name,
            password_hash=entity.password_hash,
            is_active=entity.is_active,
            is_staff=entity.is_staff,
            is_superuser=entity.is_superuser,
            created_at=entity.created_at,
        )
        self.session.add(user)
        try:
            await self.session.commit()
        except IntegrityError as err:
            await self.session.rollback()
            if "users_email_key" in str(err.orig):
                raise UserAlreadyExists("User with this email already exists") from err
        await self.session.refresh(user)
        return UserEntity(
            id=user.id,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            password_hash=user.password_hash,
            is_active=user.is_active,
            is_staff=user.is_staff,
            is_superuser=user.is_superuser,
            created_at=user.created_at,
        )

    async def get_by_email(self, email: str) -> Optional[UserEntity]:
        stmt = select(User).where(User.email == email)

        res = await self.session.execute(stmt)
        user = res.scalar_one_or_none()

        if user:
            return UserEntity(
                id=user.id,
                email=user.email,
                first_name=user.first_name,
                last_name=user.last_name,
                password_hash=user.password_hash,
                is_active=user.is_active,
                is_staff=user.is_staff,
                is_superuser=user.is_superuser,
                created_at=user.created_at,
            )

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities import UserEntity
from app.domain.interfaces.user import IUserRepository
from app.infrastructure.exceptions import UserAlreadyExistsError, UserNotFoundError
from app.infrastructure.mappers.sqla.user import UserMapping
from app.infrastructure.models.sqla import User


class UserRepositoryImpl(IUserRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def save(self, entity: UserEntity) -> UserEntity:
        user = UserMapping.to_orm(entity)
        self.session.add(user)
        try:
            await self.session.flush()
        except IntegrityError as e:
            if "users_email_key" in str(e):
                raise UserAlreadyExistsError(
                    "User with this email already exists"
                ) from e
        return UserMapping.from_orm(user)

    async def get_by_email(self, email: str) -> UserEntity:
        stmt = select(User).where(User.email == email)

        res = await self.session.execute(stmt)

        try:
            user = res.scalar_one()
        except NoResultFound:
            raise UserNotFoundError("User not found")
        return UserMapping.from_orm(user)

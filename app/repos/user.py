from sqlalchemy.ext.asyncio import AsyncSession

from app.dto.user import UserCreate, UserList
from app.interfaces.user import IUserRepository
from app.models import User

from sqlalchemy import select


class UserRepositoryImpl(IUserRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(
        self,
        payload: UserCreate,
    ) -> UserList:
        user = User(**payload.model_dump(exclude={"password"}))
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return UserList.model_validate(user)

    async def get_by_email(self, email: str) -> UserList | None:
        stmt = select(User).where(User.email == email)

        res = await self.session.execute(stmt)
        user = res.scalar_one_or_none()

        if user:
            return UserList.model_validate(user)

from abc import ABC, abstractmethod


from app.dto.user import UserCreate, UserList


class IUserRepository(ABC):
    @abstractmethod
    async def create(
        self,
        payload: UserCreate,
    ) -> UserList: ...

    @abstractmethod
    async def get_by_email(
        self,
        email: str,
    ) -> UserList | None: ...

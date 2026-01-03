from app.dto.user import UserCreate
from app.interfaces.user import IUserRepository


class CreateUserUseCase:
    def __init__(
        self,
        repo: IUserRepository,
    ) -> None:
        self.repo = repo

    async def execute(
        self,
        payload: UserCreate,
    ):
        return await self.repo.create(payload)

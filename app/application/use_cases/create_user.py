from app.application.dto.user import UserCreate
from app.domain.entities import UserEntity
from app.domain.interfaces.user import IUserRepository
from app.utils import hash_psw


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
        password_hash = hash_psw(payload.password)
        user = UserEntity.create(
            email=payload.email,
            password_hash=password_hash,
            first_name=payload.first_name,
            last_name=payload.last_name,
        )
        return await self.repo.save(user)

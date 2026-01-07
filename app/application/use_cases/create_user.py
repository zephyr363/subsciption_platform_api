from app.application.dto.user import UserCreate
from app.application.ports.uow import IUnitOfWork
from app.domain.entities import UserEntity
from app.domain.interfaces.user import IUserRepository
from app.utils import hash_psw


class CreateUserUseCase:

    def __init__(
        self,
        uow: IUnitOfWork,
        repo: IUserRepository,
    ) -> None:
        self.uow = uow
        self.repo = repo

    async def execute(
        self,
        payload: UserCreate,
    ):
        try:
            password_hash = hash_psw(payload.password)
            user = UserEntity.create(
                email=payload.email,
                password_hash=password_hash,
                first_name=payload.first_name,
                last_name=payload.last_name,
            )
            res = await self.repo.save(user)
            await self.uow.commit()
            return res
        except Exception as err:
            await self.uow.rollback()
            raise err

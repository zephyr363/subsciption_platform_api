from uuid import UUID

from app.application.dto.user import UserLogin
from app.application.ports.uow import IUnitOfWork
from app.domain.entities.session import SessionEntity
from app.domain.interfaces.session import ISessionRepository
from app.domain.interfaces.user import IUserRepository


class UserSessionLoginUseCase:

    def __init__(
        self,
        uow: IUnitOfWork,
        session_repo: ISessionRepository,
        user_repo: IUserRepository,
    ) -> None:
        self.session_repo = session_repo
        self.user_repo = user_repo
        self.uow = uow

    async def execute(
        self,
        device_id: UUID | None,
        payload: UserLogin,
    ) -> SessionEntity:
        try:
            user = await self.user_repo.get_by_email(payload.email)
            if device_id:
                old_session = await self.session_repo.get_by_device_id(device_id)
                old_session.refresh_expiry()
                return await self.session_repo.update(old_session)

            res = await self.session_repo.save(
                SessionEntity.create(
                    user_id=user.id,
                )
            )
            await self.uow.commit()
            return res
        except Exception as e:
            await self.uow.rollback()
            raise e

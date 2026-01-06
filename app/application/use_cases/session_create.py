from uuid import UUID
from app.application.dto.user import UserLogin
from app.domain.entities.session import SessionEntity
from app.domain.exceptions.user import UserNotFound
from app.domain.interfaces.session import ISessionRepository
from app.domain.interfaces.user import IUserRepository


class UserSessionLoginUseCase:

    def __init__(
        self,
        session_repo: ISessionRepository,
        user_repo: IUserRepository,
    ) -> None:
        self.session_repo = session_repo
        self.user_repo = user_repo

    async def execute(
        self,
        device_id: UUID,
        payload: UserLogin,
    ) -> SessionEntity:
        user = await self.user_repo.get_by_email(payload.email)

        if not user:
            raise UserNotFound("User not found")

        old_session = await self.session_repo.get_by_device_id(device_id)
        if old_session:
            old_session.refresh_expiry()
            return await self.session_repo.update(old_session)

        return await self.session_repo.save(
            SessionEntity.create(
                user_id=user.id,
                device_id=device_id,
            )
        )

from datetime import UTC, datetime, timedelta
from uuid import UUID
from app.dto.session import SessionCreate, SessionList, SessionUpdate
from app.dto.user import UserLogin
from app.exceptions.user import UserNotFound
from app.interfaces.session import ISessionRepository
from app.interfaces.user import IUserRepository
from app.config import settings


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
    ) -> SessionList:
        user = await self.user_repo.get_by_email(payload.email)

        if not user:
            raise UserNotFound("User not found")

        old_session = await self.session_repo.get_by_device_id(device_id)
        if old_session:
            return await self.session_repo.update(
                old_session.id,
                SessionUpdate(
                    expires_at=datetime.now(UTC)
                    + timedelta(settings.auth.cookie_max_age),
                ),
            )

        session_payload = SessionCreate(user_id=user.id)

        return await self.session_repo.create(session_payload)

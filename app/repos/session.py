from uuid import UUID
from app.dto.session import SessionCreate, SessionList, SessionUpdate
from app.exceptions.session import SessionNotFound
from app.interfaces.session import ISessionRepository
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, UTC, timedelta
from app.models import Session
from sqlalchemy import select
from app.config import settings


class SessionRepositoryImpl(ISessionRepository):
    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        self.session = session

    async def create(
        self,
        payload: SessionCreate,
    ) -> SessionList:
        session = Session(
            user_id=payload.user_id,
            expires_at=datetime.now(UTC)
            + timedelta(seconds=settings.auth.cookie_max_age),
        )
        self.session.add(session)
        await self.session.commit()
        await self.session.refresh(session)
        return SessionList.model_validate(session)

    async def get(
        self,
        session_id: UUID,
    ) -> SessionList | None:
        session = await self.session.get(Session, session_id)
        if session:
            return SessionList.model_validate(session)

    async def get_by_device_id(
        self,
        device_id: UUID,
    ) -> SessionList | None:
        stmt = select(Session).where(Session.device_id == device_id)
        res = await self.session.execute(stmt)
        session = res.scalar_one_or_none()
        if session:
            return SessionList.model_validate(session)

    async def update(
        self,
        session_id: UUID,
        payload: SessionUpdate,
    ) -> SessionList:
        session = await self.session.get(Session, session_id)

        if not session:
            raise SessionNotFound("Session not found")

        for key, value in payload.model_dump(exclude_unset=True).items():
            if hasattr(session, key):
                setattr(session, key, value)

        await self.session.commit()
        await self.session.refresh(session)
        return SessionList.model_validate(session)

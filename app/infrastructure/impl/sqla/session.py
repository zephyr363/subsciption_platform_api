from dataclasses import asdict
from typing import Optional
from uuid import UUID
from app.domain.entities import SessionEntity
from app.domain.exceptions.session import SessionNotFound
from app.domain.interfaces.session import ISessionRepository
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.models.sqla import Session
from sqlalchemy import select


class SessionRepositoryImpl(ISessionRepository):
    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        self.session = session

    async def save(
        self,
        entity: SessionEntity,
    ) -> SessionEntity:
        session = Session(
            user_id=entity.user_id,
            device_id=entity.device_id,
            expires_at=entity.expires_at,
            created_at=entity.created_at,
        )
        self.session.add(session)
        await self.session.commit()
        await self.session.refresh(session)
        return SessionEntity(
            id=session.id,
            user_id=session.user_id,
            device_id=session.device_id,
            created_at=session.created_at,
            expires_at=session.expires_at,
        )

    async def get(
        self,
        session_id: UUID,
    ) -> Optional[SessionEntity]:
        session = await self.session.get(Session, session_id)
        if session:
            return SessionEntity(
                id=session.id,
                user_id=session.user_id,
                device_id=session.device_id,
                created_at=session.created_at,
                expires_at=session.expires_at,
            )

    async def get_by_device_id(
        self,
        device_id: UUID,
    ) -> Optional[SessionEntity]:
        stmt = select(Session).where(Session.device_id == device_id)
        res = await self.session.execute(stmt)
        session = res.scalar_one_or_none()
        if session:
            return SessionEntity(
                id=session.id,
                user_id=session.user_id,
                device_id=session.device_id,
                created_at=session.created_at,
                expires_at=session.expires_at,
            )

    async def update(
        self,
        entity: SessionEntity,
    ) -> SessionEntity:
        session = await self.session.get(Session, entity.id)

        if not session:
            raise SessionNotFound("Session not found")

        updatable_fields = {"expires_at", "last_used_at", "status"}

        for key, value in asdict(entity).items():
            if key in updatable_fields:
                setattr(session, key, value)

        await self.session.commit()
        await self.session.refresh(session)
        return SessionEntity(
            id=session.id,
            user_id=session.user_id,
            device_id=session.device_id,
            created_at=session.created_at,
            expires_at=session.expires_at,
        )

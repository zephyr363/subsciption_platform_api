from dataclasses import asdict
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities import SessionEntity
from app.domain.interfaces.session import ISessionRepository
from app.infrastructure.exceptions import SessionNotFoundError
from app.infrastructure.mappers.sqla.session import SessionMapping
from app.infrastructure.models.sqla import Session


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
        session = SessionMapping.to_orm(entity)
        self.session.add(session)
        return SessionMapping.from_orm(session)

    async def get(
        self,
        session_id: UUID,
    ) -> SessionEntity:
        session = await self.session.get(Session, session_id)
        if not session:
            raise SessionNotFoundError("Session not found")
        return SessionMapping.from_orm(session)

    async def get_by_device_id(
        self,
        device_id: UUID,
    ) -> SessionEntity:
        stmt = select(Session).where(Session.device_id == device_id)
        res = await self.session.execute(stmt)
        try:
            session = res.scalar_one()
        except NoResultFound as err:
            raise SessionNotFoundError("Session not found") from err
        return SessionMapping.from_orm(session)

    async def update(
        self,
        entity: SessionEntity,
    ) -> SessionEntity:
        session = await self.session.get(Session, entity.id)

        if not session:
            raise SessionNotFoundError("Session not found")

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

from typing import AsyncGenerator, Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import async_session
from fastapi import Depends

from app.repos import SessionRepositoryImpl, UserRepositoryImpl
from app.use_cases import CreateUserUseCase, UserSessionLoginUseCase


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


async def get_session_repo(
    session: Annotated[AsyncSession, Depends(get_async_session)],
):
    return SessionRepositoryImpl(session)


async def get_user_repo(
    session: Annotated[AsyncSession, Depends(get_async_session)],
):
    return UserRepositoryImpl(session)


async def session_login_uc(
    session_repo: Annotated[SessionRepositoryImpl, Depends(get_session_repo)],
    user_repo: Annotated[UserRepositoryImpl, Depends(get_user_repo)],
):
    return UserSessionLoginUseCase(
        session_repo,
        user_repo,
    )


async def user_create_uc(
    user_repo: Annotated[UserRepositoryImpl, Depends(get_user_repo)],
):
    return CreateUserUseCase(user_repo)

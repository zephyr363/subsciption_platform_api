from typing import Annotated, AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.ports.uow import IUnitOfWork
from app.application.use_cases import (
    CreatePlanUseCase,
    CreateTrialSubscriptionUseCase,
    CreateUserUseCase,
    UserSessionLoginUseCase,
)
from app.domain.interfaces.plan import IPlanRepository
from app.domain.interfaces.session import ISessionRepository
from app.domain.interfaces.subscription import ISubscriptionRepository
from app.domain.interfaces.user import IUserRepository
from app.infrastructure.impl.sqla import (
    PlanRepositoryImpl,
    SessionRepositoryImpl,
    SubscriptionRepositoryImpl,
    UserRepositoryImpl,
)
from app.infrastructure.models.sqla import async_session
from app.infrastructure.uow.sqla import SqlAlchemyUnitOfWork


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


async def sqla_uow(
    session: Annotated[AsyncSession, Depends(get_async_session)],
):
    return SqlAlchemyUnitOfWork(session)


async def get_session_repo(
    session: Annotated[AsyncSession, Depends(get_async_session)],
):
    return SessionRepositoryImpl(session)


async def get_user_repo(
    session: Annotated[AsyncSession, Depends(get_async_session)],
):
    return UserRepositoryImpl(session)


async def get_plan_repository(
    session: Annotated[AsyncSession, Depends(get_async_session)],
):
    return PlanRepositoryImpl(session)


async def get_subscription_repository(
    session: Annotated[AsyncSession, Depends(get_async_session)],
):
    return SubscriptionRepositoryImpl(session)


async def session_login_uc(
    uow: Annotated[IUnitOfWork, Depends(sqla_uow)],
    session_repo: Annotated[ISessionRepository, Depends(get_session_repo)],
    user_repo: Annotated[IUserRepository, Depends(get_user_repo)],
):
    return UserSessionLoginUseCase(
        uow,
        session_repo,
        user_repo,
    )


async def user_create_uc(
    uow: Annotated[IUnitOfWork, Depends(sqla_uow)],
    user_repo: Annotated[IUserRepository, Depends(get_user_repo)],
):
    return CreateUserUseCase(
        uow,
        user_repo,
    )


async def create_plan_uc(
    uow: Annotated[IUnitOfWork, Depends(sqla_uow)],
    plan_repo: Annotated[IPlanRepository, Depends(get_plan_repository)],
):
    return CreatePlanUseCase(
        uow,
        plan_repo,
    )


async def create_trial_subscription_uc(
    uow: Annotated[IUnitOfWork, Depends(sqla_uow)],
    plan_repo: Annotated[IPlanRepository, Depends(get_plan_repository)],
    subscription_repo: Annotated[
        ISubscriptionRepository, Depends(get_subscription_repository)
    ],
):
    return CreateTrialSubscriptionUseCase(
        uow,
        plan_repo=plan_repo,
        subscription_repo=subscription_repo,
    )

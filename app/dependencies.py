from typing import AsyncGenerator, Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.interfaces.plan import IPlanRepository
from app.domain.interfaces.session import ISessionRepository
from app.domain.interfaces.subscription import ISubscriptionRepository
from app.domain.interfaces.user import IUserRepository
from app.infrastructure.models.sqla import async_session
from fastapi import Depends

from app.infrastructure.impl.sqla import (
    SessionRepositoryImpl,
    UserRepositoryImpl,
    PlanRepositoryImpl,
    SubscriptionRepositoryImpl,
)
from app.application.use_cases import (
    UserSessionLoginUseCase,
    CreateUserUseCase,
    CreatePlanUseCase,
    CreateTrialSubscriptionUseCase,
)


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


async def get_plan_repository(
    session: Annotated[AsyncSession, Depends(get_async_session)],
):
    return PlanRepositoryImpl(session)


async def get_subscription_repository(
    session: Annotated[AsyncSession, Depends(get_async_session)],
):
    return SubscriptionRepositoryImpl(session)


async def session_login_uc(
    session_repo: Annotated[ISessionRepository, Depends(get_session_repo)],
    user_repo: Annotated[IUserRepository, Depends(get_user_repo)],
):
    return UserSessionLoginUseCase(
        session_repo,
        user_repo,
    )


async def user_create_uc(
    user_repo: Annotated[IUserRepository, Depends(get_user_repo)],
):
    return CreateUserUseCase(user_repo)


async def create_plan_uc(
    plan_repo: Annotated[IPlanRepository, Depends(get_plan_repository)],
):
    return CreatePlanUseCase(plan_repo)


async def create_trial_subscription_uc(
    plan_repo: Annotated[IPlanRepository, Depends(get_plan_repository)],
    subscription_repo: Annotated[
        ISubscriptionRepository, Depends(get_subscription_repository)
    ],
):
    return CreateTrialSubscriptionUseCase(
        plan_repo=plan_repo, subscription_repo=subscription_repo
    )

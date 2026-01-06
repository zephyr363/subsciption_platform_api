from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends

from app.dependencies import (
    create_trial_subscription_uc,
    CreateTrialSubscriptionUseCase,
)

subscription_routes = APIRouter(prefix="/subscriptions", tags=["Plans"])


@subscription_routes.post(
    "/trial",
    summary="Create a trial subscription",
)
async def create_trial_subscription(
    user_id: UUID,
    uc: Annotated[
        CreateTrialSubscriptionUseCase,
        Depends(create_trial_subscription_uc),
    ],
):
    return await uc.execute(user_id=user_id)

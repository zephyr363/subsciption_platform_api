from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from app.dependencies import (
    CreateTrialSubscriptionUseCase,
    create_trial_subscription_uc,
)
from app.infrastructure.exceptions import (
    PlanNotFoundError,
    SubscriptionSaveError,
    SubscriptionAlreadyExistsError,
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
    try:
        return await uc.execute(user_id=user_id)
    except (
        PlanNotFoundError,
        SubscriptionSaveError,
        SubscriptionAlreadyExistsError,
    ) as err:
        raise HTTPException(
            status_code=400,
            detail=str(err),
        ) from err

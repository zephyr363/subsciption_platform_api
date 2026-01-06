from typing import Annotated
from fastapi import APIRouter, Depends

from app.application.dto.plan import PlanCreate
from app.dependencies import create_plan_uc, CreatePlanUseCase

plan_routes = APIRouter(prefix="/plans", tags=["Plans"])


@plan_routes.post(
    "/",
    summary="Create a new plan",
)
async def create_plan(
    payload: PlanCreate,
    uc: Annotated[
        CreatePlanUseCase,
        Depends(create_plan_uc),
    ],
):
    return await uc.execute(payload)

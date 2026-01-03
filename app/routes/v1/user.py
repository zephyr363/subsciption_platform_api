from typing import Annotated
from fastapi import APIRouter, Depends

from app.dependencies import CreateUserUseCase, user_create_uc
from app.dto.user import UserCreate, UserList

user_routes = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@user_routes.post(
    "/",
    description="Create user",
    response_model=UserList,
)
async def create_user(
    payload: UserCreate,
    uc: Annotated[CreateUserUseCase, Depends(user_create_uc)],
):
    return await uc.execute(payload)

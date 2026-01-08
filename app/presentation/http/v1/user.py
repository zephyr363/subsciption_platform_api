from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.application.dto.user import UserCreate, UserList
from app.dependencies import CreateUserUseCase, user_create_uc
from app.infrastructure.exceptions import UserAlreadyExistsError

user_routes = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@user_routes.post(
    "/",
    description="Create user",
    response_model=UserList,
    status_code=201,
)
async def create_user(
    payload: UserCreate,
    uc: Annotated[CreateUserUseCase, Depends(user_create_uc)],
):
    try:
        return await uc.execute(payload)
    except UserAlreadyExistsError as err:
        raise HTTPException(status_code=400, detail=str(err)) from err

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Cookie, Depends, HTTPException, Response

from app.application.dto.user import UserLogin
from app.config import settings
from app.dependencies import UserSessionLoginUseCase, session_login_uc
from app.infrastructure.exceptions import UserNotFoundError

session_routes = APIRouter(prefix="/session", tags=["Session"])


@session_routes.post(
    "/login",
    description="Create session for user",
)
async def login(
    response: Response,
    payload: UserLogin,
    uc: Annotated[UserSessionLoginUseCase, Depends(session_login_uc)],
    device_id: Annotated[
        UUID | None,
        Cookie(include_in_schema=False, alias=settings.auth.device_id_cookie_name),
    ] = None,
):
    try:
        res = await uc.execute(
            device_id,
            payload,
        )
    except UserNotFoundError as err:
        raise HTTPException(
            status_code=404,
            detail=str(err),
        ) from err

    response.set_cookie(
        key=settings.auth.cookie_name,
        value=str(res.id),
        secure=not settings.debug,
        httponly=settings.auth.httponly,
        max_age=settings.auth.cookie_max_age,
    )

    response.set_cookie(
        key=settings.auth.device_id_cookie_name,
        value=str(res.device_id),
        secure=not settings.debug,
        httponly=settings.auth.httponly,
        max_age=settings.auth.cookie_max_age,
    )

    response.status_code = 204
    return response

from fastapi import APIRouter, Body, Depends, HTTPException
from starlette import status

from api.schemas import users as schemas
from api.services.users import UsersService, get_users_service


api_router = APIRouter(prefix="/user", tags=["User"])


@api_router.put(
    "",
    description="Register new user",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.RegistrationSuccess,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Bad parameters for registration",
        },
    },
)
async def registration(
    registration_form: schemas.RegistrationModel = Body(...),
    users_service: UsersService = Depends(get_users_service),
):
    is_success, message = await users_service.register_user(registration_form)
    if is_success:
        return {"message": message}
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=message,
    )


@api_router.patch(
    "",
    description="Edit a user",
    status_code=status.HTTP_200_OK,
    response_model=schemas.RegistrationSuccess,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Bad parameters for edit",
        },
    },
)
async def edit(
    edit_form: schemas.EditModel = Body(...),
    users_service: UsersService = Depends(get_users_service),
):
    is_success, message = await users_service.edit_user(edit_form)
    if is_success:
        return {"message": message}
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=message,
    )

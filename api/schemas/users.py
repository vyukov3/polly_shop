from uuid import UUID

from pydantic import BaseModel, EmailStr, constr, validator

from api.utils import hash_password


class RegistrationModel(BaseModel):
    email: EmailStr
    password: constr(min_length=8)

    @validator("password")
    def validate_password(cls, password):
        password = hash_password(password)
        return password


class EditModel(BaseModel):
    user_id: UUID
    email: EmailStr | None = None
    password: constr(min_length=8) | None = None
    role_id: UUID | None = None

    @validator("password")
    def validate_password(cls, password):
        if password:
            password = hash_password(password)
        return password


class RegistrationSuccess(BaseModel):
    message: str

from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict, computed_field
from uuid import UUID

from app.utils import hash_psw


class UserList(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: EmailStr
    password: str

    @computed_field
    @property
    def password_hash(self) -> str:
        return hash_psw(self.password)

    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: EmailStr
    password: str

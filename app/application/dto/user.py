from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict
from uuid import UUID


class UserList(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    first_name: str = ""
    last_name: str = ""
    email: EmailStr
    password: str

    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: EmailStr
    password: str

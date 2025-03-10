from typing import Optional

from pydantic import BaseModel, EmailStr, Field


# Shared properties
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True


# Properties to receive via API on creation
class UserCreateSchema(UserBase):
    password: str = Field(..., min_length=8)


# Properties to receive via API on update
class UserUpdateSchema(UserBase):
    password: Optional[str] = None


# Properties to return via API
class UserGetSchema(UserBase):
    id: Optional[int] = None
    is_superuser: bool = False

    class Config:
        from_attributes = True


class TokenSchema(BaseModel):
    access_token: str
    token_type: str

    class Config:
        from_attributes = True
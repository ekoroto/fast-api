from datetime import datetime
from pydantic import BaseModel, EmailStr


class BaseUserSchema(BaseModel):
    email: EmailStr


class UserRequestSchema(BaseUserSchema):
    password: str


class UserResponseSchema(BaseUserSchema):
    created_at: datetime

    class Config:
        orm_mode = True

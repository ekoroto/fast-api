from datetime import datetime
from pydantic import BaseModel

from .user_schema import UserResponseSchema


class BasePostSchema(BaseModel):
    title: str
    content: str
    published: bool = True


class PostRequestSchema(BasePostSchema):
    pass


class PostResponseSchema(BasePostSchema):
    id: int
    user_id: int
    created_at: datetime
    user_id: int
    user: UserResponseSchema

    class Config:
        orm_mode = True

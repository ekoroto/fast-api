from datetime import datetime
from pydantic import BaseModel


class BasePostSchema(BaseModel):
    title: str
    content: str
    published: bool = True


class PostRequestSchema(BasePostSchema):
    pass


class PostResponseSchema(BasePostSchema):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

from fastapi import FastAPI

from .database import engine, Base
from .routers import auth_router, post_router, user_router

app = FastAPI()
app.include_router(auth_router.router)
app.include_router(post_router.router)
app.include_router(user_router.router)

Base.metadata.create_all(bind=engine)

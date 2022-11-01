import psycopg2
from fastapi import FastAPI
from psycopg2.extras import RealDictCursor

from .database import engine, Base
from .routers import post_router, user_router

app = FastAPI()
app.include_router(post_router.router)
app.include_router(user_router.router)

Base.metadata.create_all(bind=engine)

try:
    db_connection = psycopg2.connect(host='localhost', database='fastapi', user='eugene_koroto',
                                     password='postgres', cursor_factory=RealDictCursor)
    cursor = db_connection.cursor()
    print("OKKK")
except Exception as error:
    print('Error: ', error)
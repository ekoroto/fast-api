import psycopg2
from fastapi import FastAPI
from psycopg2.extras import RealDictCursor

from app.database import engine, Base

app = FastAPI()

Base.metadata.create_all(bind=engine)

try:
    db_connection = psycopg2.connect(host='localhost', database='fastapi', user='eugene_koroto',
                                     password='postgres', cursor_factory=RealDictCursor)
    cursor = db_connection.cursor()
except Exception as error:
    print('Error: ', error)
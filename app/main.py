from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models, schemas
from .database import engine
from .routers import post, user
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='kanishk', password='asdfghjk', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('Database connection was successfull!')
        break
    except Exception as err:
        print('Error while connecting to database', err)
        time.sleep(2)

app.include_router(post.router)
app.include_router(user.router)

@app.get("/")
async def root():
    return {"message": "Hello World...!"}
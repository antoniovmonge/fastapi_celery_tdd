import os
from celery import Celery
from fastapi import FastAPI

from dotenv import load_dotenv

load_dotenv(".env/local.env")

app = FastAPI()

celery = Celery(
    __name__,
    broker=os.getenv("CELERY_BROKER_URL"),
    backend=os.getenv("CELERY_RESULT_BACKEND"),
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@celery.task
def divide(x, y):
    import time
    time.sleep(5)
    return x / y

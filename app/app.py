from typing import Dict, List

from fastapi import FastAPI, HTTPException, status

from .db import database, sqlalchemy_engine
from .model import metadata
from .todo import router as todo_router

app = FastAPI()

app.include_router(todo_router, prefix="/api")


@app.on_event("startup")
async def startup():
    await database.connect()
    metadata.create_all(sqlalchemy_engine)


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

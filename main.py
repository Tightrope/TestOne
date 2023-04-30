import logging
import os
import sqlite3
import uvicorn

from routers import content_router
from contextlib import asynccontextmanager
from typing import Union
from fastapi import FastAPI

dbconnection: sqlite3.Connection
LOGLEVEL = os.environ.get('LOGLEVEL', 'WARNING').upper()
logging.basicConfig(level=LOGLEVEL)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("Starting lifespan")

    # Connect to the database
    app.dbconnection = sqlite3.connect('db.sqlite3')

    # Log the state of the dbconnection
    logging.info("DB connection state is: %s", app.dbconnection)
    logging.info("Database version is: %s", app.dbconnection.execute("SELECT SQLITE_VERSION()").fetchone())

    yield
    logging.info("Hit lifespan event end")
    app.dbconnection.close()
    logging.info("DB connection state is: %s", app.dbconnection)


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def read_root():
    return {"Hello": "World"}


if __name__ == "__main__":
    app.include_router(content_router.router, tags=["content"], prefix="/content")
    uvicorn.run(app, host="127.0.0.1", port=8000)

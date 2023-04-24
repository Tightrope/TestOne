import logging
import os
import sqlite3
import uvicorn

import main
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
    main.dbconnection = sqlite3.connect('db.sqlite3')

    # Log the state of the dbconnection
    logging.info("DB connection state is: %s", main.dbconnection)
    logging.info("Database version is: %s", main.dbconnection.execute("SELECT SQLITE_VERSION()").fetchone())
    database_tables = main.dbconnection.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
    logging.info("Database tables are: %s", database_tables)

    # If database_tables contains the content table, get the count of rows
    if ('content',) in database_tables:
        content_table_count = main.dbconnection.execute("SELECT COUNT(*) FROM content").fetchone()[0]
        logging.info("Content table row count is: %s", content_table_count)


    yield
    logging.info("Hit lifespan event end")
    main.dbconnection.close()
    logging.info("DB connection state is: %s", main.dbconnection)


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def read_root():
    logging.info("Hello World")
    logging.info("DB connection state is: %s", main.dbconnection)

    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

def getDbConnection():
    return main.dbconnection


if __name__ == "__main__":
    app.include_router(content_router.router, tags=["content"], prefix="/content")
    uvicorn.run(app, host="127.0.0.1", port=8000)
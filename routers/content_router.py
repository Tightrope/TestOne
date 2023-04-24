import logging
import main
from fastapi import status, Response
from random import random
from fastapi import APIRouter

CONTENT_TABLE_NAME = "content"
CONTENT_FILES = ["./data/beato_SFisOTDzGuE.txt", "./data/beato_xKIC9zbSJoE.txt", "./data/beato_ZavJLr5Otq4.txt"]
router = APIRouter()


@router.post("/embed", response_description="Create vector embeddings for a hard-coded list of documents",
             responses={status.HTTP_200_OK: {"description": "Embeddings already exist"},
                        status.HTTP_201_CREATED: {"description": "Embeddings created"}})
async def embed(response: Response):
    logging.info("Called /embed")

    dbconnection = main.getDbConnection()
    logging.info("DB connection state is: %s", dbconnection)

    initContentDatabseTable()

    if dbconnection.execute(f'SELECT COUNT(*) FROM {CONTENT_TABLE_NAME}').fetchone()[0] == 0:

        for file in CONTENT_FILES:
            with open(file, 'r') as f:
                content = f.read()
                statement = f'INSERT INTO {CONTENT_TABLE_NAME} VALUES (?, ?)'
                dbconnection.execute(statement, (None,content))

        dbconnection.commit()

        response.status_code = status.HTTP_201_CREATED
        response.description = "Embeddings created"
    else:
        response.status_code = status.HTTP_200_OK
        response.description = "Embeddings already exist"


def initContentDatabseTable():
    dbconnection = main.getDbConnection()
    dbconnection.execute(f'CREATE TABLE IF NOT EXISTS content (id INTEGER PRIMARY KEY AUTOINCREMENT, {CONTENT_TABLE_NAME} TEXT)')

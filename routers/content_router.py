import logging
import main
from fastapi import status, Response, Request, FastAPI
from fastapi import APIRouter

from repository.beato_transcript_repo import BeatoTranscriptRepo

CONTENT_TABLE_NAME = "content"
CONTENT_FILES = ["./data/beato_SFisOTDzGuE.txt", "./data/beato_xKIC9zbSJoE.txt", "./data/beato_ZavJLr5Otq4.txt"]
router = APIRouter()


@router.post("/embed", response_description="Create vector embeddings for a hard-coded list of documents",
             responses={status.HTTP_200_OK: {"description": "Embeddings already exist"},
                        status.HTTP_201_CREATED: {"description": "Embeddings created"}})
async def embed(request: Request, response: Response):
    logging.info("Called /embed")

    dbconnection = request.app.dbconnection
    logging.info("DB connection state is: %s", dbconnection)

    beatoRepo = BeatoTranscriptRepo(request.app.dbconnection)

    if beatoRepo.get_transcript_count() == 0:

        for file in CONTENT_FILES:
            with open(file, 'r') as f:
                content = f.read()
                beatoRepo.create_transcript(content)

        response.status_code = status.HTTP_201_CREATED
        response.description = "Embeddings created"
        logging.info(f'{response.status_code} {response.description}')
    else:
        # Iterate through all the content rows in the database
        for row in beatoRepo.get_all_transcripts():
            logging.info("Row %s: %s", row[0], row[1][:40])

        response.status_code = status.HTTP_200_OK
        response.description = "Embeddings already exist"
        logging.info(f'{response.status_code} {response.description}')


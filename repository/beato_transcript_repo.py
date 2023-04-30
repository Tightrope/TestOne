# Create a repository class for transcriptions

import logging
import sqlite3

CONTENT_TABLE_NAME = "beato_transcripts"


class BeatoTranscriptRepo:
    def __init__(self, dbconnection: sqlite3.Connection):
        self.dbconnection = dbconnection
        logging.info("DB connection state is: %s", self.dbconnection)
        logging.info("Database version is: %s", self.dbconnection.execute("SELECT SQLITE_VERSION()").fetchone())
        self.__init_transcript_table()
        database_tables = self.dbconnection.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
        logging.info("Database tables are: %s", database_tables)

        # If database_tables contains the content table, get the count of rows
        if (CONTENT_TABLE_NAME,) in database_tables:
            content_table_count = self.dbconnection.execute(f'SELECT COUNT(*) FROM {CONTENT_TABLE_NAME}').fetchone()[0]
            logging.info("Beato transcript table row count is: %s", content_table_count)

    def get_transcript(self, item_id):
        return self.dbconnection.execute(f'SELECT * FROM content WHERE id = {item_id}').fetchone()

    def get_transcript_count(self):
        return self.dbconnection.execute(f'SELECT COUNT(*) FROM content').fetchone()[0]

    def get_all_transcripts(self):
        return self.dbconnection.execute(f'SELECT * FROM content').fetchall()

    def create_transcript(self, content):
        statement = f'INSERT INTO content VALUES (?, ?)'
        self.dbconnection.execute(statement, (None, content))
        self.dbconnection.commit()

    def delete_transcript(self, item_id):
        self.dbconnection.execute(f'DELETE FROM content WHERE id = {item_id}')
        self.dbconnection.commit()

    def update_transcript(self, item_id, content):
        self.dbconnection.execute(f'UPDATE content SET content = ? WHERE id = {item_id}', (content,))
        self.dbconnection.commit()

    def __init_transcript_table(self):
        self.dbconnection.execute(
            f'CREATE TABLE IF NOT EXISTS content (id INTEGER PRIMARY KEY AUTOINCREMENT, {CONTENT_TABLE_NAME} TEXT)')
        self.dbconnection.commit()

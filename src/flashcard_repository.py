#!/usr/bin/env python
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv
#import sqlalchemy
from snowflake.sqlalchemy import URL
import pandas as pd

load_dotenv()


class FlashCardRepository:
    def __init__(self):
        self._url = URL(
            account = os.getenv('SNOWFLAKE_ACCOUNT'),
            user = os.getenv('SNOWFLAKE_USER'),
            password = os.getenv('SNOWFLAKE_PASSWORD'),
            database = os.getenv('SNOWFLAKE_DATABASE'),
            warehouse = os.getenv('SNOWFLAKE_WAREHOUSE'),
        )
        self._engine = create_engine(self._url)
        self._conn = self._engine.connect().execution_options(stream_results=True)

    def __del__(self):
        self._conn.close()
        self._engine.dispose()

    def get_sf_current_version(self):
        results = self._conn.execute('select current_version()').fetchone()
        print(results[0])
        return results

    def get_flashcards_all(self):
        results = self._conn.execute("SELECT * FROM EDW.FLASHCARD_DIM WHERE FLASHCARD_ANSWER_TEXT is not NULL LIMIT 10")

    def fetch_pandas_sqlalchemy(self):
        sql = "SELECT * FROM EDW.FLASHCARD_DIM WHERE FLASHCARD_ANSWER_TEXT is not NULL"
        rows = 0
        flashcards = pd.read_sql_query(sql, self._conn, index_col=['flashcard_key', 'flashcard_question_text', 'flashcard_answer_text'], chunksize=100)
        
        for dataframe in flashcards:
            print('CHUNK LEN'.format(len(dataframe)))
            for index, row in dataframe.iterrows():
                print('Q:{} = A:{}'.format(index[0], index[1]))

    def get_flashcards_dataframe(self):
        #sql = "SELECT * FROM EDW.FLASHCARD_DIM WHERE FLASHCARD_ANSWER_TEXT is not NULL"        
        sql = "SELECT * FROM EDW.FLASHCARD_DIM WHERE FLASHCARD_ANSWER_TEXT is not NULL LIMIT 10"        
        flashcards = pd.read_sql_query(sql, self._conn, index_col=['flashcard_key','flashcard_question_text', 'flashcard_answer_text'], chunksize=100)
        return flashcards

    #def create_dataframe(self, data):
         






        
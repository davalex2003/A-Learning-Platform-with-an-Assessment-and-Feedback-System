import json
import logging
import psycopg2

import repositories.queries.postgres.answer as answer_queries

class AnswerRepository:

    @staticmethod
    def connect_postgres():
        with open('configs/postgres.json', 'r') as f:
            config = json.load(f)
            f.close()
        try:
            conn = psycopg2.connect(dbname=config['dbname'], user=config['user'],
                                    password=config['password'], host=config['host'])
        except Exception as e:
            logging.error(e)
            return
        return conn

    def insert_answer(self, task_id: str, user_id: str, assignment_id: str, text: str):
        conn = self.connect_postgres()
        with conn.cursor() as cursor:
            cursor.execute(answer_queries.INSERT_ANSWER_TEXT, (task_id, user_id, assignment_id, text))
        conn.commit()
        conn.close()
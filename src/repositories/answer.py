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

    def insert_answer_text(self, task_id: str, user_id: str, assignment_id: str, text: str):
        conn = self.connect_postgres()
        with conn.cursor() as cursor:
            cursor.execute(answer_queries.INSERT_ANSWER_TEXT, (task_id, user_id, assignment_id, text))
        conn.commit()
        conn.close()

    def insert_answer_file(self, task_id: str, user_id: str, assignment_id: str, file: str):
        conn = self.connect_postgres()
        with conn.cursor() as cursor:
            cursor.execute(answer_queries.INSERT_ANSWER_FILE, (task_id, user_id, assignment_id, file))
        conn.commit()
        conn.close()

    def get_answer_file(self, task_id: str, user_id: str, assignment_id: str):
        conn = self.connect_postgres()
        with conn.cursor() as cursor:
            cursor.execute(answer_queries.GET_ANSWER_FILE, (task_id, user_id, assignment_id))
            file = cursor.fetchone()
        conn.close()
        return file

    def insert_answer_assessment(self, task_id: str, user_id: str, assignment_id: str, assessment: int):
        conn = self.connect_postgres()
        with conn.cursor() as cursor:
            cursor.execute(answer_queries.INSERT_ANSWER_ASSESSMENT, (assessment, task_id, user_id, assignment_id))
        conn.commit()
        conn.close()
    
    def insert_answer_feedback(self, task_id: str, user_id: str, assignment_id: str, feedback: str):
        conn = self.connect_postgres()
        with conn.cursor() as cursor:
            cursor.execute(answer_queries.INSERT_ANSWER_FEEDBACK, (feedback, task_id, user_id, assignment_id))
        conn.commit()
        conn.close()

    def get_answers(self, user_id: str, assignment_id: str):
        conn = self.connect_postgres()
        with conn.cursor() as cursor:
            cursor.execute(answer_queries.SELECT_ANSWERS, (user_id, assignment_id))
            data = cursor.fetchall()
        conn.close()
        return data
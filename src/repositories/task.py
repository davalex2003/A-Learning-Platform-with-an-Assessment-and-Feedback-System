import json
import logging
import psycopg2
from typing import Optional

import repositories.queries.postgres.task as task_queries
from schemas.task import TaskModel

class TaskRepository:

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

    def create_task(self, task: TaskModel, assignment_id: str):
        conn = self.connect_postgres()
        with conn.cursor() as cursor:
            cursor.execute(task_queries.CREATE_TASK, (assignment_id, task.question_type, task.question_text, task.answer_type, json.dumps(task.answer_variants)))
        conn.commit()
        conn.close()

    def add_question_file(self, question_file: str, task_id: str):
        conn = self.connect_postgres()
        with conn.cursor() as cursor:
            cursor.execute(task_queries.UPDATE_TASK_QUESTION_FILE, (question_file, task_id))
        conn.commit()
        conn.close()
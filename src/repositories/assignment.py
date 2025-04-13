import json
import logging
import psycopg2

import repositories.queries.postgres.assignment as assignment_queries

from schemas.assignment import AssignmentModel

class AssignmentRepository:

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

    def create_assignment(self, assignment: AssignmentModel, course_id: str) -> str:
        conn = self.connect_postgres()
        with conn.cursor() as cursor:
            cursor.execute(assignment_queries.CREATE_ASSIGNMENT, (course_id, assignment.name, assignment.started_at, assignment.ended_at))
            id = cursor.fetchone()[0]
        conn.commit()
        conn.close()
        return id

    def update_assignment(self, assignment: AssignmentModel, assignment_id: str):
        conn = self.connect_postgres()
        with conn.cursor() as cursor:
            cursor.execute(assignment_queries.UPDATE_ASSIGNMENT, (assignment.name, assignment.started_at, assignment.ended_at, assignment_id))
        conn.commit()
        conn.close()

    def delete_assignment(self, assignment_id: str):
        conn = self.connect_postgres()
        with conn.cursor() as cursor:
            cursor.execute(assignment_queries.DELETE_ASSIGNMENT, (assignment_id,))
        conn.commit()
        conn.close()

    def get_assignments(self, course_id: str):
        conn = self.connect_postgres()
        with conn.cursor() as cursor:
            cursor.execute(assignment_queries.SELECT_ASSIGNMENTS, (course_id,))
            data = cursor.fetchall()
        conn.close()
        return data
import json
import logging
import psycopg2
import redis

import repositories.queries.postgres.common as common_queries
import repositories.queries.postgres.course as course_queries
from schemas.course import CourseModel

class CourseRepository:

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
    
    def create_course(self, course: CourseModel, user_id: str) -> str:
        conn = self.connect_postgres()
        with conn.cursor() as cursor:
            cursor.execute(course_queries.CREATE_COURSE, (course.name, course.description, user_id))
            id = cursor.fetchone()[0]
        conn.commit()
        conn.close()
        return id
    
    def update_course(self, course: CourseModel, course_id: str):
        conn = self.connect_postgres()
        with conn.cursor() as cursor:
            cursor.execute(course_queries.UPDATE_COURSE, (course.name, course.description, course_id))
        conn.commit()
        conn.close()
import json
import logging
import psycopg2
import typing

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
    
    def delete_course(self, course_id: str):
        conn = self.connect_postgres()
        with conn.cursor() as cursor:
            cursor.execute(course_queries.DELETE_COURSE, (course_id,))
        conn.commit()
        conn.close()
    
    def get_courses_list(self, user_id: str):
        conn = self.connect_postgres()
        with conn.cursor() as cursor:
            cursor.execute(course_queries.SELECT_COURSES_LIST_BY_USER_ID, (user_id,))
            data = cursor.fetchall()
        conn.close()
        return data
    
    def get_course_links(self, course_id: str):
        conn = self.connect_postgres()
        with conn.cursor() as cursor:
            cursor.execute(course_queries.SELECT_COURSE_LINKS, (course_id,))
            data = cursor.fetchone()
        conn.close()
        return data
    
    def update_course_links(self, course_id: str, links: typing.List[str]):
        conn = self.connect_postgres()
        with conn.cursor() as cursor:
            cursor.execute(course_queries.UPDATE_COURSE_LINKS, (json.dumps(links), course_id))
        conn.commit()
        conn.close()

    def get_course_materials(self, course_id: str):
        conn = self.connect_postgres()
        with conn.cursor() as cursor:
            cursor.execute(course_queries.SELECT_COURSE_MATEIALS, (course_id,))
            data = cursor.fetchone()
        conn.close()
        return data

    def update_course_materials(self, course_id: str, materials: typing.List[str]):
        conn = self.connect_postgres()
        with conn.cursor() as cursor:
            cursor.execute(course_queries.UPDATE_COURSE_MATERIALS, (json.dumps(materials), course_id))
        conn.commit()
        conn.close()

    def get_links_and_materials(self, course_id: str):
        conn = self.connect_postgres()
        with conn.cursor() as cursor:
            cursor.execute(course_queries.GET_LINKS_AND_MATERIALS, (course_id,))
            data = cursor.fetchone()
        conn.close()
        return data
    
    def add_course_user_link(self, user_id: str, course_id: str):
        conn = self.connect_postgres()
        with conn.cursor() as cursor:
            cursor.execute(course_queries.CREATE_COURSE_USER_LINK, (user_id, course_id))
        conn.commit()
        conn.close()
    
    def get_courses(self, user_id: str):
        conn = self.connect_postgres()
        with conn.cursor() as cursor:
            cursor.execute(course_queries.SELECT_COURSES_LIST, (user_id,))
            data = cursor.fetchall()
        conn.close()
        return data
import json
import logging
import psycopg2
from typing import Optional

import repositories.queries.postgres.admin as admin_queries
import repositories.queries.postgres.common as common_queries

ADMIN = 'admin'

class AdminRepository:

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
    
    def get_users_list(self):
        conn = self.connect_postgres()
        with conn.cursor() as cursor:
            cursor.execute(admin_queries.SELECT_USERS_LIST)
            data = cursor.fetchall()
        conn.close()
        return data
    
    def get_role(self, email: str):
        conn = self.connect_postgres()
        with conn.cursor() as cursor:
            cursor.execute(common_queries.GET_USER_ROLE, (email,))
            data = cursor.fetchone()
        conn.close()
        return data
    
    def delete_user(self, user_id: str):
        conn = self.connect_postgres()
        with conn.cursor() as cursor:
            cursor.execute(admin_queries.DELETE_USER, (user_id, ))
        conn.commit()
        conn.close()
    
    def update_role(self, user_id: str, role: str):
        conn = self.connect_postgres()
        with conn.cursor() as cursor:
            cursor.execute(admin_queries.CHANGE_USER_ROLE, (role, user_id))
        conn.commit()
        conn.close()
    
    def get_courses_list(self):
        conn = self.connect_postgres()
        with conn.cursor() as cursor:
            cursor.execute(admin_queries.SELECT_COURSES_LIST)
            data = cursor.fetchall()
        conn.close()
        return data

    def create_admin(self, email: str, first_name: str, second_name: str, middle_name: Optional[str], hash_password: str):
        conn = self.connect_postgres()
        with conn.cursor() as cursor:
            cursor.execute(admin_queries.CREATE_ADMIN, (email, first_name, second_name, middle_name, hash_password, ADMIN, True))
        conn.commit()
        conn.close()
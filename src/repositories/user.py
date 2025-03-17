import json
import logging
import psycopg2

import repositories.queries.postgres.user as user_queries
from schemas.user import UserRegisterRequest, UserAuthorizeRequest, UserInfoResponse200
from utils.hash import get_hash_string

class UserRepository:

    @staticmethod
    def connect():
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

    def create_student(self, user: UserRegisterRequest) -> None:
        conn = self.connect()
        with conn.cursor() as cursor:
            cursor.execute(user_queries.CREATE_STUDENT, (user.email, get_hash_string(user.password), 'student', user.full_name.first_name, user.full_name.second_name, user.full_name.middle_name))
        conn.commit()
        conn.close()

    def check_by_email_and_password(self, user: UserAuthorizeRequest) -> bool:
        conn = self.connect()
        print(get_hash_string(user.password))
        with conn.cursor() as cursor:
            cursor.execute(user_queries.GET_USER, (user.email, get_hash_string(user.password)))
            data = cursor.fetchall()
        conn.close()
        if len(data) == 1:
            return True
        else:
            return False

    def check_by_email(self, email: str) -> bool:
        conn = self.connect()
        with conn.cursor() as cursor:
            cursor.execute(user_queries.SELECT_BY_EMAIL, (email,))
            data = cursor.fetchall()
        conn.close()
        if len(data) == 1:
            return True
        else:
            return False

    def get_user_info(self, email: str, hash_password: str) -> UserInfoResponse200:
        conn = self.connect()
        with conn.cursor() as cursor:
            cursor.execute(user_queries.GET_USER, (email, hash_password))
            data = cursor.fetchall()
        conn.close()
        return data
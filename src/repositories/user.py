import json
import logging
import psycopg2

import repositories.queries.postgres.user as user_queries

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

    # def create_user(self, user: User):
    #     conn = self.connect()
    #     with conn.cursor() as cursor:
    #         cursor.execute('INSERT INTO "user" (name, surname, e_mail, hash_password) '
    #                        'VALUES (%s, %s, %s, %s)', (user.name, user.surname, user.e_mail, user.hash_password))
    #     conn.commit()
    #     conn.close()

    # def validate_user(self, user: UserValidate) -> bool:
    #     conn = self.connect()
    #     with conn.cursor() as cursor:
    #         cursor.execute('SELECT * FROM "user" WHERE e_mail = %s AND hash_password = %s',
    #                        (user.e_mail, user.hash_password))
    #         data = cursor.fetchall()
    #     conn.close()
    #     if len(data) == 0:
    #         return False
    #     else:
    #         return True

    def validate_email(self, email: str) -> bool:
        conn = self.connect()
        with conn.cursor() as cursor:
            cursor.execute(user_queries.SELECT_BY_EMAIL, (email,))
            data = cursor.fetchall()
        conn.close()
        if len(data) == 1:
            return True
        else:
            return False

    # def delete_user(self, e_mail: str):
    #     conn = self.connect()
    #     with conn.cursor() as cursor:
    #         cursor.execute('DELETE FROM "user" WHERE e_mail = %s', (e_mail,))
    #     conn.commit()
    #     conn.close()

    # def update_user(self, user: UserUpdate, e_mail: str):
    #     conn = self.connect()
    #     with conn.cursor() as cursor:
    #         cursor.execute('UPDATE "user" SET name = %s, surname = %s WHERE e_mail = %s',
    #                        (user.name, user.surname, e_mail))
    #     conn.commit()
    #     conn.close()

    # def get_user_name_and_surname(self, e_mail, hash_password):
    #     conn = self.connect()
    #     with conn.cursor() as cursor:
    #         cursor.execute('SELECT name, surname FROM "user" WHERE e_mail = %s AND hash_password = %s',
    #                        (e_mail, hash_password))
    #         data = cursor.fetchone()
    #     conn.close()
    #     return data
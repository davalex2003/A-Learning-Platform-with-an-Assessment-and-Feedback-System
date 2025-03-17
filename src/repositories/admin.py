import json
import logging
import psycopg2

import repositories.queries.postgres.admin as admin_queries
import repositories.queries.postgres.common as common_queries

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
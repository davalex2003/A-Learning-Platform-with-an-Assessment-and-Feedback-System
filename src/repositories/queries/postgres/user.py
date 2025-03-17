SELECT_BY_EMAIL = 'SELECT * FROM "user" WHERE email = %s'
CREATE_STUDENT = 'INSERT INTO "user" (email, hash_password, role, first_name, second_name, middle_name) VALUES (%s, %s, %s, %s, %s, %s)'
GET_USER = 'SELECT * FROM "user" WHERE email = %s AND hash_password = %s'
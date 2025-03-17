SELECT_BY_EMAIL = 'SELECT * FROM "user" WHERE email = %s'
CREATE_STUDENT = 'INSERT INTO "user" (email, hash_password, role, first_name, second_name, middle_name) VALUES (%s, %s, %s, %s, %s, %s)'
GET_USER = 'SELECT role, first_name, second_name, middle_name, email FROM "user" WHERE email = %s AND hash_password = %s'
SET_CONFIRMED_EMAIL = 'UPDATE "user" SET has_confirmed_email = true WHERE email = %s'
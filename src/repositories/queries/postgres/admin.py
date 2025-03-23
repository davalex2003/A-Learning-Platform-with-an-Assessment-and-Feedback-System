SELECT_USERS_LIST = 'SELECT id, first_name, second_name, middle_name, email, role FROM "user"'
DELETE_USER = 'DELETE FROM "user" WHERE id = %s'
CHANGE_USER_ROLE = 'UPDATE "user" SET role = %s WHERE id = %s'
SELECT_COURSES_LIST = 'SELECT * FROM "course"'
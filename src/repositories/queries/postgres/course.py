CREATE_COURSE = 'INSERT INTO "course" (name, description, user_id) VALUES (%s, %s, %s) RETURNING id'
UPDATE_COURSE = 'UPDATE "course" SET name = %s, description = %s WHERE id = %s'
UPDATE_IS_ACTIVE_COURSE = 'UPDATE "course" SET is_active = %s WHERE id = %s'
DELETE_COURSE = 'DELETE FROM "course" WHERE id = %s'
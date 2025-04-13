CREATE_ASSIGNMENT = 'INSERT INTO "assignment" (course_id, name, started_at, ended_at) VALUES (%s, %s, %s, %s) RETURNING id'
UPDATE_ASSIGNMENT = 'UPDATE "assignment" SET name = %s, started_at = %s, ended_at = %s WHERE id = %s'
DELETE_ASSIGNMENT = 'DELETE FROM "assignment" WHERE id = %s'
SELECT_ASSIGNMENTS = 'SELECT id, name, started_at, ended_at FROM "assignment" WHERE course_id = %s'
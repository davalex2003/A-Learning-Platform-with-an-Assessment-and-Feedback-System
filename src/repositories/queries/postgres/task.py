CREATE_TASK = 'INSERT INTO "task" (assignment_id, question_type, question_text, answer_type, answer_variants) VALUES (%s, %s, %s, %s, %s)'
UPDATE_TASK_QUESTION_FILE = 'UPDATE "task" SET question_file = %s WHERE id = %s'
SELECT_QUESTION_INFO = 'SELECT question_type, question_file FROM "task" WHERE id = %s'
DELETE_TASK = 'DELETE FROM "task" WHERE id = %s'
INSERT_ANSWER_TEXT = 'INSERT INTO "answer" (task_id, user_id, assignment_id, text) VALUES (%s, %s, %s, %s)'
INSERT_ANSWER_FILE = 'INSERT INTO "answer" (task_id, user_id, assignment_id, file) VALUES (%s, %s, %s, %s)'
GET_ANSWER_FILE = 'SELECT file from "answer" WHERE task_id = %s AND user_id = %s AND assignment_id = %s'
INSERT_ANSWER_ASSESSMENT = 'UPDATE "answer" SET assessment = %s WHERE task_id = %s AND user_id = %s AND assignment_id = %s'
INSERT_ANSWER_FEEDBACK = 'UPDATE "answer" SET feedback = %s WHERE task_id = %s AND user_id = %s AND assignment_id = %s'
SELECT_ANSWERS = 'SELECT * FROM "answer" WHERE user_id = %s AND assignment_id = %s'
SELECT_ANSWER = 'SELECT text, file, assessment, feedback FROM "answer" WHERE task_id = %s AND user_id = %s'
SELECT_ANSWERS_BY_ASSIGNMENT = 'SELECT user_id, assessment FROM "answer" WHERE assignment_id = %s'
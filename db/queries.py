# USERS

CREATE_USERS_TABLE = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    telegram_id INTEGER UNIQUE NOT NULL,
    username TEXT
)
"""

GET_USER_BY_TG_ID = """
SELECT * FROM users WHERE telegram_id = ?
"""

INSERT_USER = """
INSERT OR IGNORE INTO users (telegram_id, username)
VALUES (?, ?)
"""

UPDATE_USER = """
UPDATE users SET username = ? WHERE telegram_id = ?
"""

DELETE_USER = """
DELETE FROM users WHERE telegram_id = ?
"""


# QUESTIONS

CREATE_QUESTIONS_TABLE = """
CREATE TABLE IF NOT EXISTS questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question_text TEXT NOT NULL,
    correct_answer TEXT NOT NULL
)
"""

GET_ALL_QUESTIONS = """
SELECT * FROM questions
"""

GET_QUESTION_BY_ID = """
SELECT * FROM questions WHERE id = ?
"""

INSERT_QUESTION = """
INSERT INTO questions (question_text, correct_answer)
VALUES (?, ?)
"""

UPDATE_QUESTION = """
UPDATE questions
SET question_text = ?, correct_answer = ?
WHERE id = ?
"""

DELETE_QUESTION = """
DELETE FROM questions WHERE id = ?
"""


# RESULTS

CREATE_RESULTS_TABLE = """
CREATE TABLE IF NOT EXISTS results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    question_id INTEGER NOT NULL,
    is_correct INTEGER NOT NULL
)
"""

INSERT_RESULT = """
INSERT INTO results (user_id, question_id, is_correct)
VALUES (?, ?, ?)
"""

GET_RESULT_BY_ID = """
SELECT * FROM results WHERE id = ?
"""

GET_ALL_RESULTS = """
SELECT * FROM results
"""

GET_USER_RESULTS = """
SELECT * FROM results WHERE user_id = ?
"""

UPDATE_RESULT = """
UPDATE results
SET user_id = ?, question_id = ?, is_correct = ?
WHERE id = ?
"""

DELETE_RESULT = """
DELETE FROM results WHERE id = ?
"""

GET_SCORE_BY_USER_ID = """
SELECT COUNT(*) AS total, SUM(is_correct) AS correct
FROM results
WHERE user_id = ?
"""

GET_TOP = """
SELECT u.username,
       COUNT(*) AS total,
       SUM(r.is_correct) AS correct
FROM results AS r
INNER JOIN users AS u
    ON r.user_id = u.id
GROUP BY r.user_id
ORDER BY correct DESC
LIMIT 3
"""

GET_HARDEST = """
SELECT q.question_text,
       ROUND(AVG(r.is_correct) * 100, 1) AS success_rate
FROM results AS r
INNER JOIN questions AS q
    ON r.question_id = q.id
GROUP BY r.question_id
ORDER BY success_rate ASC
LIMIT 1
"""
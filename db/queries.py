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

CREATE_QUESTIONS_TABLE = """
CREATE TABLE IF NOT EXISTS questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT NOT NULL,
    answer TEXT NOT NULL
)
"""

GET_ALL_QUESTIONS = """
SELECT * FROM questions
"""

GET_QUESTION_BY_ID = """
SELECT * FROM questions WHERE id = ?
"""

INSERT_QUESTION = """
INSERT INTO questions (question, answer)
VALUES (?, ?)
"""


# RESULTS
CREATE_RESULTS_TABLE = """
CREATE TABLE IF NOT EXISTS results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    telegram_id INTEGER NOT NULL,
    score INTEGER NOT NULL
)
"""

INSERT_RESULT = """
INSERT INTO results (telegram_id, score)
VALUES (?, ?)
"""

GET_USER_RESULTS = """
SELECT * FROM results WHERE telegram_id = ?
"""
import sqlite3

from db.queries import (
    CREATE_USERS_TABLE,
    CREATE_QUESTIONS_TABLE,
    CREATE_RESULTS_TABLE,
    GET_ALL_QUESTIONS,
    INSERT_QUESTION,
)
from src.questions import QUESTIONS

DB_NAME = "quiz.db"


def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()

    conn.execute(CREATE_USERS_TABLE)
    conn.execute(CREATE_QUESTIONS_TABLE)
    conn.execute(CREATE_RESULTS_TABLE)

    questions = conn.execute(GET_ALL_QUESTIONS).fetchall()

    if not questions:
        for item in QUESTIONS:
            conn.execute(
                INSERT_QUESTION,
                (item["q"], item["a"])
            )

    conn.commit()
    conn.close()

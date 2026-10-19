from db.database import get_db
from db.queries import INSERT_RESULT, GET_USER_RESULTS


def save_result(telegram_id: int, score: int):
    conn = get_db()
    conn.execute(INSERT_RESULT, (telegram_id, score))
    conn.commit()
    conn.close()


def get_user_results(telegram_id: int):
    conn = get_db()
    rows = conn.execute(
        GET_USER_RESULTS, (telegram_id,)
    ).fetchall()
    conn.close()

    return [dict(row) for row in rows]

from db.database import get_db
from db.queries import (
    INSERT_RESULT,
    GET_RESULT_BY_ID,
    GET_ALL_RESULTS,
    GET_USER_RESULTS,
    UPDATE_RESULT,
    DELETE_RESULT,
    GET_SCORE_BY_USER_ID,
)


def save_result(user_id: int, question_id: int, is_correct: bool):
    conn = get_db()
    conn.execute(
        INSERT_RESULT,
        (user_id, question_id, int(is_correct)),
    )
    conn.commit()
    conn.close()


def get_result(result_id: int):
    conn = get_db()
    row = conn.execute(
        GET_RESULT_BY_ID, (result_id,)
    ).fetchone()
    conn.close()
    return dict(row) if row else None


def get_all_results():
    conn = get_db()
    rows = conn.execute(GET_ALL_RESULTS).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_user_results(user_id: int):
    conn = get_db()
    rows = conn.execute(
        GET_USER_RESULTS, (user_id,)
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def update_result(
    result_id: int,
    user_id: int,
    question_id: int,
    is_correct: bool,
):
    conn = get_db()
    cursor = conn.execute(
        UPDATE_RESULT,
        (user_id, question_id, int(is_correct), result_id),
    )
    conn.commit()
    updated = cursor.rowcount > 0
    conn.close()
    return updated


def delete_result(result_id: int):
    conn = get_db()
    cursor = conn.execute(
        DELETE_RESULT, (result_id,)
    )
    conn.commit()
    deleted = cursor.rowcount > 0
    conn.close()
    return deleted


def get_score(user_id: int):
    conn = get_db()
    row = conn.execute(
        GET_SCORE_BY_USER_ID, (user_id,)
    ).fetchone()
    conn.close()

    return dict(row) if row else {"total": 0, "correct": 0}
from db.database import get_db
from db.queries import (
    GET_USER_BY_TG_ID,
    INSERT_USER,
    UPDATE_USER,
    DELETE_USER,
)


# READ — получить пользователя
def get_user(telegram_id: int):
    conn = get_db()
    user = conn.execute(
        GET_USER_BY_TG_ID, (telegram_id,)
    ).fetchone()
    conn.close()

    return dict(user) if user else None


# CREATE — создать пользователя
def create_user(telegram_id: int, username: str):
    conn = get_db()
    conn.execute(INSERT_USER, (telegram_id, username))
    conn.commit()
    conn.close()

    return get_user(telegram_id)


# UPDATE — обновить имя пользователя
def update_user(telegram_id: int, username: str):
    conn = get_db()
    conn.execute(UPDATE_USER, (username, telegram_id))
    conn.commit()
    conn.close()

    return get_user(telegram_id)


# DELETE — удалить пользователя
def delete_user(telegram_id: int):
    conn = get_db()
    cursor = conn.execute(DELETE_USER, (telegram_id,))
    conn.commit()
    deleted = cursor.rowcount > 0
    conn.close()

    return deleted
import mariadb
from app import config


def _get_connection():
    return mariadb.connect(
        host=config.DB_HOST,
        port=config.DB_PORT,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        database=config.DB_NAME,
    )


def read_query(sql: str, params: tuple = ()) -> list[tuple]:
    with _get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, params)
        return list(cursor)


def insert_query(sql: str, params: tuple = ()) -> int:
    with _get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, params)
        conn.commit()
        return cursor.lastrowid


def update_query(sql: str, params: tuple = ()) -> int:
    with _get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, params)
        conn.commit()
        return cursor.rowcount
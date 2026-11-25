
from app.database import read_query, insert_query, update_query
from app.models.reply import Reply


_REPLY_COLUMNS = """
    id, topic_id, author_id, content, created_at, updated_at
"""


def _first_or_none(rows: list[tuple]) -> Reply | None:
    return Reply.from_row(rows[0]) if rows else None


def get_by_id(reply_id: int) -> Reply | None:
    rows = read_query(
        f"SELECT {_REPLY_COLUMNS} FROM replies WHERE id = ?",
        (reply_id,)
    )
    return _first_or_none(rows)


def get_by_topic(topic_id: int) -> list[Reply]:
    rows = read_query(
        f"""SELECT {_REPLY_COLUMNS}
            FROM replies
            WHERE topic_id = ?
            ORDER BY created_at ASC, id ASC""",
        (topic_id,)
    )
    return [Reply.from_row(row) for row in rows]


def create(topic_id: int, author_id: int, content: str) -> int:
    return insert_query(
        """INSERT INTO replies (topic_id, author_id, content)
           VALUES (?, ?, ?)""",
        (topic_id, author_id, content)
    )


def update(reply_id: int, content: str) -> int:
    return update_query(
        """UPDATE replies
           SET content = ?
           WHERE id = ?""",
        (content, reply_id)
    )


def delete(reply_id: int) -> int:
    return update_query(
        "DELETE FROM replies WHERE id = ?",
        (reply_id,)
    )

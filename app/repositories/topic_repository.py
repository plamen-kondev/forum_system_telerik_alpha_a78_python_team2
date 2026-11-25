from app.database import read_query, insert_query, update_query
from app.models.topic import Topic

_TOPIC_COLUMNS = 'id, author_id, category_id, title, content, is_locked, is_private, best_reply_id, created_at, updated_at'

def _first_or_none(rows: list[tuple]) -> Topic | None:
    return Topic.from_row(rows[0]) if rows else None

def create_topic(author_id: int, category_id: int, title: str, content: str) -> int:

    return insert_query(
    '''INSERT INTO topics (author_id, category_id, title, content)
        VALUES (?, ?, ?, ?)''',
        (author_id, category_id, title, content)
    )


def get_topic_by_id(topic_id: int) -> Topic | None:
    rows = read_query(f'SELECT {_TOPIC_COLUMNS} FROM topics where id = ?', (topic_id,))
    return _first_or_none(rows)

def category_exists(category_id: int) -> bool:
    rows = read_query('SELECT 1 from categories where id = ?', (category_id,))
    return bool(rows)


from app.database import read_query
from app.models.category import Category
from app.models.home import TopicPreview


def count_users() -> int:
    return read_query("SELECT COUNT(*) FROM users")[0][0]


def count_public_topics() -> int:
    return read_query("SELECT COUNT(*) FROM topics WHERE is_private = FALSE")[0][0]


def count_public_replies() -> int:
    return read_query(
        """SELECT COUNT(*) FROM replies r
           JOIN topics t ON t.id = r.topic_id
           WHERE t.is_private = FALSE"""
    )[0][0]


def get_categories_with_counts() -> list[Category]:
    rows = read_query(
        """SELECT c.id, c.name, COUNT(t.id)
           FROM categories c
           LEFT JOIN topics t ON t.category_id = c.id AND t.is_private = FALSE
           GROUP BY c.id, c.name
           ORDER BY c.name"""
    )
    return [Category(id=id, name=name, topic_count=count) for id, name, count in rows]


def get_latest_topics(limit: int = 10) -> list[TopicPreview]:
    rows = read_query(
        """SELECT t.id, t.title, u.username, c.name, t.created_at, COUNT(r.id)
           FROM topics t
           JOIN users u ON u.id = t.author_id
           JOIN categories c ON c.id = t.category_id
           LEFT JOIN replies r ON r.topic_id = t.id
           WHERE t.is_private = FALSE
           GROUP BY t.id, t.title, u.username, c.name, t.created_at
           ORDER BY t.created_at DESC, t.id DESC
           LIMIT ?""",
        (limit,),
    )
    return [
        TopicPreview(
            id=id,
            title=title,
            author_username=username,
            category_name=category,
            created_at=created_at,
            reply_count=reply_count,
        )
        for id, title, username, category, created_at, reply_count in rows
    ]
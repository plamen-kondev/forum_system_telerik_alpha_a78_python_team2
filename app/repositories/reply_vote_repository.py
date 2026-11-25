from app.database import read_query, update_query

def set_vote(user_id: int, reply_id: int, is_like: bool) -> None:
    update_query(
        """
        INSERT INTO reply_votes (user_id, reply_id, is_like)
        VALUES (?, ?, ?)
        ON DUPLICATE KEY UPDATE is_like = VALUES(is_like)
        """,
        (user_id, reply_id, is_like)
    )


def remove_vote(user_id: int, reply_id: int) -> None:
    update_query(
        """
        DELETE FROM reply_votes
        WHERE user_id = ? AND reply_id = ?
        """,
        (user_id, reply_id)
    )


def get_counts(reply_id: int) -> tuple[int, int]:
    rows = read_query(
        """
        SELECT
            COALESCE(SUM(is_like = TRUE), 0),
            COALESCE(SUM(is_like = FALSE), 0)
        FROM reply_votes
        WHERE reply_id = ?
        """,
        (reply_id,)
    )
    return int(rows[0][0]), int(rows[0][1])


def get_user_vote(user_id: int, reply_id: int) -> bool | None:
    rows = read_query(
        """
        SELECT is_like
        FROM reply_votes
        WHERE user_id = ? AND reply_id = ?
        """,
        (user_id, reply_id)
    )
    return bool(rows[0][0]) if rows else None
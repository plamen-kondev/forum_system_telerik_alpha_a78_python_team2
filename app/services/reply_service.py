
from app.common.exceptions import (
    ForbiddenError,
    NotFoundError,
    BadRequestError,
)
from app.models.reply import Reply, ReplyCreate, ReplyUpdate
from app.models.user import User
from app.repositories import reply_repository
from app.database import read_query


def get_replies(topic_id: int) -> list[Reply]:
    _ensure_topic_exists(topic_id)
    return reply_repository.get_by_topic(topic_id)


def get_reply(reply_id: int) -> Reply:
    reply = reply_repository.get_by_id(reply_id)

    if reply is None:
        raise NotFoundError("Reply not found")

    return reply


def create_reply(topic_id: int, data: ReplyCreate, user: User) -> Reply:
    _ensure_topic_exists(topic_id)
    _ensure_topic_not_locked(topic_id)

    reply_id = reply_repository.create(
        topic_id=topic_id,
        author_id=user.id,
        content=data.content,
    )

    return get_reply(reply_id)


def update_reply(reply_id: int, data: ReplyUpdate, user: User) -> Reply:
    reply = get_reply(reply_id)

    if reply.author_id != user.id:
        raise ForbiddenError("You can only edit your own replies")

    reply_repository.update(reply_id, data.content)

    return get_reply(reply_id)


def delete_reply(reply_id: int, user: User) -> None:
    reply = get_reply(reply_id)

    if reply.author_id != user.id and not user.is_admin:
        raise ForbiddenError("You can only delete your own replies")

    reply_repository.delete(reply_id)


def _ensure_topic_exists(topic_id: int) -> None:
    rows = read_query(
        "SELECT id FROM topics WHERE id = ?",
        (topic_id,)
    )

    if not rows:
        raise NotFoundError("Topic not found")


def _ensure_topic_not_locked(topic_id: int) -> None:
    rows = read_query(
        "SELECT is_locked FROM topics WHERE id = ?",
        (topic_id,)
    )

    if not rows:
        raise NotFoundError("Topic not found")

    if rows[0][0]:
        raise BadRequestError("This topic is locked and cannot receive replies")


from fastapi import APIRouter, Depends, status

from app.common.auth import (
    get_current_user,
    require_not_blocked,
)
from app.models.user import User
from app.models.reply import ReplyCreate, ReplyUpdate, ReplyOut
from app.services import reply_service


router = APIRouter(tags=["Replies"])


@router.get(
    "/api/topics/{topic_id}/replies",
    response_model=list[ReplyOut],
)
def get_replies(topic_id: int):
    replies = reply_service.get_replies(topic_id)
    return [ReplyOut.from_reply(reply) for reply in replies]


@router.post(
    "/api/topics/{topic_id}/replies",
    response_model=ReplyOut,
    status_code=status.HTTP_201_CREATED,
)
def create_reply(
    topic_id: int,
    data: ReplyCreate,
    user: User = Depends(require_not_blocked),
):
    reply = reply_service.create_reply(topic_id, data, user)
    return ReplyOut.from_reply(reply)


@router.put(
    "/api/replies/{reply_id}",
    response_model=ReplyOut,
)
def update_reply(
    reply_id: int,
    data: ReplyUpdate,
    user: User = Depends(get_current_user),
):
    reply = reply_service.update_reply(reply_id, data, user)
    return ReplyOut.from_reply(reply)


@router.delete(
    "/api/replies/{reply_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_reply(
    reply_id: int,
    user: User = Depends(get_current_user),
):
    reply_service.delete_reply(reply_id, user)
    return None

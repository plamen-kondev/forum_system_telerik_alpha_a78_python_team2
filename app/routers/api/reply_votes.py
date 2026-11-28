
from fastapi import APIRouter, Depends, status

from app.common.auth import require_not_blocked, get_optional_user
from app.models.reply_vote import ReplyVoteCreate, ReplyVoteOut
from app.models.user import User
from app.services import reply_vote_service

router = APIRouter(tags=["Reply Votes"])


@router.put(
    "/api/replies/{reply_id}/vote",
    response_model=ReplyVoteOut,
)
def set_vote(
    reply_id: int,
    data: ReplyVoteCreate,
    user: User = Depends(require_not_blocked),
):
    return reply_vote_service.set_vote(
        reply_id=reply_id,
        is_like=data.is_like,
        user=user,
    )


@router.delete(
    "/api/replies/{reply_id}/vote",
    response_model=ReplyVoteOut,
)
def remove_vote(
    reply_id: int,
    user: User = Depends(require_not_blocked),
):
    return reply_vote_service.remove_vote(
        reply_id=reply_id,
        user=user,
    )


@router.get(
    "/api/replies/{reply_id}/votes",
    response_model=ReplyVoteOut,
)
def get_vote_summary(
    reply_id: int,
    user: User | None = Depends(get_optional_user),
):
    return reply_vote_service.get_vote_summary(
        reply_id=reply_id,
        user=user,
    )

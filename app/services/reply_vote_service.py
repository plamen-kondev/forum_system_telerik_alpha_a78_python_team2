
from app.models.reply_vote import ReplyVoteOut
from app.models.user import User
from app.repositories import reply_vote_repository
from app.services import reply_service


def set_vote(reply_id: int, is_like: bool, user: User) -> ReplyVoteOut:
    reply_service.get_reply(reply_id)

    reply_vote_repository.set_vote(
        user_id=user.id,
        reply_id=reply_id,
        is_like=is_like,
    )

    return get_vote_summary(reply_id, user)


def remove_vote(reply_id: int, user: User) -> ReplyVoteOut:
    reply_service.get_reply(reply_id)

    reply_vote_repository.remove_vote(
        user_id=user.id,
        reply_id=reply_id,
    )

    return get_vote_summary(reply_id, user)


def get_vote_summary(
    reply_id: int,
    user: User | None = None,
    ) -> ReplyVoteOut:
    reply_service.get_reply(reply_id)

    likes, dislikes = reply_vote_repository.get_counts(reply_id)

    my_vote = None
    if user is not None:
        my_vote = reply_vote_repository.get_user_vote(
            user_id=user.id,
            reply_id=reply_id,
        )

    return ReplyVoteOut(
        reply_id=reply_id,
        likes=likes,
        dislikes=dislikes,
        my_vote=my_vote,
    )

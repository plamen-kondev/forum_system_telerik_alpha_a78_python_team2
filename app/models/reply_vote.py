from pydantic import BaseModel


class ReplyVoteCreate(BaseModel):
    is_like: bool


class ReplyVote(BaseModel):
    user_id: int
    reply_id: int
    is_like: bool


class ReplyVoteOut(BaseModel):
    reply_id: int
    likes: int
    dislikes: int
    my_vote: bool | None = None
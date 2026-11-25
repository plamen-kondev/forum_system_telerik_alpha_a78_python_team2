
from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, StringConstraints


# Validation --- Reply content must contain between 2 and 8192 characters.
ReplyContent = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=2,
        max_length=8192
    )
]


# Creating a reply.
class ReplyCreate(BaseModel):
    content: ReplyContent


# Editing a reply.
class ReplyUpdate(BaseModel):
    content: ReplyContent


# Reply structure.
class Reply(BaseModel):
    id: int
    topic_id: int
    author_id: int
    content: str
    created_at: datetime
    updated_at: datetime | None = None

    @classmethod
    def from_row(cls, row: tuple) -> "Reply":
        id, topic_id, author_id, content, created_at, updated_at = row

        return cls(
            id=id,
            topic_id=topic_id,
            author_id=author_id,
            content=content,
            created_at=created_at,
            updated_at=updated_at
        )


# Reply rrepresented by the API.
class ReplyOut(BaseModel):
    id: int
    topic_id: int
    author_id: int
    content: str
    created_at: datetime
    updated_at: datetime | None = None

    @classmethod
    def from_reply(cls, reply: Reply) -> "ReplyOut":
        return cls(**reply.model_dump())

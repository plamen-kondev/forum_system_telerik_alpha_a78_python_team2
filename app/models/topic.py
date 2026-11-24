from typing import Annotated
from pydantic import BaseModel, Field, StringConstraints
from datetime import datetime

Title = Annotated[str, StringConstraints(
    strip_whitespace=True,
    min_length=16,
    max_length=128
)]

Content = Annotated[str, StringConstraints(
    strip_whitespace=True,
    min_length=32,
    max_length=8192
)]


class TopicCreate(BaseModel):
    title: Title
    content: Content
    category_id: int = Field(gt=0)

class Topic(BaseModel):
    id: int
    author_id: int = Field(gt=0)
    category_id: int = Field(gt=0)
    title: str
    content: str
    is_locked: bool
    is_private: bool
    best_reply_id: int | None = None
    created_at: datetime
    updated_at: datetime | None = None

    @classmethod
    def from_row(cls, row: tuple) -> 'Topic':
        id, author_id, category_id, title, content, is_locked, is_private,best_reply_id, created_at, updated_at = row
        return cls(
            id = id,
            author_id=author_id,
            category_id=category_id,
            title=title,
            content=content,
            is_locked=bool(is_locked),
            is_private=bool(is_private),
            best_reply_id=best_reply_id,
            created_at=created_at,
            updated_at=updated_at
        )
from datetime import datetime

from pydantic import BaseModel


class HomeStats(BaseModel):
    users: int
    topics: int
    replies: int


class TopicPreview(BaseModel):
    id: int
    title: str
    author_username: str
    category_name: str
    created_at: datetime
    reply_count: int
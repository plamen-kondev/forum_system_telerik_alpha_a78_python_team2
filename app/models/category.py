from pydantic import BaseModel

class Category(BaseModel):
    id: int
    name: str
    topic_count: int = 0  #how many public topics are in this category


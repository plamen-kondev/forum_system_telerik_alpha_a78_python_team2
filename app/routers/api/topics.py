from fastapi import APIRouter
from app.models.topic import Topic, TopicCreate
from app.services import topic_service

router = APIRouter(prefix='/topics', tags=['Topics'])

@router.post(
    '',
    response_model=Topic,
    status_code=201,
    summary='Create a topic',
    description='Creates a new topic'
    )
def create(data: TopicCreate):
    return topic_service.create_topic(data, 1)



from app.models.topic import Topic,TopicCreate
from app.repositories import topic_repository
from app.common.exceptions import AppError, NotFoundError


def create_topic(data: TopicCreate, author_id: int) -> Topic:
    if not topic_repository.category_exists(data.category_id):
        raise NotFoundError('Category not found')

    topic_id = topic_repository.create_topic(author_id, data.category_id, data.title, data.content)
    topic = topic_repository.get_topic_by_id(topic_id)
    if topic is None:
        raise AppError('Failed to retrieve newly created topic')
    
    return topic
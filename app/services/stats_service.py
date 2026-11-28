from app.models.category import Category
from app.models.home import HomeStats, TopicPreview
from app.repositories import stats_repository


def get_home_stats() -> HomeStats:
    return HomeStats(
        users=stats_repository.count_users(),
        topics=stats_repository.count_public_topics(),
        replies=stats_repository.count_public_replies(),
    )


def get_categories() -> list[Category]:
    return stats_repository.get_categories_with_counts()


def get_latest_topics(limit: int = 10) -> list[TopicPreview]:
    return stats_repository.get_latest_topics(limit)
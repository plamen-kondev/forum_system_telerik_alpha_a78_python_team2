from datetime import datetime
from unittest.mock import patch

from app.models.category import Category
from app.models.home import TopicPreview
from app.services import stats_service

REPO = "app.services.stats_service.stats_repository"


@patch(REPO)
def test_get_home_stats_collects_all_counts(mock_repo):
    mock_repo.count_users.return_value = 12
    mock_repo.count_public_topics.return_value = 30
    mock_repo.count_public_replies.return_value = 95

    stats = stats_service.get_home_stats()

    assert stats.users == 12
    assert stats.topics == 30
    assert stats.replies == 95


@patch(REPO)
def test_get_categories_returns_repository_result(mock_repo):
    categories = [Category(id=1, name="Food", topic_count=3), Category(id=2, name="Cars", topic_count=0)]
    mock_repo.get_categories_with_counts.return_value = categories

    assert stats_service.get_categories() == categories


@patch(REPO)
def test_get_latest_topics_passes_limit_to_repository(mock_repo):
    preview = TopicPreview(
        id=1, title="Pineapple belongs on pizza, fight me",
        author_username="kriska", category_name="Food",
        created_at=datetime(2026, 11, 27), reply_count=4,
    )
    mock_repo.get_latest_topics.return_value = [preview]

    result = stats_service.get_latest_topics(5)

    assert result == [preview]
    mock_repo.get_latest_topics.assert_called_once_with(5)
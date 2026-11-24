from datetime import datetime
from unittest.mock import patch

import pytest

from app.common.exceptions import ConflictError, UnauthorizedError
from app.models.user import User, Role, UserRegister, UserLogin
from app.services import auth_service

REPO = "app.services.auth_service.user_repository"


def make_user(id=1, username="ivan_99", password="secret123", role=Role.USER) -> User:
    return User(
        id=id,
        first_name="Ivan",
        last_name="Ivanov",
        email="ivan@test.com",
        username=username,
        password_hash=auth_service.hash_password(password),
        role=role,
        is_blocked=False,
        created_at=datetime(2026, 1, 1),
    )


REGISTER_DATA = UserRegister(
    first_name="Ivan", last_name="Ivanov", email="ivan@test.com", username="ivan_99", password="secret123"
)



def test_hash_password_does_not_store_plain_text():
    hashed = auth_service.hash_password("secret123")
    assert hashed != "secret123"
    assert auth_service.verify_password("secret123", hashed)


def test_verify_password_rejects_wrong_password():
    hashed = auth_service.hash_password("secret123")
    assert not auth_service.verify_password("wrong-pass", hashed)



@patch(REPO) #dokato vurvi testa istinskoto user_repository e zameneno s mock obekt
def test_register_creates_user_with_hashed_password(mock_repo):
    mock_repo.get_by_username.return_value = None
    mock_repo.get_by_email.return_value = None
    mock_repo.create.return_value = 1
    mock_repo.get_by_id.return_value = make_user()

    user = auth_service.register(REGISTER_DATA)

    assert user.id == 1
    saved_hash = mock_repo.create.call_args.kwargs["password_hash"]
    assert saved_hash != "secret123"
    assert auth_service.verify_password("secret123", saved_hash)


@patch(REPO)
def test_register_fails_when_username_taken(mock_repo):
    mock_repo.get_by_username.return_value = make_user()

    with pytest.raises(ConflictError):
        auth_service.register(REGISTER_DATA)
    mock_repo.create.assert_not_called()


@patch(REPO)
def test_register_fails_when_email_taken(mock_repo):
    mock_repo.get_by_username.return_value = None
    mock_repo.get_by_email.return_value = make_user()

    with pytest.raises(ConflictError):
        auth_service.register(REGISTER_DATA)
    mock_repo.create.assert_not_called()





@patch(REPO)
def test_login_returns_token_for_valid_credentials(mock_repo):
    user = make_user()
    mock_repo.get_by_username.return_value = user
    mock_repo.get_by_id.return_value = user
    token = auth_service.login(UserLogin(username="ivan_99", password="secret123"))
    assert auth_service.get_user_from_token(token).id == user.id


@patch(REPO)
def test_login_fails_for_wrong_password(mock_repo):
    mock_repo.get_by_username.return_value = make_user()
    with pytest.raises(UnauthorizedError):
        auth_service.login(UserLogin(username="ivan_99", password="wrong-pass"))


@patch(REPO)
def test_login_fails_for_unknown_user(mock_repo):
    mock_repo.get_by_username.return_value = None

    with pytest.raises(UnauthorizedError):
        auth_service.login(UserLogin(username="nobody", password="secret123"))



def test_get_user_from_token_rejects_garbage_token():
    with pytest.raises(UnauthorizedError):
        auth_service.get_user_from_token("this.is.not-a-token")


@patch(REPO)
def test_get_user_from_token_rejects_deleted_user(mock_repo):
    token = auth_service.create_access_token(make_user())
    mock_repo.get_by_id.return_value = None

    with pytest.raises(UnauthorizedError):
        auth_service.get_user_from_token(token)


@patch("app.services.auth_service.config")
def test_get_user_from_token_rejects_expired_token(mock_config):
    mock_config.JWT_SECRET = "test-secret"
    mock_config.JWT_EXPIRE_MINUTES = -1
    token = auth_service.create_access_token(make_user())

    with pytest.raises(UnauthorizedError):
        auth_service.get_user_from_token(token)
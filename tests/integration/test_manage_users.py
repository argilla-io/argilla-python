import pytest

from argilla_sdk import User, Argilla


@pytest.fixture(scope="session", autouse=True)
def clean_environment(client: Argilla):
    for user in client.users:
        if user.username.startswith("test"):
            user.delete()
    yield
    for user in client.users:
        if user.username.startswith("test"):
            user.delete()


class TestManageUsers:

    def test_create_user(self, client: Argilla):
        user = User(username="test_user", password="test_password")
        client.users.add(user)
        assert user.id is not None
        assert client.users(username=user.username).id == user.id

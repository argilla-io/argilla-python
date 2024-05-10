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
        user = User(username="test_user", password="test_password", client=client)
        user.create()
        try:
            assert user.id is not None
            assert user.password == "test_password"
            assert user.username == "test_user"
            assert client.users(username=user.username).id == user.id
        finally:
            user.delete()

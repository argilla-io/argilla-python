import pytest

from argilla_sdk import Argilla


class TestWorkspacesManagement:

    def test_create_and_delete_workspace(self, client: Argilla):
        workspace = client.workspaces(name="test_workspace")
        if workspace.exists():
            for dataset in workspace.datasets:
                dataset.delete()
            workspace.delete()

        workspace.create()
        assert workspace.exists()

        workspace.delete()
        assert not workspace.exists()

    def test_add_and_remove_users_to_workspace(self, client: Argilla):
        workspace = client.workspaces(name="test_workspace")

        test_user = client.users(username="test_user")
        if test_user.exists():
            test_user.delete()

        workspace.create()

        test_user.password = "test_password"
        test_user.create()

        user = workspace.add_user(user=test_user.username)
        assert user in workspace.users

        user = workspace.remove_user(user=user)
        assert user not in workspace.users

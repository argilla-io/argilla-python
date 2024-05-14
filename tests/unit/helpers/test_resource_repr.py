import uuid

import argilla_sdk as rg
from argilla_sdk._helpers._resource_repr import ResourceHTMLReprMixin
from argilla_sdk._models import DatasetModel


class TestResourceHTMLReprMixin:

    def test_represent_workspaces_as_html(self):

        client = rg.Argilla()
        workspaces = [
            rg.Workspace(name="workspace1", id=uuid.uuid4()),
            rg.Workspace(name="workspace2", id=uuid.uuid4()),
        ]

        assert (
            ResourceHTMLReprMixin()._represent_as_html(workspaces) == "<h3>Workspaces</h3>"
            "<table>"
            "<tr><th>name</th><th>id</th><th>updated_at</th></tr>"
            f"<tr><td>workspace1</td><td>{str(workspaces[0].id)}</td><td>None</td></tr>"
            f"<tr><td>workspace2</td><td>{str(workspaces[1].id)}</td><td>None</td></tr>"
            "</table>"
            ""
        )

        workspace = rg.Workspace(name="workspace1", id=uuid.uuid4())
        datasets = [
            rg.Dataset.from_model(
                DatasetModel(id=uuid.uuid4(), name="dataset1", workspace_id=workspace.id), client=client
            ),
            rg.Dataset.from_model(
                DatasetModel(id=uuid.uuid4(), name="dataset2", workspace_id=workspace.id), client=client
            ),
        ]

        assert (
            ResourceHTMLReprMixin()._represent_as_html(datasets) == "<h3>Datasets</h3>"
            "<table>"
            "<tr><th>name</th><th>id</th><th>workspace_id</th><th>updated_at</th></tr>"
            f"<tr><td>dataset1</td><td>{str(datasets[0].id)}</td><td>{str(workspace.id)}</td><td>None</td></tr>"
            f"<tr><td>dataset2</td><td>{str(datasets[1].id)}</td><td>{str(workspace.id)}</td><td>None</td></tr>"
            "</table>"
        )

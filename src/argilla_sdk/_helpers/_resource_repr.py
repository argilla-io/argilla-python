from typing import Any, Dict

from IPython.display import HTML


RESOURCE_REPR_CONFIG = {
    "Dataset": {
        "columns": ["name", "id", "workspace_id", "updated_at", "records"],
        "table_name": "Datasets",
        # "len_column": "records",
    },
    "Workspace": {
        "columns": ["name", "id", "datasets", "updated_at"],
        "table_name": "Workspaces",
        "len_column": "datasets",
    },
    "User": {"columns": ["username", "id", "role", "updated_at"], "table_name": "Users", "len_column": None},
}


class ResourceHTMLReprMixin:
    def _resource_to_table_row(self, resource) -> Dict[str, Any]:
        row = {}
        dumped_resource_model = resource._model.model_dump()
        resource_name = resource.__class__.__name__
        config = RESOURCE_REPR_CONFIG[resource_name].copy()
        len_column = config.pop("len_column", None)
        columns = config["columns"]
        if len_column is not None:
            row[len_column] = len(resource)
            columns = [column for column in columns if column != len_column]

        for column in columns:
            row[column] = dumped_resource_model[column]

        return row

    def _resource_to_table_name(self, resource) -> str:
        resource_name = resource.__class__.__name__
        return RESOURCE_REPR_CONFIG[resource_name]["table_name"]

    def _represent_as_html(self, resources) -> HTML:
        table_name = self._resource_to_table_name(resources[0])
        table_rows = [self._resource_to_table_row(resource) for resource in resources]

        html_table = f"<h3>{table_name}</h3><table><tr>"
        for column in table_rows[0]:
            html_table += f"<th>{column}</th>"
        html_table += "</tr>"

        for row in table_rows:
            html_table += "<tr>"
            for column in row:
                html_table += f"<td>{row[column]}</td>"
            html_table += "</tr>"

        html_table += "</table>"
        return HTML(html_table)._repr_html_()

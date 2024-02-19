import logging
from typing import Union, Any

from argilla_sdk._helpers._mixins import LoggingMixin
from argilla_sdk._models import DatasetModel, UserModel, WorkspaceModel
from argilla_sdk._api import APIClient


class Resource(LoggingMixin):
    """Base class for all resources (Dataset, Workspace, User, etc.)"""

    logger = logging.getLogger(__name__)
    model: Union[WorkspaceModel, UserModel, DatasetModel]
    api: APIClient

    def __repr__(self) -> str:
        return repr(f"{self.__class__.__name__}({self.model})")

    def update(self, api: APIClient, model: Union[WorkspaceModel, UserModel, DatasetModel]):
        """Updates the resource with the ClientAPI that is used to interact with
        Argilla and adds an updated model to the resource.
        Args:
            api (APIClient): The client API used to interact with Argilla
            model (Union[WorkspaceModel, UserModel, DatasetModel]): The updated model
        Returns:
            Self: The updated resource
        """
        self.log(f"Assigning API {str(api.http_client.base_url)}")
        self.api = api
        self.model = model
        return self

    def serialize(self) -> dict[str, Any]:
        return self.model.model_dump()

    def serialize_json(self) -> str:
        return self.model.model_dump_json()

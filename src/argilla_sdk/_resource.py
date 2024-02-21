from typing import Any

from argilla_sdk._helpers._mixins import LoggingMixin
from argilla_sdk._models import ResourceModel
from argilla_sdk._api import APIClient


class Resource(LoggingMixin):
    """Base class for all resources (Dataset, Workspace, User, etc.)"""

    _model: ResourceModel

    def __repr__(self) -> str:
        return repr(f"{self.__class__.__name__}({self._model})")

    def _update(self, api: APIClient, model: ResourceModel):
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
        self._model = model
        return self

    def serialize(self) -> dict[str, Any]:
        return self._model.model_dump()

    def serialize_json(self) -> str:
        return self._model.model_dump_json()

    ############################
    # State management methods #
    ############################

    def __setattr__(self, name, value):
        super().__setattr__(name, value)
        if name in self._model.model_fields:
            model_dump = self._model.model_dump()
            model_dump[name] = value
            self._model = self._model.__class__(**model_dump)

    def __getattr__(self, name):
        if name in self._model.model_fields:
            return self._model.model_dump()[name]
        else:
            super().__getattribute__(name)
